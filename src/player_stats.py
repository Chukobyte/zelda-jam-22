class MoveParams:
    def __init__(self):
        self.accel = 100
        self.cached_delta = 0.0


class PlayerStats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.move_params = MoveParams()
        return cls._instance
