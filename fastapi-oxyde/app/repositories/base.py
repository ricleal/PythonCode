from typing import Any, Generic, TypeVar

from oxyde import Model

M = TypeVar("M", bound=Model)


class BaseRepository(Generic[M]):
    """Generic CRUD operations backed by an Oxyde model."""

    _model: type[M]

    async def get_by_id(self, pk: int) -> M | None:
        return await self._model.objects.filter(id=pk).first()

    async def count(self) -> int:
        return await self._model.objects.count()

    async def create(self, data: dict[str, Any]) -> M:
        return await self._model.objects.create(**data)

    async def bulk_create(self, data: list[dict[str, Any]]) -> list[M]:
        return await self._model.objects.bulk_create(data)

    async def delete(self, pk: int) -> int:
        return await self._model.objects.filter(id=pk).delete()

    async def exists(self, **kwargs: Any) -> bool:
        return await self._model.objects.filter(**kwargs).exists()
