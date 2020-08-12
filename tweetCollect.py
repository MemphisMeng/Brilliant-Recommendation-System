from tweepy import OAuthHandler
import tweepy
import pandas as pd

# authorization tokens
consumer_key = "UK8cLFsq19FVMI50jbaRaHIpr"
consumer_secret = "v7czLcFmKFWkMtGoN8lOc6CmsIgZv0DaEr4KIHAGFHi5zB1TS5"
access_key = "1171257510889775106-qV1ZPtqfl1SpGC0Zcf5m8WUyqEs2Vx"
access_secret = "PJmS1lJ55jqeVtcVTJmVjWXO4rvQ8fUO4rouEPjyPRpUe"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# The Twitter user who we want to get tweets from
# These are the most popular accounts on twitter which focus on movies
names = ["flavorpill", "alisonwillmore", "akstanwyck", "erikdavis", "eug", "karinalongworth", "melsil", "NikkiFinke",
         "slashfilm", "petertravers", "ebertchicago"]
# Number of tweets to pull
tweetCount = 200
tweets = []


def scrape():
    # Calling the user_timeline function with our parameters

    for name in names:
        results = api.user_timeline(id=name, count=tweetCount)
        for tweet in results:
            # foreach through all tweets pulled
            # print(tweet)
            tweets.append(tweet.text)

    tweet_df = pd.DataFrame({'tweets': tweets})
    return tweet_df
