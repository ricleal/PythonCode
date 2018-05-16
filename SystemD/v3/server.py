#!/usr/bin/python3

from socketserver import TCPServer, StreamRequestHandler
import socket
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
)

logger = logging.getLogger(__name__)


class Handler(StreamRequestHandler):

    def handle(self):
        data = self.rfile.readline().strip()
        logging.info("From <{}>: {}".format(self.client_address, data))
        self.wfile.write(data.upper() + "\r\n")


class Server(TCPServer):

    # The constant would be better initialized by a systemd module
    SYSTEMD_FIRST_SOCKET_FD = 3

    def __init__(self, server_address, handler_cls):
        # Invoke base but omit bind/listen steps (performed by systemd
        # activation!)
        super().__init__(server_address, handler_cls, bind_and_activate=False)
        # Override socket
        self.socket = socket.fromfd(
            self.SYSTEMD_FIRST_SOCKET_FD,
            self.address_family,
            self.socket_type
        )


if __name__ == "__main__":
    HOST, PORT = "", 0  #
    server = Server((HOST, PORT), Handler)  # A random free port from 1024 to 65535 will be selected
    server.serve_forever()
