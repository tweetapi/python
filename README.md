# TweetAPI Python SDK

`tweetapi` is the Python SDK for [TweetAPI](https://tweetapi.com?utm_source=github&utm_medium=readme&utm_campaign=python-sdk). It provides methods for users, tweets, posts, profiles, interactions, lists, communities, Spaces, search, authentication, and direct messages.

## Install

```bash
pip install tweetapi
```

## Quick start

```python
from tweetapi import TweetAPI

client = TweetAPI(api_key="YOUR_API_KEY")

# Get a user profile
user = client.user.get_by_username(username="elonmusk")
print(user["data"]["followerCount"])

# Search tweets
results = client.explore.search(query="bitcoin", type="Latest")

# Get followers with pagination
followers = client.user.get_followers(user_id="123456")
next_page = client.user.get_followers(
    user_id="123456",
    cursor=followers["pagination"]["nextCursor"],
)
```

[Create an API key](https://tweetapi.com?utm_source=github&utm_medium=readme&utm_campaign=python-sdk) with 100 included requests. No credit card is required.

## SDK behavior

- Public methods have type annotations, and response models use `TypedDict`.
- The client retries rate limits, server errors, timeouts, and connection failures by default; username changes disable automatic retries because the mutation is non-idempotent.
- `paginate()` yields items from cursor-based responses; `paginate_pages()` yields full response pages.
- HTTP errors map to exception classes such as `RateLimitError` and `NotFoundError`.
- Timeouts can use one value or separate connect and read values.
- The package supports Python 3.9+ and depends on `requests`.

## API reference

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
| `client.tweet.get_retweets(tweet_id=...)` | Get users who retweeted |
| `client.tweet.get_quotes(tweet_id=...)` | Get quote tweets |
| `client.tweet.translate(tweet_id=..., dst_lang=...)` | Translate a tweet |

### Post

| Method | Description |
|--------|-------------|
| `client.post.create_post(auth_token=..., text=..., proxy=..., reply_option=...)` | Create a tweet |
| `client.post.create_post_quote(auth_token=..., text=..., attachment_url=..., proxy=..., reply_option=...)` | Quote tweet |
| `client.post.create_post_with_media(auth_token=..., text=..., media=..., proxy=..., reply_option=...)` | Tweet with media |
| `client.post.reply_post(auth_token=..., text=..., tweet_id=..., proxy=...)` | Reply to a tweet |
| `client.post.reply_post_with_media(...)` | Reply with media |
| `client.post.delete_post(auth_token=..., tweet_id=...)` | Delete a tweet |

### Profile

| Method | Description |
|--------|-------------|
| `client.profile.update(auth_token=..., name=..., bio=..., location=..., website=..., proxy=...)` | Update profile fields |
| `client.profile.avatar(auth_token=..., media=..., proxy=...)` | Update profile avatar |
| `client.profile.banner(auth_token=..., media=..., proxy=...)` | Update profile banner |
| `client.profile.remove_banner(auth_token=..., proxy=...)` | Remove the profile banner |
| `client.profile.set_privacy(auth_token=..., is_private=..., proxy=...)` | Make the account public or private |
| `client.profile.update_username(auth_token=..., password=..., username=..., proxy=...)` | Update the account username |

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
| `client.list.create(auth_token=..., name=..., description=..., is_private=...)` | Create a list |
| `client.list.add_member(auth_token=..., list_id=..., user_id=..., proxy=...)` | Add a member |
| `client.list.remove_member(auth_token=..., list_id=..., user_id=..., proxy=...)` | Remove a member |

### Community

| Method | Description |
|--------|-------------|
| `client.community.get_details(community_id=...)` | Get community details |
| `client.community.get_tweets(community_id=..., sort_by=...)` | Get community tweets |
| `client.community.get_members(community_id=...)` | Get members |
| `client.community.search(query=...)` | Search communities |
| `client.community.create_post(auth_token=..., text=..., community_id=..., proxy=...)` | Post in community |
| `client.community.create_post_with_media(...)` | Post with media |
| `client.community.create_quote(auth_token=..., text=..., attachment_url=..., community_id=..., proxy=...)` | Quote post in community |
| `client.community.create_quote_with_media(...)` | Quote post with media |
| `client.community.reply_post(...)` | Reply to community post |
| `client.community.reply_post_with_media(...)` | Reply with media |
| `client.community.join(auth_token=..., community_id=...)` | Join a community |
| `client.community.leave(auth_token=..., community_id=...)` | Leave a community |

### Space

| Method | Description |
|--------|-------------|
| `client.space.get_by_id(space_id=...)` | Get Space details |
| `client.space.get_stream_url(media_key=...)` | Get HLS stream URL |

### Explore

| Method | Description |
|--------|-------------|
| `client.explore.search(query=..., type=...)` | Search tweets, users, photos, or videos |

### Auth

| Method | Description |
|--------|-------------|
| `client.auth.login(username=..., password=..., proxy=..., country=...)` | Log in and return auth tokens |

`country` is the ISO 3166-1 alpha-2 code for the proxy's public egress IP (for example, `"US"`). It must match the IP used for the complete login attempt. Pass `two_factor_secret` when the account uses TOTP-based 2FA.

### X Chat (encrypted DMs)

| Method | Description |
|--------|-------------|
| `client.xchat.setup(auth_token=..., user_id=..., pin=...)` | Initialize encrypted DMs |
| `client.xchat.get_conversations(auth_token=...)` | List conversations |
| `client.xchat.send(auth_token=..., recipient_id=..., message=...)` | Send message |
| `client.xchat.get_history(auth_token=..., conversation_id=...)` | Get conversation history |
| `client.xchat.can_dm(auth_token=..., user_ids=...)` | Check DM availability |

### Unencrypted DMs

| Method | Description |
|--------|-------------|
| `client.dm.send_dm(auth_token=..., conversation_id=..., text=..., proxy=...)` | Send DM |
| `client.dm.get_dm_permissions(auth_token=..., recipient_ids=...)` | Check permissions |
| `client.dm.get_inbox_initial_state(auth_token=...)` | Get inbox state |
| `client.dm.get_inbox_trusted(auth_token=..., cursor=...)` | Get the trusted inbox |
| `client.dm.get_inbox_untrusted(auth_token=..., cursor=...)` | Get message requests |
| `client.dm.get_conversation(auth_token=..., conversation_id=...)` | Get messages |
| `client.dm.get_dm_user_updates(auth_token=..., cursor=...)` | Get DM user updates |
| `client.dm.accept_conversation(auth_token=..., conversation_id=...)` | Accept a conversation request |

## Posting and profile media

Tweet media accepts an existing TweetAPI media ID, a URL, or inline base64 data:

```python
client.post.create_post_with_media(
    auth_token="AUTH_TOKEN",
    text="Launch update",
    media=[{"media_id": "1971008286821380096"}],
    proxy="host:port:user:pass",
)
```

Use `reply_option` to set reply controls when creating standard, quote, or media posts:

```python
client.post.create_post(
    auth_token="AUTH_TOKEN",
    text="Followers can reply",
    proxy="host:port:user:pass",
    reply_option={"mode": "followers"},
)
```

Profile avatar and banner uploads accept a URL or inline `data` plus `type`:

```python
client.profile.update(auth_token="AUTH_TOKEN", name="New Name", bio="Builder")
client.profile.avatar(
    auth_token="AUTH_TOKEN",
    media={"url": "https://example.com/avatar.jpg"},
)
client.profile.banner(
    auth_token="AUTH_TOKEN",
    media={"data": "BASE64_IMAGE_DATA", "type": "image/png"},
)
client.profile.remove_banner(auth_token="AUTH_TOKEN")
client.profile.set_privacy(auth_token="AUTH_TOKEN", is_private=True)
client.profile.update_username(
    auth_token="AUTH_TOKEN",
    password="ACCOUNT_PASSWORD",
    username="NEW_USERNAME",
)
```

Use `client.list` for list mutations. The older helpers under `client.interaction` remain available:

```python
created = client.list.create(
    auth_token="AUTH_TOKEN",
    name="Research",
    description="Accounts to watch",
    is_private=True,
)
client.list.add_member(auth_token="AUTH_TOKEN", list_id=created["data"]["id"], user_id="123")
client.list.remove_member(auth_token="AUTH_TOKEN", list_id=created["data"]["id"], user_id="123")
```

Community quote posts support the same URL and media attachment shapes:

```python
client.community.create_quote(
    auth_token="AUTH_TOKEN",
    text="Useful context",
    attachment_url="https://x.com/user/status/123",
    community_id="987",
    proxy="host:port:user:pass",
)
client.community.create_quote_with_media(
    auth_token="AUTH_TOKEN",
    text="Useful context",
    attachment_url="https://x.com/user/status/123",
    community_id="987",
    media=[{"media_id": "1971008286821380096"}],
    proxy="host:port:user:pass",
)
```

## Pagination

`paginate()` yields individual items. `paginate_pages()` yields each full response page:

```python
from tweetapi import TweetAPI, paginate, paginate_pages

client = TweetAPI(api_key="YOUR_API_KEY")

# Iterate individual items across all pages
for user in paginate(
    lambda cursor: client.user.get_followers(user_id="123456", cursor=cursor),
):
    print(user["username"])

# Iterate full pages (access page-level data)
for page in paginate_pages(
    lambda cursor: client.explore.search(query="bitcoin", type="Latest", cursor=cursor),
    max_pages=5,  # optional: limit number of pages
):
    print(f"Got {len(page['data'])} results")
    print(f"Next cursor: {page['pagination']['nextCursor']}")
```

Each helper accepts a callable that takes a cursor and returns a response with `data` and `pagination.nextCursor`. Use `max_pages` to limit the number of fetched pages.

## Retries

The client retries these transient failures:

- For a 429 response, it waits for `RateLimitError.retry_after` seconds, up to `max_retry_delay`.
- For a 5xx response, timeout, or connection failure, it uses exponential backoff with up to 25% jitter.

By default, the client makes up to 3 retries. Its base delay starts at 1 second, doubles after each attempt, and is capped at 30 seconds. Other 4xx responses are not retried.

```python
# Customize retry behavior
client = TweetAPI(
    api_key="YOUR_API_KEY",
    max_retries=5,             # default: 3
    initial_retry_delay=2.0,   # default: 1.0 (seconds)
    backoff_multiplier=3.0,    # default: 2.0
    max_retry_delay=60.0,      # default: 30.0 (seconds)
)

# Disable retries entirely
client = TweetAPI(api_key="YOUR_API_KEY", max_retries=0)
```

### Rate-limit state

After a 429 response, `client.rate_limit_info` records the retry delay and the time the response was received:

```python
print(client.rate_limit_info)
```

## Error handling

The client raises retryable errors after it exhausts the configured retries. It raises other errors from the first response:

```python
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
    print(f"Rate limited. Retry in {e.retry_after}s")
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
    print(f"Error [{e.code}]: {e.message}")
```

Every error includes these attributes:

- `code`: API error code, such as `"ACCOUNT_SUSPENDED"` or `"RATE_LIMIT"`
- `status_code`: HTTP status code
- `message`: human-readable error message
- `details`: response context such as a field, reason, or retry delay

## Configuration

```python
client = TweetAPI(
    api_key="YOUR_API_KEY",           # Required
    base_url="https://...",           # Optional (default: https://api.tweetapi.com)
    timeout=30,                       # Optional; one value for connect and read
    connect_timeout=10.0,             # Optional (default: 10s)
    read_timeout=30.0,                # Optional (default: 30s)
    max_retries=3,                    # Optional (default: 3, set 0 to disable)
    backoff_multiplier=2.0,           # Optional (default: 2.0)
    initial_retry_delay=1.0,          # Optional (default: 1.0s)
    max_retry_delay=30.0,             # Optional (default: 30.0s)
)

# You can also pass a tuple for timeout
client = TweetAPI(api_key="YOUR_API_KEY", timeout=(5, 30))  # (connect, read)
```

## Requirements

- Python 3.9+
- `requests` library

## Links

- [Documentation](https://tweetapi.com/docs?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)
- [Create an API key](https://tweetapi.com?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)
- [Dashboard](https://tweetapi.com/dashboard?utm_source=github&utm_medium=readme&utm_campaign=python-sdk)
- [Node.js SDK](https://github.com/tweetapi/node)

## License

MIT

TweetAPI is a third-party service and is not affiliated with X Corp.
