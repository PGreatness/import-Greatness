from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
import json
import urllib
import os
from util import db

''' Rate Limits for APIs:
    # Dark Sky API - 1000/day (needs to be credited)
    # NYTimes API - 1000/day
    # XKCD API - Unlimited
    # IPAPI - 1000/day
'''

app = Flask(__name__)
app.secret_key = os.urandom(32)
# stubs for paths to REST APIs
NEWS_STUB = "https://api.nytimes.com/svc/topstories/v2/{}.json?api-key={}" # section of news, api key
WEATHER_STUB = "https://api.darksky.net/forecast/{}/{},{}" # api key, longitude, latitude
COMIC_STUB = "http://xkcd.com/{}/info.0.json" # comic number

@app.route("/getIP", methods=["GET"])
def getIP():
    print( jsonify({'ip': request.remote_addr}), 200 )

@app.route('/')
def home():

    # read json file containing the api keys
    with open('data/API_Keys/keys.json') as json_file:
        json_data = json.loads(json_file.read())
    print(json_data) # should print           {'News': 'api_key', 'Weather': 'api_key', 'Comic': ''}
    print(json_data['News']) #  should print      "api_key"

    # # # News API
    n = urllib.request.urlopen(NEWS_STUB.format("home", json_data['News']))
    news = json.loads(n.read())
    # print ( news )

    # # # Weather API
    w = urllib.request.urlopen(WEATHER_STUB.format(json_data['Weather'], 34, -118)) # 34,-118 is LA
    weather = json.loads(w.read())
    # print ( weather )

    # # # XKCD API
    c = urllib.request.urlopen(COMIC_STUB.format(1))
    comic = json.loads(c.read())
    # print ( comic )

    getIP()

    return render_template('home.html', weatherData = weather, newsData = news, comicData = comic)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods = ["POST"])
def auth():
    # # # Authenticate
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    all_usernames = db.get_all_users()
    if username_input in all_usernames:
        if password_input == all_usernames[username_input]:
            # Log them in
            session['user'] = username_input
            return redirect(url_for("home"))
        # Failed password and username match
        else:
            flash("Invalid password")
    # Username doesnt exist
    flash("Invalid username")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.debug = True
    app.run()
