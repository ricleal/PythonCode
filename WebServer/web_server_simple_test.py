"""
Tests for web_server_simple.py using pytest.
"""

import http.client
import json
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest
from web_server_simple import (
    RequestHandler,
    ThreadPoolHTTPServer,
    _get_counter,
    _reset_counter,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def server(free_port):
    srv = ThreadPoolHTTPServer(("127.0.0.1", free_port), RequestHandler, max_workers=5)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    _wait_for_port(free_port)
    yield free_port
    srv.shutdown()
    srv.server_close()
    srv.executor.shutdown(wait=False)
    thread.join(timeout=2)


@pytest.fixture(autouse=True)
def clean_counter():
    _reset_counter(0)


def _wait_for_port(port: int, timeout: float = 5.0) -> None:
    import time

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return
        except (OSError, socket.timeout):
            time.sleep(0.05)
    pytest.fail(f"Server did not start on port {port} within {timeout}s")


def _request(
    method: str,
    port: int,
    path: str = "/",
    body: bytes | None = None,
    timeout: float = 5.0,
) -> http.client.HTTPResponse:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
    try:
        headers = {}
        if body is not None:
            headers["Content-Type"] = "application/json"
        conn.request(method, path, body=body, headers=headers)
        return conn.getresponse()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_returns_zero_initially(self, server):
        resp = _request("GET", server)
        assert resp.status == 200
        assert json.loads(resp.read()) == {"counter": 0}

    def test_get_after_increment(self, server):
        _request("POST", server)
        resp = _request("GET", server)
        assert json.loads(resp.read()) == {"counter": 1}

    def test_get_returns_json_content_type(self, server):
        resp = _request("GET", server)
        assert resp.status == 200
        assert resp.getheader("Content-Type") == "application/json"


class TestPost:
    def test_post_default_increment(self, server):
        resp = _request("POST", server)
        assert resp.status == 200
        assert json.loads(resp.read()) == {"counter": 1}

    def test_post_custom_increment(self, server):
        _request("POST", server, body=json.dumps({"increment": 5}).encode())
        resp = _request("GET", server)
        assert json.loads(resp.read()) == {"counter": 5}

    def test_post_accumulates(self, server):
        for _ in range(3):
            _request("POST", server)
        assert _get_counter() == 3

    def test_post_negative_increment(self, server):
        _request("POST", server, body=json.dumps({"increment": 10}).encode())
        _request("POST", server, body=json.dumps({"increment": -3}).encode())
        resp = _request("GET", server)
        assert json.loads(resp.read()) == {"counter": 7}

    def test_post_invalid_body_returns_400(self, server):
        resp = _request("POST", server, body=b"not-json")
        assert resp.status == 400
        assert "error" in json.loads(resp.read())

    def test_post_concurrent(self, server):
        """20 concurrent POSTs, each incrementing by 1 → counter == 20."""

        def post(_):
            return _request("POST", server)

        with ThreadPoolExecutor(max_workers=10) as ex:
            list(ex.map(post, range(20)))
        assert _get_counter() == 20
