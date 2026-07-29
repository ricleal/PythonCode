"""
Time-based task submission with ThreadPoolExecutor and graceful shutdown.

A TimeSystem class checks the current timestamp in a loop and submits
tasks to a thread pool based on divisibility rules (3 → key 1, 5 → key 2,
7 → key 3). Handles SIGINT for graceful shutdown, waits for running
futures to finish, then prints the aggregated results.
"""

import random
import signal
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor


class TimeSystem:
    def __init__(self):
        self.shutdown = False

        self.data: dict[int, int] = defaultdict(lambda: 0)
        self.lock = threading.Lock()
        self.futures: list[Future] = []

        signal.signal(signal.SIGINT, self.handler)  # Register the handler for SIGINT

    def executor(self, key: int):
        print("Executor:", key)
        with self.lock:
            self.data[key] += 1

    def handler(self, signum, frame):
        print("signal received", signum)
        self.shutdown = True
        time_limit = time.time() + 5

        while time.time() < time_limit and any(f.running() for f in self.futures):
            time.sleep(0.1)

        print("Done:\n", dict(self.data))
        sys.exit()

    def run(self):
        with ThreadPoolExecutor(max_workers=3) as executor:
            while not self.shutdown:
                current_timestamp = time.time()
                current_timestamp = round(current_timestamp)
                f = None
                if current_timestamp % 7 == 0:
                    f = executor.submit(self.executor, 3)
                elif current_timestamp % 5 == 0:
                    f = executor.submit(self.executor, 2)
                elif current_timestamp % 3 == 0:
                    f = executor.submit(self.executor, 1)

                if f:
                    self.futures.append(f)

                time.sleep(random.random())
                self.futures = [e for e in self.futures if e.running()]


if __name__ == "__main__":
    t = TimeSystem()
    t.run()
