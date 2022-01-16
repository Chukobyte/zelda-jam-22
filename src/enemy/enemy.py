from seika.color import Color
from seika.math import Vector2
from seika.node import CollisionShape2D, AnimatedSprite

from src.stats import RoomEntityStats
from src.task.task import (
    TaskManager,
    co_suspend,
    Task,
    co_wait_until_seconds,
    co_return,
)


class EnemyStats(RoomEntityStats):
    pass


class Enemy(AnimatedSprite):
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
        self.direction = Vector2.DOWN()
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

    @Task.task_func()
    def damaged_flash(self):
        colors = self.damaged_colors.copy()
        while len(colors) > 0:
            color = colors.pop(0)
            self.modulate = color
            yield from co_wait_until_seconds(wait_time=0.1)
        yield co_return()
