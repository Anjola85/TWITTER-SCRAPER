import sys,tweepy, os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#authentication function
def twitter_auth():
    try:
        consumer_key = os.environ.get("API_KEY") 
        consumer_secret = os.environ.get("API_SECRET_KEY") 
        access_token = os.environ.get("ACCESS_TOKEN") 
        access_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    except KeyError:
        sys.stderr.write("TWITTER_* environment variable not set\n")
        sys.exit(1)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

#authenticate twitter client
def get_twitter_client():
    auth = twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client

if __name__ == '__main__':
    user = input("Enter username: ")
    client = get_twitter_client()
    for status in tweepy.Cursor(client.user_timeline, screen_name=user).items(3):
        print(status.text)