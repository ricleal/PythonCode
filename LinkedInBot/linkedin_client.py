"""LinkedIn OAuth 2.0 authentication and posting client.

Uses the official linkedin-api-client library under the hood.
"""

import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests
from linkedin_api.clients.auth.client import AuthClient
from linkedin_api.clients.restli.client import RestliClient


class LinkedInClient:
    """Handles LinkedIn OAuth 2.0 authentication and post creation.

    Wraps the official LinkedIn API client library with a simpler interface.
    """

    API_VERSION = "202606"
    POSTS_RESOURCE = "/posts"
    USERINFO_RESOURCE = "/userinfo"
    IMAGES_RESOURCE = "/images"

    # Characters reserved by LinkedIn's "little text" format that MUST be
    # escaped with a backslash, otherwise the parser stops at the first
    # unescaped occurrence and the post appears truncated on LinkedIn.
    _LITTLE_TEXT_RESERVED = str.maketrans(
        {
            "\\": "\\\\",
            '"': '\\"',
            "{": "\\{",
            "}": "\\}",
            "@": "\\@",
            "[": "\\[",
            "]": "\\]",
            "(": "\\(",
            ")": "\\)",
            "<": "\\<",
            ">": "\\>",
            "#": "\\#",
            "*": "\\*",
            "_": "\\_",
            "~": "\\~",
        }
    )

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token: str | None = None
        self.person_id: str | None = None

        # Official LinkedIn clients
        self._auth_client = AuthClient(
            client_id=client_id,
            client_secret=client_secret,
            redirect_url=redirect_uri,
        )
        self._restli_client = RestliClient()

    def authenticate(self) -> str:
        """Run the full OAuth 2.0 authorization code flow.

        Starts a local HTTP server, opens the browser for user authorization,
        captures the callback with the authorization code, and exchanges it
        for an access token using the official AuthClient.

        Returns:
            The access token string.
        """
        auth_code = self._get_auth_code_via_browser()

        # Use the official AuthClient to exchange the code for a token
        token_response = self._auth_client.exchange_auth_code_for_access_token(
            code=auth_code
        )
        self.access_token = token_response.access_token
        return self.access_token

    def _get_auth_code_via_browser(self) -> str:
        """Start a local HTTP server and open the browser for OAuth authorization."""
        auth_code: list[str] = []

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                parsed = urllib.parse.urlparse(self.path)
                params = urllib.parse.parse_qs(parsed.query)
                if "code" in params:
                    auth_code.append(params["code"][0])
                    self._send_response(
                        200,
                        "<html><body><h1>✅ Authorization successful!</h1>"
                        "<p>You can close this window and return to the terminal.</p></body></html>",
                    )
                elif "error" in params:
                    error_desc = params.get("error_description", ["Unknown error"])[0]
                    self._send_response(
                        400,
                        f"<html><body><h1>❌ Authorization failed</h1>"
                        f"<p>{error_desc}</p></body></html>",
                    )
                else:
                    self._send_response(
                        400,
                        "<html><body><h1>❌ Authorization failed</h1>"
                        "<p>No authorization code received.</p></body></html>",
                    )

            def _send_response(self, status_code: int, body: str) -> None:
                self.send_response(status_code)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))

            def log_message(self, format: str, *args) -> None:
                pass  # Suppress HTTP server logs

        # Parse redirect URI to get port
        redirect_parsed = urllib.parse.urlparse(self.redirect_uri)
        port = redirect_parsed.port or 8080

        # Use the official AuthClient to generate the auth URL
        auth_url = self._auth_client.generate_member_auth_url(
            scopes=["openid", "profile", "w_member_social", "email"]
        )

        # Start the local HTTP server in a background thread
        server = HTTPServer(("localhost", port), CallbackHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        print("\n🔐 Opening browser for LinkedIn authorization...")
        print(f"   If the browser doesn't open, visit this URL:\n   {auth_url}\n")

        import webbrowser

        webbrowser.open(auth_url)

        # Wait up to 3 minutes for the callback
        timeout = 180
        start_time = time.time()
        while not auth_code and time.time() - start_time < timeout:
            time.sleep(0.5)

        server.shutdown()

        if not auth_code:
            raise TimeoutError(
                "Authorization timed out after 3 minutes. "
                "Make sure your LinkedIn app is configured correctly."
            )

        return auth_code[0]

    def get_user_info(self) -> dict:
        """Get the authenticated user's profile information using the RestliClient."""
        self._ensure_authenticated()
        response = self._restli_client.get(
            resource_path=self.USERINFO_RESOURCE,
            access_token=self.access_token,
        )
        return response.entity

    @staticmethod
    def escape_little_text(text: str) -> str:
        """Escape characters reserved by LinkedIn's 'little text' format.

        The Posts API uses the 'little text' format where certain characters
        (``\\``, ``"``, ``{}``, ``@``, ``[]``, ``()``, ``<>``, ``#``, ``*``,
        ``_``, ``~``) are reserved for syntax elements. If they appear in
        plain text without a backslash escape, LinkedIn's parser stops at the
        first unescaped occurrence, causing the post to appear truncated.

        Args:
            text: The raw post content (may contain unescaped special chars).

        Returns:
            The text with all reserved characters properly backslash-escaped.
        """
        return text.translate(LinkedInClient._LITTLE_TEXT_RESERVED)

    def set_access_token(self, token: str) -> None:
        """Set an existing access token (e.g., loaded from the database)."""
        self.access_token = token

    def _ensure_authenticated(self) -> None:
        """Raise an error if no access token is set."""
        if not self.access_token:
            raise RuntimeError(
                "Not authenticated. Call authenticate() or set_access_token() first."
            )

    def upload_image(self, image_path: str | Path) -> str:
        """Upload an image to LinkedIn and return its image URN.

        Uses the LinkedIn Images API (action: initializeUpload) to get an
        upload URL, then PUTs the image binary data to that URL.

        Args:
            image_path: Path to the local image file to upload.

        Returns:
            The image URN (e.g. ``urn:li:image:C...``) to use in a post.
        """
        self._ensure_authenticated()

        # Get the person ID if we don't have it yet
        if not self.person_id:
            user_info = self.get_user_info()
            self.person_id = user_info.get("sub")
            if not self.person_id:
                raise RuntimeError(
                    "Could not retrieve LinkedIn person ID from user info."
                )

        # Step 1: Register the image upload
        response = self._restli_client.action(
            resource_path=self.IMAGES_RESOURCE,
            action_name="initializeUpload",
            action_params={
                "initializeUploadRequest": {
                    "owner": f"urn:li:person:{self.person_id}",
                }
            },
            version_string=self.API_VERSION,
            access_token=self.access_token,
        )

        if response.status_code not in (200, 201):
            msg = f"HTTP {response.status_code}"
            raise RuntimeError(
                f"LinkedIn image upload init failed (status {response.status_code}): {msg}"
            )

        value = response.value or {}
        upload_url = value.get("uploadUrl")
        image_urn = value.get("image")

        if not upload_url or not image_urn:
            raise RuntimeError("LinkedIn did not return an upload URL or image URN.")

        # Step 2: Upload the image binary
        with open(image_path, "rb") as f:
            image_data = f.read()

        upload_response = requests.put(
            upload_url,
            data=image_data,
            headers={
                "Content-Type": "application/octet-stream",
                "Authorization": f"Bearer {self.access_token}",
            },
            timeout=30,
        )

        if upload_response.status_code not in (200, 201):
            raise RuntimeError(
                f"LinkedIn image binary upload failed "
                f"(status {upload_response.status_code})"
            )

        return image_urn

    def create_post(
        self,
        text: str,
        image_urn: str | None = None,
        lifecycle_state: str = "PUBLISHED",
    ) -> dict:
        """Create a post on LinkedIn using the official RestliClient.

        Uses the versioned /posts endpoint with the official client library,
        which handles headers (LinkedIn-Version, X-Restli-Protocol-Version, etc.)
        automatically.

        Args:
            text: The post content/commentary.
            image_urn: Optional image URN to attach to the post
                       (from ``upload_image()``).
            lifecycle_state: ``PUBLISHED`` (visible to everyone) or ``DRAFT``
                             (only the author can see it).

        Returns:
            A dict with ``post_id`` (the LinkedIn share URN),
            ``post_url`` (a link to view the post), and ``status_code``.
        """
        self._ensure_authenticated()

        # Get the person ID if we don't have it yet
        if not self.person_id:
            user_info = self.get_user_info()
            self.person_id = user_info.get("sub")
            if not self.person_id:
                raise RuntimeError(
                    "Could not retrieve LinkedIn person ID from user info."
                )

        # Escape LinkedIn "little text" reserved characters so the parser
        # doesn't stop at the first unescaped special character, which would
        # cause the post to appear truncated on LinkedIn.
        safe_text = self.escape_little_text(text)

        # Build the post entity
        entity: dict = {
            "author": f"urn:li:person:{self.person_id}",
            "lifecycleState": lifecycle_state,
            "visibility": "PUBLIC",
            "commentary": safe_text,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "isReshareDisabledByAuthor": False,
        }

        # Attach image if provided
        if image_urn:
            entity["content"] = {
                "media": {
                    "title": "Post image",
                    "id": image_urn,
                }
            }

        # Use the /posts endpoint with the versioned API.
        # The RestliClient does NOT raise on HTTP errors, so we check status manually.
        response = self._restli_client.create(
            resource_path=self.POSTS_RESOURCE,
            entity=entity,
            version_string=self.API_VERSION,
            access_token=self.access_token,
        )

        # The RestliClient does not raise on HTTP errors — it wraps the response.
        # Check the status code explicitly and raise if the post wasn't created.
        if response.status_code != 201:
            # Try to extract error info from the raw response
            error_body = ""
            try:
                error_body = response.response.text[:500]
            except Exception:
                pass
            raise RuntimeError(
                f"LinkedIn API error (status {response.status_code}): {error_body}"
            )

        post_id = response.decoded_entity_id or response.entity_id or ""
        # Construct a URL the user can visit
        post_url = f"https://www.linkedin.com/feed/update/{post_id}"

        return {
            "post_id": post_id,
            "post_url": post_url,
            "status_code": response.status_code,
        }
