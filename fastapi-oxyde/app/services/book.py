from fastapi import HTTPException

from app.models import Book
from app.schemas import BookCreate, BookUpdate, Page
from app.uow import UnitOfWork


class BookService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def list(self, page: int, page_size: int) -> Page:
        offset = (page - 1) * page_size
        total = await self._uow.books.count()
        items = await self._uow.books.list_with_author(offset, page_size)
        return Page(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=(total + page_size - 1) // page_size,
        )

    async def get(self, book_id: int) -> Book:
        book = await self._uow.books.get_with_author(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    async def create(self, data: BookCreate) -> Book:
        if not await self._uow.authors.exists(id=data.author_id):
            raise HTTPException(status_code=400, detail="Author not found")
        return await self._uow.books.create(data.model_dump())

    async def update(self, book_id: int, data: BookUpdate) -> Book:
        book = await self._uow.books.get_by_id(book_id)
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        updates = data.model_dump(exclude_none=True)
        if "author_id" in updates and not await self._uow.authors.exists(
            id=updates["author_id"]
        ):
            raise HTTPException(status_code=400, detail="Author not found")
        for field, value in updates.items():
            setattr(book, field, value)
        return await self._uow.books.save(book)

    async def delete(self, book_id: int) -> None:
        deleted = await self._uow.books.delete(book_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Book not found")
