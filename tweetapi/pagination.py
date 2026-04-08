"""Auto-pagination helpers for cursor-based paginated endpoints."""

from __future__ import annotations

from typing import Any, Callable, Generator, Optional


def paginate_pages(
    fetcher: Callable[[Optional[str]], dict[str, Any]],
    *,
    max_pages: Optional[int] = None,
) -> Generator[dict[str, Any], None, None]:
    """Yield each full page (response dict) from a paginated endpoint.

    Args:
        fetcher: A callable that takes an optional cursor string and returns
            a paginated response dict with ``data`` and ``pagination`` keys.
        max_pages: Stop after this many pages. ``None`` means fetch all.

    Example::

        for page in paginate_pages(
            lambda cursor: client.user.get_followers(user_id="123", cursor=cursor),
        ):
            print(f"Got {len(page['data'])} users")
    """
    cursor: Optional[str] = None
    count = 0

    while True:
        page = fetcher(cursor)
        yield page
        count += 1

        if max_pages is not None and count >= max_pages:
            break

        cursor = page.get("pagination", {}).get("nextCursor")
        if not cursor:
            break


def paginate(
    fetcher: Callable[[Optional[str]], dict[str, Any]],
    *,
    max_pages: Optional[int] = None,
) -> Generator[Any, None, None]:
    """Yield individual items from all pages of a paginated endpoint.

    Args:
        fetcher: A callable that takes an optional cursor string and returns
            a paginated response dict.
        max_pages: Stop after this many pages. ``None`` means fetch all.

    Example::

        for user in paginate(
            lambda cursor: client.user.get_followers(user_id="123", cursor=cursor),
            max_pages=5,
        ):
            print(user["username"])
    """
    for page in paginate_pages(fetcher, max_pages=max_pages):
        yield from page.get("data", [])
