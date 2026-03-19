import json
import urllib.request

base = "http://127.0.0.1:8000"
all_ok = True


def req(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json"} if data else {}
    r = urllib.request.Request(
        f"{base}{path}", data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(r) as resp:
            body = resp.read()
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        return e.code, {}


def check(label, method, path, body, expected):
    global all_ok
    got, _ = req(method, path, body)
    ok = got == expected
    if not ok:
        all_ok = False
    symbol = "OK" if ok else "FAIL"
    print(f"[{symbol}] {method:6} {path:45} expected={expected} got={got}")


def req_json(method, path, body=None):
    _, data = req(method, path, body)
    return data


print("--- Static error cases ---")
check("author not found", "GET", "/authors/99999", None, 404)
check("book not found", "GET", "/books/99999", None, 404)
# 400 (bad request) is correct here: the payload references a non-existent author
check("book bad author_id", "POST", "/books/", {"title": "x", "author_id": 99999}, 400)

print("--- List / pagination ---")
check("list authors", "GET", "/authors/?page=1&page_size=5", None, 200)
check("list books", "GET", "/books/?page=1&page_size=10", None, 200)

print("--- Create resources (dynamic IDs) ---")
author = req_json("POST", "/authors/", {"name": "Check Author", "bio": "A test author"})
author_id = author["id"]
print(f"  created author id={author_id}")
check("create author", "POST", "/authors/", {"name": "Another"}, 201)

awb = req_json(
    "POST",
    "/authors/with-books",
    {
        "name": "Atomic Author",
        "books": [
            {"title": "Cosmicomics", "year": 1965},
            {"title": "Invisible Cities", "year": 1972},
        ],
    },
)
awb_author_id = awb["id"]
print(f"  created author-with-books id={awb_author_id}")
check(
    "create author with books",
    "POST",
    "/authors/with-books",
    {"name": "Atomic2", "books": [{"title": "T"}]},
    201,
)

book = req_json("POST", "/books/", {"title": "Check Book", "author_id": author_id})
book_id = book["id"]
print(f"  created book id={book_id}")
check("create book", "POST", "/books/", {"title": "B2", "author_id": author_id}, 201)

print("--- Read by ID ---")
check("get author by id", "GET", f"/authors/{author_id}", None, 200)
check("get book by id", "GET", f"/books/{book_id}", None, 200)

print("--- Update ---")
check("patch author", "PATCH", f"/authors/{author_id}", {"bio": "Updated bio"}, 200)
check("patch book", "PATCH", f"/books/{book_id}", {"title": "Updated title"}, 200)

print("--- Delete ---")
check("delete book", "DELETE", f"/books/{book_id}", None, 204)
check("delete author (cascade)", "DELETE", f"/authors/{author_id}", None, 204)
check("deleted author 404", "GET", f"/authors/{author_id}", None, 404)
check("deleted book 404", "GET", f"/books/{book_id}", None, 404)

print()
print("All passed!" if all_ok else "SOME TESTS FAILED")
