from seika.node import Node2D
from seika.input import Input
from seika.engine import Engine
from seika.audio import AudioStream

from src.room_builder import RoomBuilder


class Main(Node2D):
    def _start(self) -> None:
        music_audio_stream = AudioStream.get(stream_uid="test-music")
        music_audio_stream.play()

        # Setup Initial Room
        RoomBuilder.create_walls(node=self)

    def _physics_process(self, delta: float) -> None:
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()
