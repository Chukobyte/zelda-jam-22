from typing import Callable
from src.task_manager import TaskManager


class State:
    def __init__(self, name: str, state_func: Callable):
        self.name = name
        self.state_func = state_func


class StateExitLink:
    def __init__(self, state_to_transition: State, transition_predicate: Callable):
        self.state_to_transition = state_to_transition
        self.transition_predicate = transition_predicate


class FSM:
    def __init__(self):
        self.task_manager = TaskManager()
        self.states = {}
        self.exit_links = {}
        self.current_state = None

    def add_state(self, state: State, set_current=False) -> None:
        self.states[state.name] = state
        self.exit_links[state.name] = []
        if set_current:
            self._set_state(state)

    def add_state_exit_link(self, state: State, state_exit_link: StateExitLink) -> None:
        assert state.name in self.exit_links
        self.exit_links[state.name].append(state_exit_link)

    def process(self) -> None:
        if self.current_state:
            # Process state
            self.task_manager.run_tasks()

            # Exit check
            state_exit_links = self.exit_links[self.current_state.name]
            for exit_link in state_exit_links:
                if exit_link.transition_predicate():
                    self._set_state(exit_link.state_to_transition)
                    break

    def _set_state(self, state: State) -> None:
        if self.current_state:
            self.task_manager.remove_task(name=state.name)
        self.current_state = state
        self.task_manager.add_task(name=state.name, func=state.state_func)
