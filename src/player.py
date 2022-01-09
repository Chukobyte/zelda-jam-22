from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.player_stats import PlayerStats
from src.fsm import FSM, State, StateExitLink


class Player(AnimatedSprite):
    def _start(self) -> None:
        self.stats = PlayerStats()
        self.collider = self.get_node(name="PlayerCollider")
        self.velocity = Vector2()
        self.direction = Vector2.DOWN()
        # State Management
        self.player_fsm = FSM()
        move_state = State(name="move", state_func=self.move)
        attack_state = State(name="attack", state_func=self.attack)

        self.player_fsm.add_state(state=move_state, set_current=True)
        self.player_fsm.add_state(state=attack_state)

        # Links
        move_exit_predicate = lambda: Input.is_action_just_pressed(action_name="attack")
        move_exit = StateExitLink(
            state_to_transition=attack_state, transition_predicate=move_exit_predicate
        )
        self.player_fsm.add_state_exit_link(state=move_state, state_exit_link=move_exit)
        self.player_fsm.add_state_finished_link(
            state=attack_state, state_to_transition=move_state
        )

    def _physics_process(self, delta: float) -> None:
        self.stats.move_params.cached_delta = delta

        self.player_fsm.process()

    # Task
    def move(self):
        while True:
            delta = self.stats.move_params.cached_delta
            new_velocity = None
            accel = self.stats.move_params.accel * delta

            # Input checks
            left_pressed = Input.is_action_pressed(action_name="move_left")
            right_pressed = Input.is_action_pressed(action_name="move_right")
            up_pressed = Input.is_action_pressed(action_name="move_up")
            down_pressed = Input.is_action_pressed(action_name="move_down")
            # Resolve input
            if left_pressed:
                self.play(animation_name="move_hort")
                self.flip_h = True
                self.direction = Vector2.LEFT()
                new_velocity = Vector2(self.direction.x * accel, 0)
            elif right_pressed:
                self.play(animation_name="move_hort")
                self.flip_h = False
                self.direction = Vector2.RIGHT()
                new_velocity = Vector2(self.direction.x * accel, 0)
            elif up_pressed:
                self.play(animation_name="move_up")
                self.flip_h = False
                self.direction = Vector2.UP()
                new_velocity = Vector2(0, self.direction.y * accel)
            elif down_pressed:
                self.play(animation_name="move_down")
                self.flip_h = False
                self.direction = Vector2.DOWN()
                new_velocity = Vector2(0, self.direction.y * accel)

            # Integrate new velocity
            if new_velocity:
                collided_walls = Collision.get_collided_nodes_by_tag(
                    node=self.collider, tag="wall", offset=new_velocity
                )
                if not collided_walls:
                    self.position += new_velocity
            # TODO: Break of out of move state if not moving...
            # else:
            #     break

            yield True

    def attack(self):
        attack_timer = SimpleTimer(wait_time=0.5)
        attack_timer.start()
        while True:
            if attack_timer.tick(self.stats.move_params.cached_delta):
                yield False
            yield True
