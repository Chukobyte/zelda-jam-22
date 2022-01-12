from seika.math import Vector2

from src.room.door import DoorStatus


class RoomType:
    NONE = -1
    INTRO = 0
    COMBAT = 1
    TREASURE = 2
    BOSS = 3
    END = 4

    TYPE_TO_STRING = {
        NONE: "None",
        INTRO: "Intro",
        COMBAT: "Combat",
        TREASURE: "Treasure",
        BOSS: "Boss",
        END: "End",
    }

    @staticmethod
    def to_string(room_type: int) -> str:
        return RoomType.TYPE_TO_STRING.get(room_type, "Invalid")


class RoomData:
    def __init__(
        self,
        left_door_status=DoorStatus.CLOSED,
        right_door_status=DoorStatus.CLOSED,
        up_door_status=DoorStatus.CLOSED,
        down_door_status=DoorStatus.CLOSED,
        room_type=RoomType.NONE,
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
            left_door_status=DoorStatus.CLOSED,
            right_door_status=DoorStatus.CLOSED,
            up_door_status=DoorStatus.OPEN,
            down_door_status=DoorStatus.CLOSED,
            room_type=RoomType.INTRO,
        ),
        Vector2.UP(): RoomData(
            left_door_status=DoorStatus.CLOSED,
            right_door_status=DoorStatus.CLOSED,
            up_door_status=DoorStatus.OPEN,
            down_door_status=DoorStatus.OPEN,
            room_type=RoomType.BOSS,
        ),
        Vector2(0.0, -2.0): RoomData(
            left_door_status=DoorStatus.CLOSED,
            right_door_status=DoorStatus.CLOSED,
            up_door_status=DoorStatus.CLOSED,
            down_door_status=DoorStatus.OPEN,
            room_type=RoomType.END,
        ),
    }
