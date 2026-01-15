"""Service layer for business logic."""

from datetime import datetime
from typing import List

from models import AccessRequest, ApprovalStatus, Approver, RequestStatus
from unit_of_work import UnitOfWork


class AccessRequestService:
    """Service class for access request business logic."""

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
        Create a new access request with approvers in a single transaction.

        Args:
            requester: Email or name of the requester
            resource: Resource being requested
            approvers_data: List of dicts with 'name' and 'email' keys

        Returns:
            Created AccessRequest with approvers

        Raises:
            ValueError: If validation fails
        """
        # Validate that we have exactly 2 approvers
        if len(approvers_data) != 2:
            raise ValueError("An access request must have exactly 2 approvers")

        # Validate that approvers have different emails
        if approvers_data[0]["email"] == approvers_data[1]["email"]:
            raise ValueError("Approvers must have different email addresses")

        # All operations within this block are part of the same transaction
        async with self.uow as uow:
            # Create access request
            access_request = AccessRequest(
                requester=requester, resource=resource, status=RequestStatus.PENDING
            )
            uow.access_requests.add(access_request)

            # Flush to get the access_request ID
            await uow.session.flush()

            # Create approvers
            for approver_data in approvers_data:
                approver = Approver(
                    access_request_id=access_request.id,
                    name=approver_data["name"],
                    email=approver_data["email"],
                    status=ApprovalStatus.PENDING,
                )
                uow.approvers.add(approver)

            # Refresh to get all relationships before exiting context
            await uow.session.refresh(access_request, ["approvers"])

        # Return outside the context - relationships are already loaded
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
            ValueError: If validation fails
        """
        # All operations within this block are part of the same transaction
        async with self.uow as uow:
            # Get the access request
            access_request = await uow.access_requests.get_by_id(request_id)
            if not access_request:
                raise ValueError(f"Access request {request_id} not found")

            # Check if already finalized
            if access_request.status != RequestStatus.PENDING:
                raise ValueError(
                    f"Access request is already {access_request.status.value}"
                )

            # Find the approver
            approver = await uow.approvers.get_by_email_and_request(
                approver_email, request_id
            )

            if not approver:
                raise ValueError(
                    f"Approver with email {approver_email} not found for this request"
                )

            # Check if approver has already responded
            if approver.status != ApprovalStatus.PENDING:
                raise ValueError(
                    f"Approver has already {approver.status.value.lower()} this request"
                )

            # Update approver status
            approver.status = ApprovalStatus.APPROVED
            approver.responded_at = datetime.utcnow()
            uow.approvers.update(approver)

            # Flush to update approver in the database
            await uow.session.flush()

            # Re-evaluate access request status
            new_status = access_request.evaluate_status()
            access_request.status = new_status
            uow.access_requests.update(access_request)

            # Refresh to ensure relationships are loaded before exiting context
            await uow.session.refresh(access_request, ["approvers"])

        # Return outside the context - relationships are already loaded
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
            ValueError: If validation fails
        """
        # All operations within this block are part of the same transaction
        async with self.uow as uow:
            # Get the access request
            access_request = await uow.access_requests.get_by_id(request_id)
            if not access_request:
                raise ValueError(f"Access request {request_id} not found")

            # Check if already finalized
            if access_request.status != RequestStatus.PENDING:
                raise ValueError(
                    f"Access request is already {access_request.status.value}"
                )

            # Find the approver
            approver = await uow.approvers.get_by_email_and_request(
                approver_email, request_id
            )

            if not approver:
                raise ValueError(
                    f"Approver with email {approver_email} not found for this request"
                )

            # Check if approver has already responded
            if approver.status != ApprovalStatus.PENDING:
                raise ValueError(
                    f"Approver has already {approver.status.value.lower()} this request"
                )

            # Update approver status
            approver.status = ApprovalStatus.DENIED
            approver.responded_at = datetime.utcnow()
            uow.approvers.update(approver)

            # Flush to update approver in the database
            await uow.session.flush()

            # Re-evaluate access request status
            new_status = access_request.evaluate_status()
            access_request.status = new_status
            uow.access_requests.update(access_request)

            # Refresh to ensure relationships are loaded before exiting context
            await uow.session.refresh(access_request, ["approvers"])

        # Return outside the context - relationships are already loaded
        return access_request

    async def get_access_request(self, request_id: int) -> AccessRequest:
        """
        Get an access request by ID.

        Args:
            request_id: ID of the access request

        Returns:
            AccessRequest if found

        Raises:
            ValueError: If not found
        """
        access_request = await self.uow.access_requests.get_by_id(request_id)
        if not access_request:
            raise ValueError(f"Access request {request_id} not found")

        return access_request

    async def list_access_requests(
        self, status_filter: RequestStatus = None
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
        else:
            return await self.uow.access_requests.get_all()
