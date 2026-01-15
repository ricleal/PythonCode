"""Database models for AccessRequest and Approver."""

from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class RequestStatus(PyEnum):
    """Status enum for access requests."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class ApprovalStatus(PyEnum):
    """Status enum for approver responses."""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class AccessRequest(Base):
    """Access request model."""

    __tablename__ = "access_requests"

    id = Column(Integer, primary_key=True, index=True)
    requester = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    approvers = relationship(
        "Approver", back_populates="access_request", cascade="all, delete-orphan"
    )

    def evaluate_status(self) -> RequestStatus:
        """
        Evaluate the status based on approver responses.

        Rules:
        - DENIED: if 1 or more approvers have denied
        - APPROVED: if 2 or more approvers have approved
        - PENDING: otherwise
        """
        approved_count = sum(
            1
            for approver in self.approvers
            if approver.status == ApprovalStatus.APPROVED
        )
        denied_count = sum(
            1 for approver in self.approvers if approver.status == ApprovalStatus.DENIED
        )

        if denied_count >= 1:
            return RequestStatus.DENIED
        if approved_count >= 2:
            return RequestStatus.APPROVED
        return RequestStatus.PENDING


class Approver(Base):
    """Approver model."""

    __tablename__ = "approvers"
    __table_args__ = (
        UniqueConstraint(
            "access_request_id", "email", name="uq_approver_email_per_request"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    access_request_id = Column(
        Integer, ForeignKey("access_requests.id"), nullable=False, index=True
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(
        Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False
    )
    responded_at = Column(DateTime(timezone=True), nullable=True)

    access_request = relationship("AccessRequest", back_populates="approvers")
