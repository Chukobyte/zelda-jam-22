from typing import Callable


class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.running_tasks = []

    def add_task(self, name: str, func: Callable) -> None:
        self.tasks[name] = func
        self.running_tasks.append(func)

    def remove_task(self, name: str) -> None:
        self.running_tasks.remove(self.tasks[name])
        del self.tasks[name]

    def run_tasks(self) -> None:
        for task in self.running_tasks:
            for i in task():
                break
