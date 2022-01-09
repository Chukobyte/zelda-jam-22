from seika.node import Node2D
from seika.input import Input
from seika.engine import Engine
from seika.audio import AudioStream
from seika.utils import SimpleTimer

from src.world import World
from src.room_builder import RoomBuilder
from src.task import Task, TaskManager, co_return, co_suspend


class Main(Node2D):
    def _start(self) -> None:
        self.world = World()
        self.task_manager = TaskManager()
        self.task_manager.add_task(
            task=Task(name="count_3", func=self.three_second_countdown)
        )
        # Setup Initial Room
        music_audio_stream = AudioStream.get(stream_uid="test-music")
        music_audio_stream.play()

        RoomBuilder.create_wall_colliders(node=self)

    def _physics_process(self, delta: float) -> None:
        self.world.cached_delta = delta
        if Input.is_action_just_pressed(action_name="debug_quit"):
            Engine.exit()
        self.task_manager.run_tasks()

    # Countdown test
    @Task.task_func(debug=True)
    def three_second_countdown(self):
        count = 0
        countdown_timer = SimpleTimer(wait_time=1.0, start_on_init=True, loops=True)
        while True:
            if countdown_timer.tick(self.world.cached_delta):
                count += 1
                if count >= 3:
                    yield co_return()
            yield co_suspend()
