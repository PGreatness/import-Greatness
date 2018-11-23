from flask import Flask, render_template, request, session, url_for
from os import urandom
import json, urllib

app = Flask(__name__)

#stubs for paths to REST APIs
NEWS_STUB = ""
WEATHER_STUB = ""
COMIC_STUB = ""

@app.route('/')
def home():
    #read json file containing the api keys
    with open('data/API Keys/keys.json') as json_file:
        json_data = json.loads(json_file.read())
    print(json_data) #should print           {'News': '', 'Weather': '', 'Comic': ''}
    print(json_data['News']) # should print      ""


    return render_template('home.html')


if __name__ == "__main__":
    app.debug = True
    app.run()