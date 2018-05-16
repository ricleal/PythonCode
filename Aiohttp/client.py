import signal  
import sys  
import asyncio  
import aiohttp  
import json

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

URL = "http://0.0.0.0:8080/{}"

async def get_content(client, url):  
    async with client.get(url) as response:
        assert response.status == 200
        return await response.read()

async def get_request_content(client, param):
    data = await get_content(client, URL.format(param))
    data_decoded = data.decode('utf-8')
    logger.debug("Got from the server: {}".format(data_decoded))

def signal_handler(signal, frame):
    '''
    Handles Control+C
    '''
    loop.stop()
    client.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

loop = asyncio.get_event_loop() 
client = aiohttp.ClientSession(loop=loop)

for i in range(10):
    loop.run_until_complete(get_request_content(client, "Ricardo {}".format(i)))  
loop.close()  