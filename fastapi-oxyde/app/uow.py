from oxyde.db import transaction

from app.repositories.author import AuthorRepository
from app.repositories.book import BookRepository


class UnitOfWork:
    """
    Groups repositories and provides transaction scoping.

    Usage inside a service:
        async with self._uow.atomic():
            author = await self._uow.authors.create(...)
            book   = await self._uow.books.create(...)
    """

    def __init__(self) -> None:
        self.authors = AuthorRepository()
        self.books = BookRepository()

    def atomic(self):
        """Async context manager that wraps work in a single transaction."""
        return transaction.atomic()
