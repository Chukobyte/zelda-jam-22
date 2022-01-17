import random

from seika.assets import Texture, AnimationFrame, Animation
from seika.camera import Camera2D
from seika.math import Rect2, Vector2
from seika.utils import SimpleTimer

from src.attack.enemy_attack import CultistAttack
from src.enemy.enemy import Enemy
from src.game_context import PlayState, GameContext
from src.math.ease import Easer, Ease
from src.task.task import Task, co_wait_until_seconds, co_return, co_suspend
from src.world import World


class Cultist(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        self.animations = self._get_animations()
        self.collider.collider_rect = Rect2(0, 0, 16, 16)
        self.tasks.add_task(task=Task(name="shoot", func=self.shoot_shot))
        self.game_context = GameContext()
        self.play(animation_name="idle_down")

    def _physics_process(self, delta: float) -> None:
        if self.game_context.get_play_state() != PlayState.ROOM_TRANSITION:
            self.tasks.run_tasks()

    def _get_animations(self) -> list:
        texture = Texture.get(file_path="assets/images/enemy/enemy_cultist.png")
        animations = []

        idle_down_anim_frames = []
        for i in range(4):
            idle_down_anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(16 * i, 0, 16, 16), index=i
                )
            )
        animations.append(
            Animation(name="idle_down", speed=200, frames=idle_down_anim_frames)
        )

        attack_down_anim_frames = []
        for i in range(4):
            attack_down_anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(16 * i, 96, 16, 16), index=i
                )
            )
        animations.append(
            Animation(name="attack_down", speed=200, frames=attack_down_anim_frames)
        )

        return animations

    def _get_random_valid_room_position(self) -> Vector2:
        # Using camera position for room bounds, use room manager's current room pos if camera pos is no longer valid
        camera_pos = Camera2D.get_viewport_position()
        return camera_pos + Vector2(random.randint(100, 320), random.randint(70, 150))

    @Task.task_func()
    def shoot_shot(self):
        world = World()
        player = self.get_node(name="Player")
        assert player
        attack_life_timer = SimpleTimer(wait_time=1.0)
        while True:
            has_attacked = False
            yield from co_wait_until_seconds(wait_time=random.uniform(2.0, 4.0))
            # Randomly move 33.3% of the time, can move into a separate task later
            if random.randint(0, 2) == 0:
                teleport_duration = 0.5
                new_position = self._get_random_valid_room_position()
                teleport_easer = Easer(
                    from_pos=self.position,
                    to_pos=new_position,
                    duration=teleport_duration,
                    func=Ease.Cubic.ease_in_vec2,
                )
                teleport_timer = SimpleTimer(
                    wait_time=teleport_duration, start_on_init=True
                )
                while not teleport_timer.tick(delta=world.cached_delta):
                    self.position = teleport_easer.ease(delta=world.cached_delta)
                    yield co_suspend()
            self.loops = False
            self.play(animation_name="attack_down")
            attack = CultistAttack.new()
            attack.position = self.position
            attack.direction = attack.position.direction_to(target=player.position)
            attack_life_timer.wait_time = attack.life_time
            attack_life_timer.start()
            while not attack_life_timer.tick(delta=world.cached_delta):
                if self.frame == 3 and not has_attacked:
                    has_attacked = True
                    self.get_parent().add_child(attack)
                yield co_suspend()
            # yield from co_wait_until_seconds(wait_time=attack.life_time)
            self.play(animation_name="idle_down")
            self.loops = True
        yield co_return()

    # Temp clearing room
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
