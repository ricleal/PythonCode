from fastapi import Depends, Query

from app.services.author import AuthorService
from app.services.book import BookService
from app.uow import UnitOfWork


class PageParams:
    """Reusable pagination query parameters."""

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number (1-based)"),
        page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    ) -> None:
        self.page = page
        self.page_size = page_size


def get_uow() -> UnitOfWork:
    return UnitOfWork()


def get_author_service(uow: UnitOfWork = Depends(get_uow)) -> AuthorService:
    return AuthorService(uow)


def get_book_service(uow: UnitOfWork = Depends(get_uow)) -> BookService:
    return BookService(uow)
