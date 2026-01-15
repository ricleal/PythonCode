# Access Request Management API

A modern async FastAPI application that manages access requests with an approval workflow, using SQLite database and following the Repository and Unit of Work patterns.

## Features

- **Async/Await**: Fully asynchronous implementation with SQLAlchemy AsyncSession
- **Repository Pattern**: Data access logic is encapsulated in repository classes
- **Unit of Work Pattern**: Ensures transactional integrity with automatic commit/rollback
- **Dependency Injection**: Clean separation of concerns with FastAPI dependencies
- **Service Layer**: Business logic separated from API endpoints
- **SQLite Database**: Lightweight database with aiosqlite for async support
- **Approval Workflow**: 
  - Access requests require 2 approvals to be approved
  - A single denial immediately denies the request
  - States: PENDING, APPROVED, DENIED

## Architecture

The application follows a clean architecture with clear separation of concerns:

### Layers

1. **API Layer** (`main.py`): FastAPI endpoints, HTTP handling, response serialization
2. **Service Layer** (`service.py`): Business logic, validation, transaction orchestration
3. **Repository Layer** (`repositories.py`): Data access patterns, database queries
4. **Model Layer** (`models.py`): SQLAlchemy ORM models, database schema

### Design Patterns

- **Unit of Work**: Manages transactions with automatic commit on success, rollback on error
- **Repository Pattern**: Abstracts data access logic from business logic
- **Dependency Injection**: UnitOfWork injected into service layer via FastAPI dependencies
- **Async Context Manager**: Transactions handled automatically with `async with` pattern

### Models

- **AccessRequest**: Represents an access request with status tracking
- **Approver**: Represents an approver assigned to an access request

### Endpoints

#### Create Access Request
```http
POST /access-requests/
```
Creates a new access request with exactly 2 approvers in a single transaction.

**Request Body:**
```json
{
  "requester": "john.doe@example.com",
  "resource": "Production Database",
  "approvers": [
    {
      "name": "Alice Smith",
      "email": "alice@example.com"
    },
    {
      "name": "Bob Johnson",
      "email": "bob@example.com"
    }
  ]
}
```

#### Approve Access Request
```http
POST /access-requests/{request_id}/approve
```
Approves an access request. The request becomes APPROVED when 2 approvers approve it.

**Request Body:**
```json
{
  "approver_email": "alice@example.com"
}
```

#### Deny Access Request
```http
POST /access-requests/{request_id}/deny
```
Denies an access request. The request becomes DENIED immediately with a single denial.

**Request Body:**
```json
{
  "approver_email": "bob@example.com"
}
```

#### List Access Requests
```http
GET /access-requests/
GET /access-requests/?status_filter=PENDING
```
Lists all access requests, optionally filtered by status.

#### Get Access Request
```http
GET /access-requests/{request_id}
```
Retrieves a specific access request by ID.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
UoW/
├── main.py              # FastAPI application and API endpoints
├── service.py           # Business logic layer
├── dependencies.py      # FastAPI dependency injection
├── models.py            # SQLAlchemy ORM models
├── database.py          # Async database configuration
├── repositories.py      # Repository pattern implementation
├── unit_of_work.py      # Unit of Work pattern implementation
├── schemas.py           # Pydantic schemas for validation
├── requirements.txt     # Python dependencies
├── test_api.sh          # Shell script to test all endpoints
└── README.md            # This file
```

## Key Implementation Details

### Async Unit of Work Pattern

The UnitOfWork automatically manages transactions:

```python
async with uow as uow:
    # All operations here are in one transaction
    access_request = AccessRequest(...)
    uow.access_requests.add(access_request)
    await uow.session.flush()
    # Automatic commit on success
    # Automatic rollback on exception
```

### Service Layer Example

```python
class AccessRequestService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def create_access_request(self, requester, resource, approvers_data):
        async with self.uow as uow:
            # Business logic here
            # Transaction managed automatically
            return access_request
```

### Dependency Injection

```python
@app.post("/access-requests/")
async def create_access_request(
    request_data: AccessRequestCreate,
    uow: UnitOfWork = Depends(get_uow)  # Injected dependency
):
    service = AccessRequestService(uow)
    return await service.create_access_request(...)
```

## Testing

### Automated Test Script

Run the comprehensive test script that covers all endpoints and error cases:

```bash
./test_api.sh
```

The script tests:
- Creating access requests
- Listing and filtering requests
- Approval workflow
- Denial workflow
- Error handling

### Manual Testing with httpie

1. **Create an access request:**
```bash
http POST localhost:8000/access-requests/ \
  requester="john.doe@example.com" \
  resource="Production Server" \
  approvers:='[
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
  ]'
```

2. **First approval:**
```bash
http POST localhost:8000/access-requests/1/approve \
  approver_email="alice@example.com"
```

3. **Second approval (request becomes APPROVED):**
```bash
http POST localhost:8000/access-requests/1/approve \
  approver_email="bob@example.com"
```

4. **List all requests:**
```bash
http GET localhost:8000/access-requests/
```

5. **Filter by status:**
```bash
http GET "localhost:8000/access-requests/?status_filter=APPROVED"
```

## Business Rules

- Each access request must have exactly 2 approvers
- Approvers must have different email addresses
- An access request is **APPROVED** when 2 approvers approve it
- An access request is **DENIED** when 1 or more approvers deny it
- Once an access request is APPROVED or DENIED, no further changes can be made
- Each approver can only respond once per request
