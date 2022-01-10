from seika.node import Node, Node2D, CollisionShape2D, Sprite
from seika.math import Vector2, Rect2
from seika.assets import Texture

from src.room import WallColliders, DungeonDoors, Room, RoomManager


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
            wall_collider.tags = ["wall"]
            node.add_child(child_node=wall_collider)

        room_manager = RoomManager()
        room_manager.wall_colliders = wall_colliders

    @staticmethod
    def create_doors(node: Node) -> None:
        current_doors = DungeonDoors(
            left=CollisionShape2D.new(),
            right=CollisionShape2D.new(),
            up=CollisionShape2D.new(),
            down=CollisionShape2D.new(),
            container=Node2D.new(),
        )
        # TODO: Use for when transitioning to the next room
        # transition_doors = DungeonDoors(
        #     left=CollisionShape2D.new(),
        #     right=CollisionShape2D.new(),
        #     up=CollisionShape2D.new(),
        #     down=CollisionShape2D.new(),
        # )

        node.add_child(child_node=current_doors.container)

        left_door_texture = Texture.get("assets/images/dungeon/door_left_open.png")
        right_door_texture = Texture.get("assets/images/dungeon/door_right_open.png")
        up_door_texture = Texture.get("assets/images/dungeon/door_up_open.png")
        down_door_texture = Texture.get("assets/images/dungeon/door_down_open.png")

        for left_door in [current_doors.left]:
            left_door.position = Vector2(22, 74)
            left_door.z_index = 1
            left_door.collider_rect = Rect2(
                0, 0, left_door_texture.width, left_door_texture.height
            )
            current_doors.container.add_child(child_node=left_door)
            sprite = Sprite.new()
            sprite.draw_source = Rect2(
                0, 0, left_door_texture.width, left_door_texture.height
            )
            sprite.texture = left_door_texture
            left_door.add_child(child_node=sprite)
        for right_door in [current_doors.right]:
            right_door.position = Vector2(334, 74)
            right_door.z_index = 1
            right_door.collider_rect = Rect2(
                0, 0, right_door_texture.width, right_door_texture.height
            )
            current_doors.container.add_child(child_node=right_door)
            sprite = Sprite.new()
            sprite.draw_source = Rect2(
                0, 0, right_door_texture.width, right_door_texture.height
            )
            sprite.texture = right_door_texture
            right_door.add_child(child_node=sprite)
        for up_door in [current_doors.up]:
            up_door.position = Vector2(168, 8)
            up_door.z_index = 1
            up_door.collider_rect = Rect2(
                0, 0, up_door_texture.width, up_door_texture.height
            )
            current_doors.container.add_child(child_node=up_door)
            sprite = Sprite.new()
            sprite.draw_source = Rect2(
                0, 0, up_door_texture.width, up_door_texture.height
            )
            sprite.texture = up_door_texture
            up_door.add_child(child_node=sprite)
        for down_door in [current_doors.down]:
            down_door.position = Vector2(168, 190)
            down_door.z_index = 1
            down_door.collider_rect = Rect2(
                0, 0, down_door_texture.width, down_door_texture.height
            )
            current_doors.container.add_child(child_node=down_door)
            sprite = Sprite.new()
            sprite.draw_source = Rect2(
                0, 0, down_door_texture.width, down_door_texture.height
            )
            sprite.texture = down_door_texture
            down_door.add_child(child_node=sprite)

        room_manager = RoomManager()
        room_manager.room_doors = current_doors

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
            room_bg_sprite.texture = room_bg_texture
            room_bg_sprite.draw_source = Rect2(
                0, 0, room_bg_texture.width, room_bg_texture.height
            )
            room_bg_sprite.position = room_manager.get_world_position(room.position)
            node.add_child(child_node=room_bg_sprite)
