# TweetAPI Python SDK

Official Python SDK for [TweetAPI](https://tweetapi.com?utm_source=github&utm_medium=readme&utm_campaign=python-sdk) — the Twitter/X Data API for developers and researchers.

Access tweets, user profiles, followers, analytics, and full interaction capabilities. 70+ endpoints with built-in error handling and type hints.

## Install

```bash
pip install tweetapi
```

## Quick Start

```python
from tweetapi import TweetAPI

client = TweetAPI(api_key="YOUR_API_KEY")

# Get a user profile
user = client.user.get_by_username(username="elonmusk")
print(user["data"]["followerCount"])  # 180000000

# Search tweets
results = client.explore.search(query="bitcoin", type="Latest")

# Get followers with pagination
followers = client.user.get_followers(user_id="123456")
next_page = client.user.get_followers(
    user_id="123456",
    cursor=followers["pagination"]["nextCursor"],
)
```

> **Get your free API key** — [100 requests, no credit card required](https://tweetapi.com?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)

## Features

- **70+ endpoints** covering users, tweets, posts, interactions, DMs, communities, spaces, and search
- **Full type hints** with TypedDict definitions for IDE autocomplete
- **Solid error handling** with typed exceptions (`RateLimitError`, `NotFoundError`, etc.)
- **Single dependency** — `requests` only
- **Pagination support** with cursor-based navigation
- **Python 3.9+** compatible

## API Reference

### User

| Method | Description |
|--------|-------------|
| `client.user.get_by_username(username=...)` | Get user profile by username |
| `client.user.get_by_usernames(usernames=...)` | Get multiple users (comma-separated) |
| `client.user.get_by_user_id(user_id=...)` | Get user profile by ID |
| `client.user.get_by_user_ids(user_ids=...)` | Get multiple users by IDs |
| `client.user.get_tweets(user_id=...)` | Get a user's tweets |
| `client.user.get_tweets_and_replies(user_id=...)` | Get tweets and replies |
| `client.user.get_following(user_id=...)` | Get who a user follows |
| `client.user.get_followers(user_id=...)` | Get a user's followers |
| `client.user.get_verified_followers(user_id=...)` | Get verified followers |
| `client.user.get_subscriptions(user_id=...)` | Get subscriptions |
| `client.user.get_following_v1(user_id=...)` | Get following (v1, supports count) |
| `client.user.get_followers_v1(user_id=...)` | Get followers (v1, supports count) |
| `client.user.get_following_ids(user_id=...)` | Get following user IDs |
| `client.user.get_followers_ids(user_id=...)` | Get follower user IDs |
| `client.user.check_follow(subject_id=..., target_id=...)` | Check follow relationship |
| `client.user.about_account(username=...)` | Get account transparency info |

### Tweet

| Method | Description |
|--------|-------------|
| `client.tweet.get_details_and_conversation(tweet_id=...)` | Get tweet details and replies |
| `client.tweet.get_details_by_ids(ids=...)` | Get multiple tweets (max 200) |
| `client.tweet.get_retweets(tweet_id=...)` | Get who retweeted |
| `client.tweet.get_quotes(tweet_id=...)` | Get quote tweets |
| `client.tweet.translate(tweet_id=..., dst_lang=...)` | Translate a tweet |

### Post

| Method | Description |
|--------|-------------|
| `client.post.create_post(auth_token=..., text=..., proxy=...)` | Create a tweet |
| `client.post.create_post_quote(auth_token=..., text=..., attachment_url=..., proxy=...)` | Quote tweet |
| `client.post.create_post_with_media(auth_token=..., text=..., media=..., proxy=...)` | Tweet with media |
| `client.post.reply_post(auth_token=..., text=..., tweet_id=..., proxy=...)` | Reply to a tweet |
| `client.post.reply_post_with_media(...)` | Reply with media |
| `client.post.delete_post(auth_token=..., tweet_id=...)` | Delete a tweet |

### Interaction

| Method | Description |
|--------|-------------|
| `client.interaction.favorite_post(auth_token=..., tweet_id=...)` | Like a tweet |
| `client.interaction.unfavorite_post(auth_token=..., tweet_id=...)` | Unlike a tweet |
| `client.interaction.retweet(auth_token=..., tweet_id=...)` | Retweet |
| `client.interaction.delete_retweet(auth_token=..., tweet_id=...)` | Remove retweet |
| `client.interaction.bookmark(auth_token=..., tweet_id=...)` | Bookmark a tweet |
| `client.interaction.delete_bookmark(auth_token=..., tweet_id=...)` | Remove bookmark |
| `client.interaction.follow(auth_token=..., user_id=...)` | Follow a user |
| `client.interaction.unfollow(auth_token=..., user_id=...)` | Unfollow a user |
| `client.interaction.add_member_to_list(auth_token=..., list_id=..., user_id=...)` | Add to list |
| `client.interaction.remove_member_from_list(auth_token=..., list_id=..., user_id=...)` | Remove from list |
| `client.interaction.get_notifications(auth_token=...)` | Get notifications |
| `client.interaction.get_user_analytics(auth_token=...)` | Get analytics |

### List

| Method | Description |
|--------|-------------|
| `client.list.get_details(list_id=...)` | Get list details |
| `client.list.get_tweets(list_id=...)` | Get tweets in a list |
| `client.list.get_members(list_id=...)` | Get list members |
| `client.list.get_followers(list_id=...)` | Get list followers |

### Community

| Method | Description |
|--------|-------------|
| `client.community.get_details(community_id=...)` | Get community details |
| `client.community.get_tweets(community_id=..., sort_by=...)` | Get community tweets |
| `client.community.get_members(community_id=...)` | Get members |
| `client.community.search(query=...)` | Search communities |
| `client.community.create_post(auth_token=..., text=..., community_id=..., proxy=...)` | Post in community |
| `client.community.create_post_with_media(...)` | Post with media |
| `client.community.reply_post(...)` | Reply to community post |
| `client.community.reply_post_with_media(...)` | Reply with media |
| `client.community.join(auth_token=..., community_id=...)` | Join |
| `client.community.leave(auth_token=..., community_id=...)` | Leave |

### Space

| Method | Description |
|--------|-------------|
| `client.space.get_by_id(space_id=...)` | Get Space details |
| `client.space.get_stream_url(media_key=...)` | Get HLS stream URL |

### Explore

| Method | Description |
|--------|-------------|
| `client.explore.search(query=..., type=...)` | Search tweets/users/photos/videos |

### Auth

| Method | Description |
|--------|-------------|
| `client.auth.login(username=..., password=..., proxy=...)` | Log in, get auth tokens |

### X Chat (Encrypted DMs)

| Method | Description |
|--------|-------------|
| `client.xchat.setup(auth_token=..., user_id=..., pin=...)` | Initialize encrypted DMs |
| `client.xchat.get_conversations(auth_token=...)` | List conversations |
| `client.xchat.send(auth_token=..., recipient_id=..., message=...)` | Send message |
| `client.xchat.get_history(auth_token=..., conversation_id=...)` | Get history |
| `client.xchat.can_dm(auth_token=..., user_ids=...)` | Check DM availability |

### Unencrypted DMs

| Method | Description |
|--------|-------------|
| `client.dm.send_dm(auth_token=..., conversation_id=..., text=..., proxy=...)` | Send DM |
| `client.dm.get_dm_permissions(auth_token=..., recipient_ids=...)` | Check permissions |
| `client.dm.get_inbox_initial_state(auth_token=...)` | Get inbox state |
| `client.dm.get_inbox_trusted(auth_token=..., cursor=...)` | Trusted inbox |
| `client.dm.get_inbox_untrusted(auth_token=..., cursor=...)` | Message requests |
| `client.dm.get_conversation(auth_token=..., conversation_id=...)` | Get messages |
| `client.dm.get_dm_user_updates(auth_token=..., cursor=...)` | DM user updates |
| `client.dm.accept_conversation(auth_token=..., conversation_id=...)` | Accept request |

## Error Handling

The SDK throws typed exceptions you can catch and handle:

```python
import time
from tweetapi import (
    TweetAPI,
    TweetAPIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    ServerError,
    NetworkError,
)

client = TweetAPI(api_key="YOUR_API_KEY")

try:
    user = client.user.get_by_username(username="elonmusk")
except RateLimitError as e:
    # Wait and retry
    print(f"Rate limited. Retry in {e.retry_after}s")
    time.sleep(e.retry_after)
except NotFoundError:
    print("User not found")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Bad request: {e.message}")
except ServerError:
    print("API is having issues, try again later")
except NetworkError:
    print("Network error — check your connection")
except TweetAPIError as e:
    # Catch-all for any other API error
    print(f"Error [{e.code}]: {e.message}")
```

Every error includes:
- `code` — API error code (e.g., `"ACCOUNT_SUSPENDED"`, `"RATE_LIMIT"`)
- `status_code` — HTTP status code
- `message` — Human-readable error message
- `details` — Additional context (field, reason, retry_after, etc.)

## Configuration

```python
client = TweetAPI(
    api_key="YOUR_API_KEY",           # Required
    base_url="https://...",           # Optional (default: https://api.tweetapi.com)
    timeout=30,                       # Optional (default: 30 seconds)
)
```

## Requirements

- Python 3.9+
- `requests` library

## Links

- [Full Documentation](https://tweetapi.com/docs?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)
- [Get API Key (Free)](https://tweetapi.com?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)
- [Dashboard](https://tweetapi.com/dashboard?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)
- [Node.js SDK](https://github.com/tweetapi/tweetapi-node)

## License

MIT

---

*TweetAPI is a third-party service and is not affiliated with X Corp.*
