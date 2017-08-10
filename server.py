"""Server for Motivational Mashup"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Result, Tweet, Picture

from twitter_handler import TwitterClient
from flickr_handler import flickrClient


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    # age = int(request.form["age"])
    # zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password)

    # age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)



@app.route('/about')
def about():
    """Links the user to the about page."""

    return render_template("about.html")

@app.route('/profile')
def profile():
    """Allows user to go to their personal profile page."""

    return render_template("user.html")

@app.route('/feelings', methods=['GET'])
def feelings_form():
    """Show feeligns form"""

    return render_template("feelings_form.html")

@app.route('/results', methods=['POST'])
def process_feelings():
    """Process feelings form."""


    #gets form input from feelings form
    feels = request.form["feelings"]

    # new_feelings = Result(keyword=feels)
    # db.session.add(new_feelings)
    # db.session.commit()

    #calls to the flickrClient class in flickr_handler
    fApi = flickrClient()

    #calls to the get_photos method in f_handler to get the f_url
    photos = fApi.get_photos(feels)
    print photos

    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = feels, count = 200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
   
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
   
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")

    for tweet in ptweets[:10]:
        pResults = (tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")

    for tweet in ntweets[:10]:
        nResults = (tweet['text'])

    return render_template("results.html",
                            feels=feels,
                            nResults=nResults,
                            pResults=pResults,
                            photos=photos)


#THIS ROUTE IS A WORK IN PROGRESS
@app.route('/saved', methods=['POST'])
def save_results():
    """Saving the img and the text from results"""


    # Get form variables
    keyword = request.form["keyword"]
   
    #also need to add twitter text
    #also need to add flickr url

    new_keyword = Result(keywords=keyword)

    # age=age, zipcode=zipcode)

    db.session.add(keyword)
    db.session.commit()

    return redirect('/profile')
    pass


    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")