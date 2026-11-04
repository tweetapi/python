from tweetapi import TweetAPI

client = TweetAPI(api_key="YOUR_API_KEY")

# Search for latest tweets about Bitcoin
results = client.explore.search(query="bitcoin", type="Latest")

print(f'Found {len(results["data"])} tweets\n')

for tweet in results["data"]:
    author = tweet["author"]
    print(f'@{author["username"]}: {tweet["text"][:100]}')
    print(f'  ♥ {tweet["likeCount"]}  🔁 {tweet["retweetCount"]}  💬 {tweet["replyCount"]}\n')

# Paginate if more results exist
next_cursor = results["pagination"]["nextCursor"]
if next_cursor:
    print(f'More results available. Use cursor to paginate:')
    print(f'  cursor="{next_cursor}"')
