from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.world import World
from src.player_stats import PlayerStats
from src.task import Task, co_return, co_suspend
from src.fsm import FSM, State, StateExitLink


class Player(AnimatedSprite):
    def _start(self) -> None:
        self.stats = PlayerStats()
        self.collider = self.get_node(name="PlayerCollider")
        self.velocity = Vector2()
        self.direction = Vector2.DOWN()
        self.player_fsm = FSM()
        self._configure_fsm()

    def _configure_fsm(self) -> None:
        # State Management
        idle_state = State(name="idle", state_func=self.idle)
        move_state = State(name="move", state_func=self.move)
        attack_state = State(name="attack", state_func=self.attack)

        self.player_fsm.add_state(state=idle_state, set_current=True)
        self.player_fsm.add_state(state=move_state)
        self.player_fsm.add_state(state=attack_state)

        # Links
        # Idle
        idle_move_exit = StateExitLink(
            state_to_transition=move_state,
            transition_predicate=(
                lambda: Input.is_action_just_pressed(action_name="move_left")
                or Input.is_action_pressed(action_name="move_right")
                or Input.is_action_pressed(action_name="move_up")
                or Input.is_action_pressed(action_name="move_down")
            ),
        )
        idle_attack_exit = StateExitLink(
            state_to_transition=attack_state,
            transition_predicate=lambda: Input.is_action_just_pressed(
                action_name="attack"
            ),
        )
        self.player_fsm.add_state_exit_link(idle_state, state_exit_link=idle_move_exit)
        self.player_fsm.add_state_exit_link(
            idle_state, state_exit_link=idle_attack_exit
        )
        # Move
        move_exit = StateExitLink(
            state_to_transition=attack_state,
            transition_predicate=lambda: Input.is_action_just_pressed(
                action_name="attack"
            ),
        )
        self.player_fsm.add_state_exit_link(state=move_state, state_exit_link=move_exit)
        self.player_fsm.add_state_finished_link(
            state=move_state, state_to_transition=idle_state
        )
        # Attack
        self.player_fsm.add_state_finished_link(
            state=attack_state, state_to_transition=move_state
        )

    def _physics_process(self, delta: float) -> None:
        self.player_fsm.process()

    @Task.task_func(debug=True)
    def idle(self):
        while True:
            yield co_suspend()

    @Task.task_func(debug=True)
    def move(self):
        world = World()
        while True:
            delta = world.cached_delta
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
            else:
                yield co_return()

            yield co_suspend()

    @Task.task_func(debug=True)
    def attack(self):
        world = World()
        attack_timer = SimpleTimer(wait_time=0.5, start_on_init=True)
        while True:
            if attack_timer.tick(world.cached_delta):
                yield co_return()
            yield co_suspend()
