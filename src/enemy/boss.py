import random

from seika.assets import Texture
from seika.math import Rect2, Vector2

from src.attack.enemy_attack import EnemyAttack
from src.enemy.enemy import Enemy
from src.game_context import GameContext
from src.room.room_manager import *  # Fix circular dependency
from src.task.task import Task, co_wait_until_seconds, co_return


class Boss(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_boss.png")
        self.texture = boss_texture
        self.collider.collider_rect = Rect2(
            0, 0, boss_texture.width, boss_texture.height
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
            attack.position = self.position
            attack.direction = self.position.direction_to(target=player.position)
            self.get_parent().add_child(attack)
            yield from co_wait_until_seconds(wait_time=attack.life_time)
            attack.queue_deletion()
        yield co_return()

    # TODO: temp win state when defeated
    def _end(self) -> None:
        # GameContext().has_won = True
        RoomManager().set_current_room_to_cleared()
