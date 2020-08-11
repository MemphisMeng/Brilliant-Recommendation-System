import sys
import tweepy
from datetime import datetime, timedelta

# authorization tokens
consumer_key = "UK8cLFsq19FVMI50jbaRaHIpr"
consumer_secret = "v7czLcFmKFWkMtGoN8lOc6CmsIgZv0DaEr4KIHAGFHi5zB1TS5"
access_key = "1171257510889775106-qV1ZPtqfl1SpGC0Zcf5m8WUyqEs2Vx"
access_secret = "PJmS1lJ55jqeVtcVTJmVjWXO4rvQ8fUO4rouEPjyPRpUe"


# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",", "\n"]
        for c in remove_characters:
            text.replace(c, " ")
            quoted_text.replace(c, " ")

        with open("data/tweets.csv", "a", encoding='utf-8') as f:
            # collect the latest 24hrs' tweets
            if datetime.now() - status.created_at <= timedelta(seconds=1):
                f.write("%s,%s,%s,%s,%s,%s\n" % (
                    status.created_at, status.user.screen_name, is_retweet, is_quote, text, quoted_text))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    with open("data/tweets.csv", "w", encoding='utf-8') as f:
        f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
    tags = ["movie", "film", "actor", "actress", "director", "producer", "celebrity",
            "movies", "films", "actors", "actresses", "directors", "producers", "celebrities"]
    stream.filter(track=tags)
