from flask import Flask, render_template, request, session, url_for, redirect
from os import urandom
import json, urllib

app = Flask(__name__)

#stubs for paths to REST APIs
NEWS_STUB = "https://developers.nytimes.com/svc/topstories/v2/{}.json?api-key={}" #section of news, api key
WEATHER_STUB = "https://api.darksky.net/forecast/{}/{},{}" #api key, longitude, latitude
COMIC_STUB = "http://xkcd.com/{}/info.0.json" #comic number

@app.route('/')
def home():
    #read json file containing the api keys
    with open('data/API_Keys/keys.json') as json_file:
        json_data = json.loads(json_file.read())
    print(json_data) #should print           {'News': 'api_key', 'Weather': 'api_key', 'Comic': ''}
    print(json_data['News']) # should print      "api_key"

    f = urllib.request.urlopen(WEATHER_STUB.format(json_data['Weather'],34,-118)) #34,-118 is LA
    weather = json.loads(f.read())
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth')
def auth():
    ###Authenticate
    return redirect(url_for(home))

if __name__ == "__main__":
    app.debug = True
    app.run()
