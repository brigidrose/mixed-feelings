"""Server for Mixed Feelings"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Result, Tweet, Picture

from twitter_handler import TwitterClient
from flickr_handler import flickrClient
from text_sentiment import sentiment
import datetime
from flask_sqlalchemy import SQLAlchemy
import pdb
import pprint

from os import path
from wordcloud import WordCloud

from giphy_handler import get_giphy
import giphypop

app = Flask(__name__)
fApi = flickrClient()
tApi = TwitterClient()


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


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

    session["user_id"] = new_user.user_id

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)



@app.route('/about')
def about():
    """Links the user to the about page."""

    return render_template("about.html")

@app.route('/users/<user_id>')
def profile(user_id):
    """Allows user to go to their personal profile page."""

    past_saves = Result.query.filter_by(user_id=user_id).all()

    return render_template("user.html", saved_mixes=past_saves)

@app.route('/feelings', methods=['GET'])
def feelings_form():
    """Show feeligns form"""

    return render_template("feelings_form.html")

@app.route('/results', methods=['POST'])
def process_feelings():
    """Process feelings form."""

############ FORM INPUTS ###################################################

    #gets form input from feelings form
    feels = request.form["feeling_keyword"]
    #get paragraph block of text.
    block = request.form["b_text"]
    #gets the information from the radio toggle button
    toggle = request.form["feels"]



########### CLASS CALLS AND METHOD CALLS ##################################

    #calls to the get_photos method in f_handler to get the f_url
    # photos = fApi.get_photos(feels)
    # print photos
    # img = giphypop.translate(feels)
    # return img.url
    photos = get_giphy(feels)
    print photos

    # calling function to get tweets
    get_tweets = tApi.get_tweets(query=feels, count=200)
    print get_tweets

    # analysis = tApi.get_tweet_sentiment(tweet=)


############# SENTIMENT ANALYSIS ###################################
    
    #block text analysis
    analyzed_text = sentiment(block) + sentiment(feels)
    print "LOOOOOKKKKKK RIGHT HERE!!!!!!!!!!!!!!!!!!!!!!"
    print analyzed_text



    #twitter text analysis based on users choice
    if toggle == "full":
        feeling ='positive'
        print "POSIIIIII"
    else:
        feeling = 'negative'
        print "NEGIIIIII"
        # picking positive tweets from tweets
    get_tweets = [tweet for tweet in get_tweets if tweet['sentiment'] == feeling]
    print get_tweets
    if len(get_tweets) == 0:
        return render_template("broke_the_internet.html")

    tweet_text = tweet['text']

    return render_template("results.html",
                            feels=feels,
                            tweet_text=tweet_text,
                            photos=photos,
                            block=block,
                            toggle=toggle,
                            analyzed_text=analyzed_text)


@app.route('/remix', methods=['POST'])
def refresh_results():

    feelings = request.form["keyword"]
    toggle = request.form["toggle"]


    # photos = fApi.get_photos(feelings)
    photos = get_giphy(feelings)

    get_tweets = tApi.get_tweets(query=feelings, count=200)

    if toggle == "full":
        feeling ='positive'
        print "POSIIIIII"
    else:
        feeling = 'negative'
        print "NEGIIIIII"
        # picking positive tweets from tweets
    get_tweets = [tweet for tweet in get_tweets if tweet['sentiment'] == feeling]

    if len(get_tweets) == 0:
        return render_template("broke_the_internet.html")
    
    results = {"photo": photos, "tweets": tweet['text']}
    
    return jsonify(results)


@app.route('/saved', methods=['POST'])
def save_results():
    """Saving the img and the text from results"""


    # Get form variables
    keyword = request.form["keywords"]
    text_results = request.form["twitter"]
    flick_url = request.form["flickr"]
    block = request.form["b_text"]
    sentiment = request.form["sentiment"]
    lat = request.form["lat"]
    lng = request.form["long"]


    #Saving current user info into the db
    user_id = session.get("user_id")
    #Saving tweet data to db
    save_twit = Tweet(tweet_text=text_results)
    db.session.add(save_twit)
    db.session.commit()
    #Saving flickr data to db
    save_flick = Picture(flickr_url=flick_url)
    db.session.add(save_flick)
    db.session.commit()
    #Saving block text input
  
    #Get geolocation information once user saves results.



    new_keyword = Result(keywords=keyword, 
                         tweet_id=save_twit.tweet_id, 
                         flickr_id=save_flick.flickr_id,
                         block_text=block,
                         sentiment=sentiment,
                         generated_at=datetime.datetime.now(),
                         user_id=user_id,
                         lat=lat,
                         lng=lng)

    

    db.session.add(new_keyword)
    db.session.commit()



    return redirect("/users/%s" % user_id)

@app.route('/global_feelings')
def see_all_feelings():

    return render_template("map.html")
    
@app.route('/feelings.json')
def users_feelings():

    feelings = {
        result.result_id: {
            "user_id": result.user_id,
            "tweet_id": result.tweet.tweet_text,
            "flickr_id": result.picture.flickr_url,
            "generated_at": result.generated_at,
            "keywords": result.keywords,
            "block_text": result.block_text,
            "sentiment": result.sentiment,
            "lat": result.lat,
            "lng": result.lng
        }
        for result in Result.query.limit(500)}

    return jsonify(feelings)

# @app.route('/search', methods= ['GET', 'POST'])
# def search_feelings():

#         search = request.form("search")

#         q = Result.query.filter(Result.keywords.like('%' + search + '%')) | (Result.block_text.like('%' + search + '%')).all()

#         print q

#         #change this route to the proper thing.
#         return render_template("test.html")

@app.route('/word_cloud', methods=['GET'])
def create_word_cloud():

    user_results = db.session.query(Result.keywords,          #what would I put for current user id?
                                    Result.block_text).filter(Result.user_id == session['user_id']).all()

    corpus = " ".join([keywords + " " + block_text for keywords, block_text in user_results])

    print type(corpus)

    

    wordcloud = WordCloud().generate(corpus)

    # # # Display the generated image:
    # # # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

  
    plt.show()

    return render_template("word_cloud.html")




@app.route('/logout')
def logout():

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")