import math
import random

from seika.assets import Texture
from seika.color import Color
from seika.math import Vector2

from src.enemy.enemy_spawner import EnemySpawner
from src.game_context import PlayState, GameContext
from src.item.rainbow_orb import RainbowOrb
from src.item.tricolora import Tricolora
from src.npc.npc import GainBombNPC, GainWaveNPC, GainShieldNPC
from src.room.room import Room
from src.room.door import Door, DoorState
from src.project_properties import ProjectProperties
from src.room.room_model import RoomType


class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.current_room = None
            cls.rooms = {}
            cls.wall_colliders = None
            cls.room_doors = None
            cls.transition_doors = None
            cls.room_background = None
            cls.transition_room_background = None
            cls.horizontal_door_overhead_texture = Texture.get(
                file_path="assets/images/dungeon/horizontal_door_overhead.png"
            )
            cls.horizontal_cracked_wall_door_overhead_texture = Texture.get(
                file_path="assets/images/dungeon/horizontal_cracked_wall_door_overhead.png"
            )
            cls.vertical_door_overhead_texture = Texture.get(
                file_path="assets/images/dungeon/vertical_door_overhead.png"
            )
            cls.vertical_cracked_wall_door_overhead_texture = Texture.get(
                file_path="assets/images/dungeon/vertical_cracked_wall_door_overhead.png"
            )
        return cls._instance

    def add_room(self, room: Room) -> None:
        self.rooms[f"{room.position.x},{room.position.y}"] = room

    def set_current_room(self, position: Vector2) -> None:
        pos_key = f"{position.x},{position.y}"
        if pos_key in self.rooms:
            self.current_room = self.rooms[pos_key]
        else:
            print(f"pos_key {pos_key} not found!")

    def get_room(self, position: Vector2) -> Room:
        return self.rooms[f"{position.x},{position.y}"]

    def get_grid_position(self, position: Vector2) -> Vector2:
        return Vector2(
            math.floor(position.x / ProjectProperties.BASE_RESOLUTION.x),
            math.floor(position.y / ProjectProperties.BASE_RESOLUTION.y),
        )

    def get_world_position(self, grid_position: Vector2) -> Vector2:
        return Vector2(
            math.floor(grid_position.x * ProjectProperties.BASE_RESOLUTION.x),
            math.floor(grid_position.y * ProjectProperties.BASE_RESOLUTION.y),
        )

    def start_room_transition(self, collided_door: Door) -> None:
        room_transitioning_from = self.current_room
        new_room_position = self.current_room.position + collided_door.direction
        self.set_current_room(position=new_room_position)
        self.current_room.position = new_room_position
        new_world_position = self.get_world_position(new_room_position)
        self.transition_doors.move(new_world_position)
        # Swap room backgrounds and set position
        new_transition_room_background = self.transition_room_background
        self.transition_room_background = self.room_background
        self.room_background = new_transition_room_background
        self.room_background.position = new_world_position
        # Swap doors
        new_transition_doors = self.transition_doors
        self.transition_doors = self.room_doors
        self.room_doors = new_transition_doors
        self.refresh_current_doors_status()
        # Setup door overhead
        previous_room_world_position = self.get_world_position(
            room_transitioning_from.position
        )
        horizontal_door_overhead = collided_door.get_node(name="HorizontalDoorOverhead")
        vertical_door_overhead = collided_door.get_node(name="VerticalDoorOverhead")
        horizontal_door_overhead.modulate = Color(1.0, 1.0, 1.0, 1.0)
        vertical_door_overhead.modulate = Color(1.0, 1.0, 1.0, 1.0)
        if collided_door.direction == Vector2.UP():
            horizontal_door_overhead.position = previous_room_world_position + Vector2(
                0.0, -24.0
            )
            if collided_door.get_state() == DoorState.OPEN:
                horizontal_door_overhead.texture = self.horizontal_door_overhead_texture
            elif collided_door.get_state() == DoorState.CRACKED_OPEN_WALL:
                horizontal_door_overhead.texture = (
                    self.horizontal_cracked_wall_door_overhead_texture
                )
        elif collided_door.direction == Vector2.DOWN():
            horizontal_door_overhead.position = previous_room_world_position + Vector2(
                0.0, -24.0 + self.current_room.size.y
            )
            if collided_door.get_state() == DoorState.OPEN:
                horizontal_door_overhead.texture = self.horizontal_door_overhead_texture
            elif collided_door.get_state() == DoorState.CRACKED_OPEN_WALL:
                horizontal_door_overhead.texture = (
                    self.horizontal_cracked_wall_door_overhead_texture
                )
        elif collided_door.direction == Vector2.LEFT():
            vertical_door_overhead.position = previous_room_world_position + Vector2(
                -55.0, 0.0
            )
            if collided_door.get_state() == DoorState.OPEN:
                vertical_door_overhead.texture = self.vertical_door_overhead_texture
            elif collided_door.get_state() == DoorState.CRACKED_OPEN_WALL:
                vertical_door_overhead.texture = (
                    self.vertical_cracked_wall_door_overhead_texture
                )
        elif collided_door.direction == Vector2.RIGHT():
            vertical_door_overhead.position = previous_room_world_position + Vector2(
                -55.0 + self.current_room.size.x, 0.0
            )
            if collided_door.get_state() == DoorState.OPEN:
                vertical_door_overhead.texture = self.vertical_door_overhead_texture
            elif collided_door.get_state() == DoorState.CRACKED_OPEN_WALL:
                vertical_door_overhead.texture = (
                    self.vertical_cracked_wall_door_overhead_texture
                )

        GameContext.set_play_state(PlayState.ROOM_TRANSITION)

    def _close_current_room_doors(self) -> None:
        if self.current_room.data.up_door_status == DoorState.OPEN:
            self.current_room.data.up_door_status = DoorState.CLOSED
            self.room_doors.up.set_state(state=DoorState.CLOSED)
        if self.current_room.data.down_door_status == DoorState.OPEN:
            self.current_room.data.down_door_status = DoorState.CLOSED
            self.room_doors.down.set_state(state=DoorState.CLOSED)
        if self.current_room.data.left_door_status == DoorState.OPEN:
            self.current_room.data.left_door_status = DoorState.CLOSED
            self.room_doors.left.set_state(state=DoorState.CLOSED)
        if self.current_room.data.right_door_status == DoorState.OPEN:
            self.current_room.data.right_door_status = DoorState.CLOSED
            self.room_doors.right.set_state(state=DoorState.CLOSED)
        self.refresh_current_room_wall_colliders()

    def finish_room_transition(self, main_node) -> None:
        if (
            self.current_room.data.room_type == RoomType.COMBAT
            and not self.current_room.data.is_cleared
        ):
            base_room_position = self.get_world_position(
                grid_position=self.current_room.position
            )
            for i in range(self.current_room.data.enemies):
                rand_pos = Vector2(random.randint(100, 320), random.randint(70, 150))
                if random.randint(0, 1) == 0:
                    EnemySpawner.spawn_cultist(
                        main_node=main_node, position=base_room_position + rand_pos
                    )
                else:
                    EnemySpawner.spawn_shield(
                        main_node=main_node, position=base_room_position + rand_pos
                    )
            self._close_current_room_doors()
        elif (
            self.current_room.data.room_type == RoomType.GAIN_ATTACK
            and not self.current_room.data.is_cleared
        ):
            gain_wave_npc = GainWaveNPC.new()
            gain_wave_npc.position = self.get_world_position(
                grid_position=self.current_room.position
            ) + Vector2(160, 60)
            main_node.add_child(gain_wave_npc)
        elif (
            self.current_room.data.room_type == RoomType.GAIN_BOMB
            and not self.current_room.data.is_cleared
        ):
            rainbow_orb = RainbowOrb.new()
            rainbow_orb.position = self.get_world_position(
                grid_position=self.current_room.position
            ) + Vector2(200, 60)
            main_node.add_child(rainbow_orb)

            bomb_npc = GainBombNPC.new()
            bomb_npc.position = rainbow_orb.position + Vector2(-40, 0)
            main_node.add_child(bomb_npc)

            self._close_current_room_doors()
        elif (
            self.current_room.data.room_type == RoomType.GAIN_SHIELD
            and not self.current_room.data.is_cleared
        ):
            gain_shield_npc = GainShieldNPC.new()
            gain_shield_npc.position = self.get_world_position(
                grid_position=self.current_room.position
            ) + Vector2(160, 60)
            main_node.add_child(gain_shield_npc)
        elif (
            self.current_room.data.room_type == RoomType.END
            and not self.current_room.data.is_cleared
        ):
            tricolora = Tricolora.new()
            tricolora.position = self.get_world_position(
                grid_position=self.current_room.position
            ) + Vector2(200, 60)
            main_node.add_child(tricolora)

        horizontal_door_overhead = main_node.get_node(name="HorizontalDoorOverhead")
        vertical_door_overhead = main_node.get_node(name="VerticalDoorOverhead")
        horizontal_door_overhead.modulate = Color(1.0, 1.0, 1.0, 0.0)
        vertical_door_overhead.modulate = Color(1.0, 1.0, 1.0, 0.0)

        self.refresh_current_room_wall_colliders()

    def set_current_room_to_cleared(self) -> None:
        self.current_room.data.is_cleared = True
        if self.current_room.data.up_door_status == DoorState.CLOSED:
            self.current_room.data.up_door_status = DoorState.OPEN
            self.room_doors.up.set_state(state=DoorState.OPEN)
        if self.current_room.data.down_door_status == DoorState.CLOSED:
            self.current_room.data.down_door_status = DoorState.OPEN
            self.room_doors.down.set_state(state=DoorState.OPEN)
        if self.current_room.data.left_door_status == DoorState.CLOSED:
            self.current_room.data.left_door_status = DoorState.OPEN
            self.room_doors.left.set_state(state=DoorState.OPEN)
        if self.current_room.data.right_door_status == DoorState.CLOSED:
            self.current_room.data.right_door_status = DoorState.OPEN
            self.room_doors.right.set_state(state=DoorState.OPEN)
        self.refresh_current_room_wall_colliders()

    def refresh_current_doors_status(self) -> None:
        self.room_doors.left.set_state(self.current_room.data.left_door_status)
        self.room_doors.right.set_state(self.current_room.data.right_door_status)
        self.room_doors.up.set_state(self.current_room.data.up_door_status)
        self.room_doors.down.set_state(self.current_room.data.down_door_status)

    def refresh_current_room_wall_colliders(self) -> None:
        self.wall_colliders.update_collision_rects_near_door(
            data=self.current_room.data
        )

    # TOOD: Figure out while current room has to be set on the engine side, will try to retrieve non-existing entity
    def clean_up(self) -> None:
        self.current_room = None
