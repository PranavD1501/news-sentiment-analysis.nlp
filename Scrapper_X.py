import tweepy
import pandas as pd
from datetime import datetime
import time

bearer_token = "AAAAAAAAAAAAAAAAAAAAAPN42gEAAAAA7XoaHb0kZrM2Pq3hyR%2BgBHVNqBU%3DvPnJD6L6HhkQKJOoC2BUZgTpcn2gHrBOoiSc0ldOhTtjdudmCe" 
client = tweepy.Client(bearer_token=bearer_token,wait_on_rate_limit=True)

assets = ["AAPL", "TSLA"]

def scrape_x_posts(asset, max_results=10):
    query = f"{asset} -is:retweet"  

    try:
        tweets = client.search_recent_tweets(
            query=query,
            tweet_fields=["created_at", "text"],  
            max_results=max_results
        )

        data = [
            {
                "asset": asset,
                "text": tweet.text,
                "timestamp": tweet.created_at.strftime("%Y-%m-%d")
            }
            for tweet in (tweets.data or [])
        ]

        return data
    
    except tweepy.TooManyRequests as e:
        print(f"Rate limit hit while scrapping {asset}")
        time.sleep(900)
        return scrape_x_posts(asset,max_results)

    except Exception as e:
        print(f"Error scraping {asset} : {e}")
        return []

alldata = []

for asset in assets:
    print(f"Scrapping for {asset}")
    data = scrape_x_posts(asset, max_results=10)
    alldata.extend(data)
    time.sleep(5)

df = pd.DataFrame(alldata)

if not df.empty:
    df.to_csv("x_data.csv", index=False)
    print("Saved data to csv")
else:
    print("No data Scrapped")

print(df.head())
