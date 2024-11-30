import time
from datetime import timedelta
from functools import partial

from periodic_tasks import periodic, run_loop, make_periodic

start_time = time.time()


@periodic(interval=0.1)
def task_1():
    dt = time.time() - start_time
    print(f"Started a _fast_ task at t={dt:.3f}")


@periodic(interval=0.5)
def task_2():
    dt = time.time() - start_time
    print(f"Started a *slow* task at t={dt:.3f}")

    if dt < 2:
        time.sleep(0.91)
    else:
        time.sleep(0.09)


def task_3(custom_text: str):
    print(custom_text)
    time.sleep(0.5)


make_periodic(partial(task_3, "Hello periodic"), interval=timedelta(milliseconds=100))

run_loop()
