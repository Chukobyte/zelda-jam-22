from seika.node import Node, CollisionShape2D
from seika.math import Vector2, Rect2

from src.project_properties import ProjectProperties


class RoomBuilder:
    @staticmethod
    def create_walls(node: Node) -> None:
        room_dimensions = ProjectProperties.BASE_RESOLUTION
        vertical_rect = Rect2(0, 0, 64, room_dimensions.y)
        horizontal_rect = Rect2(0, 0, room_dimensions.x, 32)

        left_wall_collider = CollisionShape2D.new()
        left_wall_collider.collider_rect = vertical_rect
        left_wall_collider.tags = ["wall"]
        node.add_child(child_node=left_wall_collider)

        right_wall_collider = CollisionShape2D.new()
        right_wall_collider.collider_rect = vertical_rect
        right_wall_collider.position = Vector2(room_dimensions.x - vertical_rect.w, 0)
        right_wall_collider.tags = ["wall"]
        node.add_child(child_node=right_wall_collider)

        up_wall_collider = CollisionShape2D.new()
        up_wall_collider.collider_rect = horizontal_rect
        up_wall_collider.position = Vector2(0, 0)
        up_wall_collider.tags = ["wall"]
        node.add_child(child_node=up_wall_collider)

        down_wall_collider = CollisionShape2D.new()
        down_wall_collider.collider_rect = horizontal_rect
        down_wall_collider.position = Vector2(0, room_dimensions.y - horizontal_rect.h)
        down_wall_collider.tags = ["wall"]
        node.add_child(child_node=down_wall_collider)
