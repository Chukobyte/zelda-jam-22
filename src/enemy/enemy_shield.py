import random

from seika.assets import Texture, AnimationFrame, Animation
from seika.math import Rect2, Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.enemy.enemy import Enemy
from src.game_context import GameContext, PlayState
from src.task.task import Task, co_return, co_suspend
from src.world import World


class EnemyShield(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        self.animations = self._get_animations()
        self.collider.collider_rect = Rect2(0, 0, 16, 16)
        self.tasks.add_task(task=Task(name="move_randomly", func=self.move_randomly))
        self.game_context = GameContext()
        self.play()

    def _get_animations(self) -> list:
        texture = Texture.get(file_path="assets/images/enemy/enemy_shield.png")
        animations = []

        down_anim_frames = []
        for i in range(4):
            down_anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(16 * i, 0, 16, 16), index=i
                )
            )
        animations.append(
            Animation(name="move_down", speed=200, frames=down_anim_frames)
        )

        up_anim_frames = []
        for i in range(4):
            up_anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(16 * i, 16, 16, 16), index=i
                )
            )
        animations.append(Animation(name="move_up", speed=200, frames=up_anim_frames))

        right_anim_frames = []
        for i in range(4):
            right_anim_frames.append(
                AnimationFrame(
                    texture=texture, draw_source=Rect2(16 * i, 32, 16, 16), index=i
                )
            )
        animations.append(
            Animation(name="move_hort", speed=200, frames=right_anim_frames)
        )

        return animations

    def _physics_process(self, delta: float) -> None:
        if self.game_context.get_play_state() != PlayState.ROOM_TRANSITION:
            self.tasks.run_tasks()

    def _get_movement_dir_towards_player(self, player_pos: Vector2) -> Vector2:
        player_dir = self.position.direction_to(target=player_pos)
        valid_dirs = []
        if player_dir.x > 0:
            valid_dirs.append(Vector2.RIGHT())
        elif player_dir.x < 0:
            valid_dirs.append(Vector2.RIGHT())
        if player_dir.y > 0:
            valid_dirs.append(Vector2.DOWN())
        elif player_dir.y < 0:
            valid_dirs.append(Vector2.UP())
        if not valid_dirs:
            valid_dirs = [Vector2.DOWN(), Vector2.UP(), Vector2.LEFT(), Vector2.RIGHT()]
        return random.choice(valid_dirs)

    @Task.task_func()
    def move_randomly(self):
        world = World()
        player = self.get_node(name="Player")
        move_speed = 25
        while True:
            # Will sometimes move towards the player, otherwise move randomly
            if random.randint(0, 2) <= 1:
                new_dir = self._get_movement_dir_towards_player(player.position)
            else:
                new_dir = random.choice(
                    [
                        Vector2.DOWN(),
                        Vector2.UP(),
                        Vector2.LEFT(),
                        Vector2.RIGHT(),
                    ]
                )
            if new_dir == Vector2.UP():
                self.play(animation_name="move_up")
                self.flip_h = False
            if new_dir == Vector2.DOWN():
                self.play(animation_name="move_down")
                self.flip_h = False
            elif new_dir == Vector2.RIGHT():
                self.play(animation_name="move_hort")
                self.flip_h = False
            elif new_dir == Vector2.LEFT():
                self.play(animation_name="move_hort")
                self.flip_h = True
            move_timer = SimpleTimer(
                wait_time=random.uniform(2.0, 3.0), start_on_init=True
            )
            while not move_timer.tick(delta=world.cached_delta):
                new_vel = Vector2(
                    new_dir.x * move_speed * world.cached_delta,
                    new_dir.y * move_speed * world.cached_delta,
                )

                new_pos = new_vel + self.position
                collisions = Collision.get_collided_nodes_by_tag(
                    node=self.collider, tag="solid", offset=new_vel
                )
                if not collisions:
                    self.position = new_pos
                # Check if collided with player
                player_colliders = Collision.get_collided_nodes_by_tag(
                    node=self.collider, tag="player"
                )
                if player_colliders:
                    player_collided = player_colliders[0].get_parent()
                    player_collided.take_damage()
                yield co_suspend()
        yield co_return()

    # Temp clearing room
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
