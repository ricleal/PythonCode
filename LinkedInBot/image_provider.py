"""Fetch images from Unsplash to accompany LinkedIn posts.

Uses the free Unsplash API (requires an access key).
Rate limit: 50 requests/hour on the free tier.
"""

import os
import tempfile
from pathlib import Path

import requests


class ImageProvider:
    """Search Unsplash for images matching a subject and download them."""

    UNSPLASH_SEARCH_URL = "https://api.unsplash.com/search/photos"

    # Map common subject keywords to broader visual concepts.
    # Unsplash has lots of tech/office/abstract images that work well.
    _FALLBACK_QUERIES = [
        "technology abstract",
        "software development",
        "coding",
        "data center",
        "digital transformation",
        "modern office",
        "engineering",
    ]

    def __init__(self, access_key: str | None = None):
        self.access_key = access_key or os.getenv("UNSPLASH_ACCESS_KEY", "")

    def _keywords_from_subject(self, subject: str) -> list[str]:
        """Extract search keywords from a subject line."""
        # Strip common prefixes
        text = subject.lower()
        for prefix in [
            "how to ",
            "how ",
            "why ",
            "what ",
            "the ",
            "building ",
            "designing ",
            "lessons from ",
            "lessons learned from ",
        ]:
            if text.startswith(prefix):
                text = text[len(prefix) :]
                break

        # Remove anything after a colon or em dash (subtitle)
        for sep in [": ", ": ", " — ", " — ", " – ", " - "]:
            if sep in text:
                text = text[: text.index(sep)]
                break

        # Remove trailing question marks
        text = text.rstrip("?.")

        # Take first 3 meaningful words
        stop_words = {
            "a",
            "an",
            "the",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "is",
            "it",
            "are",
            "was",
            "that",
            "this",
            "these",
            "those",
            "its",
            "your",
            "our",
            "their",
        }
        words = [w for w in text.split() if w not in stop_words and len(w) > 2]
        return words[:3] if words else ["technology"]

    def fetch_image(self, subject: str) -> tuple[str | None, str | None]:
        """Find an image on Unsplash matching the subject and download it.

        Returns:
            A tuple of (local_file_path, unsplash_image_url).
            Both are None if no image could be fetched.
        """
        if not self.access_key:
            print("   ⚠️  UNSPLASH_ACCESS_KEY not set — skipping image.")
            return None, None

        keywords = self._keywords_from_subject(subject)
        query = " ".join(keywords)

        # Try the specific query first; fall back to broader tech queries
        queries_to_try = [query] + self._FALLBACK_QUERIES

        for q in queries_to_try:
            image_url, download_url = self._search_unsplash(q)
            if image_url:
                local_path = self._download_image(image_url)
                if local_path:
                    return str(local_path), image_url
            # Don't keep retrying the fallbacks if the first failed due to auth
            if q == queries_to_try[0] and not self.access_key:
                break

        print("   ⚠️  Could not find a suitable image on Unsplash.")
        return None, None

    def _search_unsplash(self, query: str) -> tuple[str | None, str | None]:
        """Search Unsplash for a query. Returns (image_url, download_url).

        The ``image_url`` is a direct image URL (usable for downloading).
        The ``download_url`` is an API endpoint for tracking downloads
        (requires a separate authed request).
        """
        try:
            response = requests.get(
                self.UNSPLASH_SEARCH_URL,
                headers={"Authorization": f"Client-ID {self.access_key}"},
                params={
                    "query": query,
                    "per_page": 3,
                    "orientation": "landscape",
                    "content_filter": "high",
                },
                timeout=10,
            )

            if response.status_code == 401:
                print("   ⚠️  Unsplash API key is invalid.")
                return None, None

            if response.status_code == 403:
                print("   ⚠️  Unsplash rate limit exceeded. Try again later.")
                return None, None

            response.raise_for_status()
            data = response.json()

            if not data.get("results"):
                return None, None

            # Pick the first result — use the raw URL for downloading
            # (raw gives highest quality; regular is a good fallback)
            photo = data["results"][0]
            img_url = photo["urls"]["raw"] or photo["urls"]["regular"]
            download_url = photo["links"]["download_location"]
            return img_url, download_url

        except requests.RequestException as e:
            print(f"   ⚠️  Unsplash search failed: {e}")
            return None, None

    def _download_image(self, image_url: str) -> Path | None:
        """Download an image to a temporary file."""
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()

            # Save to a temp file
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            tmp.write(response.content)
            tmp.close()
            return Path(tmp.name)

        except requests.RequestException as e:
            print(f"   ⚠️  Failed to download image: {e}")
            return None

    @staticmethod
    def cleanup(path: str | Path | None) -> None:
        """Delete a temporary image file."""
        if path:
            try:
                Path(path).unlink(missing_ok=True)
            except Exception:
                pass
