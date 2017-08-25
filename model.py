from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    #I kind of want a lot more user data so I am wondering if I should just
    #figure out how to use FB to sign in. Would love thoughts on this.

    __tablename__ = "users"
  
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s username=%s >" % (self.user_id, self.email)

###############################################################################

class Result(db.Model):
    """Movie on ratings website."""

    __tablename__ = "results"

    result_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.tweet_id'))
    flickr_id = db.Column(db.Integer, db.ForeignKey('pictures.flickr_id'))
    generated_at = db.Column(db.DateTime)
    keywords = db.Column(db.String(500))
    block_text = db.Column(db.String(500))
    sentiment = db.Column(db.Float)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
  

    # Define relationship to user
    user = db.relationship("User", backref=db.backref("results"))
    tweet = db.relationship("Tweet", backref=db.backref("results"))
    picture = db.relationship("Picture", backref=db.backref("results"))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Result result_id=%s user_id=%s>" % (self.result_id, self.user_id)

###############################################################################

class Tweet(db.Model):
    """Saves the info from a twitter API call."""

    __tablename__ = "tweets"

    tweet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_text = db.Column(db.String(400))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Tweet tweet_id=%s>" % (self.tweet_id)



##############################################################################

class Picture(db.Model):
    """Saves the info from a Flickr API call."""

    __tablename__ = "pictures"

    flickr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    flickr_url = db.Column(db.String(400))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Picture flickr_id=%s>" % (self.flickr_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mixed-feelings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
