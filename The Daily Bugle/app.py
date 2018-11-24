from flask import Flask, render_template, request, session, url_for
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


    return render_template('home.html')


if __name__ == "__main__":
    app.debug = True
    app.run()