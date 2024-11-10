from datetime import timedelta
from functools import partial
from threading import Event
from time import monotonic
from typing import Callable


class _Task:
    def __init__(self, task: Callable, interval: timedelta):
        self.task = task
        self.interval = interval
        self.previous_call = monotonic()
        self.missed_executions = 0

    def next_call(self) -> float:
        return self.previous_call + self.interval.total_seconds()


_tasks: list[_Task] = []


def make_periodic(
    task: Callable[[], None], *, interval: float | timedelta
) -> Callable[[], None]:
    if not isinstance(interval, timedelta):
        # Raises TypeError
        interval = timedelta(seconds=interval)

    _tasks.append(_Task(task, interval))
    return task


def periodic(interval: float | timedelta) -> Callable[[Callable], Callable]:
    """
    Decorator syntax
    :return:
    """
    if not isinstance(interval, timedelta):
        # Raises TypeError
        interval = timedelta(seconds=interval)

    return partial(make_periodic, interval=interval)


def run_pending():
    t = monotonic()
    for task in _tasks:
        intervals_since_last_call: float = (
            t - task.previous_call
        ) / task.interval.total_seconds()
        if intervals_since_last_call >= 1:
            i_intervals_since_last_call = int(intervals_since_last_call)
            task.previous_call += (
                task.interval.total_seconds() * i_intervals_since_last_call
            )
            task.missed_executions += i_intervals_since_last_call - 1
            task.task()


def run_loop(
    stop_event: Event | None = None,
    return_after: float | timedelta | None = float("inf"),
):
    """
    Runs the pending tasks until the stop_event is set, or until an exception is raised by a task.

    Args:
        stop_event: optionally provide an event that will trigger a clean return from the loop when set
        return_after: loop exits after a certain amount of time; especially useful for testing

    Raises:
        Exception: All exceptions raised by the tasks will propagate through here
    """
    if stop_event is None:
        stop_event = Event()
    assert isinstance(stop_event, Event)

    start_time = monotonic()
    if isinstance(return_after, timedelta):
        # timedelta doesn't support float('inf')
        return_after = return_after.total_seconds()

    while not stop_event.is_set() and not monotonic() - start_time > return_after:
        run_pending()

        next_call_time_list = [t.next_call() for t in _tasks]
        if len(next_call_time_list):
            next_call_time = min([t.next_call() for t in _tasks]) - monotonic()
        else:
            next_call_time = float("inf")
        elapsed_time = monotonic() - start_time
        next_call_time = min(next_call_time, return_after - elapsed_time)
        if next_call_time > 0:
            stop_event.wait(next_call_time)


def reset():
    _tasks.clear()
