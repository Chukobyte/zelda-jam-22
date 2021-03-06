import random

from seika.assets import Texture
from seika.audio import Audio
from seika.camera import Camera2D
from seika.math import Rect2, Vector2
from seika.node import AnimatedSprite
from seika.physics import Collision
from seika.assets import Animation, AnimationFrame

from src.attack.attack import Attack
from src.enemy.enemy import Enemy


# TODO: Refactor to avoid duplication
from src.room.door import DoorState
from src.room.room_manager import RoomManager


class WaveAttack(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.anim_sprite = None
        self.set_life_time(0.5)
        self.damage = 1
        self.enemy_damaged_entity_ids = []

    def _start(self) -> None:
        super()._start()
        self.anim_sprite = AnimatedSprite.new()
        self.anim_sprite.animations = [self._get_animation()]
        self.add_child(self.anim_sprite)
        self.anim_sprite.loops = False
        self.anim_sprite.play()

        self.collider_rect = Rect2(0, 0, 60, 34)

    def _get_animation(self) -> Animation:
        texture = Texture.get(file_path="assets/images/player/player_wave_attack.png")
        anim_frames = []
        for i in range(6):
            anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(60 * i, 0, 60, 34), index=i
                )
            )
        # return Animation(name="wave", speed=300, frames=anim_frames)
        return Animation(name="wave", speed=80, frames=anim_frames)

    def _physics_process(self, delta: float) -> None:
        super()._physics_process(delta)
        enemies_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag=Enemy.TAG
        )
        if enemies_colliders:
            for collider in enemies_colliders:
                enemy = collider.get_parent()
                if enemy.entity_id not in self.enemy_damaged_entity_ids:
                    enemy.take_damage(attack=self)
                    self.enemy_damaged_entity_ids.append(enemy.entity_id)


class BombExplosion(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.anim_sprite = None
        self.set_life_time(1.0)
        self.damage = 3
        self.enemy_damaged_entity_ids = []

    def _get_animation(self) -> Animation:
        texture = Texture.get(
            file_path="assets/images/player/player_bomb_explosion.png"
        )
        anim_frames = []
        for i in range(7):
            anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(37 * i, 0, 37, 33), index=i
                )
            )
        return Animation(name="explode", speed=100, frames=anim_frames)

    def _start(self) -> None:
        super()._start()
        self.anim_sprite = AnimatedSprite.new()
        self.anim_sprite.animations = [self._get_animation()]
        self.add_child(self.anim_sprite)
        self.anim_sprite.loops = False
        self.anim_sprite.frame = 0
        self.anim_sprite.play(animation_name="explode")

        self.collider_rect = Rect2(0, 0, 37, 37)
        Audio.play_sound(sound_id="assets/audio/sfx/bomb_explosion.wav")

    def _physics_process(self, delta: float) -> None:
        enemies_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag=Enemy.TAG
        )

        if enemies_colliders:
            for collider in enemies_colliders:
                enemy = collider.get_parent()
                if enemy.entity_id not in self.enemy_damaged_entity_ids:
                    enemy.take_damage(attack=self)
                    self.enemy_damaged_entity_ids.append(enemy.entity_id)

        breakable_wall_colliders = Collision.get_collided_nodes_by_tag(
            node=self, tag="break_wall"
        )
        if breakable_wall_colliders:
            room_manager = RoomManager()
            breakable_wall_colliders[0].set_state(DoorState.CRACKED_OPEN_WALL)
            if breakable_wall_colliders[0].direction == Vector2.RIGHT():
                room_manager.current_room.data.right_door_status = (
                    DoorState.CRACKED_OPEN_WALL
                )
            elif breakable_wall_colliders[0].direction == Vector2.LEFT():
                room_manager.current_room.data.left_door_status = (
                    DoorState.CRACKED_OPEN_WALL
                )
            elif breakable_wall_colliders[0].direction == Vector2.UP():
                room_manager.current_room.data.up_door_status = (
                    DoorState.CRACKED_OPEN_WALL
                )
            elif breakable_wall_colliders[0].direction == Vector2.DOWN():
                room_manager.current_room.data.down_door_status = (
                    DoorState.CRACKED_OPEN_WALL
                )
            room_manager.refresh_current_room_wall_colliders()

        if self.life_timer.tick(delta):
            Camera2D.set_offset(offset=Vector2.ZERO())
            self.queue_deletion()
        else:
            Camera2D.set_offset(
                offset=Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
            )


class BombAttack(Attack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.anim_sprite = None
        # self.sprite = None
        self.set_life_time(2.0)
        self.damage = 1

    def _start(self) -> None:
        super()._start()
        self.anim_sprite = AnimatedSprite.new()
        self.anim_sprite.animations = [self._get_animation()]
        self.add_child(self.anim_sprite)
        self.anim_sprite.loops = False
        self.anim_sprite.play()

        self.collider_rect = Rect2(0, 0, 8, 8)
        self.position_spawned = self.position

    def _get_animation(self) -> Animation:
        texture = Texture.get(file_path="assets/images/player/player_bomb_attack.png")
        anim_frames = []
        for i in range(6):
            anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(8 * i, 0, 8, 8), index=i
                )
            )
        return Animation(name="bomb", speed=300, frames=anim_frames)

    # TODO: There is a bug with grabbing component values for at least transformation in thr _end function.
    #  Components should still be accessible during this time.
    def _physics_process(self, delta: float) -> None:
        if self.life_timer.tick(delta):
            bomb_explosion = BombExplosion.new()
            bomb_explosion.position = self.position + Vector2(-16, -16)
            main_node = self.get_node(name="Main")
            main_node.add_child(bomb_explosion)
            self.queue_deletion()
