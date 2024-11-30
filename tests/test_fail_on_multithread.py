import pytest

from periodic_tasks import run_loop, reset

from threading import Thread

def test_fail_on_multithread():
    def start_in_another_thread():
        with pytest.raises(AssertionError):
            run_loop()
    Thread(target=start_in_another_thread, args=()).start()

@pytest.fixture(autouse=True)
def reset_scheduler():
    print("reset")
    reset()
if __name__ == '__main__':
    test_fail_on_multithread()