from fastapi import APIRouter, Depends

from app.dependencies import PageParams, get_book_service
from app.schemas import BookCreate, BookUpdate, Page
from app.services.book import BookService

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=Page)
async def list_books(
    params: PageParams = Depends(),
    service: BookService = Depends(get_book_service),
) -> Page:
    return await service.list(params.page, params.page_size)


@router.get("/{book_id}")
async def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    return await service.get(book_id)


@router.post("/", status_code=201)
async def create_book(
    data: BookCreate,
    service: BookService = Depends(get_book_service),
):
    return await service.create(data)


@router.patch("/{book_id}")
async def update_book(
    book_id: int,
    data: BookUpdate,
    service: BookService = Depends(get_book_service),
):
    return await service.update(book_id, data)


@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
) -> None:
    await service.delete(book_id)
