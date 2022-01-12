from seika.engine import Engine
from seika.input import Input
from seika.node import Node2D
from seika.audio import AudioStream
from seika.scene import SceneTree

from src.game_context import GameContext, GameState


class EndScreen(Node2D):
    def _start(self) -> None:
        # Update play time
        game_context = GameContext()
        play_time_label = self.get_node(name="PlayTimeLabel")
        play_time_label.text = (
            f"Play Time: {game_context.play_time_counter.time_played_text}"
        )
        # Stop Music
        music_audio_stream = AudioStream.get(stream_uid="no-color-theme")
        music_audio_stream.stop()

    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()

        if Input.is_action_just_pressed(action_name="attack"):
            game_context = GameContext()
            game_context.has_won = False
            game_context.play_time_counter.reset()
            GameContext.set_game_state(GameState.PLAYING)
            SceneTree.change_scene(scene_path="scenes/main.sscn")
