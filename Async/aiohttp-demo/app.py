import aiohttp
from aiohttp import web
import signal  

async def index(request):
    name = request.match_info.get('name', "Anonymous")
    return web.Response(text="Hello %s from aiohttp server" % name)


async def index_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.text:
            print('Received:', msg.data)
            await ws.send_str("Server Echo, {}".format(msg.data))
        elif msg.type == aiohttp.WSMsgType.binary:
            print('Received binary...')
            await ws.send_bytes(msg.data)
        elif msg.type == aiohttp.WSMsgType.close:
            print('Received close...')
            break

    return ws


def setup_routes(app, root=""):
    app.router.add_get('/ws', index_websocket)
    app.router.add_static('/static', 'static')
    app.router.add_get('/{name}', index)


def init_app():
    app = web.Application()
    setup_routes(app)
    return app

if __name__ == "__main__":
    app = init_app()
    web.run_app(app, host='localhost', port=8080)
