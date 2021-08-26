import sys,tweepy

#authentication function
def twitter_auth():
    try:
        consumer_key = 'elhI4v5ChCqMHLwRcHOKMpu1s' #api_key
        consumer_secret = "v5LbwgCcjRSE0s5DBsvGwAVZegIvX9VtL66q5DctnCOzxKcgHb"  #api_secret_key
        access_token = "912250283383717888-QMnFLZfNzDTo0s2ZM9JqZIB7vXA6bvt" 
        access_secret = "yUaiCGXVr4jCsiYhsS7qG0E3ByxrjtlFS8fiU2oS9TpVK"
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