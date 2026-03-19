from fastapi import HTTPException

from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate, AuthorWithBooksCreate, Page
from app.uow import UnitOfWork


class AuthorService:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def list(self, page: int, page_size: int) -> Page:
        offset = (page - 1) * page_size
        total = await self._uow.authors.count()
        items = await self._uow.authors.list_with_books(offset, page_size)
        return Page(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=(total + page_size - 1) // page_size,
        )

    async def get(self, author_id: int) -> Author:
        author = await self._uow.authors.get_with_books(author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    async def create(self, data: AuthorCreate) -> Author:
        return await self._uow.authors.create(data.model_dump())

    async def create_with_books(self, data: AuthorWithBooksCreate) -> Author:
        async with self._uow.atomic():
            author = await self._uow.authors.create(
                {"name": data.name, "bio": data.bio}
            )
            for book in data.books:
                await self._uow.books.create(
                    {"title": book.title, "year": book.year, "author_id": author.id}
                )
        # Reload with books attached so the response is complete
        return await self._uow.authors.get_with_books(author.id)

    async def update(self, author_id: int, data: AuthorUpdate) -> Author:
        author = await self._uow.authors.get_by_id(author_id)
        if author is None:
            raise HTTPException(status_code=404, detail="Author not found")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(author, field, value)
        return await self._uow.authors.save(author)

    async def delete(self, author_id: int) -> None:
        deleted = await self._uow.authors.delete(author_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Author not found")
