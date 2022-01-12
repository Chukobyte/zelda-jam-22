import math

from seika.math import Vector2

from src.enemy.enemy_spawner import EnemySpawner
from src.game_context import PlayState, GameContext
from src.room.room import Room
from src.room.door import Door, DoorStatus
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
        return cls._instance

    def add_room(self, room: Room) -> None:
        self.rooms[f"{room.position.x},{room.position.y}"] = room

    def set_current_room(self, position: Vector2) -> None:
        pos_key = f"{position.x},{position.y}"
        if pos_key in self.rooms:
            self.current_room = self.rooms[pos_key]

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
        # New
        # new_room_position = self.current_room.position + collided_door.direction
        # Old
        new_room_position = self.current_room.position + collided_door.direction
        self.set_current_room(position=new_room_position)
        self.current_room.position = new_room_position
        new_world_position = self.get_world_position(new_room_position)
        self.transition_doors.move(new_world_position)
        # Swap doors
        new_transition_doors = self.transition_doors
        self.transition_doors = self.room_doors
        self.room_doors = new_transition_doors
        # Update current room doors
        self.room_doors.left.set_status(self.current_room.data.left_door_status)
        self.room_doors.right.set_status(self.current_room.data.right_door_status)
        self.room_doors.up.set_status(self.current_room.data.up_door_status)
        self.room_doors.down.set_status(self.current_room.data.down_door_status)

        GameContext.set_play_state(PlayState.ROOM_TRANSITION)

    def finish_room_transition(self, main_node) -> None:
        if (
            self.current_room.data.room_type == RoomType.BOSS
            and not self.current_room.data.is_cleared
        ):
            boss_position = self.get_world_position(
                grid_position=self.current_room.position
            ) + Vector2(200, 45)
            EnemySpawner.spawn_boss(main_node=main_node, position=boss_position)

    def set_current_room_to_cleared(self) -> None:
        self.current_room.data.is_cleared = True

    # TODO: Figure out why rooms aren't being cleaned up without this...
    # TODO: Something to do with Sprite node clean ups as it happens with Attacks too
    def clean_up(self) -> None:
        for door in self.room_doors.doors + self.transition_doors.doors:
            door.queue_deletion()
