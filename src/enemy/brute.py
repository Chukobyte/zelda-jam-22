import random

from seika.assets import Texture
from seika.math import Rect2, Vector2
from seika.utils import SimpleTimer

from src.attack.enemy_attack import EnemyAttack
from src.enemy.enemy import Enemy
from src.task.task import Task, co_wait_until_seconds, co_return, co_suspend
from src.world import World


class Brute(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_brute.png")
        self.texture = boss_texture
        self.collider.collider_rect = Rect2(
            0, 0, boss_texture.width, boss_texture.height
        )
        self.tasks.add_task(task=Task(name="move_randomly", func=self.move_randomly))

    def _physics_process(self, delta: float) -> None:
        self.tasks.run_tasks()

    @Task.task_func(debug=True)
    def move_randomly(self):
        world = World()
        player = self.get_node(name="Player")
        assert player
        move_speed = 50
        while True:
            yield from co_wait_until_seconds(wait_time=random.uniform(2.0, 4.0))
            rand_dirs = [Vector2.DOWN(), Vector2.UP(), Vector2.LEFT(), Vector2.RIGHT()]
            random.shuffle(rand_dirs)
            new_dir = rand_dirs.pop(0)
            move_count = 0
            move_timer = SimpleTimer(
                wait_time=random.uniform(0.5, 1.5), start_on_init=True
            )
            while not move_timer.tick(delta=world.cached_delta):
                self.position += Vector2(
                    new_dir.x * move_speed * world.cached_delta,
                    new_dir.y * move_speed * world.cached_delta,
                )
                yield co_suspend()
        yield co_return()

    # Temp clearing room
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
