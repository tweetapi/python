import time

from tweetapi import TweetAPI, TweetAPIError

client = TweetAPI(api_key="YOUR_API_KEY")

AUTH_TOKEN = "YOUR_AUTH_TOKEN"
PROXY = "host:port@user:pass"

try:
    # Upload the file once; the API waits up to 30 seconds for X to process it
    media = client.post.upload_media(
        auth_token=AUTH_TOKEN,
        proxy=PROXY,
        media={"url": "https://example.com/clip.mp4"},
    )["data"]
    print(f'Uploaded {media["type"]} {media["mediaId"]}: {media["state"]}')

    # A long video can still be processing. Each status check costs one unit.
    status = media
    while status["state"] in ("pending", "in_progress"):
        time.sleep(status["checkAfterSecs"] or 5)
        status = client.post.get_media_status(
            auth_token=AUTH_TOKEN,
            proxy=PROXY,
            media_id=media["mediaId"],
        )["data"]
        print(f'State: {status["state"]}')

    if status["state"] == "failed":
        print(f'X could not process the file: {status["error"]["message"]}')
    else:
        # Post it with the same auth token that uploaded it
        post = client.post.create_post_with_media(
            auth_token=AUTH_TOKEN,
            text="Posted with TweetAPI",
            media=[{"media_id": media["mediaId"]}],
            proxy=PROXY,
        )
        print(f'Tweet created: {post["data"]["metadata"]["tweet_id"]}')

except TweetAPIError as e:
    print(f"API error [{e.code}]: {e.message}")
