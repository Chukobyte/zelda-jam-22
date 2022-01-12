from seika.math import Vector2
from seika.node import CollisionShape2D


class Attack(CollisionShape2D):
    Z_INDEX = 2

    def __init__(self, entity_id: int):
        super().__init__(entity_id=entity_id)
        self.life_time = 0.0
        self.damage = 0
        self.has_collided = False
        self.direction = Vector2()
        self.speed = 100

    def _start(self) -> None:
        self.z_index = Attack.Z_INDEX
