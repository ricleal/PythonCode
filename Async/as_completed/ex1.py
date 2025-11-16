import asyncio
import random
import time
from collections import defaultdict

data: dict[int, float] = defaultdict(lambda: 0)

lock = asyncio.Lock()


async def check_time(id) -> tuple[int, dict]:
    await asyncio.sleep(random.random())
    t = time.time()
    async with lock:
        if round(t) % 2 == 0:
            data[2] += t
        else:
            data[1] += t
        return (id, dict(data))


async def main():
    tasks = [check_time(i) for i in range(10)]

    for t in asyncio.as_completed(tasks):
        r = await t
        print(f"t = {r}")


if __name__ == "__main__":
    asyncio.run(main())
