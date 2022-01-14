from seika.node import Node2D
from seika.scene import SceneTree

from src.game_context import GameContext, GameState


class Init(Node2D):
    def _start(self) -> None:
        GameContext.set_game_state(GameState.INIT)
        SceneTree.change_scene(scene_path="scenes/title_screen.sscn")
        # SceneTree.change_scene(scene_path="scenes/ease_test.sscn")
