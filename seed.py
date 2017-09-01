
import datetime
from sqlalchemy import func
import random

from model import User, Result, Tweet, Picture, connect_to_db, db
from server import app

from faker import Faker
from flickr_handler import flickrClient
from twitter_handler import TwitterClient
from giphy_handler import get_giphy

fake = Faker()
fApi = flickrClient()
tApi = TwitterClient()

feels = ['happy', 'sad', 'angry', 'sleepy', 'upset', 'excited', 'scared', 'anxious',
        'intrepid', 'goofy', 'grumpy', 'dumbfounded', 'tremendous', 'spectacular',
        'depressed', 'low', 'itchy', 'smelly', 'irrational']

lats = [43.76316, 42.738944, 30.968189, 33.348885, 41.43449, 35.380093, 46.24825,
      26.02717, 46.004593, 31.269161, 46.004593, 32.801128, 36.840065, 27.327855,
      34.411442, 50.369993, 39.465885, 41.603121, 21.079375, 43.161116, 36.416862,
      27.327855, 51.477962, 41.603121, 47.00648, 60.562679, 51.368351, 47.364874,
      42.126747, 30.102366]

lngs = [-115.3125, -72.773438, -98.085938, -113.554688, -86.484375, -96.679688,
        -116.367188, -103.359375, -76.289063, -81.914063, -119.53125, -116.191406,
        -93.164063, -81.5625, -108.28125, -91.40625, -76.289063, -72.421875,
        -78.574219, -107.578125, -90.703125, -108.632813, -126.210938, -84.726563,
        -97.558594, -142.910156, -59.414063, -81.210938, -76.816406, -91.40625]



def load_users():

    print "Users"

    for _ in range (0,30):
        email = str(fake.email())
        password = str(fake.password())
        user = User(email=email,
                password=password)
        db.session.add(user)

    db.session.commit()

def load_pictures():
    
    for _ in range (0,30):
        new_feeling = random.choice(feels)
        print new_feeling
        # photos = fApi.get_photos(new_feeling)
        photos = get_giphy(feels)
        pic = Picture(flickr_url=photos)
        db.session.add(pic)
    
    db.session.commit()

def load_tweets():

    i = 0

    while i < 30:
        new_feeling = random.choice(feels)
        print new_feeling
        get_tweets = tApi.get_tweets(query=new_feeling, count=5)
        print get_tweets
        try:
            tweet = random.choice(get_tweets)['text']
        except IndexError:
            continue

        query = Tweet.query.filter_by(tweet_text=tweet).first()

        if query == None:
            tweet_text = Tweet(tweet_text=tweet)
            db.session.add(tweet_text)
            i = i+1
        else:
            continue

    db.session.commit()

def load_results():

    for i in range(0, 30):

        user_id = (random.choice(User.query.all())).user_id
        tweet_id = (random.choice(Tweet.query.all())).tweet_id
        pic_id = (random.choice(Picture.query.all())).flickr_id
        date = fake.date()
        keyword = random.choice(feels)
        block = str(fake.text())
        sentiment = random.choice(range(-5, 5))
        lat = lats[i]
        lng = lngs[i]
 
        result = Result(user_id=user_id,
                        tweet_id=tweet_id,
                        flickr_id=pic_id,
                        generated_at=date,
                        keywords=keyword,
                        block_text=block,
                        sentiment=sentiment,
                        lat=lat,
                        lng=lng)

        db.session.add(result)
    

        db.session.commit()

  
    


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_pictures()
    load_tweets()
    load_results()



