from seika.node import Node2D
from seika.math import Vector2

from src.enemy.boss import Boss


class EnemySpawner:
    @staticmethod
    def spawn_boss(main_node: Node2D, position: Vector2) -> Boss:
        boss = Boss.new()
        boss.position = position
        main_node.add_child(boss)
