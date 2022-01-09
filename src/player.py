from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.player_stats import PlayerStats, State


class Player(AnimatedSprite):
    def _start(self) -> None:
        self.stats = PlayerStats()
        self.collider = self.get_node(name="PlayerCollider")
        self.velocity = Vector2()

        def attack_timeout_func():
            self.stats.state = State.IDLE

        self.attack_timer = SimpleTimer(wait_time=0.5, timeout_func=attack_timeout_func)

    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="attack"):
            if self.stats.state != State.ATTACK:
                self.stats.state = State.ATTACK
                self.attack_timer.start()

        if self.stats.state == State.ATTACK:
            self.attack_timer.tick(delta=delta)
        else:
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
            collided_walls = Collision.get_collided_nodes_by_tag(
                node=self.collider, tag="wall", offset=new_velocity
            )
            if not collided_walls:
                self.stats.state = State.MOVE
                self.position += new_velocity
        else:
            self.stats.state = State.IDLE
