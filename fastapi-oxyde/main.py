"""
FastAPI + Oxyde ORM – Books & Authors CRUD

Database: SQLite in-memory (sqlite://:memory:)
Tables are created on startup via raw SQL, since migrations require a file-backed DB.

Run:
    uv run uvicorn main:app --reload

Interactive docs: http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from oxyde import AsyncDatabase, disconnect_all, execute_raw

from app.routers import authors, books
from app.seed import seed_db

DATABASE_URL = "sqlite://:memory:"
DB_NAME = "default"


async def _create_tables() -> None:
    await execute_raw(
        """
        CREATE TABLE IF NOT EXISTS authors (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL,
            bio  TEXT
        )
        """,
        using=DB_NAME,
    )
    await execute_raw(
        """
        CREATE TABLE IF NOT EXISTS books (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            year      INTEGER,
            author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE
        )
        """,
        using=DB_NAME,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = AsyncDatabase(DATABASE_URL, name=DB_NAME)
    await db.connect()
    await _create_tables()
    await seed_db()
    yield
    await disconnect_all()


app = FastAPI(
    title="Books & Authors API",
    description="CRUD example using FastAPI and Oxyde ORM with SQLite in-memory.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(authors.router)
app.include_router(books.router)
