from seika.assets import Texture
from seika.math import Vector2
from seika.node import CollisionShape2D, Node2D


class DoorStatus:
    OPEN = 0
    CLOSED = 1
    BREAKABLE_WALL = 2
    OPEN_WALL = 3


class Door(CollisionShape2D):
    Z_INDEX = 1
    ROOM_LEFT_POSITION = Vector2(22, 74)
    ROOM_RIGHT_POSITION = Vector2(334, 74)
    ROOM_UP_POSITION = Vector2(168, 8)
    ROOM_DOWN_POSITION = Vector2(168, 190)
    OPEN_DOOR_TAG = ["open-door"]

    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.direction = Vector2()
        self._status = DoorStatus.CLOSED
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

    def set_status(self, status: int) -> None:
        self._status = status
        dir_string = self._get_dir_string()
        is_open_string = ""
        if self._status == DoorStatus.OPEN:
            is_open_string = "open"
            self.tags = Door.OPEN_DOOR_TAG
        elif self._status == DoorStatus.CLOSED:
            is_open_string = "closed"
            self.tags = ["solid"]
        if is_open_string:
            texture_file_path = (
                f"assets/images/dungeon/door_{dir_string}_{is_open_string}.png"
            )
            self.sprite.texture = Texture.get(file_path=texture_file_path)
        else:
            print(f"{status} is an invalid status!")

    def get_status(self) -> int:
        return self._status

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
