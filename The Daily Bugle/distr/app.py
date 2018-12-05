import json
import urllib
import os

from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from passlib.hash import md5_crypt
import datetime

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
IPAPI_STUB = "https://ipapi.co/{}/json/"

@app.route("/getIP", methods=["GET"])
def getIP():
    # return jsonify({'ip': request.remote_addr}), 200
    # return request.headers['X-Real-IP']
    # return request.environ['REMOTE_ADDR']
    # return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    # use another api to get ip, returns a text
    qwerty = urllib.request.urlopen('https://api.ipify.org')
    # decode else binary
    return(qwerty.read().decode('utf-8'))

@app.route('/')
def home():

    # read json file containing the api keys
    with open('data/API_Keys/keys.json') as json_file:
        json_data = json.loads(json_file.read())
    print(json_data) # should print           {'News': 'api_key', 'Weather': 'api_key', 'Comic': ''}
    print(json_data['News']) #  should print      "api_key"

    # Checking the longitude and latitiude based on the ip address
    print ("\n\nTHE IP ADDRESS: ")
    print ( getIP() )
    p = urllib.request.urlopen(IPAPI_STUB.format(getIP()))
    ip = json.loads(p.read())
    print (ip)
    location = ""
    location += ip['city'] + ", " + ip['country_name']
    print (location)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    f = open('data/content.json', 'r')
    data = json.loads(f.read())
    f.close()

    # if it is time to update/never had it
    # update it
    if today not in data:
        w = urllib.request.urlopen(WEATHER_STUB.format(json_data['Weather'], ip['latitude'], ip['longitude'])) # based on your ip address location
        weather = json.loads(w.read())

        c = urllib.request.urlopen(COMIC_STUB.format(1))
        comic = json.loads(c.read())

        n = urllib.request.urlopen(NEWS_STUB.format("home", json_data['News']))
        news = json.loads(n.read())

        # Create our own json file for easier read/less space taken
        data[today] = dict()
        data[today]['weather-summary'] = weather['daily']['summary']
        data[today]['comic-image'] = comic['img']
        data[today]['news'] = []
        for i in range(7): #add article info (dicts) into list of articles
            data[today]['news'] += [dict()]
            copy = data[today]['news'][i]
            article = news['results'][i]
            copy['id'] = i
            copy['title'] = article['title']
            copy['abstract'] = article['abstract']
            copy['link'] = article['url']
            copy['date'] = article['updated_date'].split('T')[0] #Gets the yyyy-mm-dd
            if len(article['multimedia']) != 0:
                copy['image-url'] = article['multimedia'][-1]['url']
                copy['image-caption'] = article['multimedia'][-1]['caption']
            else:
                copy['image-url'] = 'https://www.logistec.com/wp-content/uploads/2017/12/placeholder.png' #If there is no image
                copy['image-caption'] = ''

        # Add it all to our own file
        f = open('data/content.json', 'w')
        f.write(json.dumps(data))
        f.close()
    return render_template('home.html', data = data[today], session = session)


@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/auth', methods = ["POST"])
def auth():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Intermediate to authenticate login by user'''
    # # # Authenticate
    username_input = request.form.get("username")
    password_input = request.form.get("password")
    all_usernames = db.get_all_users()
    if username_input in all_usernames:
        # If the hashes match
        if md5_crypt.verify(password_input, all_usernames[username_input]):
            # Log them in
            session['user'] = username_input
            return redirect(url_for("home"))
        # Failed password and username match
        else:
            flash("Invalid password")
    else:
        # Username doesnt exist
        flash("Invalid username")
    return redirect(url_for("login"))

@app.route('/register', methods = ["GET", "POST"])
def register():
    if 'user' in session:
        return redirect(url_for('home'))
    '''Adding users to the database'''
    if request.form.get("reg_username") != None:
        r_username = request.form.get("reg_username")
        r_password = request.form.get("reg_password")
        check_pass = request.form.get("check_password")
        if r_username in db.get_all_users():
            flash("Username taken")
        elif r_password != check_pass:
            flash("Passwords do not match!")
        elif r_password.count(' ') != 0:
            flash("Password can not contain spaces")
        elif not r_username.isalnum():
            flash("Username should be alphanumeric")
        else:
            session['user'] = r_username
            db.add_user(r_username, md5_crypt.encrypt(r_password))
            return redirect(url_for("home"))
    return render_template('register.html')

@app.route('/reset', methods = ["POST"])
def reset():
    if 'user' in session:
        return redirect(url_for('home'))
    '''To reset userpassword'''
    if request.form.get("reg_username") != None:
        r_username = request.form.get("reg_username")
        r_question = request.form.get("reg_question")
        r_answer = request.form.get("reg_answer")
        r_password = request.form.get("reg_password")
        check_pass = request.form.get("check_password")
        if r_username not in db.get_all_users():
            flash("Username taken")
        elif r_password != check_pass:
            flash("Passwords do not match!")
        elif r_password.count(' ') != 0:
            flash("Password can not contain spaces")
        elif not r_username.isalnum():
            flash("Username should be alphanumeric")
        else:
            session['user'] = r_username
            # adds the question and answer to the db
            db.add_user(r_question, md5_crypt.encrypt(r_answer))
            # changes the user password
            db.add_user(r_username, md5_crypt.encrypt(r_password))
            return redirect(url_for("login"))
    return render_template('register.html')

@app.route('/logout', methods = ['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))

# def savePage():
#     response = urllib2.urlopen(url)
#     webContent = response.read()
#
#     f = open('obo-t17800628-33.html', 'w')
#     f.write(webContent)
#     f.close


if __name__ == "__main__":
    app.debug = True
    app.run()
