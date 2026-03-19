# fastapi-oxyde

CRUD example using [FastAPI](https://fastapi.tiangolo.com/) and [Oxyde ORM](https://github.com/mr-fatalyst/oxyde) with Books & Authors models.

Database: SQLite in-memory (`sqlite:///:memory:`).

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Run

```bash
uv run uvicorn main:app --reload
```

Interactive docs: <http://127.0.0.1:8000/docs>

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/authors/` | List all authors (with books) |
| POST | `/authors/` | Create an author |
| GET | `/authors/{id}` | Get an author |
| PATCH | `/authors/{id}` | Update an author |
| DELETE | `/authors/{id}` | Delete an author |
| GET | `/books/` | List all books (with author) |
| POST | `/books/` | Create a book |
| GET | `/books/{id}` | Get a book |
| PATCH | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |
