"""Unit of Work pattern implementation."""

from typing import Optional, Sequence

from repositories import AccessRequestRepository, ApproverRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    """
    Unit of Work pattern implementation.

    Manages database transactions and provides access to repositories.
    Transaction lifecycle (commit/rollback) is managed by the dependency injection layer.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self._access_requests: Optional[AccessRequestRepository] = None
        self._approvers: Optional[ApproverRepository] = None

    @property
    def access_requests(self) -> AccessRequestRepository:
        """Get the AccessRequest repository."""
        if self._access_requests is None:
            self._access_requests = AccessRequestRepository(self.session)
        return self._access_requests

    @property
    def approvers(self) -> ApproverRepository:
        """Get the Approver repository."""
        if self._approvers is None:
            self._approvers = ApproverRepository(self.session)
        return self._approvers

    async def flush(self) -> None:
        """Flush pending changes to the database without committing."""
        await self.session.flush()

    async def refresh(self, instance: object, attribute_names: Sequence[str]) -> None:
        """Refresh an instance from the database, loading specified attributes."""
        await self.session.refresh(instance, attribute_names)

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the current transaction."""
        await self.session.rollback()

    async def close(self) -> None:
        """Close the session."""
        await self.session.close()

    async def __aenter__(self):
        """Enter async context manager."""
        # await self.session.begin(), not needed because sqlalchemy by default is autobegin
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context manager."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
