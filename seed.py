
import datetime
from sqlalchemy import func
import random

from model import User, Result, Tweet, Picture, connect_to_db, db
from server import app

from faker import Faker
from flickr_handler import flickrClient
from twitter_handler import TwitterClient

fake = Faker()
fApi = flickrClient()
tApi = TwitterClient()

feels = ['happy', 'sad', 'angry', 'sleepy', 'upset', 'excited', 'scared', 'anxious',
        'intrepid', 'goofy', 'grumpy', 'dumbfounded', 'tremendous', 'spectacular',
        'depressed', 'low', 'itchy', 'smelly', 'irrational']

# def load_users():

#     print "Users"

#     for stuff in range (0,50):
#         email = str(fake.email())
#         password = str(fake.password())
#         user = User(email=email,
#                 password=password)
#         db.session.add(user)

#     db.session.commit()

# def load_pictures():
    
#     for stuff in range (0,50):
#         new_feeling = random.choice(feels)
#         print new_feeling
#         photos = fApi.get_photos(new_feeling)
#         pic = Picture(flickr_url=photos)
#         db.session.add(pic)
    
#     db.session.commit()

# def load_tweets():

#     i = 0

#     while i < 50:
#         new_feeling = random.choice(feels)
#         print new_feeling
#         get_tweets = tApi.get_tweets(query=new_feeling, count=10)
#         print get_tweets
#         try:
#             tweet = random.choice(get_tweets)['text']
#         except IndexError:
#             continue

#         query = Tweet.query.filter_by(tweet_text=tweet).first()

#         if query == None:
#             tweet_text = Tweet(tweet_text=tweet)
#             db.session.add(tweet_text)
#             i = i+1
#         else:
#             continue

#     db.session.commit()

def load_results():


    #user_id
    for stuff in range(0,3):
        user_id = (random.choice(User.query.all())).user_id
        tweet_id = (random.choice(Tweet.query.all())).tweet_id
        pic_id = (random.choice(Picture.query.all())).flickr_id
        date = fake.date()
        keyword = random.choice(feels)
        block = str(fake.text())
        lat = int(fake.latitude())
        lng = int(fake.longitude())
        print "u-id:", user_id
        print "t-id:", tweet_id
        print "f-id:", pic_id
        print "date:", date
        print "text:", block
        print "lat:", lat
        print "lng:", lng




  
    


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # load_users()
    # load_pictures()
    # load_tweets()
    load_results()