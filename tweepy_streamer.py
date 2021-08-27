from fetch_tweets import twitter_auth
import tweepy
from tweepy.streaming import StreamListener #listens to tweet based on certain keywords
from tweepy import OAuthHandler #reponsible for authenticating based on env variables which are associated with the twitter app
from tweepy import Stream 
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

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to the Twitter Streaming API.
        listener = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)    
        stream = Stream(auth, listener) #listener which handles the return, can be data or error
        stream.filter(track=hash_tag_list)
        

#this class will inherit from streamlistener class 
class StdOutListener(StreamListener):
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
        print(status)
        
        
if __name__ == "__main__":
    # can pass hash_tag list that corresponds to tweet in track=""
    # hash_tag_lisy = []
    match_doge = "(d|D)(o|O)(g|G)(e|E)" #regex to match doge word
    fetched_tweets_filename = "tweets.json" #return in json format
    
    # twitter streaner object
    twitter_streaner = TwitterStreamer()
    twitter_streaner.stream_tweets(fetched_tweets_filename, match_doge)
