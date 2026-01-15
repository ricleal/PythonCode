"""Service layer for business logic."""

from typing import List, Optional

from exceptions import (
    AccessRequestNotFoundError,
    AlreadyFinalizedError,
    AlreadyRespondedError,
    ApproverNotFoundError,
    DuplicateApproverError,
    InvalidApproverCountError,
)
from models import AccessRequest, ApprovalStatus, Approver, RequestStatus, utc_now
from unit_of_work import UnitOfWork


class AccessRequestService:
    """Service class for access request business logic."""

    REQUIRED_APPROVERS = 2

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the service with a Unit of Work.

        Args:
            uow: Unit of Work instance for transaction management
        """
        self.uow = uow

    async def create_access_request(
        self, requester: str, resource: str, approvers_data: List[dict]
    ) -> AccessRequest:
        """
        Create a new access request with approvers.

        Args:
            requester: Email or name of the requester
            resource: Resource being requested
            approvers_data: List of dicts with 'name' and 'email' keys

        Returns:
            Created AccessRequest with approvers

        Raises:
            InvalidApproverCountError: If approver count doesn't match requirement
            DuplicateApproverError: If duplicate approver emails are provided
        """
        if len(approvers_data) != self.REQUIRED_APPROVERS:
            raise InvalidApproverCountError(self.REQUIRED_APPROVERS, len(approvers_data))

        emails = [a["email"] for a in approvers_data]
        if len(emails) != len(set(emails)):
            duplicates = [e for e in emails if emails.count(e) > 1]
            raise DuplicateApproverError(duplicates[0])

        async with self.uow:
            access_request = AccessRequest(
                requester=requester, resource=resource, status=RequestStatus.PENDING
            )
            self.uow.access_requests.add(access_request)

            await self.uow.flush()

            for approver_data in approvers_data:
                approver = Approver(
                    access_request_id=access_request.id,
                    name=approver_data["name"],
                    email=approver_data["email"],
                    status=ApprovalStatus.PENDING,
                )
                self.uow.approvers.add(approver)

            await self.uow.flush()
            await self.uow.refresh(access_request, ["approvers"])

            return access_request

    async def approve_access_request(
        self, request_id: int, approver_email: str
    ) -> AccessRequest:
        """
        Approve an access request.

        Args:
            request_id: ID of the access request
            approver_email: Email of the approver

        Returns:
            Updated AccessRequest

        Raises:
            AccessRequestNotFoundError: If request not found
            AlreadyFinalizedError: If request is already finalized
            ApproverNotFoundError: If approver not found
            AlreadyRespondedError: If approver already responded
        """
        async with self.uow:
            access_request = await self._get_request_for_update(request_id)
            approver = await self._get_approver_for_update(approver_email, request_id)

            approver.status = ApprovalStatus.APPROVED
            approver.responded_at = utc_now()

            await self.uow.flush()

            access_request.status = access_request.evaluate_status()

            await self.uow.flush()
            await self.uow.refresh(access_request, ["approvers"])

            return access_request

    async def deny_access_request(
        self, request_id: int, approver_email: str
    ) -> AccessRequest:
        """
        Deny an access request.

        Args:
            request_id: ID of the access request
            approver_email: Email of the approver

        Returns:
            Updated AccessRequest

        Raises:
            AccessRequestNotFoundError: If request not found
            AlreadyFinalizedError: If request is already finalized
            ApproverNotFoundError: If approver not found
            AlreadyRespondedError: If approver already responded
        """
        async with self.uow:
            access_request = await self._get_request_for_update(request_id)
            approver = await self._get_approver_for_update(approver_email, request_id)

            approver.status = ApprovalStatus.DENIED
            approver.responded_at = utc_now()

            await self.uow.flush()

            access_request.status = access_request.evaluate_status()

            await self.uow.flush()
            await self.uow.refresh(access_request, ["approvers"])

            return access_request

    async def get_access_request(self, request_id: int) -> AccessRequest:
        """
        Get an access request by ID.

        Args:
            request_id: ID of the access request

        Returns:
            AccessRequest if found

        Raises:
            AccessRequestNotFoundError: If not found
        """
        access_request = await self.uow.access_requests.get_by_id(request_id)
        if not access_request:
            raise AccessRequestNotFoundError(request_id)

        return access_request

    async def list_access_requests(
        self, status_filter: Optional[RequestStatus] = None
    ) -> List[AccessRequest]:
        """
        List all access requests, optionally filtered by status.

        Args:
            status_filter: Optional status to filter by

        Returns:
            List of AccessRequest objects
        """
        if status_filter:
            return await self.uow.access_requests.get_by_status(status_filter)
        return await self.uow.access_requests.get_all()

    async def _get_request_for_update(self, request_id: int) -> AccessRequest:
        """Get and validate an access request for updating."""
        access_request = await self.uow.access_requests.get_by_id(request_id)
        if not access_request:
            raise AccessRequestNotFoundError(request_id)

        if access_request.status != RequestStatus.PENDING:
            raise AlreadyFinalizedError(request_id, access_request.status.value)

        return access_request

    async def _get_approver_for_update(
        self, approver_email: str, request_id: int
    ) -> Approver:
        """Get and validate an approver for updating."""
        approver = await self.uow.approvers.get_by_email_and_request(
            approver_email, request_id
        )

        if not approver:
            raise ApproverNotFoundError(approver_email, request_id)

        if approver.status != ApprovalStatus.PENDING:
            raise AlreadyRespondedError(approver_email, approver.status.value)

        return approver


class AuditService:
    """Service class for audit logging business logic."""

    def __init__(self, uow: UnitOfWork):
        """
        Initialize the service with a Unit of Work.

        Args:
            uow: Unit of Work instance for transaction management
        """
        self.uow = uow

    async def log_approval_action(
        self, request_id: int, approver_email: str, action: str
    ) -> None:
        """
        Log an approval action (for demonstration purposes).

        In a real application, this would write to an audit log table.

        Args:
            request_id: ID of the access request
            approver_email: Email of the approver
            action: Action taken (APPROVED/DENIED)
        """
        # In a real implementation, you'd add a record to an audit log table
        # For now, we'll just demonstrate the pattern
        print(f"AUDIT: Request {request_id} - {action} by {approver_email}")
        
        # If you had an audit repository:
        # audit_entry = AuditLog(
        #     request_id=request_id,
        #     approver_email=approver_email,
        #     action=action,
        #     timestamp=utc_now()
        # )
        # self.uow.audit_logs.add(audit_entry)
        # await self.uow.flush()
        
        # Note: We DON'T commit here - the caller will commit the entire transaction
