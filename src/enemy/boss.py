from seika.assets import Texture
from seika.math import Rect2

from src.enemy.enemy import Enemy
from src.game_context import GameContext


class Boss(Enemy):
    def _start(self) -> None:
        super()._start()
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_boss.png")
        self.texture = boss_texture
        self.collider.collider_rect = Rect2(
            0, 0, boss_texture.width, boss_texture.height
        )

    def _physics_process(self, delta: float) -> None:
        pass

    # TODO: temp win state when defeated
    def _end(self) -> None:
        # GameContext().has_won = True
        pass
