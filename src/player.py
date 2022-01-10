import math

from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2
from seika.physics import Collision
from seika.utils import SimpleTimer
from seika.camera import Camera2D

from src.world import World
from src.room import RoomManager
from src.player_stats import PlayerStats
from src.attack import PlayerAttack
from src.task import Task, co_return, co_suspend
from src.fsm import FSM, State, StateExitLink
from src.project_properties import ProjectProperties


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
                    node=self.collider, tag="wall", offset=new_velocity
                )
                if not collided_walls:
                    self.position += new_velocity
                    # TODO: Temp for update room position based on player, will move logic elsewhere
                    current_grid_position = room_manager.current_room.position
                    new_grid_position = room_manager.get_grid_position(
                        position=self.position
                    )
                    if current_grid_position != new_grid_position:
                        print(
                            f"current_grid = {current_grid_position}, new_grid = {new_grid_position}"
                        )
                        room_manager.set_current_room(position=new_grid_position)
                        room_manager.current_room.position = new_grid_position
                        new_room_world_position = room_manager.get_world_position(
                            new_grid_position
                        )
                        Camera2D.set_viewport_position(new_room_world_position)

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
