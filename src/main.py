from seika.node import Node2D
from seika.input import Input
from seika.engine import Engine
from seika.audio import AudioStream

from src.world import World
from src.game_context import GameContext
from src.room.room_builder import RoomBuilder
from src.task.task import Task, TaskManager, co_return, co_wait_until_seconds


class Main(Node2D):
    def _start(self) -> None:
        self.world = World()
        self.game_context = GameContext()
        self.task_manager = TaskManager(
            initial_tasks=[Task(name="start_music", func=self.start_music)]
        )
        # Setup Initial Room
        RoomBuilder.create_wall_colliders(node=self)
        RoomBuilder.create_doors(node=self)
        RoomBuilder.create_rooms(node=self)

    def _physics_process(self, delta: float) -> None:
        self.world.cached_delta = delta
        self.game_context.play_time_counter.update(delta=delta)
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()
        self.task_manager.run_tasks()

    # Countdown test
    @Task.task_func()
    def start_music(self):
        yield from co_wait_until_seconds(wait_time=0.25)

        music_audio_stream = AudioStream.get(stream_uid="no-color-theme")
        music_audio_stream.play()
        yield co_return()
