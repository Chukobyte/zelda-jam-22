from seika.math import Vector2

from src.room.room import Room
from src.stats import RoomEntityStats


class MoveParams:
    def __init__(self):
        self.accel = 100
        self.non_facing_dir_accel = 20


class PlayerStats(RoomEntityStats):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.move_params = MoveParams()
            cls.base_hp = 0
            cls.hp = 0
        return cls._instance

    def __init__(self):
        pass
