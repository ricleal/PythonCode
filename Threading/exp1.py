"""
Launch redis server with docker:
docker run --name my_redis_server -p 6379:6379 -d redis:7.2

"""

import time
import urllib.parse

import redis
import requests

# Redis connection
r = redis.Redis()


# Delete all created keys
def delete_all_keys(app_id, organization_id, system_id):
    keys = r.keys(f"{app_id}:{organization_id}:{system_id}:*")
    if keys:
        r.delete(*keys)


# Function to fetch and store URL content
def fetch_and_store_url(app_id, organization_id, system_id, url):
    key = f"{app_id}:{organization_id}:{system_id}:{urllib.parse.quote(url)}"

    # Check if content is already in Redis
    cached_content = r.get(key)
    if cached_content:
        print(f"\tCache hit! key={key}")
        return cached_content.decode("utf-8")

    # Fetch content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        r.set(key, content)
        return content
    else:
        raise Exception(f"Failed to fetch URL {url}: {response.status_code}")


# Example usage
app_id = "myapp"
organization_id = "o_myorg"
system_id = "r_mysystem"
urls = ["https://jsonplaceholder.typicode.com/posts/{}".format(i) for i in range(1, 6)]


for url in urls * 2:
    start = time.time()
    content = fetch_and_store_url(app_id, organization_id, system_id, url)
    print(
        f"Fetching {url} :: {(time.time() - start) * 1000:.3f} ms ({len(content)} Bytes, md5={hash(content)})"
    )

# If it didn't crash, delete all keys created
delete_all_keys(app_id, organization_id, system_id)
