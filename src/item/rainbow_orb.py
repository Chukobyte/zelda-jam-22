from seika.assets import Texture
from seika.color import Color
from seika.math import Rect2
from seika.node import CollisionShape2D, Sprite

from src.task.task import co_suspend, Task, co_wait_until_seconds, TaskManager


class RainbowOrb(CollisionShape2D):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None
        self.color_ramp = [
            Color(255 / 255.0, 97 / 255.0, 178 / 255.0),
            Color(255 / 255.0, 162 / 255.0, 0),
            Color(235 / 255.0, 211 / 255.0, 32 / 255.0),
            Color(154 / 255.0, 235 / 255.0, 0),
            Color(97, 211, 227 / 255.0),
            Color(162 / 255.0, 113 / 255.0, 255 / 255.0),
            Color(243 / 255.0, 97 / 255.0, 255 / 255.0),
        ]
        self.tasks = TaskManager(
            initial_tasks=[Task(name="change_color", func=self.change_colors)]
        )

    def _start(self) -> None:
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/items/rainbow_orb.png")
        self.sprite.texture = texture
        self.collider_rect = Rect2(0, 0, texture.width, texture.height)
        self.add_child(self.sprite)
        self.tags = ["rainbow_orb"]

    def _physics_process(self, delta: float) -> None:
        self.tasks.run_tasks()

    @Task.task_func(debug=True)
    def change_colors(self):
        current_color_ramp = []
        while True:
            if len(current_color_ramp) <= 0:
                current_color_ramp = self.color_ramp.copy()
            new_color = current_color_ramp.pop(0)
            self.sprite.modulate = new_color
            yield from co_wait_until_seconds(wait_time=0.2)
        yield co_suspend()
