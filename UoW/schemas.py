"""Pydantic schemas for request and response validation."""

from datetime import datetime
from typing import List, Optional

from models import ApprovalStatus, RequestStatus
from pydantic import BaseModel, EmailStr


class ApproverCreate(BaseModel):
    """Schema for creating an approver."""

    name: str
    email: EmailStr


class ApproverResponse(BaseModel):
    """Schema for approver response."""

    id: int
    name: str
    email: str
    status: ApprovalStatus
    responded_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AccessRequestCreate(BaseModel):
    """Schema for creating an access request."""

    requester: str
    resource: str
    approvers: List[ApproverCreate]


class AccessRequestResponse(BaseModel):
    """Schema for access request response."""

    id: int
    requester: str
    resource: str
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    approvers: List[ApproverResponse]

    class Config:
        from_attributes = True


class ApprovalRequest(BaseModel):
    """Schema for approval/denial request."""

    approver_email: EmailStr
