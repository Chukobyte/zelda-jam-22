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


class Door(CollisionShape2D):
    Z_INDEX = 1
    ROOM_LEFT_POSITION = Vector2(22, 74)
    ROOM_RIGHT_POSITION = Vector2(334, 74)
    ROOM_UP_POSITION = Vector2(168, 8)
    ROOM_DOWN_POSITION = Vector2(168, 190)
    OPEN_DOOR_TAG = ["open-door"]

    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.direction = Vector2()

    @staticmethod
    def new_door(dir: Vector2):
        door = Door.new()
        door.direction = dir
        return door


class DungeonDoors:
    def __init__(
        self,
        left: Door,
        right: Door,
        up: Door,
        down: Door,
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
    SOLID_TAG = ["solid"]

    def __init__(self, position: Vector2):
        self.position = position
        self.size = ProjectProperties.BASE_RESOLUTION

    def __str__(self):
        return f"(position = {self.position}, size = {self.size})"

    def __repr__(self):
        return f"(position = {self.position}, size = {self.size})"
