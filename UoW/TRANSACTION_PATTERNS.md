# Transaction Management with Multiple Services

## The Problem
When an endpoint needs to use multiple services, you want to ensure:
1. All changes happen in a **single database transaction**
2. **Only ONE commit** occurs (not multiple)
3. If anything fails, everything rolls back (atomicity)

## The Solution: Share the Same UnitOfWork

### ✅ CORRECT Pattern - Single Transaction

```python
@app.post("/access-requests/{request_id}/approve-with-audit")
async def approve_with_audit(
    request_id: int,
    approval_data: ApprovalRequest,
    uow: UnitOfWork = Depends(get_uow),  # Inject ONE UoW instance
):
    # Pass the SAME UnitOfWork to both services
    access_request_service = AccessRequestService(uow)
    audit_service = AuditService(uow)

    try:
        async with uow:  # Start transaction
            # Service 1 operations
            access_request = await access_request_service._get_request_for_update(request_id)
            # ... make changes ...
            await uow.flush()
            
            # Service 2 operations
            await audit_service.log_approval_action(request_id, email, "APPROVED")
            await uow.flush()
            
            # ONE commit happens here automatically when exiting context
            return access_request
            
    except Exception as e:
        # Automatic rollback on exception
        raise HTTPException(status_code=400, detail=str(e))
```

**Key Points:**
- ✅ One `UnitOfWork` instance injected by FastAPI dependency
- ✅ Both services share the same `uow` (same database session)
- ✅ Use `async with uow:` in the endpoint to manage transaction lifecycle
- ✅ Call `await uow.flush()` between operations to sync changes without committing
- ✅ Commit happens automatically when exiting the context manager
- ✅ Rollback happens automatically on exception

### ❌ INCORRECT Pattern - Double Commits

```python
# DON'T DO THIS!
@app.post("/bad-example")
async def bad_example(
    request_id: int,
    uow: UnitOfWork = Depends(get_uow),
):
    service1 = AccessRequestService(uow)
    service2 = AuditService(uow)
    
    # ❌ DON'T use async with inside service methods
    access_request = await service1.approve_access_request(request_id, email)  # Commits!
    await service2.log_approval_action(request_id, email, "APPROVED")  # Commits again!
    
    # Problem: Two separate commits! If service2 fails, service1 already committed.
```

## Service Design Pattern

### Services Should NOT Auto-Commit

Services should perform operations but let the **caller** control when to commit:

```python
class MyService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def do_something(self, data):
        """
        Perform operations but DON'T commit.
        Let the caller manage the transaction.
        """
        entity = await self.uow.my_repo.get_by_id(data.id)
        entity.update(data)
        await self.uow.flush()  # ✅ Flush changes
        # ❌ DON'T call self.uow.commit() here
        return entity
```

### When Service Methods Need Atomicity

If a service method needs to be atomic when called standalone:

```python
class MyService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def standalone_operation(self, data):
        """
        Can be called standalone or as part of a larger transaction.
        """
        async with self.uow:  # Only commits if not already in a context
            entity = await self.uow.my_repo.get_by_id(data.id)
            entity.update(data)
            await self.uow.flush()
            return entity
```

**Note:** If `standalone_operation()` is called within an existing `async with uow:` block, the inner context manager won't commit - only the outermost one will.

## Best Practices

### 1. **Single UnitOfWork per Request**
```python
# FastAPI injects ONE UnitOfWork per request
uow: UnitOfWork = Depends(get_uow)
```

### 2. **Share UnitOfWork Across Services**
```python
service1 = Service1(uow)  # Same uow
service2 = Service2(uow)  # Same uow
service3 = Service3(uow)  # Same uow
```

### 3. **Manage Transaction at Endpoint Level**
```python
async with uow:
    # All service operations here
    result1 = await service1.operation()
    result2 = await service2.operation()
    result3 = await service3.operation()
    # Single commit happens here
```

### 4. **Use flush() Between Operations**
```python
async with uow:
    await service1.create_entity()
    await uow.flush()  # Make ID available
    
    await service2.use_entity_id()  # Can now access the ID
    await uow.flush()
    
    # Commit all changes together
```

### 5. **Let Exceptions Trigger Rollback**
```python
async with uow:
    await service1.operation()
    await service2.operation()  # If this raises, automatic rollback
```

## Advanced: Nested Transactions (Savepoints)

For complex scenarios with partial rollback:

```python
async with uow:
    # Operation 1
    await service1.critical_operation()
    await uow.flush()
    
    try:
        # Operation 2 (might fail, but we want to keep operation 1)
        # Would need savepoint support in your UnitOfWork
        await service2.risky_operation()
        await uow.flush()
    except SpecificError:
        # Rollback only operation 2
        pass
    
    # Commit operation 1 (and operation 2 if successful)
```

## Summary

**The Golden Rule:** 
> Pass the same `UnitOfWork` instance to all services involved in a single endpoint operation. Manage the transaction lifecycle (commit/rollback) at the **endpoint level** using the `async with uow:` context manager.

This ensures:
- ✅ Single database transaction
- ✅ Single commit
- ✅ Automatic rollback on errors
- ✅ Data consistency across all services
