import tweepy
from tweepy.streaming import StreamListener #listens to tweet based on certain keywords
from tweepy import OAuthHandler #reponsible for authenticating based on env variables which are associated with the twitter app
from tweepy import Stream, API, Cursor
import sys,os, re
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# global variables
consumer_key = os.environ.get("CONSUMER_KEY") 
consumer_secret = os.environ.get("CONSUMER_SECRET_KEY")
access_token = os.environ.get("ACCESS_TOKEN") 
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Twitter Client
class TwitterClient():
    
    def __init__(self, twitter_user=None):
        # authenticate to properly communicate with the Twitter API
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    
    # def get_specific_tweet(self, num_tweets):
    #     tweets = []
    #     for tweet in Cursor(self.twitter_client.seach_tweets(q="(d|D)(o|O)(g|G)(e|E)"), id=self.twitter_user).items(num_tweets):
    #         tweets.append(tweet)
    #     return tweets
        
    

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener) #listener which handles the return, can be data or error
        
        # This line filters Twitter Streams to capture data by keywords
        stream.filter(track=hash_tag_list)
        

#this class will inherit from streamlistener class 
class TwitterListener(StreamListener):
    """
    This is a basic listener class that just prints recieved tweets to stdout.
    """
    
    #constructor
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    #takes in data from streamListener
    def on_data(self, data): 
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
    
    # method that handles error
    def on_error(self, status):
        if status == 420:
            # returning False on data method in case rate limit occurs.
            return False
        print(status)
        
        
if __name__ == "__main__":
    # can pass hash_tag list that corresponds to tweet in track=""
    # hash_tag_lisy = []
    match_doge = "(d|D)(o|O)(g|G)(e|E)" #regex to match doge word
    fetched_tweets_filename = "tweets.json" #return in json format

    twitter_client = TwitterClient('elonmusk')
    print(twitter_client.get_specific_tweet(1))
    
    # twitter_streaner = TwitterStreamer()  
    # twitter_streaner.stream_tweets(fetched_tweets_filename, match_doge)
