from typing import Any

from pydantic import BaseModel

# ── Pagination ────────────────────────────────────────────────────────────────


class Page(BaseModel):
    """Generic paginated response envelope."""

    items: list[Any]
    total: int
    page: int
    page_size: int
    pages: int


# ── Author ────────────────────────────────────────────────────────────────────


class AuthorCreate(BaseModel):
    name: str
    bio: str | None = None


class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None


class BookInline(BaseModel):
    """Book payload when creating together with its author."""

    title: str
    year: int | None = None


class AuthorWithBooksCreate(BaseModel):
    """Create an author and all their books in one atomic request."""

    name: str
    bio: str | None = None
    books: list[BookInline] = []


# ── Book ──────────────────────────────────────────────────────────────────────


class BookCreate(BaseModel):
    title: str
    year: int | None = None
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    author_id: int | None = None
