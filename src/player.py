from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2


class Dir:
    LEFT = "l"
    RIGHT = "r"
    UP = "u"
    DOWN = "d"


class PlayerStats:
    class MoveParams:
        def __init__(self):
            self.accel = 100

    def __init__(self):
        self.move_params = PlayerStats.MoveParams()


class Player(AnimatedSprite):
    def _start(self) -> None:
        self.stats = PlayerStats()
        self.collider = self.get_node(name="PlayerCollider")

    def _physics_process(self, delta: float) -> None:
        self._move(delta=delta)

    def _move(self, delta: float) -> None:
        new_velocity = None
        accel = self.stats.move_params.accel * delta

        # Input checks
        left_pressed = Input.is_action_pressed(action_name="move_left")
        right_pressed = Input.is_action_pressed(action_name="move_right")
        up_pressed = Input.is_action_pressed(action_name="move_up")
        down_pressed = Input.is_action_pressed(action_name="move_down")
        # Resolve input
        if left_pressed:
            self.play(animation_name="move_hort")
            self.flip_h = True
            self.direction = Vector2.LEFT()
            new_velocity = Vector2(self.direction.x * accel, 0)
        elif right_pressed:
            self.play(animation_name="move_hort")
            self.flip_h = False
            self.direction = Vector2.RIGHT()
            new_velocity = Vector2(self.direction.x * accel, 0)
        elif up_pressed:
            self.play(animation_name="move_up")
            self.flip_h = False
            self.direction = Vector2.UP()
            new_velocity = Vector2(0, self.direction.y * accel)
        elif down_pressed:
            self.play(animation_name="move_down")
            self.flip_h = False
            self.direction = Vector2.DOWN()
            new_velocity = Vector2(0, self.direction.y * accel)

        # Integrate new velocity
        if new_velocity:
            self.position += new_velocity
