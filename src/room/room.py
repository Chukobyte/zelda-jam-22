from seika.math import Vector2, Rect2
from seika.node import CollisionShape2D

from src.project_properties import ProjectProperties
from src.room.door import DoorState
from src.room.room_model import RoomData, RoomModel


class WallColliderCollisionRect:
    LEFT_UP_UP = Rect2(64, 0, 124, 32)
    LEFT_UP_LEFT = Rect2(0, 0, 64, 100)
    LEFT_DOWN_LEFT = Rect2(0, 124, 64, 100)
    LEFT_DOWN_DOWN = Rect2(64, 192, 124, 32)

    RIGHT_UP_UP = Rect2(212, 0, 128, 32)
    RIGHT_UP_RIGHT = Rect2(340, 0, 64, 100)
    RIGHT_DOWN_RIGHT = Rect2(340, 124, 64, 100)
    RIGHT_DOWN_DOWN = Rect2(212, 192, 128, 32)


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

    def set_default_collision_rects(self) -> None:
        self.left_up_up.collider_rect = WallColliderCollisionRect.LEFT_UP_UP
        self.left_up_left.collider_rect = WallColliderCollisionRect.LEFT_UP_LEFT
        self.left_down_left.collider_rect = WallColliderCollisionRect.LEFT_DOWN_LEFT
        self.left_down_down.collider_rect = WallColliderCollisionRect.LEFT_DOWN_DOWN

        self.right_up_up.collider_rect = WallColliderCollisionRect.RIGHT_UP_UP
        self.right_up_right.collider_rect = WallColliderCollisionRect.RIGHT_UP_RIGHT
        self.right_down_right.collider_rect = WallColliderCollisionRect.RIGHT_DOWN_RIGHT
        self.right_down_down.collider_rect = WallColliderCollisionRect.RIGHT_DOWN_DOWN

    def update_collision_rects_near_door(self, data: RoomData) -> None:
        solid_door_statuses = [
            DoorState.SOLID_WALL,
            DoorState.BREAKABLE_WALL,
            DoorState.CLOSED,
        ]
        left_up_up_rect = WallColliderCollisionRect.LEFT_UP_UP

        if data.up_door_status in solid_door_statuses:
            left_up_up_rect += Rect2(0.0, 0.0, 32.0, 0.0)
        self.left_up_up.collider_rect = left_up_up_rect

        left_up_left_rect = WallColliderCollisionRect.LEFT_UP_LEFT
        if data.left_door_status in solid_door_statuses:
            left_up_left_rect += Rect2(0.0, 0.0, 0.0, 32.0)
        self.left_up_left.collider_rect = left_up_left_rect

        left_down_down_rect = WallColliderCollisionRect.LEFT_DOWN_DOWN
        if data.down_door_status in solid_door_statuses:
            left_down_down_rect += Rect2(0.0, 0.0, 32.0, 0.0)
        self.left_down_down.collider_rect = left_down_down_rect

        right_up_right_rect = WallColliderCollisionRect.RIGHT_UP_RIGHT
        if data.right_door_status in solid_door_statuses:
            right_up_right_rect += Rect2(0.0, 0.0, 0.0, 32.0)
        self.right_up_right.collider_rect = right_up_right_rect


class Room:
    SOLID_TAG = ["solid"]

    def __init__(self, position: Vector2):
        self.position = position
        self.size = ProjectProperties.BASE_RESOLUTION
        self.data = RoomData()

    def set_room_data(self, data: RoomData) -> None:
        self.data.left_door_status = data.left_door_status
        self.data.right_door_status = data.right_door_status
        self.data.up_door_status = data.up_door_status
        self.data.down_door_status = data.down_door_status
        self.data.room_type = data.room_type
        self.data.enemies = data.enemies

    def __str__(self):
        return f"(position = {self.position}, size = {self.size}, data = {self.data})"

    def __repr__(self):
        return f"(position = {self.position}, size = {self.size}, data = {self.data})"
