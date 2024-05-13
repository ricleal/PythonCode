# FastAPI Cursor pagination

See the [code](main.py) for the implementation.

## The response format

```bash
❯ http "http://0.0.0.0:8080/users?size=3"
```

```json                           
{
    "current_page": "Pg%3D%3D",
    "current_page_backwards": "PGk6MTAwNA%3D%3D",
    "items": [
        {
            "age": 0,
            "id": 1001,
            "name": "User 0"
        },
        {
            "age": 1,
            "id": 1002,
            "name": "User 1"
        },
        {
            "age": 2,
            "id": 1003,
            "name": "User 2"
        }
    ],
    "next_page": "Pmk6MTAwMw%3D%3D",
    "previous_page": null,
    "total": null
}


```

## Example

In terminal 1 run the FastAPI server:
```bash
poetry shell

fastapi dev --port 8080 main.py
```

In terminal 2 run the following to test the cursor pagination:
```bash
# Get all users (default page size is 50)
http "http://0.0.0.0:8080/users"

# Get all users starting from the 2nd page
http "http://0.0.0.0:8080/users?next_page=Pmk6MTA1MA%3D%3D"

# Get all users starting from the 2nd page with a page size of 3
http "http://0.0.0.0:8080/users?next_page=Pmk6MTA1MA%3D%3D&size=3"

```
