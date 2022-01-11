from seika.node import Sprite, CollisionShape2D, Node2D


class EnemyStats:
    def __init__(self):
        self.base_hp = 0
        self.hp = 0

    def set_all_hp(self, value: int) -> None:
        self.base_hp = value
        self.hp = value


class EnemyCache:
    """
    Includes an enemy cache to get around bug with not getting proper instances with collision checks
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.cache = {}
        return cls._instance

    def add(self, enemy: Node2D) -> None:
        self.cache[enemy.entity_id] = enemy

    def remove(self, enemy: Node2D) -> None:
        del self.cache[enemy.entity_id]

    def get(self, enemy: Node2D):
        return self.cache[enemy.entity_id]


class Enemy(Sprite):
    """
    Base class for enemies.  Includes the following:
        * stats
        * collider
        * task fsm
        * helper functions
    Also registers/removes entity to/from entity cache
    """

    TAG = "enemy"

    def __init__(self, entity_id: int) -> None:
        super().__init__(entity_id)
        self.stats = EnemyStats()
        self.collider = None
        self.task = None

    def _start(self) -> None:
        EnemyCache().add(self)
        self.collider = CollisionShape2D.new()
        self.collider.tags = [Enemy.TAG]
        self.add_child(self.collider)

    def take_damage(self, attack) -> None:
        self.stats.hp -= attack.damage
        if self.stats.hp <= 0:
            self.queue_deletion()

    def _end(self) -> None:
        EnemyCache().remove(self)


class EnemyCast:
    """
    Static class to hide the details of the Enemy Cache
    """

    @staticmethod
    def cast(node2D: Node2D) -> Enemy:
        return EnemyCache().get(node2D)
