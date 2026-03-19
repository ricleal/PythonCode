from app.models import Book

from .base import BaseRepository


class BookRepository(BaseRepository[Book]):
    _model = Book

    async def list_with_author(self, offset: int, limit: int) -> list[Book]:
        return (
            await Book.objects.join("author")
            .order_by("id")
            .offset(offset)
            .limit(limit)
            .all()
        )

    async def get_with_author(self, book_id: int) -> Book | None:
        results = await Book.objects.filter(id=book_id).join("author").all()
        return results[0] if results else None

    async def save(self, book: Book) -> Book:
        await book.save()
        return book
