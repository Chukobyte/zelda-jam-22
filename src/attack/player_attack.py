from seika.assets import Texture
from seika.math import Rect2, Vector2
from seika.node import Sprite
from seika.physics import Collision

from src.attack.attack import Attack
from src.enemy.enemy import Enemy


# TODO: Refactor to avoid duplication
class PlayerAttack(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None
        self.set_life_time(0.5)
        self.damage = 1

    def _start(self) -> None:
        super()._start()
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/player/player_attack.png")
        self.sprite.texture = texture
        self.add_child(self.sprite)

        self.collider_rect = Rect2(0, 0, texture.width, texture.height)

    def _physics_process(self, delta: float) -> None:
        super()._physics_process(delta)
        enemies_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag=Enemy.TAG
        )
        if enemies_colliders and not self.has_collided:
            self.has_collided = True
            first_enemy = enemies_colliders[0].get_parent()
            first_enemy.take_damage(attack=self)


class BoltAttack(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None
        self.set_life_time(3.0)
        self.damage = 1

    def _start(self) -> None:
        super()._start()
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/player/player_bolt_attack.png")
        self.sprite.texture = texture
        self.add_child(self.sprite)

        self.collider_rect = Rect2(0, 0, texture.width, texture.height)

    def _physics_process(self, delta: float) -> None:
        super()._physics_process(delta)
        self.position += self.direction * Vector2(
            self.speed * delta, self.speed * delta
        )
        enemies_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag=Enemy.TAG
        )
        if enemies_colliders and not self.has_collided:
            self.has_collided = True
            first_enemy = enemies_colliders[0].get_parent()
            first_enemy.take_damage(attack=self)


class BombAttack(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None
        self.set_life_time(2.0)
        self.damage = 1

    def _start(self) -> None:
        super()._start()
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/player/player_bomb_attack.png")
        self.sprite.texture = texture
        self.add_child(self.sprite)

        self.collider_rect = Rect2(0, 0, texture.width, texture.height)

    def _physics_process(self, delta: float) -> None:
        super()._physics_process(delta)
        enemies_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag=Enemy.TAG
        )
        if enemies_colliders and not self.has_collided:
            self.has_collided = True
            first_enemy = enemies_colliders[0].get_parent()
            first_enemy.take_damage(attack=self)
