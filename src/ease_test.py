import math

from seika.engine import Engine
from seika.input import Input
from seika.math import Vector2
from seika.node import Node2D
from seika.utils import SimpleTimer
from src.math.ease import Ease


class EaseTest(Node2D):
    def _start(self) -> None:
        self.start_timer = SimpleTimer(wait_time=1.0, start_on_init=True)
        self.has_started = False
        self.point_a = self.get_node("PointASprite")
        self.point_b = self.get_node("PointBSprite")
        self.position_text_label = self.get_node("APositionTextLabel")
        self.elapsed_time = 0.0

    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()

        if self.start_timer.tick(delta):
            self.has_started = True
        if self.has_started:
            self.elapsed_time += delta
            new_position = Ease.Cubic.ease_out_vec2(
                elapsed_time=self.elapsed_time,
                from_pos=self.point_a.position,
                to_pos=self.point_b.position,
                duration=5.0,
            )
            # new_position.x = math.floor(new_position.x)
            # new_position.y = math.floor(new_position.y)
            self.point_a.position = new_position
            self.position_text_label.text = self.get_pos_string(new_position)

    def get_pos_string(self, vec2: Vector2) -> str:
        return f"Position: ({vec2.x:.4f}, {vec2.y:.4f})"
