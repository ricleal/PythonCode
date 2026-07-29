from threading import Lock

from fastapi import FastAPI
from pydantic import BaseModel

storage: dict[str, int] = {}

lock = Lock()

# Initialize the FastAPI application
app = FastAPI()


# Optional: Define a data model for POST requests
class Item(BaseModel):
    name: str
    price: float


@app.get("/")
@app.get("/items")
def read_root():
    with lock:
        return [Item(name=k, price=v) for k, v in storage.items()]


# 2. A GET endpoint with path and query parameters
@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None):
    with lock:
        return storage.get(item_id)


# 3. A POST endpoint that accepts a JSON body
@app.post("/items", status_code=201)
def create_item(item: Item):
    with lock:
        storage[item.name] = item.price
