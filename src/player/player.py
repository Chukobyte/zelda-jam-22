import random
from typing import Tuple, Optional

from seika.assets import Texture
from seika.audio import Audio, AudioStream
from seika.camera import Camera2D
from seika.color import Color
from seika.node import AnimatedSprite, Sprite
from seika.input import Input
from seika.math import Vector2, Rect2
from seika.physics import Collision
from seika.scene import SceneTree
from seika.utils import SimpleTimer

from src.attack.attack import Attack
from src.event.event_textbox import TextboxManager
from src.game_context import GameContext, PlayState, GameState
from src.math.ease import Ease, Easer
from src.room.door import DoorState
from src.world import World
from src.room.room_manager import RoomManager
from src.player.player_stats import PlayerStats
from src.attack.player_attack import WaveAttack, BoltAttack, BombAttack
from src.task.task import (
    Task,
    co_return,
    co_suspend,
    co_wait_until_seconds,
    TaskManager,
)
from src.task.fsm import FSM, State, StateExitLink

# TODO: Refactor this class especially move()...
class Player(AnimatedSprite):
    TAG = "player"

    def _start(self) -> None:
        self.stats = PlayerStats()
        self.stats.set_all_hp(value=6)
        self.collider = self.get_node(name="PlayerCollider")
        self.player_ui_sprite = self.get_node(name="PlayerUISprite")
        self.velocity = Vector2()
        self.direction = Vector2.DOWN()
        self.tasks = TaskManager()
        self.task_fsm = FSM()
        self._configure_fsm()

        self.collider.tags = [Player.TAG]
        self.last_collided_door = None
        self.on_damage_cool_down = False
        self.bomb_unlocked = False
        self.bomb_cooldown_timer = SimpleTimer(wait_time=3.5, start_on_init=True)

    def _configure_fsm(self) -> None:
        # State Management
        idle_state = State(name="idle", state_func=self.idle)
        move_state = State(name="move", state_func=self.move)
        wave_attack_state = State(name="wave_attack", state_func=self.wave_attack)
        # bolt_attack_state = State(name="bolt_attack", state_func=self.bolt_attack)
        bomb_attack_state = State(name="bomb_attack", state_func=self.bomb_attack)
        transitioning_to_room_state = State(
            name="transitioning_to_room", state_func=self.transitioning_to_room
        )
        event_state = State(name="event", state_func=self.event)

        self.task_fsm.add_state(state=idle_state, set_current=True)
        self.task_fsm.add_state(state=move_state)
        self.task_fsm.add_state(state=wave_attack_state)
        # self.task_fsm.add_state(state=bolt_attack_state)
        self.task_fsm.add_state(state=bomb_attack_state)
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
                lambda: Input.is_action_pressed(action_name="move_left")
                or Input.is_action_pressed(action_name="move_right")
                or Input.is_action_pressed(action_name="move_up")
                or Input.is_action_pressed(action_name="move_down")
            ),
        )
        idle_attack_exit = StateExitLink(
            state_to_transition=wave_attack_state,
            transition_predicate=lambda: Input.is_action_just_pressed(
                action_name="attack"
            ),
        )
        # idle_bolt_attack_exit = StateExitLink(
        #     state_to_transition=bolt_attack_state,
        #     transition_predicate=lambda: Input.is_action_just_pressed(
        #         action_name="bolt_attack"
        #     ),
        # )
        idle_bomb_attack_exit = StateExitLink(
            state_to_transition=bomb_attack_state,
            transition_predicate=lambda: Input.is_action_just_pressed(
                action_name="bomb_attack"
            )
            and self.bomb_unlocked
            and self.bomb_cooldown_timer.time_left <= 0,
        )
        self.task_fsm.add_state_exit_link(idle_state, state_exit_link=idle_move_exit)
        self.task_fsm.add_state_exit_link(idle_state, state_exit_link=idle_attack_exit)
        # self.task_fsm.add_state_exit_link(
        #     idle_state, state_exit_link=idle_bolt_attack_exit
        # )
        self.task_fsm.add_state_exit_link(
            idle_state, state_exit_link=idle_bomb_attack_exit
        )
        self.task_fsm.add_state_exit_link(idle_state, state_exit_link=event_exit)
        # Move
        move_attack_exit = StateExitLink(
            state_to_transition=wave_attack_state,
            transition_predicate=lambda: Input.is_action_just_pressed(
                action_name="attack"
            ),
        )
        # move_attack_bolt_exit = StateExitLink(
        #     state_to_transition=bolt_attack_state,
        #     transition_predicate=lambda: Input.is_action_just_pressed(
        #         action_name="bolt_attack"
        #     ),
        # )
        move_attack_bomb_exit = StateExitLink(
            state_to_transition=bomb_attack_state,
            transition_predicate=lambda: Input.is_action_just_pressed(
                action_name="bomb_attack"
            )
            and self.bomb_unlocked
            and self.bomb_cooldown_timer.time_left <= 0,
        )
        move_exit_to_room_transition = StateExitLink(
            state_to_transition=transitioning_to_room_state,
            transition_predicate=lambda: GameContext.get_play_state()
            == PlayState.ROOM_TRANSITION,
        )
        self.task_fsm.add_state_exit_link(
            state=move_state, state_exit_link=move_attack_exit
        )
        # self.task_fsm.add_state_exit_link(
        #     state=move_state, state_exit_link=move_attack_bolt_exit
        # )
        self.task_fsm.add_state_exit_link(
            state=move_state, state_exit_link=move_attack_bomb_exit
        )
        self.task_fsm.add_state_exit_link(
            state=move_state, state_exit_link=move_exit_to_room_transition
        )
        self.task_fsm.add_state_exit_link(state=move_state, state_exit_link=event_exit)
        self.task_fsm.add_state_finished_link(
            state=move_state, state_to_transition=idle_state
        )
        # Attacks
        self.task_fsm.add_state_finished_link(
            state=wave_attack_state, state_to_transition=idle_state
        )
        # self.task_fsm.add_state_finished_link(
        #     state=bolt_attack_state, state_to_transition=idle_state
        # )
        self.task_fsm.add_state_finished_link(
            state=bomb_attack_state, state_to_transition=idle_state
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
        self.tasks.run_tasks()
        self.bomb_cooldown_timer.tick(delta=delta)

    def take_damage(self, attack=None) -> None:
        if not self.on_damage_cool_down:
            attack_damage = 1
            if attack:
                attack_damage = attack.damage
            self.stats.hp -= attack_damage
            if self.stats.hp <= 0:
                self.player_ui_sprite.play("empty")
                RoomManager().clean_up()
                GameContext.set_game_state(GameState.END_SCREEN)
                SceneTree.change_scene(scene_path="scenes/end_screen.sscn")
                # TODO: Do more stuff...
            else:
                if self.stats.hp == 5:
                    self.player_ui_sprite.play("five_hearts")
                elif self.stats.hp == 4:
                    self.player_ui_sprite.play("four_hearts")
                elif self.stats.hp == 3:
                    self.player_ui_sprite.play("three_hearts")
                elif self.stats.hp == 2:
                    self.player_ui_sprite.play("two_hearts")
                elif self.stats.hp == 1:
                    self.player_ui_sprite.play("one_heart")
                self.on_damage_cool_down = True
                self.tasks.add_task(
                    task=Task(name="damaged", func=self.damaged_from_attack)
                )

    def set_stat_ui_visibility(self, visible: bool) -> None:
        if visible:
            self.player_ui_sprite.modulate = Color(1.0, 1.0, 1.0, 1.0)
        else:
            self.player_ui_sprite.modulate = Color(1.0, 1.0, 1.0, 0.0)

    def _process_collisions(self):
        pass

    @Task.task_func()
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
        is_move_pressed = False
        elapsed_time = 0.0
        while True:
            # Temp event toggle
            # if Input.is_action_just_pressed(action_name="credits"):
            #     if GameContext.get_play_state() == PlayState.MAIN:
            #         GameContext.set_play_state(PlayState.EVENT)
            #         TextboxManager().hide_textbox()

            delta = world.cached_delta
            elapsed_time += delta
            new_velocity = None
            non_facing_velocity = None
            accel = self.stats.move_params.accel * delta
            non_facing_accel = self.stats.move_params.non_facing_dir_accel * delta

            # TODO: Put into function
            # Input checks
            left_pressed = Input.is_action_pressed(action_name="move_left")
            right_pressed = Input.is_action_pressed(action_name="move_right")
            up_pressed = Input.is_action_pressed(action_name="move_up")
            down_pressed = Input.is_action_pressed(action_name="move_down")
            # Resolve input
            if not is_move_pressed:
                if left_pressed:
                    self.play(animation_name="move_hort")
                    self.flip_h = True
                    self.direction = Vector2.LEFT()
                    new_velocity = Vector2(self.direction.x * accel, 0)
                    is_move_pressed = True
                elif right_pressed:
                    self.play(animation_name="move_hort")
                    self.flip_h = False
                    self.direction = Vector2.RIGHT()
                    new_velocity = Vector2(self.direction.x * accel, 0)
                    is_move_pressed = True
                elif up_pressed:
                    self.play(animation_name="move_up")
                    self.flip_h = False
                    self.direction = Vector2.UP()
                    new_velocity = Vector2(0, self.direction.y * accel)
                    is_move_pressed = True
                elif down_pressed:
                    self.play(animation_name="move_down")
                    self.flip_h = False
                    self.direction = Vector2.DOWN()
                    new_velocity = Vector2(0, self.direction.y * accel)
                    is_move_pressed = True
            else:
                if self.direction == Vector2.LEFT():
                    if left_pressed:
                        new_velocity = Vector2(self.direction.x * accel, 0)
                        if up_pressed:
                            non_facing_velocity = Vector2(0, -1.0 * non_facing_accel)
                        elif down_pressed:
                            non_facing_velocity = Vector2(0, 1.0 * non_facing_accel)
                    else:
                        is_move_pressed = False
                elif self.direction == Vector2.RIGHT():
                    if right_pressed:
                        new_velocity = Vector2(self.direction.x * accel, 0)
                        if up_pressed:
                            non_facing_velocity = Vector2(0, -1.0 * non_facing_accel)
                        elif down_pressed:
                            non_facing_velocity = Vector2(0, 1.0 * non_facing_accel)
                    else:
                        is_move_pressed = False
                elif self.direction == Vector2.UP():
                    if up_pressed:
                        new_velocity = Vector2(0, self.direction.y * accel)
                        if left_pressed:
                            non_facing_velocity = Vector2(-1.0 * non_facing_accel, 0)
                        elif right_pressed:
                            non_facing_velocity = Vector2(1.0 * non_facing_accel, 0)
                    else:
                        is_move_pressed = False
                elif self.direction == Vector2.DOWN():
                    if down_pressed:
                        new_velocity = Vector2(0, self.direction.y * accel)
                        if left_pressed:
                            non_facing_velocity = Vector2(-1.0 * non_facing_accel, 0)
                        elif right_pressed:
                            non_facing_velocity = Vector2(1.0 * non_facing_accel, 0)
                    else:
                        is_move_pressed = False

            # Integrate new velocity
            if not new_velocity and not non_facing_velocity:
                yield co_return()
            else:
                for vel in [new_velocity, non_facing_velocity]:
                    if vel:
                        collided_walls = Collision.get_collided_nodes_by_tag(
                            node=self.collider, tag="solid", offset=vel
                        )
                        open_doors = Collision.get_collided_nodes_by_tag(
                            node=self.collider, tag="open-door", offset=vel
                        )
                        rainbow_orbs = Collision.get_collided_nodes_by_tag(
                            node=self.collider, tag="rainbow_orb", offset=vel
                        )
                        tricolora = Collision.get_collided_nodes_by_tag(
                            node=self.collider, tag="tricolora", offset=vel
                        )
                        # Collision checks
                        if collided_walls:
                            pass
                        elif open_doors:
                            # TODO: temp win state
                            if GameContext().has_won:
                                room_manager.clean_up()
                                GameContext.set_game_state(GameState.END_SCREEN)
                                SceneTree.change_scene(
                                    scene_path="scenes/end_screen.sscn"
                                )
                                yield co_return()
                            else:
                                collided_door = open_doors[0]
                                self.last_collided_door = collided_door
                                room_manager.start_room_transition(collided_door)
                            break
                        elif rainbow_orbs:
                            music_audio_stream = AudioStream.get(
                                stream_uid="no-color-theme"
                            )
                            music_audio_stream.stop()
                            Audio.play_sound(
                                sound_id="assets/audio/sfx/rainbow_orb.wav"
                            )
                            rainbow_orbs[0].queue_deletion()
                            self.bomb_unlocked = True
                            room_manager.set_current_room_to_cleared()
                            break
                        elif tricolora:
                            music_audio_stream = AudioStream.get(
                                stream_uid="no-color-theme"
                            )
                            music_audio_stream.stop()
                            Audio.play_sound(
                                sound_id="assets/audio/sfx/rainbow_orb.wav"
                            )
                            victory_pose_sprite = Sprite.new()
                            victory_pose_sprite.texture = Texture.get(
                                file_path="assets/images/player/player_victory_pose.png"
                            )
                            victory_pose_sprite.position = self.position
                            self.get_parent().add_child(victory_pose_sprite)
                            self.modulate = Color(1.0, 1.0, 1.0, 0.0)
                            self.set_stat_ui_visibility(visible=False)
                            # Transition to end game state
                            GameContext.set_play_state(PlayState.EVENT)
                            GameContext().has_won = True
                            tricolora[0].queue_deletion()
                            break
                        else:
                            current_pos = self.position
                            # TODO: Figure out if a different easing function is needed
                            self.position = Ease.Cubic.ease_out_vec2(
                                elapsed_time=elapsed_time,
                                from_pos=current_pos,
                                to_pos=current_pos + vel,
                                duration=elapsed_time + 0.1,
                            )
                            # self.position += vel

            yield co_suspend()

    def _setup_attack(self, attack: Attack, adjust_orientation: bool) -> None:
        self.set_stat_ui_visibility(visible=False)
        move_offset = Vector2(4, 4)
        self.get_parent().add_child(attack)
        if self.direction == Vector2.UP():
            move_offset += (self.direction * Vector2(0, 14)) + Vector2(-2, 0)
            if adjust_orientation:
                attack.sprite.rotation = 270
                attack.collider_rect = Rect2(2, -2, 8, 12)
        elif self.direction == Vector2.DOWN():
            move_offset += (self.direction * Vector2(0, 14)) + Vector2(-2, 0)
            if adjust_orientation:
                attack.sprite.rotation = 90
                attack.collider_rect = Rect2(2, -2, 8, 12)
        elif self.direction == Vector2.LEFT():
            move_offset += self.direction * Vector2(14, 0)
            if adjust_orientation:
                attack.sprite.flip_h = True
        elif self.direction == Vector2.RIGHT():
            move_offset += self.direction * Vector2(11, 0)
        attack.position = self.position + move_offset

    def _setup_wave_attack(self, attack: WaveAttack) -> None:
        self.set_stat_ui_visibility(visible=False)
        move_offset = Vector2(-22, -12)
        self.get_parent().add_child(attack)
        if self.direction == Vector2.UP():
            move_offset += self.direction * Vector2(0, 28)
            attack.anim_sprite.rotation = 270
            attack.collider_rect = Rect2(15, -12, 32, 52)
        elif self.direction == Vector2.DOWN():
            move_offset += (self.direction * Vector2(0, 36)) + Vector2(0, 0)
            attack.anim_sprite.rotation = 90
            attack.collider_rect = Rect2(15, -6, 32, 52)
        elif self.direction == Vector2.LEFT():
            move_offset += self.direction * Vector2(28, 0) + Vector2(0, 2)
            attack.anim_sprite.flip_h = True
        elif self.direction == Vector2.RIGHT():
            move_offset += self.direction * Vector2(28, 0) + Vector2(0, 2)
        attack.position = self.position + move_offset

    @Task.task_func()
    def wave_attack(self):
        Audio.play_sound(sound_id="assets/audio/sfx/wave.wav")
        player_attack = WaveAttack.new()
        self._setup_wave_attack(attack=player_attack)

        world = World()
        screen_shaker_timer = SimpleTimer(
            wait_time=player_attack.life_time / 2.0, start_on_init=True
        )
        while not screen_shaker_timer.tick(delta=world.cached_delta):
            Camera2D.set_offset(
                offset=Vector2(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
            )
            yield co_suspend()

        Camera2D.set_offset(offset=Vector2(0.0, 0.0))
        yield from co_wait_until_seconds(wait_time=player_attack.life_time / 2.0)

        self.set_stat_ui_visibility(visible=True)
        yield co_return()

    # @Task.task_func()
    # def bolt_attack(self):
    #     Audio.play_sound(sound_id="assets/audio/sfx/bolt.wav")
    #     player_attack = BoltAttack.new()
    #     player_attack.direction = self.direction
    #     self._setup_attack(attack=player_attack, adjust_orientation=True)
    #
    #     yield from co_wait_until_seconds(wait_time=0.25)
    #
    #     self.set_stat_ui_visibility(visible=True)
    #     yield co_return()

    @Task.task_func()
    def bomb_attack(self):
        Audio.play_sound(sound_id="assets/audio/sfx/bomb_place.wav")
        self.bomb_cooldown_timer.start()
        player_attack = BombAttack.new()
        self._setup_attack(attack=player_attack, adjust_orientation=False)

        yield from co_wait_until_seconds(wait_time=0.5)

        self.set_stat_ui_visibility(visible=True)
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
        self.set_stat_ui_visibility(visible=False)
        # Delay
        self.stop()
        yield from co_wait_until_seconds(wait_time=0.5)
        # Transition Start
        # TODO: Move some of the transition logic from player to something else...
        self.play()
        if move_dir.x != 0:
            wait_time = 2.5
        else:
            wait_time = 2.0
        new_player_pos = self.position + Vector2(130 * move_dir.x, 80 * move_dir.y)
        player_easer = Easer(
            from_pos=self.position,
            to_pos=new_player_pos,
            duration=wait_time,
            func=Ease.Cubic.ease_out_vec2,
        )
        camera_easer = Easer(
            from_pos=camera_pos,
            to_pos=new_world_position,
            duration=wait_time,
            func=Ease.Cubic.ease_in_vec2,
        )
        transition_timer = SimpleTimer(wait_time=wait_time, start_on_init=True)
        while not transition_timer.tick(delta=world.cached_delta):
            self.position = player_easer.ease(delta=world.cached_delta)
            camera_pos = camera_easer.ease(delta=world.cached_delta)
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
    def damaged_from_attack(self):
        lower_opacity = True
        for i in range(15):
            if lower_opacity:
                self.modulate = Color(1.0, 1.0, 1.0, 0.4)
            else:
                self.modulate = Color(1.0, 1.0, 1.0, 1.0)
            yield from co_wait_until_seconds(wait_time=0.1)
            lower_opacity = not lower_opacity

        self.modulate = Color(1.0, 1.0, 1.0, 1.0)
        self.on_damage_cool_down = False
        yield co_return()

    @Task.task_func()
    def event(self):
        while True:
            yield co_suspend()
