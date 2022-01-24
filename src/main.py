import random

from seika.math import Vector2
from seika.node import Node2D

from src.event.event_textbox import TextboxManager
from src.item.health_container import HealthContainer
from src.room.room_manager import RoomManager
from src.world import World
from src.game_context import GameContext, PlayState, DialogueEvent
from src.room.room_builder import RoomBuilder
from src.player.player_stats import PlayerStats


class Main(Node2D):
    def _start(self) -> None:
        self.world = World()
        self.game_context = GameContext()
        self.spawnable_hearts = 3
        # Setup Initial Room
        RoomBuilder.create_wall_colliders(node=self)
        RoomBuilder.create_doors(node=self)
        RoomBuilder.create_rooms(node=self)
        room_manager = RoomManager()
        room_manager.refresh_current_doors_status()
        room_manager.refresh_current_room_wall_colliders()

        textbox_manager = TextboxManager()
        textbox_manager.register_textbox(textbox=self.get_node(name="EventTextbox"))
        textbox_manager.set_text("...")
        textbox_manager.show_textbox()
        GameContext.set_dialogue_event(DialogueEvent.INIT)
        GameContext.set_play_state(PlayState.DIALOGUE)

    def _physics_process(self, delta: float) -> None:
        self.world.cached_delta = delta
        self.game_context.play_time_counter.update(delta=delta)

    def _on_room_cleared(self, args: list) -> None:
        room_manager = RoomManager()
        room_manager.current_room.data.enemies -= 1
        if room_manager.current_room.data.enemies <= 0:
            RoomManager().set_current_room_to_cleared()
            player_stats = PlayerStats()
            if self.spawnable_hearts > 0:
                if player_stats.hp <= 2 or (
                    player_stats.hp == 3 and random.randint(0, 1) == 0
                ):
                    self.spawnable_hearts -= 1
                    world_pos = room_manager.get_world_position(
                        grid_position=room_manager.current_room.position
                    )
                    h_container = HealthContainer.new()
                    h_container.position = world_pos + Vector2(200.0, 110.0)
                    self.add_child(h_container)
