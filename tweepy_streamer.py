from tweepy.streaming import StreamListener #listens to tweet based on certain keywords
from tweepy import OAuthHandler #reponsible for authenticating based on env variables which are associated with the twitter app
from tweepy import Stream 
import sys,os, re
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class TwitterStreamer():
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        pass
        # This handles Twitter authentication and the connection to the Twitter Streaming API
    

#this class will inherit from streamlistener class 
class StdOutListener(StreamListener):
    
    #takes in data from streamListener
    def on_data(self, data): 
        print(data)
        return True
    
    # method that handles error
    def on_error(self, status):
        print(status)
        
        
if __name__ == "__main__":
    
    #listener object
    listener = StdOutListener()
    
    #authenticate app
    consumer_key = os.environ.get("CONSUMER_KEY") 
    consumer_secret = os.environ.get("CONSUMER_SECRET_KEY")
    access_token = os.environ.get("ACCESS_TOKEN") 
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    print(consumer_key, consumer_secret, access_token, access_token_secret)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    #creating twitter stream
    #Stream takes in two parameters
    #auth - which authenticates the user
    #listener which handles the return, can be data or error
    stream = Stream(auth, listener)
    
    #regex to match doge word
    match_doge = "(d|D)(o|O)(g|G)(e|E)"
    
    #return tweets focused on keyword "doge"
    stream.filter(track=match_doge)
    