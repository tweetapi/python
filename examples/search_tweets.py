from tweetapi import TweetAPI

client = TweetAPI(api_key="YOUR_API_KEY")

# Search for latest tweets about Bitcoin
results = client.explore.search(query="bitcoin", type="Latest")

print(f'Found {results["meta"]["resultCount"]} results in {results["meta"]["completedIn"]}ms\n')

for item in results["data"]:
    if "text" in item and "author" in item:
        author = item["author"]
        print(f'@{author["username"]}: {item["text"][:100]}')
        print(f'  ♥ {item["likeCount"]}  🔁 {item["retweetCount"]}  💬 {item["replyCount"]}\n')

# Paginate if more results exist
next_cursor = results["pagination"]["nextCursor"]
if next_cursor:
    print(f'More results available. Use cursor to paginate:')
    print(f'  cursor="{next_cursor}"')
