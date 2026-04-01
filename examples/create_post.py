from tweetapi import TweetAPI, AuthenticationError, TweetAPIError

client = TweetAPI(api_key="YOUR_API_KEY")

try:
    # First, log in to get an auth token
    login_result = client.auth.login(
        username="your_twitter_username",
        password="your_twitter_password",
        proxy="hostname:port@username:password",
    )

    auth_token = login_result["data"]["cookies"]["auth_token"]
    print(f'Logged in as @{login_result["data"]["user"]["username"]}')

    # Create a tweet
    post = client.post.create_post(
        auth_token=auth_token,
        text="Hello from TweetAPI! 🚀",
        proxy="hostname:port@username:password",
    )

    print(f'Tweet created: {post["data"]["metadata"]["tweet_id"]}')
    print(f'URL: {post["data"]["metadata"]["url"]}')

    # Like the tweet we just created
    client.interaction.favorite_post(
        auth_token=auth_token,
        tweet_id=post["data"]["id"],
        proxy="hostname:port@username:password",
    )
    print("Liked the tweet!")

except AuthenticationError:
    print("Authentication failed. Check your credentials.")
except TweetAPIError as e:
    print(f"API error [{e.code}]: {e.message}")
