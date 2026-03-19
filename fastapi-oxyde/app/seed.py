"""Seed the database with 5 authors and 100 books.

Book distribution:
  20 base titles × 5 volumes = 100 books
  Each volume is assigned to a different author → every author gets 20 books.
"""

from app.models import Author, Book

_AUTHORS: list[tuple[str, str]] = [
    ("Jane Austen", "English novelist celebrated for her wit and social commentary."),
    ("George Orwell", "English novelist and essayist known for political allegory."),
    (
        "Fyodor Dostoevsky",
        "Russian novelist exploring psychology and existential themes.",
    ),
    (
        "Gabriel García Márquez",
        "Colombian Nobel laureate and pioneer of magical realism.",
    ),
    ("Toni Morrison", "American Nobel laureate renowned for her lyrical prose."),
]

_BOOK_TITLES: list[str] = [
    "The Starless Night",
    "Echoes of Silence",
    "A Fractured Sky",
    "The Hollow Crown",
    "Where Rivers End",
    "The Gilded Cage",
    "A Distant Shore",
    "Beneath the Ash",
    "The Waking Dream",
    "Shards of Light",
    "The Crimson Tide",
    "Into the Abyss",
    "A Thousand Voices",
    "The Burning Hour",
    "Pale Shadows",
    "The Iron Covenant",
    "Dust and Memory",
    "The Last Vigil",
    "Sovereign Night",
    "Threads of Fate",
]


async def seed_db() -> None:
    """Insert 5 authors and 100 books if the database is empty."""
    if await Author.objects.count() > 0:
        return

    authors = await Author.objects.bulk_create(
        [{"name": name, "bio": bio} for name, bio in _AUTHORS]
    )

    books: list[dict] = []
    for title_idx, base_title in enumerate(_BOOK_TITLES):
        for vol, author in enumerate(authors, start=1):
            title = base_title if vol == 1 else f"{base_title}: Volume {vol}"
            books.append(
                {
                    "title": title,
                    "year": 1960 + title_idx * 3 + vol,
                    "author_id": author.id,
                }
            )

    await Book.objects.bulk_create(books)
