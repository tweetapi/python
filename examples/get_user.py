from tweetapi import TweetAPI, NotFoundError, RateLimitError, TweetAPIError

client = TweetAPI(api_key="YOUR_API_KEY")

try:
    # Get a single user by username
    user = client.user.get_by_username(username="elonmusk")
    data = user["data"]
    print(f'{data["name"]} (@{data["username"]})')
    print(f'Followers: {data["followerCount"]:,}')
    print(f'Tweets: {data["tweetCount"]:,}')
    print(f'Verified: {data["isBlueVerified"]}')

    # Get first page of followers
    followers = client.user.get_followers(user_id=data["id"])
    print(f"\nFirst {len(followers['data'])} followers:")
    for follower in followers["data"][:5]:
        print(f'  - @{follower["username"]} ({follower["followerCount"]} followers)')

    # Paginate to next page
    next_cursor = followers["pagination"]["nextCursor"]
    if next_cursor:
        next_page = client.user.get_followers(user_id=data["id"], cursor=next_cursor)
        print(f"\nNext page: {len(next_page['data'])} more followers")

except NotFoundError:
    print("User not found")
except RateLimitError as e:
    print(f"Rate limited. Retry in {e.retry_after} seconds")
except TweetAPIError as e:
    print(f"API error [{e.code}]: {e.message}")
