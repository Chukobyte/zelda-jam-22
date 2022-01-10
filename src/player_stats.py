from seika.math import Vector2

from src.room import Room


class MoveParams:
    def __init__(self):
        self.accel = 100


class DungeonParams:
    def __init__(self):
        self.current_room = None
        self.rooms = {}

    def add_room(self, room: Room) -> None:
        self.rooms[f"{room.position.x}-{room.position.y}"] = room

    def set_current_room(self, position: Vector2) -> None:
        pos_key = f"{position.x}-{position.y}"
        if pos_key in self.rooms:
            self.current_room = self.rooms[pos_key]

    def get_room(self, position: Vector2) -> Room:
        return self.rooms[f"{position.x}-{position.y}"]


class PlayerStats:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.move_params = MoveParams()
            cls.dungeon_params = DungeonParams()
        return cls._instance
