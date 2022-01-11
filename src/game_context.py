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


class PlayTimerCounter:
    def __init__(self) -> None:
        self._accumulated_delta = 0.0

    def reset(self) -> None:
        self._accumulated_delta = 0.0

    def update(self, delta: float) -> None:
        self._accumulated_delta += delta

    @property
    def time_played_text(self) -> str:
        return f"{self._accumulated_delta:.2f}"


class GameContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.game_state = GameState.INIT
            cls.play_state = PlayState.MAIN
            cls.play_time_counter = PlayTimerCounter()
            # Temp
            cls.has_won = False
        return cls._instance

    @staticmethod
    def set_game_state(state: str) -> None:
        GameContext().game_state = state

    @staticmethod
    def get_game_state() -> str:
        return GameContext().game_state

    @staticmethod
    def set_play_state(state: str) -> None:
        GameContext().play_state = state

    @staticmethod
    def get_play_state() -> str:
        return GameContext().play_state
