from seika.node import Node, CollisionShape2D
from seika.math import Vector2, Rect2

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
        pass


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
        wall_colliders.left_down_down.collider_rect = Rect2(64, 188, 124, 32)
        wall_colliders.right_up_up.collider_rect = Rect2(212, 0, 128, 32)
        wall_colliders.right_up_right.collider_rect = Rect2(340, 0, 64, 100)
        wall_colliders.right_down_right.collider_rect = Rect2(340, 124, 64, 100)
        wall_colliders.right_down_down.collider_rect = Rect2(212, 188, 128, 32)

        for wall_collider in wall_colliders.walls:
            wall_collider.tags = ["wall"]
            node.add_child(child_node=wall_collider)
