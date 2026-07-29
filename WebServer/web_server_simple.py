"""
A simple counter server using BaseHTTPRequestHandler with concurrent
request handling via ThreadPoolExecutor.

- GET  /  → returns {"counter": <value>}
- POST /  → increments counter, returns {"counter": <new_value>}
"""

import json
import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------------------------------------------------------------------------
# Thread-safe counter
# ---------------------------------------------------------------------------

_counter_lock = threading.Lock()
_counter = 0


def _get_counter() -> int:
    with _counter_lock:
        return _counter


def _increment_counter(amount: int = 1) -> int:
    global _counter
    with _counter_lock:
        _counter += amount
        return _counter


# ---------------------------------------------------------------------------
# ThreadPool-based HTTPServer
# ---------------------------------------------------------------------------


class ThreadPoolHTTPServer(HTTPServer):
    """HTTPServer that dispatches requests via a ThreadPoolExecutor."""

    def __init__(self, server_address, RequestHandlerClass, max_workers=10):
        super().__init__(server_address, RequestHandlerClass)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def process_request(self, request, client_address):
        self.executor.submit(self.process_request_thread, request, client_address)

    def process_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except Exception:
            self.handle_error(request, client_address)
            self.shutdown_request(request)


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------


class RequestHandler(BaseHTTPRequestHandler):
    """Simple counter: GET returns value, POST increments it."""

    def _send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self._send_json(200, {"counter": _get_counter()})

    def do_POST(self) -> None:
        amount = 1
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            try:
                data = json.loads(self.rfile.read(content_length))
                amount = int(data.get("increment", 1))
            except (json.JSONDecodeError, ValueError):
                self._send_json(400, {"error": "Invalid JSON body"})
                return
        new_value = _increment_counter(amount)
        self._send_json(200, {"counter": new_value})


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Thread-safe counter HTTP server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--workers", type=int, default=10)
    args = parser.parse_args()

    server = ThreadPoolHTTPServer(
        (args.host, args.port), RequestHandler, max_workers=args.workers
    )
    print(f"Server on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()
        server.executor.shutdown(wait=False)


if __name__ == "__main__":
    main()
