import random

from seika.assets import Texture
from seika.math import Rect2, Vector2

from src.attack.enemy_attack import EnemyAttack
from src.enemy.enemy import Enemy
from src.task.task import Task, co_wait_until_seconds, co_return


class Boss(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_boss.png")
        self.texture = boss_texture
        self.collider.collider_rect = Rect2(
            8, 2, boss_texture.width - 8, boss_texture.height - 2
        )
        self.tasks.add_task(task=Task(name="shoot", func=self.shoot_shot))

    def _physics_process(self, delta: float) -> None:
        self.tasks.run_tasks()

    @Task.task_func(debug=True)
    def shoot_shot(self):
        player = self.get_node(name="Player")
        assert player
        while True:
            yield from co_wait_until_seconds(wait_time=random.uniform(2.0, 4.0))
            attack = EnemyAttack.new()
            attack.position = self.position + Vector2(32, 0)
            attack.direction = attack.position.direction_to(target=player.position)
            self.get_parent().add_child(attack)
            yield from co_wait_until_seconds(wait_time=attack.life_time)
        yield co_return()

    # TODO: temp win state when defeated
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
