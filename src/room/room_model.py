from seika.math import Vector2

from src.room.door import DoorStatus


class RoomType:
    NONE = -1
    INTRO = 0
    COMBAT = 1
    TREASURE = 2
    BOSS = 3
    END = 4


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
        Vector2(0, -2): RoomData(
            left_door_status=DoorStatus.CLOSED,
            right_door_status=DoorStatus.CLOSED,
            up_door_status=DoorStatus.CLOSED,
            down_door_status=DoorStatus.CLOSED,
            room_type=RoomType.END,
        ),
    }
