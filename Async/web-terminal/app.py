import asyncio

import asyncssh
import aiohttp
from aiohttp import web


# Async Web Server
async def index(request):
    return web.Response(text="Hello from aiohttp server")


async def index_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    loop = asyncio.get_event_loop()
    ssh_task = loop.create_task(run_ssh_client(ws))
    await asyncio.gather(ssh_task)

    return ws


def setup_routes(app, root=""):
    app.router.add_get('/', index)

    app.router.add_get('/ws', index_websocket)
    app.router.add_static('/static', 'static')


def init_app():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    setup_routes(app)
    return app

# Simple async SSHV2 Server

async def run_ssh_client(ws):
    # Example
    # ssh_config = {
    #     "host": "login.newton.utk.edu",
    #     "port": 22,
    #     "username": "costrouc",
    #     "client_keys": "/home/costrouc/.ssh/id_rsa_cluster",
    #     "passphrase": "<not going to tell you>",
    #     "password": <if using password client keys and passphrase not needed>"
    # }

    # I used this to hide my password from version control
    # from config import ssh_config

    terminal_config = {
        "term_type": "xterm-256color",
        "term_size": (80, 40),
        "encoding": "utf-8"
    }

    loop = asyncio.get_event_loop()
    connection = await asyncssh.connect(**ssh_config)

    with connection:
        stdin, stdout, stderr = await connection.open_session(**terminal_config)
        stdin_write_task = loop.create_task(terminal_write(ws, stdin))
        stdout_read_task = loop.create_task(terminal_read(ws, stdout))
        stderr_read_task = loop.create_task(terminal_read(ws, stderr))
        await stdin.channel.wait_closed()


async def terminal_write(websocket, write_stream):
      async for msg in websocket:
          if msg.type == aiohttp.WSMsgType.TEXT:
              write_stream.write(msg.data)
              await write_stream.drain()
          elif msg.type == aiohttp.WSMsgType.ERROR:
              print('ws connection closed with exception %s' %
                  ws.exception())


async def terminal_read(websocket, read_stream):
     while not read_stream.at_eof():
         msg = await read_stream.read(128)
         websocket.send_str(msg)


if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host='localhost', port=8080)
