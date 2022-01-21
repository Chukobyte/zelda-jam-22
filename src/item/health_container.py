from seika.assets import Texture
from seika.math import Rect2
from seika.node import CollisionShape2D, Sprite


class HealthContainer(CollisionShape2D):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None

    def _start(self) -> None:
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/ui/player_health_ui_spritesheet.png")
        self.sprite.texture = texture
        health_container_rect = Rect2(0.0, 0.0, 6.0, 6.0)
        self.sprite.draw_source = health_container_rect
        self.collider_rect = health_container_rect
        self.add_child(self.sprite)
        self.tags = ["health"]
