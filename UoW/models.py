"""Database models for AccessRequest and Approver."""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship with approvers
    approvers = relationship(
        "Approver", back_populates="access_request", cascade="all, delete-orphan"
    )

    def evaluate_status(self) -> RequestStatus:
        """
        Evaluate the status based on approver responses.
        - APPROVED: if 2 or more approvers have approved
        - DENIED: if 1 or more approvers have denied
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
        elif approved_count >= 2:
            return RequestStatus.APPROVED
        else:
            return RequestStatus.PENDING


class Approver(Base):
    """Approver model."""

    __tablename__ = "approvers"

    id = Column(Integer, primary_key=True, index=True)
    access_request_id = Column(
        Integer, ForeignKey("access_requests.id"), nullable=False
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(
        Enum(ApprovalStatus), default=ApprovalStatus.PENDING, nullable=False
    )
    responded_at = Column(DateTime, nullable=True)

    # Relationship with access request
    access_request = relationship("AccessRequest", back_populates="approvers")
