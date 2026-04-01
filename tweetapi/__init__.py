"""TweetAPI Python SDK — Official client for the Twitter/X Data API.

Usage::

    from tweetapi import TweetAPI

    client = TweetAPI(api_key="YOUR_API_KEY")

    user = client.user.get_by_username(username="elonmusk")
    print(user["data"]["followerCount"])
"""

from .client import TweetAPI
from .errors import (
    TweetAPIError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    ConnectionError_ as NetworkError,
)

__all__ = [
    "TweetAPI",
    "TweetAPIError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]

__version__ = "1.0.0"
