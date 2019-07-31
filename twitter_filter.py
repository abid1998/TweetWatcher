import json
import tweepy
from textblob import TextBlob as TB
from tweet_store import TweetStore
import datetime

config_path = 'config/config.json'

store = TweetStore()

with open(config_path) as f:
    twitter_api = json.loads(f.read())

consumer_key = twitter_api['consumer_key']
consumer_secret_key = twitter_api['consumer_secret_key']
access_token = twitter_api['access_token']
access_token_secret = twitter_api['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class Listener(tweepy.StreamListener):

    def on_status(self, status):

        if('RT @' not in status.text):
            blob = TB(status.text)
            sent = blob.sentiment
            polarity = blob.polarity
            subjectivity = sent.subjectivity

            tweet_item = {
                'id_str': status.id_str,
                'text': status.text,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                'recieved_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            store.push(tweet_item)
            print(tweet_item)

    def on_error(self, status_code):
        if(status_code == 420):
            return False


stream_listener = Listener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["@Reebok", "@adidas", "@Nike"])
