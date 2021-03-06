from seika.assets import Texture
from seika.math import Rect2
from seika.node import CollisionShape2D, Sprite


class Tricolora(CollisionShape2D):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None

    def _start(self) -> None:
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/items/tricolora.png")
        self.sprite.texture = texture
        self.collider_rect = Rect2(0, 0, texture.width, texture.height)
        self.add_child(self.sprite)
        self.tags = ["tricolora"]
