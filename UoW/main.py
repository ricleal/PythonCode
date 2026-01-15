"""FastAPI application with access request management."""

from contextlib import asynccontextmanager
from typing import List, Optional

from database import create_tables
from dependencies import get_uow
from exceptions import NotFoundError, ValidationError
from fastapi import Depends, FastAPI, HTTPException, status
from models import RequestStatus
from schemas import AccessRequestCreate, AccessRequestResponse, ApprovalRequest
from service import AccessRequestService
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
