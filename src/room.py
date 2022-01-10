from seika.math import Vector2

from src.project_properties import ProjectProperties


class Room:
    def __init__(self, position: Vector2):
        self.position = position
        self.size = ProjectProperties.BASE_RESOLUTION

    def __str__(self):
        return f"(position = {self.position}, size = {self.size})"

    def __repr__(self):
        return f"(position = {self.position}, size = {self.size})"


class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.current_room = None
            cls.rooms = {}
        return cls._instance

    def add_room(self, room: Room) -> None:
        self.rooms[f"{room.position.x}-{room.position.y}"] = room

    def set_current_room(self, position: Vector2) -> None:
        pos_key = f"{position.x}-{position.y}"
        if pos_key in self.rooms:
            self.current_room = self.rooms[pos_key]

    def get_room(self, position: Vector2) -> Room:
        return self.rooms[f"{position.x}-{position.y}"]
