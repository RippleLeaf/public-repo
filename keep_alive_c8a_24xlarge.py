#!/usr/bin/env python3

import multiprocessing
import os
import signal
import time


TARGET_TOTAL_PERCENT = 2.0
CYCLE_SECONDS = 1.0

stop_requested = False


def handle_signal(signum, frame):
    global stop_requested
    stop_requested = True


def cpu_worker(duty_cycle: float) -> None:
    """Consume approximately duty_cycle of one logical CPU."""
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    while not stop_requested:
        cycle_start = time.monotonic()
        busy_time = CYCLE_SECONDS * duty_cycle

        # Controlled busy loop
        while time.monotonic() - cycle_start < busy_time:
            _ = sum(i * i for i in range(1000))

        remaining = CYCLE_SECONDS - (time.monotonic() - cycle_start)
        if remaining > 0:
            time.sleep(remaining)


def main() -> None:
    cpu_count = os.cpu_count() or 1

    # Total equivalent fully utilized CPU cores required.
    required_core_load = cpu_count * TARGET_TOTAL_PERCENT / 100.0

    # Spread the work over enough processes that no process exceeds 80%.
    worker_count = max(1, int(required_core_load / 0.8) + 1)
    duty_cycle = min(required_core_load / worker_count, 0.8)

    print(f"Detected logical CPUs: {cpu_count}", flush=True)
    print(f"Target total CPU: {TARGET_TOTAL_PERCENT:.2f}%", flush=True)
    print(f"Workers: {worker_count}", flush=True)
    print(f"Load per worker: {duty_cycle * 100:.2f}%", flush=True)

    processes = [
        multiprocessing.Process(target=cpu_worker, args=(duty_cycle,))
        for _ in range(worker_count)
    ]

    for process in processes:
        process.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        pass
    finally:
        for process in processes:
            process.terminate()
        for process in processes:
            process.join()


if __name__ == "__main__":
    main()
