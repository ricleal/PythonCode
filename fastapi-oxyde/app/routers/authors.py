from fastapi import APIRouter, Depends

from app.dependencies import PageParams, get_author_service
from app.schemas import AuthorCreate, AuthorUpdate, AuthorWithBooksCreate, Page
from app.services.author import AuthorService

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=Page)
async def list_authors(
    params: PageParams = Depends(),
    service: AuthorService = Depends(get_author_service),
) -> Page:
    return await service.list(params.page, params.page_size)


@router.get("/{author_id}")
async def get_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
):
    return await service.get(author_id)


@router.post("/", status_code=201)
async def create_author(
    data: AuthorCreate,
    service: AuthorService = Depends(get_author_service),
):
    return await service.create(data)


@router.post("/with-books", status_code=201)
async def create_author_with_books(
    data: AuthorWithBooksCreate,
    service: AuthorService = Depends(get_author_service),
):
    """Create an author and their books atomically.

    The entire operation is wrapped in a single transaction: if any book
    insert fails the author is also rolled back.
    """
    return await service.create_with_books(data)


@router.patch("/{author_id}")
async def update_author(
    author_id: int,
    data: AuthorUpdate,
    service: AuthorService = Depends(get_author_service),
):
    return await service.update(author_id, data)


@router.delete("/{author_id}", status_code=204)
async def delete_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service),
) -> None:
    await service.delete(author_id)
