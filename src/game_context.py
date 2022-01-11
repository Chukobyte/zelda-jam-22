class GameState:
    INIT = "init"
    TITLE_SCREEN = "title_screen"
    PLAYING = "playing"
    CREDITS = "credits"


class PlayState:
    MAIN = "main"
    ROOM_TRANSITION = "room_transition"
    PAUSED = "paused"
    DIALOGUE = "dialogue"


class GameContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.game_state = GameState.INIT
            cls.play_state = PlayState.MAIN
        return cls._instance

    @staticmethod
    def set_game_state(state: str) -> None:
        game = GameContext()
        game.game_state = state

    @staticmethod
    def set_play_state(state: str) -> None:
        game = GameContext()
        game.play_state = state
