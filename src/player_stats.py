from seika.math import Vector2

from src.room import Room


class MoveParams:
    def __init__(self):
        self.accel = 100


class PlayerStats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.move_params = MoveParams()
        return cls._instance
