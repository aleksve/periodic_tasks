
# Periodic Task Scheduling Package Review

This package provides a lightweight framework for scheduling and executing periodic tasks with precision. Its minimalist syntax and focused functionality make it well-suited for business-critical applications that require reliable task execution at fixed intervals.

## Key Features
1. **Minimalist Design**: The package avoids unnecessary complexity, focusing on a clear and concise interface for defining and managing periodic tasks.
2. **No Busy-Waiting**: It uses an efficient wait mechanism, minimizing CPU usage during idle periods between task executions.
3. **Missed Execution Handling**: If a task misses its scheduled execution due to delays or processing overhead, the package tracks these missed executions without stacking them up, ensuring that the application stays responsive.
4. **Accurate Timing**: Tasks are executed with a high degree of timing accuracy, crucial for applications with strict timing requirements.

## Example Usage
The following example demonstrates how to create periodic tasks using the package:

```python
import time
from datetime import timedelta
from functools import partial

from periodic_tasks import periodic, run_loop, make_periodic

start_time = time.time()

# Define a fast task that executes every 0.1 seconds
@periodic(interval=0.1)
def task_1():
    dt = time.time() - start_time
    print(f"Started a _fast_ task at t={{dt:.3f}}")

# Define a slower task that executes every 0.5 seconds
@periodic(interval=0.5)
def task_2():
    dt = time.time() - start_time
    print(f"Started a *slow* task at t={{dt:.3f}}")

    if dt < 2:
        time.sleep(0.91)  # Simulate a delay in the task
    else:
        time.sleep(0.09)  # Shorter delay after initial period

# Create a custom task with parameters
def task_3(custom_text: str):
    print(custom_text)
    time.sleep(0.5)

# Schedule task_3 to run periodically using a partial function
make_periodic(partial(task_3, "Hello periodic"), interval=timedelta(milliseconds=100))

# Start the periodic task loop
run_loop()
```

In this example:
- `task_1` and `task_2` are defined using the `@periodic` decorator with specified intervals.
- `task_3` is scheduled with `make_periodic`, allowing custom parameters using `functools.partial`.
- `run_loop` initiates the loop that manages the task execution, handling missed executions without delay accumulation.

Overall, this framework offers robust, no-frills functionality for time-sensitive applications, and its approach to task scheduling is both efficient and effective.
