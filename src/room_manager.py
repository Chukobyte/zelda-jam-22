import math

from seika.camera import Camera2D
from seika.math import Vector2

from src.game_context import PlayState, GameContext
from src.room import Room, Door
from src.project_properties import ProjectProperties


class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.current_room = None
            cls.rooms = {}
            cls.wall_colliders = None
            cls.room_doors = None
        return cls._instance

    def add_room(self, room: Room) -> None:
        self.rooms[f"{room.position.x}-{room.position.y}"] = room

    def set_current_room(self, position: Vector2) -> None:
        pos_key = f"{position.x}-{position.y}"
        if pos_key in self.rooms:
            self.current_room = self.rooms[pos_key]

    def get_room(self, position: Vector2) -> Room:
        return self.rooms[f"{position.x}-{position.y}"]

    def get_grid_position(self, position: Vector2) -> Vector2:
        return Vector2(
            math.floor(position.x / ProjectProperties.BASE_RESOLUTION.x),
            math.floor(position.y / ProjectProperties.BASE_RESOLUTION.y),
        )

    def get_world_position(self, grid_position: Vector2) -> Vector2:
        return Vector2(
            math.floor(grid_position.x * ProjectProperties.BASE_RESOLUTION.x),
            math.floor(grid_position.y * ProjectProperties.BASE_RESOLUTION.y),
        )

    def start_room_transition(self, collided_door: Door) -> None:
        new_room_position = self.current_room.position + collided_door.direction
        self.set_current_room(position=new_room_position)
        self.current_room.position = new_room_position
        new_world_position = self.get_world_position(new_room_position)
        Camera2D.set_viewport_position(new_world_position)
        GameContext.set_play_state(PlayState.ROOM_TRANSITION)

    # def process_room_bounds(self, player_position: Vector2) -> bool:
    #     current_grid_position = self.current_room.position
    #     current_grid_position.x = math.floor(current_grid_position.x)
    #     current_grid_position.y = math.floor(current_grid_position.y)
    #     new_grid_position = self.get_grid_position(position=player_position)
    #     if current_grid_position != new_grid_position:
    #         print(
    #             f"current_grid = {current_grid_position}, new_grid = {new_grid_position}"
    #         )
    #         self.set_current_room(position=new_grid_position)
    #         self.current_room.position = new_grid_position
    #         new_room_world_position = self.get_world_position(new_grid_position)
    #         Camera2D.set_viewport_position(new_room_world_position)
    #         # TODO: Transition into proper functions
    #         # GameContext.set_play_state(PlayState.ROOM_TRANSITION)
    #         return True
    #     return False
