from seika.camera import Camera2D
from seika.color import Color
from seika.node import AnimatedSprite
from seika.input import Input
from seika.math import Vector2
from seika.physics import Collision
from seika.scene import SceneTree
from seika.utils import SimpleTimer

from src.event.event_textbox import TextboxManager
from src.game_context import GameContext, PlayState, GameState
from src.math.ease import Ease
from src.room.door import DoorStatus
from src.world import World
from src.room.room_manager import RoomManager
from src.player.player_stats import PlayerStats
from src.attack.player_attack import PlayerAttack
from src.task.task import Task, co_return, co_suspend, co_wait_until_seconds
from src.task.fsm import FSM, State, StateExitLink


class Player(AnimatedSprite):
    TAG = "player"

    def _start(self) -> None:
        self.stats = PlayerStats()
        self.stats.set_all_hp(value=3)
        self.collider = self.get_node(name="PlayerCollider")
        self.player_ui_sprite = self.get_node(name="PlayerUISprite")
        self.velocity = Vector2()
        self.direction = Vector2.DOWN()
        self.task_fsm = FSM()
        self._configure_fsm()
        # Temp
        self.collider.tags = [Player.TAG]
        self.last_collided_door = None

    def _configure_fsm(self) -> None:
        # State Management
        idle_state = State(name="idle", state_func=self.idle)
        move_state = State(name="move", state_func=self.move)
        attack_state = State(name="attack", state_func=self.attack)
        transitioning_to_room_state = State(
            name="transitioning_to_room", state_func=self.transitioning_to_room
        )
        event_state = State(name="event", state_func=self.event)

        self.task_fsm.add_state(state=idle_state, set_current=True)
        self.task_fsm.add_state(state=move_state)
        self.task_fsm.add_state(state=attack_state)
        self.task_fsm.add_state(state=transitioning_to_room_state)
        self.task_fsm.add_state(state=event_state)

        # Links
        event_exit = StateExitLink(
            state_to_transition=event_state,
            transition_predicate=lambda: GameContext.get_play_state()
            == PlayState.EVENT,
        )
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
        self.task_fsm.add_state_exit_link(idle_state, state_exit_link=idle_move_exit)
        self.task_fsm.add_state_exit_link(idle_state, state_exit_link=idle_attack_exit)
        self.task_fsm.add_state_exit_link(idle_state, state_exit_link=event_exit)
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
        self.task_fsm.add_state_exit_link(state=move_state, state_exit_link=move_exit)
        self.task_fsm.add_state_exit_link(
            state=move_state, state_exit_link=move_exit_to_room_transition
        )
        self.task_fsm.add_state_exit_link(state=move_state, state_exit_link=event_exit)
        self.task_fsm.add_state_finished_link(
            state=move_state, state_to_transition=idle_state
        )
        # Attack
        self.task_fsm.add_state_finished_link(
            state=attack_state, state_to_transition=move_state
        )
        # Transitioning To Room
        self.task_fsm.add_state_finished_link(
            state=transitioning_to_room_state, state_to_transition=idle_state
        )
        # Event
        to_idle_from_event_exit = StateExitLink(
            state_to_transition=idle_state,
            transition_predicate=lambda: GameContext.get_play_state()
            != PlayState.EVENT,
        )
        self.task_fsm.add_state_exit_link(
            state=event_state, state_exit_link=to_idle_from_event_exit
        )

    def _physics_process(self, delta: float) -> None:
        self.task_fsm.process()

    def take_damage(self, attack) -> None:
        self.stats.hp -= attack.damage
        if self.stats.hp <= 0:
            self.player_ui_sprite.play("empty")
            # TODO: Do more stuff...
        else:
            if self.stats.hp == 2:
                self.player_ui_sprite.play("two_hearts")
            if self.stats.hp == 1:
                self.player_ui_sprite.play("one_heart")

    def set_stat_ui_visibility(self, visible: bool) -> None:
        if visible:
            self.player_ui_sprite.modulate = Color(1.0, 1.0, 1.0, 1.0)
        else:
            self.player_ui_sprite.modulate = Color(1.0, 1.0, 1.0, 0.0)

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

    @Task.task_func()
    def move(self):
        world = World()
        room_manager = RoomManager()
        while True:
            # Temp event toggle
            if Input.is_action_just_pressed(action_name="credits"):
                if GameContext.get_play_state() == PlayState.MAIN:
                    GameContext.set_play_state(PlayState.EVENT)
                    TextboxManager().hide_textbox()

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
                rainbow_orbs = Collision.get_collided_nodes_by_tag(
                    node=self.collider, tag="rainbow_orb", offset=new_velocity
                )
                # Collision checks
                if collided_walls:
                    pass
                elif open_doors:
                    # TODO: temp win state
                    if GameContext().has_won:
                        room_manager.clean_up()
                        GameContext.set_game_state(GameState.END_SCREEN)
                        SceneTree.change_scene(scene_path="scenes/end_screen.sscn")
                        yield co_return()
                    else:
                        collided_door = open_doors[0]
                        self.last_collided_door = collided_door
                        room_manager.start_room_transition(collided_door)
                elif rainbow_orbs:
                    GameContext().has_won = True
                    rainbow_orbs[0].queue_deletion()
                    # Temp open up door
                    room_manager.room_doors.up.set_status(DoorStatus.OPEN)
                else:
                    self.position += new_velocity
            else:
                yield co_return()

            yield co_suspend()

    @Task.task_func()
    def attack(self):
        player_attack = PlayerAttack.new()
        player_attack.position = (
            self.position + Vector2(4, 4) + (self.direction * Vector2(8, 12))
        )
        self.get_parent().add_child(player_attack)

        yield from co_wait_until_seconds(wait_time=player_attack.life_time)

        yield co_return()

    @Task.task_func()
    def transitioning_to_room(self):
        world = World()
        room_manager = RoomManager()
        move_dir = self.last_collided_door.direction
        new_world_position = room_manager.get_world_position(
            room_manager.current_room.position
        )
        camera_pos = Camera2D.get_viewport_position()
        initial_camera_pos = camera_pos
        self.set_stat_ui_visibility(visible=False)
        # Delay
        self.stop()
        yield from co_wait_until_seconds(wait_time=0.5)
        # Transition Start
        # TODO: Move some of the transition logic from player to something else...
        self.play()
        wait_time = 2.0
        elapsed_time = 0.0
        new_player_pos = self.position + Vector2(80 * move_dir.x, 80 * move_dir.y)
        current_pos = self.position
        transition_timer = SimpleTimer(wait_time=wait_time, start_on_init=True)
        while not transition_timer.tick(delta=world.cached_delta):
            elapsed_time += world.cached_delta
            self.position = Ease.Cubic.ease_in_vec2(
                elapsed_time=elapsed_time,
                from_pos=current_pos,
                to_pos=new_player_pos,
                duration=wait_time,
            )
            camera_pos = Ease.Cubic.ease_in_vec2(
                elapsed_time=elapsed_time,
                from_pos=initial_camera_pos,
                to_pos=new_world_position,
                duration=wait_time,
            )
            Camera2D.set_viewport_position(camera_pos)
            yield co_suspend()
        # Transition End
        self.position = new_player_pos
        Camera2D.set_viewport_position(new_world_position)
        room_manager.wall_colliders.update_wall_positions(new_world_position)
        GameContext.set_play_state(PlayState.MAIN)
        self.set_stat_ui_visibility(visible=True)

        room_manager.finish_room_transition(main_node=self.get_parent())

    @Task.task_func()
    def event(self):
        while True:
            if Input.is_action_just_pressed(action_name="credits"):
                GameContext.set_play_state(PlayState.MAIN)
            yield co_suspend()
