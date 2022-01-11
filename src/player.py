from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer

from src.game_context import GameContext, PlayState
from src.world import World
from src.room_manager import RoomManager
from src.player_stats import PlayerStats
from src.attack import PlayerAttack
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
        transitioning_to_room_state = State(
            name="transitioning_to_room", state_func=self.transitioning_to_room
        )

        self.player_fsm.add_state(state=idle_state, set_current=True)
        self.player_fsm.add_state(state=move_state)
        self.player_fsm.add_state(state=attack_state)
        self.player_fsm.add_state(state=transitioning_to_room_state)

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
        move_exit_to_room_transition = StateExitLink(
            state_to_transition=transitioning_to_room_state,
            transition_predicate=lambda: GameContext.get_play_state()
            == PlayState.ROOM_TRANSITION,
        )
        self.player_fsm.add_state_exit_link(state=move_state, state_exit_link=move_exit)
        self.player_fsm.add_state_exit_link(
            state=move_state, state_exit_link=move_exit_to_room_transition
        )
        self.player_fsm.add_state_finished_link(
            state=move_state, state_to_transition=idle_state
        )
        # Attack
        self.player_fsm.add_state_finished_link(
            state=attack_state, state_to_transition=move_state
        )
        # Transitioning To Room
        self.player_fsm.add_state_finished_link(
            state=transitioning_to_room_state, state_to_transition=idle_state
        )

    def _physics_process(self, delta: float) -> None:
        self.player_fsm.process()

    @Task.task_func(debug=True)
    def idle(self):
        while True:
            if self.direction == Vector2.UP():
                self.play(animation_name="idle_up")
                self.flip_h = False
            elif self.direction == Vector2.DOWN():
                self.play(animation_name="idle_down")
                self.flip_h = False
            elif self.direction == Vector2.RIGHT():
                self.play(animation_name="idle_hort")
                self.flip_h = False
            elif self.direction == Vector2.LEFT():
                self.play(animation_name="idle_hort")
                self.flip_h = True
            yield co_suspend()

    @Task.task_func(debug=True)
    def move(self):
        world = World()
        room_manager = RoomManager()
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
                    node=self.collider, tag="solid", offset=new_velocity
                )
                open_doors = Collision.get_collided_nodes_by_tag(
                    node=self.collider, tag="open-door", offset=new_velocity
                )
                if collided_walls:
                    pass
                elif open_doors:
                    print("door")
                else:
                    self.position += new_velocity
                    entered_new_room = room_manager.process_room_bounds(
                        player_position=self.position
                    )
            else:
                yield co_return()

            yield co_suspend()

    @Task.task_func(debug=True)
    def attack(self):
        world = World()
        player_attack = PlayerAttack.new()
        player_attack.position = (
            self.position + Vector2(4, 4) + (self.direction * Vector2(8, 12))
        )
        self.get_parent().add_child(player_attack)
        attack_timer = SimpleTimer(wait_time=0.5, start_on_init=True)
        while not attack_timer.tick(world.cached_delta):
            yield co_suspend()
        player_attack.queue_deletion()

    @Task.task_func(debug=True)
    def transitioning_to_room(self):
        game_context = GameContext()
        while True:
            if game_context.play_state != PlayState.ROOM_TRANSITION:
                break
            yield co_suspend()
