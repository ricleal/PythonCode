from app.models import Author

from .base import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    _model = Author

    async def list_with_books(self, offset: int, limit: int) -> list[Author]:
        return (
            await Author.objects.prefetch("books")
            .order_by("id")
            .offset(offset)
            .limit(limit)
            .all()
        )

    async def get_with_books(self, author_id: int) -> Author | None:
        results = await Author.objects.filter(id=author_id).prefetch("books").all()
        return results[0] if results else None

    async def save(self, author: Author) -> Author:
        await author.save()
        return author
