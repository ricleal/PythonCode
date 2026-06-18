#!/usr/bin/env python3
"""LinkedIn Bot — Generate posts with DeepSeek and publish to LinkedIn.

Usage:
  python main.py              Interactive mode (menu-driven)
  python main.py --auto       Automated mode — picks a subject, generates,
                              posts to LinkedIn, and exits. Suitable for cron.
"""

import argparse
import os
import random
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI

import db
from linkedin_client import LinkedInClient

# ── Configuration ──────────────────────────────────────────────────────────

load_dotenv()

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
LINKEDIN_REDIRECT_URI = os.getenv(
    "LINKEDIN_REDIRECT_URI", "http://localhost:8080/callback"
)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
MAX_POST_LENGTH = int(os.getenv("MAX_POST_LENGTH", "3000"))
POST_LANGUAGE = os.getenv("POST_LANGUAGE", "en")
DB_PATH = os.getenv("DB_PATH", "posts.db")

BASE_DIR = Path(__file__).parent
SUBJECTS_FILE = BASE_DIR / "subjects.yaml"
DB_PATH_ABS = BASE_DIR / DB_PATH


# ── Helpers ────────────────────────────────────────────────────────────────


def load_subjects() -> list[str]:
    """Load the list of subjects from the YAML file."""
    if not SUBJECTS_FILE.exists():
        print(f"❌ Subjects file not found: {SUBJECTS_FILE}")
        sys.exit(1)
    with open(SUBJECTS_FILE, "r") as f:
        data = yaml.safe_load(f)
    return data.get("subjects", [])


def pick_random_subject(subjects: list[str]) -> str:
    """Pick a random subject from the list."""
    return random.choice(subjects)


def generate_post(subject: str) -> str | None:
    """Generate a LinkedIn post using the DeepSeek API.

    Returns the generated text, or None if generation failed.
    """
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")

    system_prompt = (
        f"You are an expert LinkedIn content creator. "
        f"Write engaging, professional LinkedIn posts in {POST_LANGUAGE}. "
        f"The post should be insightful, well-structured, and suitable for a "
        f"tech-savvy audience of software engineers and developers. "
        f"Use a natural, conversational tone. "
        f"Keep the post under {MAX_POST_LENGTH} characters. "
        # f"Do NOT use hashtags unless they are naturally part of the content. "
        f"The post should feel authentic, not like marketing."
    )

    user_prompt = (
        f"Write a LinkedIn post about the following topic:\n\n"
        f"Subject: {subject}\n\n"
        f"Make it engaging and thought-provoking. Include personal insights, "
        f"practical advice, or lessons learned. The post should feel authentic "
        f"and provide value to other software engineers."
    )

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=min(MAX_POST_LENGTH, 4096),
            temperature=0.8,
        )
        content = response.choices[0].message.content
        if content:
            return content.strip()
        return None
    except Exception as e:
        print(f"\n❌ Error generating post with DeepSeek: {e}")
        return None


def show_menu() -> str:
    """Display the interactive menu and return the user's choice."""
    print("\n" + "─" * 60)
    print("What would you like to do?")
    print("  [p]  Post it to LinkedIn")
    print("  [r]  Regenerate (generate again with same subject)")
    print("  [n]  New subject (pick a different topic)")
    print("  [s]  Skip / Save as draft (don't post)")
    print("  [a]  Abort (discard and exit)")
    print("  [h]  Show post history")
    print("─" * 60)

    while True:
        choice = input("→ Your choice: ").strip().lower()
        if choice in ("p", "r", "n", "s", "a", "h"):
            return choice
        print("  Invalid choice. Please enter p, r, n, s, a, or h.")


def show_post_history() -> None:
    """Display recent post history from the database."""
    posts = db.get_post_history(DB_PATH_ABS, limit=10)
    if not posts:
        print("\n📭 No posts in history yet.")
        return

    print("\n" + "─" * 60)
    print("📋  RECENT POST HISTORY")
    print("─" * 60)
    for post in posts:
        status_icon = {
            "posted": "✅",
            "generated": "📝",
            "discarded": "🗑️",
            "draft": "📄",
        }.get(post["status"], "❓")
        created = post["created_at"][:19] if post["created_at"] else "?"
        posted = f" | posted: {post['posted_at'][:19]}" if post.get("posted_at") else ""
        print(f"  {status_icon}  #{post['id']} — {post['subject'][:60]}")
        print(f"     {created}{posted} | status: {post['status']}")
    print("─" * 60)


