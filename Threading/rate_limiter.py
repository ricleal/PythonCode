"""
Example of a rate limiter with exponential backoff and jitter.

* Only 100 requests per minute are allowed, after that exponential backoff with jitter is applied.
* Every client is identified by an ID (for example the user_id got from the JWT)
* This has to be thread-safe.
* Use the python `concurrent.futures` module for thread pool management.
"""

import logging
import random
import threading
import time
import uuid
from collections import deque
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

lock = threading.Lock()


def rate_limiter(attempt: int, base: float = 1.0, max_delay: float = 60.0) -> float:
    # Exponential backoff with jitter
    delay = min(base * (2**attempt), max_delay)
    jitter = random.uniform(0, delay * 0.1)
    return delay + jitter


class Buffer:
    data: deque

    def __init__(self):
        # only keeps the timestamps within the last minute
        self.data = deque()

    def insert(self):
        now = time.time()  # timestamp (float) in s
        start_limit = now - timedelta(minutes=1).total_seconds()

        self.data.append(now)

        # remove the old records
        for ts in list(self.data):
            # ^ to avoid: RuntimeError: deque mutated during iteration
            if ts < start_limit:
                self.data.popleft()
            else:
                break

    def is_overflowed(self) -> bool:
        return True if len(self.data) > 100 else False


class Request:
    def __init__(self):
        self.attempt: int = 0  # attempts when rate limited
        self.requests: Buffer = Buffer()


state: dict[str, Request] = {}


def wait(client_id: uuid.UUID):
    """
    Either return 0 if this client is not rate limited,
    or return the time in seconds it has to wait
    """
    with lock:
        if client_id not in state:
            # if the key is new:
            state[client_id] = Request()
        state[client_id].requests.insert()
        if state[client_id].requests.is_overflowed():
            state[client_id].attempt += 1
            return rate_limiter(state[client_id].attempts)
        else:
            state[client_id].attempts = 0
            return 0


# main

client_ids = [uuid.uuid4() for _ in range(10)]
logger.debug(client_ids)
