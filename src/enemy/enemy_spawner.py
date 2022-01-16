from seika.node import Node2D
from seika.math import Vector2

from src.enemy.boss import Boss
from src.enemy.enemy_shield import EnemyShield
from src.enemy.cultist import Cultist


class EnemySpawner:
    @staticmethod
    def spawn_boss(main_node: Node2D, position: Vector2) -> Boss:
        boss = Boss.new()
        boss.position = position
        main_node.add_child(boss)
        return boss

    @staticmethod
    def spawn_cultist(main_node: Node2D, position: Vector2) -> Cultist:
        cultist = Cultist.new()
        cultist.position = position
        main_node.add_child(cultist)
        return cultist

    @staticmethod
    def spawn_shield(main_node: Node2D, position: Vector2) -> EnemyShield:
        shield = EnemyShield.new()
        shield.position = position
        main_node.add_child(shield)
        return shield
