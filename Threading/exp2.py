import queue
from concurrent.futures import ThreadPoolExecutor

import requests

initial_url = "https://jsonplaceholder.typicode.com/posts"


def fetch(url):
    print(f"\tFetching {url}")
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch URL {url}: {response.status_code}")


def process_url(url: str, q_in: queue.Queue):
    content = fetch(url)
    out = []
    if type(content) is not list:
        parseable = True
        out.append(content["title"])
    else:
        for item in content:
            if "id" in item:
                parseable = True
                out.append(item["title"])
                q_in.put(f"https://jsonplaceholder.typicode.com/posts/{item['id']}")
    return out


e = ThreadPoolExecutor(max_workers=2)

q_in = queue.Queue()


q_in.put(initial_url)


while not q_in.empty():
    url = q_in.get()
    f = e.submit(process_url, url, q_in)
    print(f.result())

e.shutdown(wait=True)

print("Done")
