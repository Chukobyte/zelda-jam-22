import random

from seika.assets import Texture
from seika.camera import Camera2D
from seika.math import Rect2, Vector2
from seika.node import Sprite
from seika.physics import Collision

from src.attack.enemy_attack import EnemyAttack
from src.enemy.enemy import Enemy
from src.task.fsm import FSM, State
from src.task.task import Task, co_wait_until_seconds, co_return


class MeteorShowerAttack(EnemyAttack):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None
        self.set_life_time(3.0)
        self.damage = 1

    def _start(self) -> None:
        self.sprite = Sprite.new()
        texture = Texture.get(file_path="assets/images/enemy/enemy_boss_spear.png")
        self.sprite.texture = texture
        self.add_child(self.sprite)

        self.collider_rect = Rect2(0, 0, texture.width, texture.height)

    def _physics_process(self, delta: float) -> None:
        super()._physics_process(delta)
        self.position += self.direction * Vector2(
            self.speed * delta, self.speed * delta
        )
        if not self.has_collided:
            player_colliders = Collision.get_collided_nodes_by_tag(
                node=self, tag="player"
            )
            if player_colliders:
                self.has_collided = True
                first_enemy = player_colliders[0].get_parent()
                first_enemy.take_damage(attack=self)


class Boss(Enemy):
    def _start(self) -> None:
        super()._start()
        self.stats.set_all_hp(3)
        boss_texture = Texture.get(file_path="assets/images/enemy/enemy_boss.png")
        self.texture = boss_texture
        self.collider.collider_rect = Rect2(
            8, 2, boss_texture.width - 8, boss_texture.height - 2
        )

        self.task_fsm = FSM()
        self._configure_fsm()

    def _configure_fsm(self) -> None:
        shoot_shot_state = State(name="shoot", state_func=self.shoot_shot)
        meteor_shower_state = State(name="meteor", state_func=self.meteor_shower)

        self.task_fsm.add_state(state=shoot_shot_state, set_current=False)
        self.task_fsm.add_state(state=meteor_shower_state, set_current=True)

        self.task_fsm.add_state_finished_link(
            state=shoot_shot_state, state_to_transition=meteor_shower_state
        )
        self.task_fsm.add_state_finished_link(
            state=meteor_shower_state, state_to_transition=shoot_shot_state
        )
        # self.task_fsm.add_state_finished_link(state=meteor_shower_state, state_to_transition=meteor_shower_state)

    def _physics_process(self, delta: float) -> None:
        self.task_fsm.process()
        self.tasks.run_tasks()

    @Task.task_func(debug=True)
    def shoot_shot(self):
        player = self.get_node(name="Player")
        assert player
        while True:
            yield from co_wait_until_seconds(wait_time=random.uniform(2.0, 4.0))
            attack = EnemyAttack.new()
            attack.position = self.position + Vector2(32, 0)
            attack.direction = attack.position.direction_to(target=player.position)
            self.get_parent().add_child(attack)
            yield from co_wait_until_seconds(wait_time=attack.life_time)
            rand_n = random.randint(0, 1)
            if rand_n == 1:
                break
        yield co_return()

    @Task.task_func(debug=True)
    def meteor_shower(self):
        camera_pos = Camera2D.get_viewport_position()
        base_pos = camera_pos + Vector2(0, 120)
        yield from co_wait_until_seconds(wait_time=random.uniform(1.0, 2.0))

        if random.randint(0, 1) == 0:
            direction = Vector2.RIGHT()
            base_pos.x += 80
        else:
            direction = Vector2.LEFT()
            base_pos.x += 340

        for meteor_pos_offset in [Vector2(0, 0), Vector2(0, 20), Vector2(0, 40)]:
            attack = MeteorShowerAttack.new()
            attack.position = base_pos + meteor_pos_offset
            attack.direction = direction
            self.get_parent().add_child(attack)

        yield co_return()

    # TODO: temp win state when defeated
    def _end(self) -> None:
        main_node = self.get_node(name="Main")
        self.connect_signal("room_cleared", main_node, "_on_room_cleared")
        self.emit_signal(signal_id="room_cleared")
