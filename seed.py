
import datetime
from sqlalchemy import func

from model import User, Result, Tweet, Picture, connect_to_db, db
from server import app

from faker import Faker 

fake = Faker()

def load_users():

    print "Users"

    # user = User(user_id=user_id,
    #             email=email,
    #             password=password)
    #user id
    for stuff in range (0,50):
        print fake.random_number()
        print str(fake.email())
        print str(fake.password())

    return stuff

def load_results():