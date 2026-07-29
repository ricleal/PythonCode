import uuid
from unittest.mock import MagicMock, patch

import pytest
from rate_limiter import Buffer, rate_limiter, wait


@pytest.fixture(scope="function")
def state():
    import rate_limiter

    keys = rate_limiter.state.keys()
    for k in list(keys):
        del rate_limiter.state[k]
    rate_limiter.state = {}
    yield rate_limiter.state


def test_rate_limiter():
    v = rate_limiter(0)
    assert 1 < v < 2
    v = rate_limiter(1)
    assert 2 < v < 4


def test_buffer():
    b = Buffer()

    for _ in range(50):
        b.insert()
    assert b.is_overflowed() is False

    for _ in range(50):
        b.insert()
    assert b.is_overflowed() is False

    b.insert()
    assert b.is_overflowed() is True


@patch("rate_limiter.time.time")
def test_buffer_over_time(mock_time: MagicMock):
    # 100 requests over a minute
    initial_date = 3600.0
    b = Buffer()
    mock_time.return_value = initial_date

    for i in range(200):
        b.insert()
        mock_time.return_value = initial_date + (1.0 / 100.0) * i * 60

    assert len(b.data) == 101

    assert b.data[0] < b.data[-1]

    assert b.data[-1] - b.data[0] >= 60.0, f"Real value: {b.data[-1] - b.data[0]}"
    assert b.data[-1] - b.data[0] < 61.0


@patch("rate_limiter.time.time")
def test_wait_no_throttling(mock_time: MagicMock, state):
    """TODO"""
    client_id = uuid.uuid4()

    initial_date = 3600.0
    mock_time.return_value = initial_date

    for i in range(200):
        wait_period = wait(client_id)
        mock_time.return_value = initial_date + (1.0 / 98.0) * i * 60

        assert wait_period == 0, f"Index not 0: {len(state[client_id].requests.data)}"

        # print(i, wait_period, len(state[client_id].requests.data))


@patch("rate_limiter.time.time")
def test_wait_throttling(mock_time: MagicMock, state):
    """TODO"""
    client_id = uuid.uuid4()

    initial_date = 3600.0
    mock_time.return_value = initial_date

    # throttling
    for i in range(200):
        wait_period = wait(client_id)
        mock_time.return_value = initial_date + (1.0 / 110.0) * i * 60

        # if state:
        #     print(i, wait_period, len(state[client_id].requests.data))
        if i < 100:
            assert wait_period == 0, (
                f"Index not 0: {len(state[client_id].requests.data)}"
            )
        else:
            assert wait_period > 0


@patch("rate_limiter.time.time")
def test_wait_no_throttling_parallel(mock_time: MagicMock):
    """TODO"""
    from concurrent.futures import ThreadPoolExecutor

    client_ids = [uuid.uuid4() for _ in range(5)]

    initial_date = 3600.0
    mock_time.return_value = initial_date

    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(200):
            wait_periods = executor.map(wait, client_ids)

            mock_time.return_value = initial_date + (1.0 / 98.0) * i * 60

            assert all(wait_periods) == 0


@patch("rate_limiter.time.time")
def test_wait_throttling_parallel(mock_time: MagicMock, state):
    """TODO"""
    import concurrent.futures
    from concurrent.futures import ThreadPoolExecutor

    client_ids = [uuid.uuid4() for _ in range(5)]

    initial_date = 3600.0
    mock_time.return_value = initial_date

    # throttling
    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(200):
            # Instead of:
            # wait_periods = executor.map(wait, client_ids)
            # Let's dp it differently

            futures = [executor.submit(wait, client_id) for client_id in client_ids]

            # Processing results as they complete:")
            for future in concurrent.futures.as_completed(futures):
                wait_period = future.result()
                if i < 100:
                    assert wait_period == 0
                else:
                    assert wait_period > 0

            mock_time.return_value = initial_date + (1.0 / 110.0) * i * 60
