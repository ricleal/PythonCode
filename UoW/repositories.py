"""Repository pattern implementation for data access."""

from typing import List, Optional

from models import AccessRequest, Approver, RequestStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class AccessRequestRepository:
    """Repository for AccessRequest operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, access_request: AccessRequest) -> AccessRequest:
        """Add a new access request to the session."""
        self.session.add(access_request)
        return access_request

    async def get_by_id(self, request_id: int) -> Optional[AccessRequest]:
        """Get an access request by ID with eagerly loaded approvers."""
        result = await self.session.execute(
            select(AccessRequest)
            .options(selectinload(AccessRequest.approvers))
            .filter(AccessRequest.id == request_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[AccessRequest]:
        """Get all access requests with eagerly loaded approvers."""
        result = await self.session.execute(
            select(AccessRequest).options(selectinload(AccessRequest.approvers))
        )
        return list(result.scalars().all())

    async def get_by_status(self, status: RequestStatus) -> List[AccessRequest]:
        """Get access requests by status with eagerly loaded approvers."""
        result = await self.session.execute(
            select(AccessRequest)
            .options(selectinload(AccessRequest.approvers))
            .filter(AccessRequest.status == status)
        )
        return list(result.scalars().all())

    async def delete(self, access_request: AccessRequest) -> None:
        """Delete an access request."""
        await self.session.delete(access_request)


class ApproverRepository:
    """Repository for Approver operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, approver: Approver) -> Approver:
        """Add a new approver to the session."""
        self.session.add(approver)
        return approver

    async def get_by_id(self, approver_id: int) -> Optional[Approver]:
        """Get an approver by ID."""
        result = await self.session.execute(
            select(Approver).filter(Approver.id == approver_id)
        )
        return result.scalar_one_or_none()

    async def get_by_access_request(self, request_id: int) -> List[Approver]:
        """Get all approvers for an access request."""
        result = await self.session.execute(
            select(Approver).filter(Approver.access_request_id == request_id)
        )
        return list(result.scalars().all())

    async def get_by_email_and_request(
        self, email: str, request_id: int
    ) -> Optional[Approver]:
        """Get an approver by email and access request ID."""
        result = await self.session.execute(
            select(Approver).filter(
                Approver.email == email, Approver.access_request_id == request_id
            )
        )
        return result.scalar_one_or_none()

    async def delete(self, approver: Approver) -> None:
        """Delete an approver."""
        await self.session.delete(approver)
