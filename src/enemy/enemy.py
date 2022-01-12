from seika.color import Color
from seika.node import Sprite, CollisionShape2D, Node2D

from src.task.task import (
    TaskManager,
    co_suspend,
    Task,
    co_wait_until_seconds,
    co_return,
)


class EnemyStats:
    def __init__(self):
        self.base_hp = 0
        self.hp = 0

    def set_all_hp(self, value: int) -> None:
        self.base_hp = value
        self.hp = value


class Enemy(Sprite):
    """
    Base class for enemies.  Includes the following:
        * stats
        * collider
        * task fsm
        * helper functions
    """

    TAG = "enemy"

    def __init__(self, entity_id: int) -> None:
        super().__init__(entity_id)
        self.stats = EnemyStats()
        self.collider = None
        self.tasks = TaskManager()
        self.damaged_colors = [
            Color(2.0, 2.0, 2.0),
            Color(2.0, 1.5, 1.5),
            Color(0.8, 0.5, 0.5),
            Color(0.5, 0.25, 0.25),
            Color(1.0, 1.0, 1.0),
        ]

    def _start(self) -> None:
        self.collider = CollisionShape2D.new()
        self.collider.tags = [Enemy.TAG]
        self.add_child(self.collider)

    def take_damage(self, attack) -> None:
        self.stats.hp -= attack.damage
        color_value = self.modulate.r * 0.75
        self.modulate = Color(color_value, color_value, color_value)
        if self.stats.hp <= 0:
            self.queue_deletion()
        else:
            self.tasks.add_task(
                task=Task(name="damaged_flash", func=self.damaged_flash)
            )

    @Task.task_func(debug=True)
    def damaged_flash(self):
        colors = self.damaged_colors.copy()
        while len(colors) > 0:
            color = colors.pop()
            self.modulate = color
            yield from co_wait_until_seconds(wait_time=0.1)
        yield co_return()
