from seika.node import Sprite, CollisionShape2D


class Enemy(Sprite):
    """
    Base class for enemies.  Includes helper functions and a collider.
    All enemies are procedurally generated for now.
    """

    def __init__(self, entity_id: int) -> None:
        super().__init__(entity_id)
        self.collider = None
        self.task = None

    def _start(self) -> None:
        self.collider = CollisionShape2D.new()
