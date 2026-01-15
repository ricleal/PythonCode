"""FastAPI dependencies for dependency injection."""

from typing import AsyncGenerator

from database import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from unit_of_work import UnitOfWork


async def get_uow(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[UnitOfWork, None]:
    """
    Dependency to get a Unit of Work instance.

    Transaction lifecycle is managed by the service layer via context manager.
    This dependency only provides and cleans up the UoW.
    """
    uow = UnitOfWork(session)
    try:
        yield uow
    except Exception:
        await uow.rollback()
        raise
    finally:
        await uow.close()
