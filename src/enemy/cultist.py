import random

from seika.assets import Texture
from seika.math import Rect2, Vector2

from src.attack.enemy_attack import CultistAttack
from src.enemy.enemy import Enemy
from src.game_context import PlayState, GameContext
from src.task.task import Task, co_wait_until_seconds, co_return


class Cultist(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_cultist.png")
        self.texture = boss_texture
        self.draw_source = Rect2(0, 0, 16, 16)
        self.collider.collider_rect = Rect2(0, 0, 16, 16)
        self.tasks.add_task(task=Task(name="shoot", func=self.shoot_shot))
        self.game_context = GameContext()

    def _physics_process(self, delta: float) -> None:
        if self.game_context.get_play_state() != PlayState.ROOM_TRANSITION:
            self.tasks.run_tasks()

    @Task.task_func()
    def shoot_shot(self):
        player = self.get_node(name="Player")
        assert player
        while True:
            yield from co_wait_until_seconds(wait_time=random.uniform(2.0, 4.0))
            attack = CultistAttack.new()
            attack.position = self.position
            attack.direction = attack.position.direction_to(target=player.position)
            self.get_parent().add_child(attack)
            yield from co_wait_until_seconds(wait_time=attack.life_time)
        yield co_return()

    # Temp clearing room
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
