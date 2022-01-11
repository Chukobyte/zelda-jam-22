from seika.node import CollisionShape2D, Sprite
from seika.assets import Texture
from seika.math import Rect2
from seika.physics import Collision

from src.enemy.enemy import Enemy

# Will probably have multiple attacks broken out into separate files...


class Attack(CollisionShape2D):
    pass


class PlayerAttack(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None

    def _start(self) -> None:
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/player_attack.png")
        self.sprite.texture = texture
        self.add_child(self.sprite)

        self.collider_rect = Rect2(0, 0, texture.width, texture.height)

    def _physics_process(self, delta: float) -> None:
        enemies_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag=Enemy.TAG
        )
        if enemies_colliders:
            first_enemy = enemies_colliders[0].get_parent()
            first_enemy.queue_deletion()