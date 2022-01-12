class RoomEntityStats:
    def __init__(self):
        self.base_hp = 0
        self.hp = 0

    def __str__(self):
        return f"(base_hp = {self.base_hp}, hp = {self.hp})"

    def __repr__(self):
        return f"(base_hp = {self.base_hp}, hp = {self.hp})"

    def set_all_hp(self, value: int) -> None:
        self.base_hp = value
        self.hp = value
