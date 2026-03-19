#!/usr/bin/env bash
# test_api.sh – smoke-test every endpoint with httpie
#
# Prerequisites:
#   pip install httpie   (or: uv tool install httpie)
#   uv run uvicorn main:app   ← running in another terminal
#
# Usage:
#   chmod +x test_api.sh && ./test_api.sh

set -euo pipefail

BASE="http://127.0.0.1:8000"
SEP="─────────────────────────────────────────"

ok()  { echo ""; echo "▶ $*"; }
sep() { echo "$SEP"; }

# ─────────────────────────────────────────────────────────────────────────────
# AUTHORS
# ─────────────────────────────────────────────────────────────────────────────

sep
ok "LIST authors (page 1, 5 per page)"
http GET "$BASE/authors/" page==1 page_size==5

sep
ok "LIST authors (page 2)"
http GET "$BASE/authors/" page==2 page_size==5

sep
ok "GET single author (id=1)"
http GET "$BASE/authors/1"

sep
ok "GET author that does not exist → 404"
http --ignore-stdin GET "$BASE/authors/99999" || true

sep
ok "CREATE author"
AUTHOR=$(http --ignore-stdin POST "$BASE/authors/" \
    name="Virginia Woolf" \
    bio="English modernist author and essayist.")
echo "$AUTHOR"
AUTHOR_ID=$(echo "$AUTHOR" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "  → created author id=$AUTHOR_ID"

sep
ok "UPDATE author (PATCH)"
http --ignore-stdin PATCH "$BASE/authors/$AUTHOR_ID" \
    bio="English novelist, essayist, and publisher."

sep
ok "GET updated author"
http GET "$BASE/authors/$AUTHOR_ID"

sep
ok "CREATE author WITH BOOKS (atomic transaction)"
http --ignore-stdin POST "$BASE/authors/with-books" \
    name="Italo Calvino" \
    bio="Italian journalist and writer of fantasy and science fiction." \
    books:='[
        {"title": "Invisible Cities",      "year": 1972},
        {"title": "If on a winters night", "year": 1979},
        {"title": "Cosmicomics",           "year": 1965}
    ]'

# ─────────────────────────────────────────────────────────────────────────────
# BOOKS
# ─────────────────────────────────────────────────────────────────────────────

sep
ok "LIST books (page 1, 10 per page)"
http GET "$BASE/books/" page==1 page_size==10

sep
ok "LIST books (last page)"
http GET "$BASE/books/" page==10 page_size==10

sep
ok "GET single book (id=1)"
http GET "$BASE/books/1"

sep
ok "GET book that does not exist → 404"
http --ignore-stdin GET "$BASE/books/99999" || true

sep
ok "CREATE book (linked to author id=$AUTHOR_ID)"
BOOK=$(http --ignore-stdin POST "$BASE/books/" \
    title="Mrs Dalloway" \
    year:=1925 \
    author_id:="$AUTHOR_ID")
echo "$BOOK"
BOOK_ID=$(echo "$BOOK" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "  → created book id=$BOOK_ID"

sep
ok "CREATE book with non-existent author → 400"
http --ignore-stdin POST "$BASE/books/" \
    title="Ghost Book" \
    author_id:=99999 || true

sep
ok "UPDATE book (PATCH)"
http --ignore-stdin PATCH "$BASE/books/$BOOK_ID" \
    title="Mrs Dalloway (revised edition)" \
    year:=1926

sep
ok "GET updated book"
http GET "$BASE/books/$BOOK_ID"

sep
ok "DELETE book"
http --ignore-stdin DELETE "$BASE/books/$BOOK_ID" && echo "  → 204 No Content"

sep
ok "GET deleted book → 404"
http --ignore-stdin GET "$BASE/books/$BOOK_ID" || true

sep
ok "DELETE author (cascades to books)"
http --ignore-stdin DELETE "$BASE/authors/$AUTHOR_ID" && echo "  → 204 No Content"

sep
ok "GET deleted author → 404"
http --ignore-stdin GET "$BASE/authors/$AUTHOR_ID" || true

sep
echo ""
echo "✓ All tests finished."
