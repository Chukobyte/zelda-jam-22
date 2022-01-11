from seika.engine import Engine
from seika.input import Input
from seika.node import Node2D


class EndScreen(Node2D):
    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()
