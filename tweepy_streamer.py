"""
TWITTER SCRAPER
"""
import tweepy
from tweepy.streaming import StreamListener #listens to tweet based on certain keywords
from tweepy import OAuthHandler #reponsible for authenticating based on env variables which are associated with the twitter app
from tweepy import Stream, API, Cursor
import sys,os, re
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# import twitter credentials
import pandas as pd
import numpy as np

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
        
    def get_twitter_client_api(self):
        return self.twitter_client #returns Twittter API

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
        

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    
    # Default constructor
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    
    """
    Returns every stream of tweet by twitter users.
    @param Takes in two parameters
    @fetched_tweets_filename: what format should be returned by the function.
    @hash_tag_list: format tweet content should match.
    """
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener) #listener which handles the return, can be data or errorå
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
        
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def tweets_to_data_frame(self, tweets):
        # creating a data frame based on specified tweet content
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        #vice vers but id
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets]) #device that sent tweet
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df
        
if __name__ == "__main__":
    
    twitter_client = TwitterClient();
    tweet_analyzer = TweetAnalyzer()
    
    api = twitter_client.get_twitter_client_api()    
    
    tweets = api.user_timeline(screen_name = "elonmusk", count=20)
    
    # print(dir(tweets[0]))
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(10)) 