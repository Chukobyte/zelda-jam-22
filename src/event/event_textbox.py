from seika.node import Sprite


class TextboxManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.textbox = None
        return cls._instance

    def register_textbox(self, textbox) -> None:
        self.textbox = textbox

    def clear_textbox(self) -> None:
        self.textbox = None

    def hide_textbox(self) -> None:
        self.textbox.hide_all()

    def show_textbox(self) -> None:
        self.textbox.show_all()

    def set_text(self, value: str) -> None:
        self.textbox.set_text(value)


class EventTextbox(Sprite):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.label = None
        TextboxManager().textbox = self

    def _start(self) -> None:
        self.label = self.get_node(name="EventTextLabel")
        self.label.word_wrap = True
        self.label.max_characters_per_line = 52
        self.label.new_line_padding = 2
        # self.set_text("Test text to see how this will show up within the scene!  How does this look in the textbox?  It's going to be used for events!")
        self.hide_all()

    def set_text(self, value: str) -> None:
        self.label.text = value

    def hide_all(self) -> None:
        self.hide()
        self.label.hide()

    def show_all(self) -> None:
        self.show()
        self.label.show()

    def _end(self) -> None:
        TextboxManager().clear_textbox()