def handle_linkedin_auth() -> LinkedInClient | None:
    """Handle LinkedIn authentication, using stored token if available."""
    client = LinkedInClient(
        LINKEDIN_CLIENT_ID,
        LINKEDIN_CLIENT_SECRET,
        LINKEDIN_REDIRECT_URI,
    )

    # Check if we already have a stored token
    stored_token = db.get_linkedin_token(DB_PATH_ABS)
    if stored_token and stored_token.get("access_token"):
        print("\n🔑 Using stored LinkedIn access token.")
        client.set_access_token(stored_token["access_token"])
        try:
            # Verify the token is still valid
            user_info = client.get_user_info()
            print(f"   👤 Authenticated as: {user_info.get('name', 'Unknown')}")
            return client
        except Exception:
            print("   ⚠️  Stored token expired or invalid. Re-authenticating...")

    # Run OAuth flow
    print("\n🔐 Need to authenticate with LinkedIn...")
    try:
        client.authenticate()
        user_info = client.get_user_info()
        print(f"\n   ✅ Authenticated as: {user_info.get('name', 'Unknown')}")
        # Store the token
        db.save_linkedin_token(DB_PATH_ABS, client.access_token)
        return client
    except Exception as e:
        print(f"\n❌ LinkedIn authentication failed: {e}")
        print("   You can still generate posts and save them as drafts.")
        return None


# ── Auto Mode (cron-friendly) ──────────────────────────────────────────────


def run_auto() -> None:
    """Automated mode: generate a post and publish without any prompts.

    Designed to be called from cron. Exits with code 0 on success, 1 on error.
    """
    # Validate configuration
    if not DEEPSEEK_API_KEY:
        print("❌ DEEPSEEK_API_KEY is not set in .env file.", flush=True)
        sys.exit(1)

    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        print("❌ LinkedIn credentials are not configured in .env file.", flush=True)
        sys.exit(1)

    # Initialize database
    db.init_db(DB_PATH_ABS)

    # Load subjects and pick one at random
    subjects = load_subjects()
    subject = pick_random_subject(subjects)

    # Authenticate with LinkedIn using stored token (fails if no token)
    linkedin_client = LinkedInClient(
        LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI
    )
    stored_token = db.get_linkedin_token(DB_PATH_ABS)
    if not stored_token or not stored_token.get("access_token"):
        print(
            "❌ No stored LinkedIn token. Run interactive mode first to authenticate.",
            flush=True,
        )
        sys.exit(1)

    linkedin_client.set_access_token(stored_token["access_token"])
    try:
        user_info = linkedin_client.get_user_info()
        print(f"🔑 Authenticated as: {user_info.get('name', 'Unknown')}", flush=True)
    except Exception as e:
        print(f"❌ LinkedIn token expired or invalid: {e}", flush=True)
        print("   Run interactive mode to re-authenticate.", flush=True)
        sys.exit(1)

    # Generate post
    print(f"📌 Subject: {subject}", flush=True)

    print("⏳ Generating post with DeepSeek...", flush=True)
    generated_text = generate_post(subject)
    if not generated_text:
        print("❌ Failed to generate post.", flush=True)
        sys.exit(1)

    # Save to database
    post_id = db.save_post(DB_PATH_ABS, subject, generated_text)

    print("⏳ Posting to LinkedIn...", flush=True)
    try:
        linkedin_client.create_post(generated_text)
        db.update_post_status(DB_PATH_ABS, post_id, "posted")
        print(f"✅ Posted successfully! (post #{post_id}) — {subject[:60]}", flush=True)
    except Exception as e:
        print(f"❌ Failed to post to LinkedIn: {e}", flush=True)
        db.update_post_status(DB_PATH_ABS, post_id, "draft")
        sys.exit(1)


# ── Main (Interactive) ─────────────────────────────────────────────────────


