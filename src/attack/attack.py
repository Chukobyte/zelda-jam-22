from seika.math import Vector2
from seika.node import CollisionShape2D
from seika.utils import SimpleTimer


class Attack(CollisionShape2D):
    Z_INDEX = 2

    def __init__(self, entity_id: int):
        super().__init__(entity_id=entity_id)
        self.life_timer = SimpleTimer(wait_time=0.0)
        self.life_time = 0.0
        self.damage = 0
        self.has_collided = False
        self.direction = Vector2()
        self.speed = 100

    @property
    def life_time(self) -> float:
        return self.life_timer.wait_time

    @life_time.setter
    def life_time(self, value: float) -> None:
        self.set_life_time(value)

    def set_life_time(self, value: float) -> None:
        self.life_timer.wait_time = value

    def _start(self) -> None:
        self.z_index = Attack.Z_INDEX
        self.life_timer.start()

    def _physics_process(self, delta: float) -> None:
        if self.life_timer.tick(delta):
            self.queue_deletion()
