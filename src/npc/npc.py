from seika.assets import Texture
from seika.node import Sprite

from src.event.event_textbox import TextboxManager
from src.game_context import PlayState, GameContext, DialogueEvent


class GainWaveNPC(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None

    def _start(self) -> None:
        self.texture = Texture.get(file_path="assets/images/npc/bomb_npc.png")
        # Start dialogue
        textbox_manager = TextboxManager()
        textbox_manager.set_text("You can now attack I think...")
        textbox_manager.show_textbox()
        GameContext.set_dialogue_event(DialogueEvent.GAIN_WAVE)
        GameContext.set_play_state(PlayState.DIALOGUE)


class GainBombNPC(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None

    def _start(self) -> None:
        self.texture = Texture.get(file_path="assets/images/npc/bomb_npc.png")
        # Start dialogue
        textbox_manager = TextboxManager()
        textbox_manager.set_text(
            "Pick up this to gain the bomb ability.  You can use it to blow up a northern wall to the north east to gain access to the tricolora, I think..."
        )
        textbox_manager.show_textbox()
        GameContext.set_dialogue_event(DialogueEvent.GAIN_BOMB)
        GameContext.set_play_state(PlayState.DIALOGUE)


class GainShieldNPC(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.sprite = None

    def _start(self) -> None:
        self.texture = Texture.get(file_path="assets/images/npc/bomb_npc.png")
        # Start dialogue
        textbox_manager = TextboxManager()
        textbox_manager.set_text(
            "You can now block projectiles facing your direction...I think..."
        )
        textbox_manager.show_textbox()
        GameContext.set_dialogue_event(DialogueEvent.GAIN_SHIELD)
        GameContext.set_play_state(PlayState.DIALOGUE)
