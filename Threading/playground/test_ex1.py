import random
import threading
from unittest.mock import patch

from ex1 import TimeSystem

random.seed(1234)


def test_executor_increments_data():
    """Test that the executor correctly increments data"""
    t = TimeSystem()

    # Test the executor directly
    t.executor(1)
    t.executor(1)
    t.executor(2)

    assert t.data[1] == 2
    assert t.data[2] == 1


def test_executor_thread_safety():
    """Test that the executor is thread-safe"""
    t = TimeSystem()

    def worker():
        for _ in range(100):
            t.executor(1)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # With 10 threads each doing 100 increments, we should have exactly 1000
    assert t.data[1] == 1000


@patch("ex1.time.sleep")
@patch("ex1.time.time")
def test_run_with_different_timestamps(mock_time, mock_sleep):
    """Test that run() submits tasks based on timestamp conditions"""
    t = TimeSystem()

    # Simulate timestamps: 15 (divisible by 3 and 5), 21 (divisible by 3 and 7), 35 (divisible by 5 and 7)
    l = [15, 15, 21, 21, 35, 35]
    mock_time.side_effect = l

    # Make sleep trigger shutdown after a few iterations
    call_count: int = 0

    def sleep_side_effect(duration):
        nonlocal call_count
        call_count += 1
        if call_count == len(l):
            t.shutdown = True

    mock_sleep.side_effect = sleep_side_effect

    t.run()

    # Verify that executors were called
    assert len(t.futures) > 0


@patch("ex1.time.sleep")
@patch("ex1.time.time")
def test_shutdown_mechanism(mock_time, mock_sleep):
    """Test that shutdown flag stops the run loop"""
    t = TimeSystem()

    # Simulate a few timestamps
    mock_time.side_effect = [10, 10, 15, 15, 21, 21]

    # Track submitted futures
    submitted_count = 0

    # Make sleep trigger shutdown after a few iterations
    call_count = 0

    def sleep_side_effect(duration):
        nonlocal call_count
        nonlocal submitted_count

        call_count += 1
        # Count futures submitted before shutdown
        if call_count == 1:
            submitted_count = len(t.futures)
        if call_count >= 2:
            t.shutdown = True

    mock_sleep.side_effect = sleep_side_effect

    t.run()

    # Verify shutdown happened and futures were created
    assert t.shutdown is True
    assert submitted_count > 0, (
        "Should have submitted at least one future before shutdown"
    )


def test_handler_sets_shutdown():
    """Test that the signal handler sets shutdown flag"""
    t = TimeSystem()

    # Mock sys.exit to prevent test from exiting
    with patch("ex1.sys.exit") as mock_exit:
        t.handler(2, None)

        assert t.shutdown is True
        mock_exit.assert_called_once()
