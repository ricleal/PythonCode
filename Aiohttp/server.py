from aiohttp import web

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# this will run on 8080
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    logger.debug("Sending to client: {}".format(text))
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

web.run_app(app)
