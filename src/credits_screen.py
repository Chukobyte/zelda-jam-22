from seika.node import Node2D
from seika.scene import SceneTree
from seika.input import Input
from seika.engine import Engine

from src.game_context import GameContext, GameState


class CreditsScreen(Node2D):
    def _physics_process(self, delta: float) -> None:
        if Input.is_action_pressed(action_name="debug_quit"):
            Engine.exit()

        if Input.is_action_just_pressed(
            action_name="attack"
        ) or Input.is_action_just_pressed(action_name="credits"):
            GameContext.set_game_state(GameState.TITLE_SCREEN)
            SceneTree.change_scene(scene_path="scenes/title_screen.sscn")
