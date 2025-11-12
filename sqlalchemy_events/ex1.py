"""
SQLAlchemy Event Listeners - Synchronous Behavior Demonstration

Purpose:
--------
This example demonstrates that SQLAlchemy event listeners execute SYNCHRONOUSLY
within the database transaction lifecycle. Key observations:

1. Event listeners block the main thread - the commit() call waits for all
   event handlers to complete before returning control.

2. The 'after_flush' event fires during commit(), before data is committed,
   allowing you to track changes while objects are still in their pre-commit state.

3. The 'after_commit' event fires after successful commit, but still blocks
   the calling code until all handlers complete.

4. Time-consuming operations (like the simulated 1-second email delay) will
   block the transaction, demonstrating the synchronous nature of these events.

Use Cases:
----------
- Tracking changes to specific model attributes
- Triggering actions after successful commits
- Maintaining audit logs or change history
- Sending notifications (though async alternatives are preferred for production)

Note: For production systems with expensive I/O operations (emails, API calls),
consider using async task queues (Celery, RQ) triggered by these events rather
than performing the work directly in the event handlers.

Expected Output:
----------------
$ python ex1.py

--- Case 1: Creating new user 'Alice' ---
[FLUSH] Tracking new user: Alice
[EMAIL] Sending 'Welcome' email to Alice (alice@example.com)
[EMAIL] Email sent.
[COMMIT] Finished processing actions.

--- Case 2: Updating 'Alice's email ---
[FLUSH] Tracking updated user (email changed): Alice
[EMAIL] Sending 'Profile Update' notification to Alice (alice_new@example.com)
[EMAIL] Email sent.
[COMMIT] Finished processing actions.

--- Case 3: Updating 'Alice's name (untracked attribute) ---
[COMMIT] Finished processing actions.

Notice the 1-second delay per email demonstrates synchronous blocking behavior.
"""

import time

from sqlalchemy import Column, Integer, String, create_engine, event, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Setup the Database and Models
Base = declarative_base()
Engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=Engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))


Base.metadata.create_all(Engine)


# 2. Event Listeners
def send_email(user_info, action_type):
    """Simulated function to send an email. Runs after commit."""
    if action_type == "created":
        print(
            f"[EMAIL] Sending 'Welcome' email to {user_info['name']} ({user_info['email']})"
        )
    elif action_type == "updated":
        print(
            f"[EMAIL] Sending 'Profile Update' notification to {user_info['name']} ({user_info['email']})"
        )

    time.sleep(1)  # Simulate network delay
    print("[EMAIL] Email sent.")


@event.listens_for(SessionLocal, "after_flush")
def track_changes_after_flush(session, flush_context):
    """
    Tracks new and updated User objects *before* commit.
    Stores metadata in the session.info dictionary.
    """
    if "commit_actions" not in session.info:
        session.info["commit_actions"] = []
    # Track new objects (insertions)
    for obj in session.new:
        if isinstance(obj, User):
            # We must capture the data now, as objects expire after commit
            user_data = {"name": obj.name, "email": obj.email}
            session.info["commit_actions"].append(
                {"type": "created", "data": user_data}
            )
            print(f"[FLUSH] Tracking new user: {obj.name}")
    # Track updated objects
    for obj in session.dirty:
        if isinstance(obj, User):
            # Check if relevant attributes actually changed
            state = inspect(obj)
            if state.attrs.email.history.has_changes():
                user_data = {"name": obj.name, "email": obj.email}
                session.info["commit_actions"].append(
                    {"type": "updated", "data": user_data}
                )
                print(f"[FLUSH] Tracking updated user (email changed): {obj.name}")


@event.listens_for(SessionLocal, "after_commit")
def process_actions_after_commit(session):
    """
    Executes actions (like sending emails) after a successful commit.
    Cannot perform new SQL operations here.
    """
    # Retrieve tracked actions from session.info
    actions = session.info.get("commit_actions", [])
    for action in actions:
        send_email(action["data"], action["type"])
    # Clean up the info dictionary for the next transaction
    session.info.pop("commit_actions", None)
    print("[COMMIT] Finished processing actions.")


# 3. Demonstration of Usage
if __name__ == "__main__":
    session = SessionLocal()
    try:
        # --- Case 1: Create a new user ---
        print("\n--- Case 1: Creating new user 'Alice' ---")
        alice = User(name="Alice", email="alice@example.com")
        session.add(alice)
        session.commit()
        # The after_flush and after_commit listeners run during the commit() call above.
        # --- Case 2: Update an existing user ---
        print("\n--- Case 2: Updating 'Alice's email ---")
        # Note: 'alice' is now "expired" (attributes unloaded)
        # We access an attribute to reload it from the DB
        alice.email = "alice_new@example.com"
        session.add(
            alice
        )  # Not strictly necessary if already tracked, but good practice
        session.commit()
        # --- Case 3: Update an attribute that is *not* tracked ---
        print("\n--- Case 3: Updating 'Alice's name (untracked attribute) ---")
        alice.name = "Alice Liddell"  # We only track email changes in our listener
        session.commit()  # No email will be sent for this change.
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
