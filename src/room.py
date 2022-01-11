from seika.math import Vector2
from seika.node import Node2D, CollisionShape2D

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
        container: Node2D,
    ):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.container = container
        self.doors = [left, right, up, down]

    def move(self, position: Vector2) -> None:
        self.container.position = position


class Room:
    def __init__(self, position: Vector2):
        self.position = position
        self.size = ProjectProperties.BASE_RESOLUTION

    def __str__(self):
        return f"(position = {self.position}, size = {self.size})"

    def __repr__(self):
        return f"(position = {self.position}, size = {self.size})"
