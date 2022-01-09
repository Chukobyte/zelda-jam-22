class MoveParams:
    def __init__(self):
        self.accel = 100


class State:
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"


class PlayerStats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.move_params = MoveParams()
            cls.state = State.IDLE
        return cls._instance
