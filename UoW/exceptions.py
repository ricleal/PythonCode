"""Custom exceptions for the access request application."""


class AccessRequestError(Exception):
    """Base exception for access request errors."""

    pass


class NotFoundError(AccessRequestError):
    """Raised when a resource is not found."""

    pass


class AccessRequestNotFoundError(NotFoundError):
    """Raised when an access request is not found."""

    def __init__(self, request_id: int):
        self.request_id = request_id
        super().__init__(f"Access request {request_id} not found")


class ApproverNotFoundError(NotFoundError):
    """Raised when an approver is not found."""

    def __init__(self, email: str, request_id: int):
        self.email = email
        self.request_id = request_id
        super().__init__(
            f"Approver with email {email} not found for request {request_id}"
        )


class ValidationError(AccessRequestError):
    """Raised when validation fails."""

    pass


class InvalidApproverCountError(ValidationError):
    """Raised when the approver count is invalid."""

    def __init__(self, expected: int, actual: int):
        self.expected = expected
        self.actual = actual
        super().__init__(f"Expected {expected} approvers, got {actual}")


class DuplicateApproverError(ValidationError):
    """Raised when duplicate approver emails are provided."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Duplicate approver email: {email}")


class AlreadyFinalizedError(ValidationError):
    """Raised when trying to modify an already finalized request."""

    def __init__(self, request_id: int, status: str):
        self.request_id = request_id
        self.status = status
        super().__init__(f"Access request {request_id} is already {status}")


class AlreadyRespondedError(ValidationError):
    """Raised when an approver has already responded."""

    def __init__(self, email: str, status: str):
        self.email = email
        self.status = status
        super().__init__(f"Approver {email} has already {status.lower()} this request")
