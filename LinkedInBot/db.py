"""SQLite database operations for LinkedIn Bot."""

import sqlite3
from datetime import datetime


def get_connection(db_path: str) -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db(db_path: str) -> None:
    """Initialize the database and create tables if they don't exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            generated_text TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'generated',
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posted_at TIMESTAMP
        )
    """)

    # Migration: add image_url column to existing posts tables
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN image_url TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS linkedin_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            access_token TEXT NOT NULL,
            refresh_token TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_post(
    db_path: str,
    subject: str,
    generated_text: str,
    status: str = "generated",
    image_url: str | None = None,
) -> int:
    """Save a generated post to the database. Returns the post ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (subject, generated_text, status, image_url) VALUES (?, ?, ?, ?)",
        (subject, generated_text, status, image_url),
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id


def update_post_status(db_path: str, post_id: int, status: str) -> None:
    """Update the status of a post."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    if status == "posted":
        cursor.execute(
            "UPDATE posts SET status = ?, posted_at = ? WHERE id = ?",
            (status, datetime.now(), post_id),
        )
    else:
        cursor.execute(
            "UPDATE posts SET status = ? WHERE id = ?",
            (status, post_id),
        )

    conn.commit()
    conn.close()


def update_post_image(db_path: str, post_id: int, image_url: str) -> None:
    """Update the image_url for a post."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE posts SET image_url = ? WHERE id = ?",
        (image_url, post_id),
    )
    conn.commit()
    conn.close()


def save_linkedin_token(
    db_path: str,
    access_token: str,
    refresh_token: str | None = None,
    expires_at: str | None = None,
) -> None:
    """Save LinkedIn OAuth tokens, replacing any existing tokens."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM linkedin_tokens")
    cursor.execute(
        "INSERT INTO linkedin_tokens (access_token, refresh_token, expires_at) VALUES (?, ?, ?)",
        (access_token, refresh_token, expires_at),
    )
    conn.commit()
    conn.close()


def get_linkedin_token(db_path: str) -> dict | None:
    """Get the stored LinkedIn OAuth token, if any."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM linkedin_tokens ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_post_history(db_path: str, limit: int = 10) -> list[dict]:
    """Get recent post history."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, subject, status, image_url, created_at, posted_at FROM posts ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
