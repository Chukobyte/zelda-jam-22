from typing import Callable


class Task:
    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func

    def resume(self) -> bool:
        coroutine = self.func()
        return next(coroutine, False)

    def stop(self) -> None:
        pass


class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.running_tasks = []

    def add_task(self, task: Task) -> None:
        self.tasks[task.name] = task
        self.running_tasks.append(task)

    def remove_task(self, name: str) -> None:
        self.running_tasks.remove(self.tasks[name])
        del self.tasks[name]

    def run_tasks(self) -> None:
        for task in self.running_tasks:
            task.resume()
