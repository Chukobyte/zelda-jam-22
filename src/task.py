from typing import Callable


class Awaitable:
    def __init__(self, finished: bool):
        self.finished = finished


# Static functions to control coroutine state
def co_suspend():
    return Awaitable(finished=False)


def co_return():
    return Awaitable(finished=True)


class Task:
    """
    A class to represent coroutines.
    """

    def __init__(self, name: str, func: Callable):
        self.name = name
        self.func = func
        self.coroutine = None
        self.reset_state()

    def reset_state(self) -> None:
        self.coroutine = self.func()

    def resume(self) -> Awaitable:
        """
        Will resume the coroutine.
        :return: has_finished: bool
            Coroutines should return 'True' if continuing and 'False' if not
        """
        return next(self.coroutine, co_return())

    def stop(self) -> None:
        pass

    @staticmethod
    def task_func(debug=False):
        """
        Just a fancy way of denoting task functions...
        """

        def setup_task_func(func: Callable):
            def func_result(*args, **kwargs):
                if debug:
                    print(f"Running task func {func}")
                return func(*args, **kwargs)

            return func_result

        return setup_task_func


class TaskManager:
    def __init__(self, initial_tasks=None):
        self.tasks = {}
        self.running_tasks = []
        if initial_tasks:
            for task in initial_tasks:
                self.add_task(task)

    def add_task(self, task: Task) -> None:
        self.tasks[task.name] = task
        self.running_tasks.append(task)

    def remove_task(self, name: str) -> None:
        self.running_tasks.remove(self.tasks[name])
        del self.tasks[name]

    def run_tasks(self) -> None:
        tasks_to_remove = []
        for task in self.running_tasks:
            awaitable = task.resume()
            if awaitable.finished:
                tasks_to_remove.append(task)
        for finished_task in tasks_to_remove:
            self.remove_task(name=finished_task.name)
