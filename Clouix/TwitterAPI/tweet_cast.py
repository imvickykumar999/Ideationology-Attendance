
def funaid():
    import tweepy, os
    import pandas as pd

    CONSUMER_KEY = "U6n6m0C9A9qp00z6HrhCLESVI"
    CONSUMER_SECRET = "1YpllSaRsRLpgHNSYWPdJTHN81U5Kt2LrlgSy7vCIdBYXz39Cu"
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    ACCESS_TOKEN = "1487141902294081536-ZUVADsDhQoYB7dg3VpVfmZ7KVkxAGm"
    ACCESS_TOKEN_SECRET = "YtdPzPSSzRlVq5qQKmCAkMNl4w9HfwutnW58BjvyNY6gq"
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    API = tweepy.API(auth)
    try:
        API.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    aid = []
    for i in API.home_timeline(count=50):
        aid.append('https://twitter.com/i/status/' + str(i.id))

    return aid