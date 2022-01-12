from seika.node import Node, Node2D, CollisionShape2D, Sprite
from seika.math import Vector2, Rect2
from seika.assets import Texture

from src.room.room import WallColliders, DungeonDoors, Room, Door
from src.room.room_manager import RoomManager


class RoomBuilder:
    @staticmethod
    def create_wall_colliders(node: Node) -> None:
        wall_colliders = WallColliders(
            left_up_up=CollisionShape2D.new(),
            left_up_left=CollisionShape2D.new(),
            left_down_left=CollisionShape2D.new(),
            left_down_down=CollisionShape2D.new(),
            right_up_up=CollisionShape2D.new(),
            right_up_right=CollisionShape2D.new(),
            right_down_right=CollisionShape2D.new(),
            right_down_down=CollisionShape2D.new(),
        )

        wall_colliders.left_up_up.collider_rect = Rect2(64, 0, 124, 32)
        wall_colliders.left_up_left.collider_rect = Rect2(0, 0, 64, 100)
        wall_colliders.left_down_left.collider_rect = Rect2(0, 124, 64, 100)
        wall_colliders.left_down_down.collider_rect = Rect2(64, 192, 124, 32)

        wall_colliders.right_up_up.collider_rect = Rect2(212, 0, 128, 32)
        wall_colliders.right_up_right.collider_rect = Rect2(340, 0, 64, 100)
        wall_colliders.right_down_right.collider_rect = Rect2(340, 124, 64, 100)
        wall_colliders.right_down_down.collider_rect = Rect2(212, 192, 128, 32)

        for wall_collider in wall_colliders.walls:
            wall_collider.tags = Room.SOLID_TAG
            node.add_child(child_node=wall_collider)

        room_manager = RoomManager()
        room_manager.wall_colliders = wall_colliders

    @staticmethod
    def create_doors(node: Node) -> None:
        current_doors = DungeonDoors(
            left=Door.new_door(Vector2.LEFT()),
            right=Door.new_door(Vector2.RIGHT()),
            up=Door.new_door(Vector2.UP()),
            down=Door.new_door(Vector2.DOWN()),
            container=Node2D.new(),
        )
        # TODO: Use for when transitioning to the next room
        transition_doors = DungeonDoors(
            left=Door.new_door(Vector2.LEFT()),
            right=Door.new_door(Vector2.RIGHT()),
            up=Door.new_door(Vector2.UP()),
            down=Door.new_door(Vector2.DOWN()),
            container=Node2D.new(),
        )
        transition_doors.container.position = Vector2(1000, 1000)

        node.add_child(child_node=current_doors.container)
        node.add_child(child_node=transition_doors.container)

        left_door_texture = Texture.get("assets/images/dungeon/door_left_open.png")
        right_door_texture = Texture.get("assets/images/dungeon/door_right_open.png")
        up_door_texture = Texture.get("assets/images/dungeon/door_up_open.png")
        down_door_texture = Texture.get("assets/images/dungeon/door_down_open.png")

        # Temp vars
        left_door_collider_rect = Rect2(10, 0, 20, left_door_texture.height)
        right_door_collider_rect = Rect2(15, 0, 20, right_door_texture.height)
        up_door_collider_rect = Rect2(0, 6, up_door_texture.width, 10)
        down_door_collider_rect = Rect2(0, 10, down_door_texture.width, 10)

        # Setting up data list to iterate setting up doors
        doors_setup_data = [
            # Current Doors
            [
                current_doors.left,
                Door.ROOM_LEFT_POSITION,
                left_door_collider_rect,
                True,
                current_doors.container,
                left_door_texture,
            ],
            [
                current_doors.right,
                Door.ROOM_RIGHT_POSITION,
                right_door_collider_rect,
                True,
                current_doors.container,
                right_door_texture,
            ],
            [
                current_doors.up,
                Door.ROOM_UP_POSITION,
                up_door_collider_rect,
                True,
                current_doors.container,
                up_door_texture,
            ],
            [
                current_doors.down,
                Door.ROOM_DOWN_POSITION,
                down_door_collider_rect,
                True,
                current_doors.container,
                down_door_texture,
            ],
            # Transition
            [
                transition_doors.left,
                Door.ROOM_LEFT_POSITION,
                left_door_collider_rect,
                False,
                transition_doors.container,
                left_door_texture,
            ],
            [
                transition_doors.right,
                Door.ROOM_RIGHT_POSITION,
                right_door_collider_rect,
                False,
                transition_doors.container,
                right_door_texture,
            ],
            [
                transition_doors.up,
                Door.ROOM_UP_POSITION,
                up_door_collider_rect,
                False,
                transition_doors.container,
                up_door_texture,
            ],
            [
                transition_doors.down,
                Door.ROOM_DOWN_POSITION,
                down_door_collider_rect,
                False,
                transition_doors.container,
                down_door_texture,
            ],
        ]

        for door_data in doors_setup_data:
            door = door_data[0]
            door.position = door_data[1]
            door.collider_rect = door_data[2]
            door.set_open(door_data[3])
            container = door_data[4]
            container.add_child(child_node=door)
            sprite = Sprite.new()
            sprite.texture = door_data[5]
            door.add_child(child_node=sprite)

        room_manager = RoomManager()
        room_manager.room_doors = current_doors
        room_manager.transition_doors = transition_doors

    @staticmethod
    def create_rooms(node: Node) -> None:
        room_manager = RoomManager()
        # (0, 0) Room is setup in editor
        initial_room = Room(position=Vector2.ZERO())
        room_manager.add_room(initial_room)
        room_manager.current_room = initial_room
        # Other rooms are created procedurally
        room_bg_texture = Texture.get(file_path="assets/images/dungeon_level.png")
        for room in [Room(position=Vector2.UP())]:
            room_manager.add_room(room)
            room_bg_sprite = Sprite.new()
            room_bg_sprite.z_index = -1
            room_bg_sprite.texture = room_bg_texture
            room_bg_sprite.position = room_manager.get_world_position(room.position)
            node.add_child(child_node=room_bg_sprite)
