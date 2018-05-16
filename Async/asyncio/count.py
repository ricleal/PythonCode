import asyncio
import itertools

async def ticker(interval):
    for i in itertools.count():
        print(interval, ' '*2*interval, i)
        await asyncio.sleep(interval)

loop = asyncio.get_event_loop()
task1 = loop.create_task(ticker(5))
task2 = loop.create_task(ticker(1))
task3 = loop.create_task(ticker(2))
loop.run_forever()
