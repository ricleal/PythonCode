"""FastAPI application with access request management."""

from contextlib import asynccontextmanager
from typing import List, Optional

from database import create_tables
from dependencies import get_uow
from exceptions import NotFoundError, ValidationError
from fastapi import Depends, FastAPI, HTTPException, status
from models import RequestStatus, ApprovalStatus, utc_now
from schemas import AccessRequestCreate, AccessRequestResponse, ApprovalRequest
from service import AccessRequestService, AuditService
from unit_of_work import UnitOfWork


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    await create_tables()
    yield


app = FastAPI(title="Access Request Management API", lifespan=lifespan)


@app.post(
    "/access-requests/",
    response_model=AccessRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_access_request(
    request_data: AccessRequestCreate, uow: UnitOfWork = Depends(get_uow)
):
    """Create a new access request with approvers."""
    service = AccessRequestService(uow)

    try:
        approvers_data = [
            {"name": approver.name, "email": approver.email}
            for approver in request_data.approvers
        ]

        return await service.create_access_request(
            requester=request_data.requester,
            resource=request_data.resource,
            approvers_data=approvers_data,
        )

    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/access-requests/{request_id}/approve", response_model=AccessRequestResponse)
async def approve_access_request(
    request_id: int,
    approval_data: ApprovalRequest,
    uow: UnitOfWork = Depends(get_uow),
):
    """
    Approve an access request.

    The request is approved if 2 approvers have approved it.
    """
    service = AccessRequestService(uow)

    try:
        return await service.approve_access_request(
            request_id=request_id,
            approver_email=approval_data.approver_email,
        )

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/access-requests/{request_id}/deny", response_model=AccessRequestResponse)
async def deny_access_request(
    request_id: int,
    approval_data: ApprovalRequest,
    uow: UnitOfWork = Depends(get_uow),
):
    """
    Deny an access request.

    The request is denied if 1 or more approvers have denied it.
    """
    service = AccessRequestService(uow)

    try:
        return await service.deny_access_request(
            request_id=request_id,
            approver_email=approval_data.approver_email,
        )

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/access-requests/", response_model=List[AccessRequestResponse])
async def list_access_requests(
    status_filter: Optional[RequestStatus] = None, uow: UnitOfWork = Depends(get_uow)
):
    """List all access requests, optionally filtered by status."""
    service = AccessRequestService(uow)
    return await service.list_access_requests(status_filter=status_filter)


@app.get("/access-requests/{request_id}", response_model=AccessRequestResponse)
async def get_access_request(request_id: int, uow: UnitOfWork = Depends(get_uow)):
    """Get a specific access request by ID."""
    service = AccessRequestService(uow)

    try:
        return await service.get_access_request(request_id=request_id)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.post(
    "/access-requests/{request_id}/approve-with-audit",
    response_model=AccessRequestResponse,
)
async def approve_access_request_with_audit(
    request_id: int,
    approval_data: ApprovalRequest,
    uow: UnitOfWork = Depends(get_uow),
):
    """
    Approve an access request with audit logging.
    
    This endpoint demonstrates using 2 services within a single transaction.
    The key principle: Pass the SAME UnitOfWork instance to both services,
    and commit only ONCE at the end (handled by the UoW context manager).
    """
    # Create both services with the SAME UnitOfWork instance
    access_request_service = AccessRequestService(uow)
    audit_service = AuditService(uow)

    try:
        # Use the UnitOfWork context manager to manage the transaction
        async with uow:
            # Service 1: Update the access request
            access_request = await access_request_service._get_request_for_update(request_id)
            approver = await access_request_service._get_approver_for_update(
                approval_data.approver_email, request_id
            )
            
            approver.status = ApprovalStatus.APPROVED
            approver.responded_at = utc_now()
            await uow.flush()
            
            access_request.status = access_request.evaluate_status()
            await uow.flush()
            
            # Service 2: Log the audit entry
            await audit_service.log_approval_action(
                request_id=request_id,
                approver_email=approval_data.approver_email,
                action="APPROVED"
            )
            
            # Refresh to get updated relationships
            await uow.refresh(access_request, ["approvers"])
            
            # The commit happens automatically when exiting the context manager
            # Both services' changes are committed in ONE transaction
            return access_request

    except NotFoundError as e:
        # Rollback happens automatically on exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
