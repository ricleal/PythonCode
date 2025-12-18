"""SQLAlchemy Event Listeners - Synchronous Execution Demo"""

import time

from sqlalchemy import Column, Integer, String, create_engine, event, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

# ANSI Color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Setup Database and Models
Base = declarative_base()
Engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=Engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))


Base.metadata.create_all(Engine)


# Event Listeners
def send_email(user_info, action_type):
    """Simulates email sending with 1s delay to demonstrate synchronous blocking."""
    print(f"{MAGENTA}  [EMAIL START] Time: {time.strftime('%H:%M:%S')}{RESET}")
    if action_type == "created":
        print(
            f"{MAGENTA}    [EMAIL] Sending 'Welcome' email to {user_info['name']} ({user_info['email']}){RESET}"
        )
    elif action_type == "updated":
        print(
            f"{MAGENTA}    [EMAIL] Sending 'Profile Update' notification to {user_info['name']} ({user_info['email']}){RESET}"
        )

    time.sleep(1)
    print(f"{MAGENTA}  [EMAIL END] Time: {time.strftime('%H:%M:%S')} (took 1s){RESET}")


@event.listens_for(SessionLocal, "after_flush")
def track_changes_after_flush(session, flush_context):
    """Tracks User changes during flush (before commit)."""
    print(f"{YELLOW}  [FLUSH EVENT] Time: {time.strftime('%H:%M:%S')}{RESET}")
    if "commit_actions" not in session.info:
        session.info["commit_actions"] = []
    for obj in session.new:
        if isinstance(obj, User):
            user_data = {"name": obj.name, "email": obj.email}
            session.info["commit_actions"].append(
                {"type": "created", "data": user_data}
            )
            print(f"{YELLOW}    Tracking new user: {obj.name}{RESET}")

    for obj in session.dirty:
        if isinstance(obj, User):
            state = inspect(obj)
            if state.attrs.email.history.has_changes():
                user_data = {"name": obj.name, "email": obj.email}
                session.info["commit_actions"].append(
                    {"type": "updated", "data": user_data}
                )
                print(
                    f"{YELLOW}    Tracking updated user (email changed): {obj.name}{RESET}"
                )


@event.listens_for(SessionLocal, "after_commit")
def process_actions_after_commit(session):
    """Processes actions after successful commit."""
    print(f"{GREEN}  [COMMIT EVENT] Time: {time.strftime('%H:%M:%S')}{RESET}")
    actions = session.info.get("commit_actions", [])
    for action in actions:
        send_email(action["data"], action["type"])
    session.info.pop("commit_actions", None)
    print(f"{GREEN}  [COMMIT DONE] Time: {time.strftime('%H:%M:%S')}{RESET}")


# Demo
if __name__ == "__main__":
    session = SessionLocal()
    try:
        print(f"\n{BOLD}{CYAN}--- Case 1: Creating new user 'Alice' ---{RESET}")
        print(f"{BLUE}Before commit: {time.strftime('%H:%M:%S')}{RESET}")
        alice = User(name="Alice", email="alice@example.com")
        session.add(alice)
        session.commit()  # Events execute synchronously here - blocks for ~1 second
        print(f"{BLUE}After commit: {time.strftime('%H:%M:%S')}{RESET}\n")

        print(f"\n{BOLD}{CYAN}--- Case 2: Updating Alice's email ---{RESET}")
        print(f"{BLUE}Before commit: {time.strftime('%H:%M:%S')}{RESET}")
        alice.email = "alice_new@example.com"
        session.add(alice)
        session.commit()  # Blocks again for ~1 second
        print(f"{BLUE}After commit: {time.strftime('%H:%M:%S')}{RESET}\n")

        print(f"\n{BOLD}{CYAN}--- Case 3: Updating Alice's name (untracked) ---{RESET}")
        print(f"{BLUE}Before commit: {time.strftime('%H:%M:%S')}{RESET}")
        alice.name = "Alice Liddell"
        session.commit()  # No email sent, returns quickly
        print(f"{BLUE}After commit: {time.strftime('%H:%M:%S')}{RESET}\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

# Example Output:
#
# ❯ python ex1.py

# --- Case 1: Creating new user 'Alice' ---
# Before commit: 10:40:31
#   [FLUSH EVENT] Time: 10:40:31
#     Tracking new user: Alice
#   [COMMIT EVENT] Time: 10:40:31
#   [EMAIL START] Time: 10:40:31
#     [EMAIL] Sending 'Welcome' email to Alice (alice@example.com)
#   [EMAIL END] Time: 10:40:32 (took 1s)
#   [COMMIT DONE] Time: 10:40:32
# After commit: 10:40:32


# --- Case 2: Updating Alice's email ---
# Before commit: 10:40:32
#   [FLUSH EVENT] Time: 10:40:32
#     Tracking updated user (email changed): Alice
#   [COMMIT EVENT] Time: 10:40:32
#   [EMAIL START] Time: 10:40:32
#     [EMAIL] Sending 'Profile Update' notification to Alice (alice_new@example.com)
#   [EMAIL END] Time: 10:40:33 (took 1s)
#   [COMMIT DONE] Time: 10:40:33
# After commit: 10:40:33


# --- Case 3: Updating Alice's name (untracked) ---
# Before commit: 10:40:33
#   [FLUSH EVENT] Time: 10:40:33
#   [COMMIT EVENT] Time: 10:40:33
#   [COMMIT DONE] Time: 10:40:33
# After commit: 10:40:33
