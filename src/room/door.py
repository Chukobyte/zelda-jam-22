from seika.assets import Texture
from seika.color import Color
from seika.math import Vector2
from seika.node import CollisionShape2D, Node2D


class DoorState:
    OPEN = 0
    CLOSED = 1
    SOLID_WALL = 2
    BREAKABLE_WALL = 3
    CRACKED_OPEN_WALL = 4


class Door(CollisionShape2D):
    Z_INDEX = 1
    ROOM_LEFT_POSITION = Vector2(21, 74)
    ROOM_RIGHT_POSITION = Vector2(334, 74)
    ROOM_UP_POSITION = Vector2(168, 8)
    ROOM_DOWN_POSITION = Vector2(168, 190)
    OPEN_DOOR_TAG = ["open-door"]

    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.direction = Vector2()
        self._state = DoorState.CLOSED
        self.sprite = None

    def _get_dir_string(self) -> str:
        if self.direction == Vector2.UP():
            return "up"
        elif self.direction == Vector2.DOWN():
            return "down"
        elif self.direction == Vector2.RIGHT():
            return "right"
        elif self.direction == Vector2.LEFT():
            return "left"

    def set_state(self, state: int) -> None:
        self._state = state
        dir_string = self._get_dir_string()
        is_open_string = ""
        if self._state == DoorState.OPEN:
            is_open_string = "open"
            self.tags = Door.OPEN_DOOR_TAG
            self.sprite.modulate = Color(1.0, 1.0, 1.0, 1.0)
        elif self._state == DoorState.CLOSED:
            is_open_string = "closed"
            self.tags = ["solid"]
            self.sprite.modulate = Color(1.0, 1.0, 1.0, 1.0)
        elif self._state == DoorState.SOLID_WALL:
            is_open_string = "closed"
            self.tags = ["solid"]
            self.sprite.modulate = Color(1.0, 1.0, 1.0, 0.0)
        elif self._state == DoorState.BREAKABLE_WALL:
            is_open_string = "closed"
            self.tags = ["solid"]
            self.sprite.modulate = Color(1.0, 1.0, 1.0, 0.0)
        elif self._state == DoorState.CRACKED_OPEN_WALL:
            dir_string = f"wall_cracked_{dir_string}"
            is_open_string = "open"
            self.tags = Door.OPEN_DOOR_TAG
            self.sprite.modulate = Color(1.0, 1.0, 1.0, 1.0)
        if is_open_string:
            texture_file_path = (
                f"assets/images/dungeon/door_{dir_string}_{is_open_string}.png"
            )
            self.sprite.texture = Texture.get(file_path=texture_file_path)
        else:
            print(f"{state} is an invalid state!")

    def get_state(self) -> int:
        return self._state

    @staticmethod
    def new_door(dir: Vector2):
        door = Door.new()
        door.direction = dir
        return door


class DungeonDoors:
    def __init__(
        self,
        left: Door,
        right: Door,
        up: Door,
        down: Door,
        container: Node2D,
    ):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.container = container
        self.doors = [left, right, up, down]

    def move(self, position: Vector2) -> None:
        self.container.position = position

    def update_tags(self, tags: list) -> None:
        for door in self.doors:
            door.tags = tags

    def set_doors_is_open(self, value: bool) -> None:
        for door in self.doors:
            door.set_open(value)
