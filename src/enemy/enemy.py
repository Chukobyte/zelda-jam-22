from seika.node import Sprite, CollisionShape2D


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
    All enemies are procedurally generated for now.
    """

    TAG = "enemy"

    def __init__(self, entity_id: int) -> None:
        super().__init__(entity_id)
        self.stats = EnemyStats()
        self.collider = None
        self.task = None

    def _start(self) -> None:
        self.collider = CollisionShape2D.new()
        self.collider.tags = [Enemy.TAG]
        self.add_child(self.collider)

    def take_damage(self, attack) -> None:
        self.stats.hp -= attack.damage
        if self.stats.hp <= 0:
            self.queue_deletion()
