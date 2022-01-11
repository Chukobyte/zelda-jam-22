from seika.engine import Engine
from seika.input import Input
from seika.node import Node2D

from src.game_context import GameContext


class EndScreen(Node2D):
    def _start(self) -> None:
        game_context = GameContext()
        play_time_label = self.get_node(name="PlayTimeLabel")
        play_time_label.text = (
            f"Play Time: {game_context.play_time_counter.time_played_text}"
        )

    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()
