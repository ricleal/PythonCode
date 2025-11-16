from unittest.mock import Mock, patch

import ex1
import pytest


@pytest.mark.asyncio
@patch("ex1.time.time", return_value=2)
async def test_check_time_pair(mock_time):
    r = await ex1.check_time(2)
    print(r)
    assert (2, {2: 2}) == r


@pytest.mark.asyncio
@patch("ex1.time.time")
async def test_check_time_odd(mock_time: Mock):
    ex1.data.pop(2)
    times = [3, 5]
    mock_time.side_effect = times

    for _ in times:
        r = await ex1.check_time(3)
    print(r)
    assert r == (3, {1: 8})
