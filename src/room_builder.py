from seika.node import Node, CollisionShape2D, Sprite
from seika.math import Vector2, Rect2
from seika.assets import Texture

from src.project_properties import ProjectProperties


class WallColliders:
    def __init__(
        self,
        left_up_up: CollisionShape2D,
        left_up_left: CollisionShape2D,
        left_down_left: CollisionShape2D,
        left_down_down: CollisionShape2D,
        right_up_up: CollisionShape2D,
        right_up_right: CollisionShape2D,
        right_down_down: CollisionShape2D,
        right_down_right: CollisionShape2D,
    ):
        self.left_up_up = left_up_up
        self.left_up_left = left_up_left
        self.left_down_left = left_down_left
        self.left_down_down = left_down_down
        self.right_up_up = right_up_up
        self.right_up_right = right_up_right
        self.right_down_down = right_down_down
        self.right_down_right = right_down_right
        self.walls = [
            left_up_up,
            left_up_left,
            left_down_left,
            left_down_down,
            right_up_up,
            right_down_down,
            right_down_right,
            right_up_right,
        ]

    def update_wall_positions(self, position: Vector2) -> None:
        for wall_collider in self.walls:
            wall_collider.position = position


class DungeonDoors:
    def __init__(
        self,
        left: CollisionShape2D,
        right: CollisionShape2D,
        up: CollisionShape2D,
        down: CollisionShape2D,
    ):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.doors = [left, right, up, down]


class RoomBuilder:
    @staticmethod
    def create_wall_colliders(node: Node) -> None:
        room_dimensions = ProjectProperties.BASE_RESOLUTION

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

    @staticmethod
    def create_doors(node: Node) -> None:
        current_doors = DungeonDoors(
            left=CollisionShape2D.new(),
            right=CollisionShape2D.new(),
            up=CollisionShape2D.new(),
            down=CollisionShape2D.new(),
        )
        # transition_doors = DungeonDoors(
        #     left=CollisionShape2D.new(),
        #     right=CollisionShape2D.new(),
        #     up=CollisionShape2D.new(),
        #     down=CollisionShape2D.new(),
        # )

        left_door_texture = Texture.get("assets/images/dungeon/door_left_open.png")
        right_door_texture = Texture.get("assets/images/dungeon/door_right_open.png")
        # up_door_texture = Texture.get("assets/images/dungeon/door_up_open.png")
        # down_door_texture = Texture.get("assets/images/dungeon/door_down_open.png")

        print(f"left_texture = {left_door_texture}")
        for left_door in [current_doors.left]:
            left_door.position = Vector2(22, 74)
            left_door.z_index = 1
            left_door.collider_rect = Rect2(
                0, 0, left_door_texture.width, left_door_texture.height
            )
            node.add_child(child_node=left_door)
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
            node.add_child(child_node=right_door)
            sprite = Sprite.new()
            sprite.draw_source = Rect2(
                0, 0, right_door_texture.width, right_door_texture.height
            )
            sprite.texture = right_door_texture
            right_door.add_child(child_node=sprite)
        # for up_door in [current_doors.up]:
        #     up_door.z_index = 1
        #     up_door.collider_rect = Rect2(0, 0, up_door_texture.width, up_door_texture.height)
        #     node.add_child(child_node=up_door)
        #     sprite = Sprite.new()
        #     sprite.draw_source = Rect2(0, 0, 45, 75)
        #     sprite.texture = up_door_texture
        #     up_door.add_child(child_node=sprite)
        # for down_door in [current_doors.down]:
        #     down_door.z_index = 1
        #     down_door.collider_rect = Rect2(0, 0, down_door_texture.width, down_door_texture.height)
        #     node.add_child(child_node=down_door)
        #     sprite = Sprite.new()
        #     sprite.draw_source = Rect2(0, 0, 45, 75)
        #     sprite.texture = down_door_texture
        #     down_door.add_child(child_node=sprite)
