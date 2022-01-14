import random

from seika.assets import Texture
from seika.math import Rect2, Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.enemy.enemy import Enemy
from src.math.ease import Ease
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
        move_speed = 90
        while True:
            yield from co_wait_until_seconds(wait_time=random.uniform(2.0, 4.0))
            rand_dirs = [Vector2.DOWN(), Vector2.UP(), Vector2.LEFT(), Vector2.RIGHT()]
            random.shuffle(rand_dirs)
            new_dir = rand_dirs.pop(0)
            move_timer = SimpleTimer(
                wait_time=random.uniform(0.9, 1.3), start_on_init=True
            )
            elapsed_time = 0.0
            while not move_timer.tick(delta=world.cached_delta):
                elapsed_time += world.cached_delta
                new_vel = Vector2(
                    new_dir.x * move_speed * world.cached_delta,
                    new_dir.y * move_speed * world.cached_delta,
                )
                new_pos = new_vel + self.position
                new_pos = Ease.Cubic.ease_out_vec2(elapsed_time=elapsed_time, from_pos=self.position, to_pos=new_pos, duration=move_timer.wait_time)
                collisions = Collision.get_collided_nodes_by_tag(
                    node=self.collider, tag="solid", offset=new_vel
                )
                if not collisions:
                    self.position = new_pos
                elif len(rand_dirs) > 0:
                    new_dir = rand_dirs.pop(0)
                yield co_suspend()
        yield co_return()

    # Temp clearing room
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
