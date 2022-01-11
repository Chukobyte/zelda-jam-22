from seika.node import Node2D
from seika.scene import SceneTree
from seika.input import Input
from seika.engine import Engine

from src.game_context import GameContext, GameState


class TitleScreen(Node2D):
    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()

        if Input.is_action_just_pressed(action_name="credits"):
            GameContext.set_game_state(GameState.CREDITS)
            SceneTree.change_scene(scene_path="scenes/credits_screen.sscn")

        if Input.is_action_just_pressed(action_name="attack"):
            GameContext.set_game_state(GameState.PLAYING)
            SceneTree.change_scene(scene_path="scenes/main.sscn")