def main() -> None:
    print("\n" + "═" * 60)
    print("   🚀  LinkedIn Bot — AI-Powered Post Generator")
    print("═" * 60)

    # Validate configuration
    if not DEEPSEEK_API_KEY:
        print("❌ DEEPSEEK_API_KEY is not set in .env file.")
        sys.exit(1)

    if not LINKEDIN_CLIENT_ID or not LINKEDIN_CLIENT_SECRET:
        print("⚠️  LinkedIn credentials are not fully configured in .env.")
        print("   Posts can be generated and saved as drafts but not published.\n")

    # Initialize database
    db.init_db(DB_PATH_ABS)
    print(f"📦 Database initialized at: {DB_PATH_ABS}")

    # Load subjects
    subjects = load_subjects()
    print(f"📚 Loaded {len(subjects)} subjects.\n")

    # Authenticate with LinkedIn (optional — allows posting)
    linkedin_client = handle_linkedin_auth() if LINKEDIN_CLIENT_ID else None

    # Ask the user how to pick the subject
    print("─" * 60)
    print("How would you like to choose the subject?")
    print("  [r]  Random — pick a random subject from the list")
    print("  [l]  List — browse subjects and pick one by number")
    print("  [c]  Custom — type your own subject")
    print("─" * 60)

    current_subject: str | None = None
    while current_subject is None:
        choice = input("→ Your choice: ").strip().lower()

        if choice == "r":
            current_subject = pick_random_subject(subjects)
            print(f"\n📌 Random subject: {current_subject}")

        elif choice == "l":
            print()
            for i, s in enumerate(subjects, start=1):
                print(f"  {i:4d}. {s}")
            while True:
                try:
                    idx = input(f"\n  Enter number (1-{len(subjects)}): ").strip()
                    n = int(idx)
                    if 1 <= n <= len(subjects):
                        current_subject = subjects[n - 1]
                        print(f"\n📌 Subject #{n}: {current_subject}")
                        break
                    print(f"  Please enter a number between 1 and {len(subjects)}.")
                except ValueError:
                    print("  Please enter a valid number.")

        elif choice == "c":
            custom = input("\n  Enter your subject: ").strip()
            if custom:
                current_subject = custom
                print(f"\n📌 Custom subject: {current_subject}")
            else:
                print("  Subject cannot be empty.")

        else:
            print("  Invalid choice. Please enter r, l, or c.")

    last_post_id = None
    last_post_id = None

    while True:
        print(f"\n{'─' * 60}")
        print(f"📌  SUBJECT: {current_subject}")
        print(f"{'─' * 60}")

        print("\n⏳ Generating post with DeepSeek...")
        generated_text = generate_post(current_subject)

        if not generated_text:
            print(
                "\n❌ Failed to generate post. Try a different subject or check your API key."
            )
            choice = input("\n  [n] New subject  |  [a] Abort\n→ ").strip().lower()
            if choice == "a":
                break
            elif choice == "n":
                current_subject = pick_random_subject(subjects)
                continue
            else:
                break

        # Save to database
        last_post_id = db.save_post(DB_PATH_ABS, current_subject, generated_text)
        print(f"\n💾 Post saved to database (ID: {last_post_id})")

        # Show the generated text
        print(f"\n{'═' * 60}")
        print("   📝  GENERATED POST")
        print(f"{'═' * 60}")
        print(generated_text)
        print(f"\n{'─' * 60}")
        print(f"   📊 Characters: {len(generated_text)}  |  Subject: {current_subject}")
        print(f"{'─' * 60}")

        # Show menu
        while True:
            choice = show_menu()

            if choice == "p":
                if not linkedin_client:
                    print("\n❌ Cannot post: LinkedIn not configured/authenticated.")
                    print(
                        "   Save as draft instead, or configure LinkedIn credentials in .env."
                    )
                    continue

                print("\n⏳ Posting to LinkedIn...")
                try:
                    linkedin_client.create_post(generated_text)
                    db.update_post_status(DB_PATH_ABS, last_post_id, "posted")
                    print("\n✅  POSTED SUCCESSFULLY TO LINKEDIN! 🎉")
                except Exception as e:
                    print(f"\n❌ Failed to post to LinkedIn: {e}")
                    print("   The post is saved as a draft in the database.")
                    retry = input("   Try again? [y/N]: ").strip().lower()
                    if retry == "y":
                        continue
                break

            elif choice == "r":
                db.update_post_status(DB_PATH_ABS, last_post_id, "regenerated")
                break  # Break inner loop to regenerate

            elif choice == "n":
                db.update_post_status(DB_PATH_ABS, last_post_id, "discarded")
                current_subject = pick_random_subject(subjects)
                break  # Break inner loop to start new subject

            elif choice == "s":
                db.update_post_status(DB_PATH_ABS, last_post_id, "draft")
                print("\n📄 Post saved as draft in database.")
                # Ask if user wants to continue with another subject
                another = input("\n   Generate another post? [y/N]: ").strip().lower()
                if another == "y":
                    current_subject = pick_random_subject(subjects)
                    break
                else:
                    print("\n👋 Goodbye!")
                    return

            elif choice == "a":
                db.update_post_status(DB_PATH_ABS, last_post_id, "discarded")
                print("\n👋 Aborted. Goodbye!")
                return

            elif choice == "h":
                show_post_history()
                continue  # Show menu again after history

        # If we posted and the user wants to continue
        if choice == "p":
            another = input("\n   Generate another post? [y/N]: ").strip().lower()
            if another == "y":
                current_subject = pick_random_subject(subjects)
                continue
            else:
                print("\n👋 Goodbye!")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LinkedIn Bot — AI-powered post generator"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automated mode: generate, post to LinkedIn, then exit. Suitable for cron.",
    )
    args = parser.parse_args()

    if args.auto:
        run_auto()
    else:
        main()
