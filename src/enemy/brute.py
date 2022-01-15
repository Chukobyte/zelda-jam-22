import random

from seika.assets import Texture
from seika.math import Rect2, Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.attack.attack import Attack
from src.enemy.enemy import Enemy
from src.math.ease import Ease
from src.task.task import Task, co_wait_until_seconds, co_return, co_suspend
from src.world import World


class Brute(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_brute.png")
        self.texture = boss_texture
        self.collider.collider_rect = Rect2(
            0, 0, boss_texture.width, boss_texture.height
        )
        self.tasks.add_task(task=Task(name="move_randomly", func=self.move_randomly))

    def _physics_process(self, delta: float) -> None:
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
        assert player
        # move_speed = 90
        move_speed = 25
        while True:
            # Will sometimes move towards the player, otherwise move randomly
            if random.randint(0, 1) == 0:
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
