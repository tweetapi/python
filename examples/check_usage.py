from tweetapi import TweetAPI, TweetAPIError

client = TweetAPI(api_key="YOUR_API_KEY")

try:
    # Costs no units; it only counts toward the per-minute rate limit
    usage = client.account.get_usage()["data"]
    print(f'Units available: {usage["availableUnits"]:,}')

    plan = usage["plan"]
    if plan:
        resets = f', resets {plan["periodEnd"]}' if plan["periodEnd"] else ""
        print(f'Plan: {plan["usedUnits"]:,} of {plan["requestLimit"]:,} used{resets}')

    payg = usage["payg"]
    if payg:
        expires = f', expire {payg["expiresAt"]}' if payg["expiresAt"] else ""
        print(f'PAYG: {payg["availableUnits"]:,} units{expires}')

    print(f'Rate limit: {usage["rateLimit"]["requestsPerMinute"]} requests per minute')

except TweetAPIError as e:
    print(f"API error [{e.code}]: {e.message}")
