class MoveParams:
    def __init__(self):
        self.accel = 100


class State:
    IDLE = "idle"
    MOVE = "move"
    ATTACK = "attack"


class PlayerStats:
    def __init__(self):
        self.move_params = MoveParams()
        self.state = State.IDLE
