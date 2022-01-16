from seika.math import Vector2

from src.room.door import DoorState


class RoomType:
    NONE = -1
    INTRO = 0
    COMBAT = 1
    EMPTY = 2
    GAIN_BOMB = 3
    BOSS = 4
    END = 5

    TYPE_TO_STRING = {
        NONE: "None",
        INTRO: "Intro",
        COMBAT: "Combat",
        GAIN_BOMB: "GainBomb",
        BOSS: "Boss",
        END: "End",
    }

    @staticmethod
    def to_string(room_type: int) -> str:
        return RoomType.TYPE_TO_STRING.get(room_type, "Invalid")


class AreaType:
    INVALID = "invalid"  # 1
    RED = "red"  # 1
    BLUE = "blue"  # 2
    GREEN = "green"  # 3
    PURPLE = "purple"  # 4


class RoomData:
    def __init__(
        self,
        left_door_status=DoorState.CLOSED,
        right_door_status=DoorState.CLOSED,
        up_door_status=DoorState.CLOSED,
        down_door_status=DoorState.CLOSED,
        room_type=RoomType.NONE,
        area_type=AreaType.INVALID,
        is_cleared=False,
    ) -> None:
        self.left_door_status = left_door_status
        self.right_door_status = right_door_status
        self.up_door_status = up_door_status
        self.down_door_status = down_door_status
        self.is_cleared = is_cleared
        self.room_type = room_type

    def __str__(self):
        return f"(is_cleared = {self.is_cleared}, room_type = {RoomType.to_string(self.room_type)})"

    def __repr__(self):
        return f"(is_cleared = {self.is_cleared}, room_type = {RoomType.to_string(self.room_type)})"


class RoomModel:
    INITIAL_DATA = {
        Vector2.ZERO(): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.SOLID_WALL,
            room_type=RoomType.INTRO,
            area_type=AreaType.RED,
        ),
        Vector2.UP(): RoomData(
            left_door_status=DoorState.OPEN,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(0.0, -2.0): RoomData(
            left_door_status=DoorState.OPEN,
            right_door_status=DoorState.OPEN,
            up_door_status=DoorState.SOLID_WALL,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(-1.0, -1.0): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.OPEN,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.SOLID_WALL,
            # room_type=RoomType.BOSS,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(-1.0, -2.0): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.OPEN,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(-1.0, -3.0): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.SOLID_WALL,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.GAIN_BOMB,
            area_type=AreaType.RED,
        ),
        Vector2(1.0, -2.0): RoomData(
            left_door_status=DoorState.OPEN,
            right_door_status=DoorState.OPEN,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.SOLID_WALL,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(1.0, -3.0): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.OPEN,
            up_door_status=DoorState.SOLID_WALL,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(2.0, -2.0): RoomData(
            left_door_status=DoorState.OPEN,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.SOLID_WALL,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(2.0, -3.0): RoomData(
            left_door_status=DoorState.OPEN,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.BREAKABLE_WALL,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(2.0, -4.0): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.OPEN,
            down_door_status=DoorState.CRACKED_OPEN_WALL,
            room_type=RoomType.EMPTY,
            area_type=AreaType.RED,
        ),
        Vector2(2.0, -5.0): RoomData(
            left_door_status=DoorState.SOLID_WALL,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.CLOSED,
            down_door_status=DoorState.OPEN,
            room_type=RoomType.COMBAT,
            area_type=AreaType.RED,
        ),
        Vector2(3.0, -5.0): RoomData(
            left_door_status=DoorState.OPEN,
            right_door_status=DoorState.SOLID_WALL,
            up_door_status=DoorState.CLOSED,
            down_door_status=DoorState.SOLID_WALL,
            room_type=RoomType.END,
            area_type=AreaType.RED,
        ),
    }
