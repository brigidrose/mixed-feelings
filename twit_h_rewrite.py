import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os
import json


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

            # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query, count = 10):
            '''
            Main function to fetch tweets and parse them.
            '''
            # empty list to store parsed tweets
            #tweets = []
            fetched_tweets = self.api.search(q = query, count = count)

            for tweet in fetched_tweets:
                print tweet
            return

def main():

    api = TwitterClient()

    tweets = api.get_tweets(query = "grumpy", count = 30)

    print tweets

if __name__ == "__main__":
    main()

            # try:
            #     # call twitter api to fetch tweets
            #     fetched_tweets = self.api.search(q = query, count = count)
            #     print fetched_tweets

            # except tweepy.TweepError as e:
            #     # print error (if any)
            #     print("Error : " + str(e))