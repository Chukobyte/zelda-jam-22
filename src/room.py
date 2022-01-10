from seika.math import Vector2

from src.project_properties import ProjectProperties


class Room:
    def __init__(self, position: Vector2):
        self.position = position
        self.size = ProjectProperties.BASE_RESOLUTION
