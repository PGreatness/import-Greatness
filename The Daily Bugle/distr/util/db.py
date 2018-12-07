import sqlite3
DB = "data/accounts.db"


def add_user(username, hashed_pass):
    '''adds users to use table'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "INSERT INTO users (username,password)VALUES(?,?);"
    c.execute(command, (username, hashed_pass))
    db.commit()
    db.close()

def add_userFull(username, hashed_pass, question, hashed_ans):
    '''adds users to use table'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "INSERT INTO users (username,password, question, answer)VALUES(?,?,?,?);"
    c.execute(command, (username, hashed_pass, question, hashed_ans))
    db.commit()
    db.close()

def update_pass(user, hashed_pass):
    '''resets users password'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    # command = "SELECT * FROM users;"
    # c.execute(command)
    # something = c.fetchall()
    # print(something)
    # print(user)
    # print(hashed_pass)
    command = "UPDATE users SET password='" + hashed_pass + "'WHERE username='" + user + "';"
    c.execute(command)
    # print("passwords updated")
    db.commit()
    db.close()

def qaDict():
    '''returns all the users and hashed answers in dict {user:answer}'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT username,answer from users;"
    c.execute(command)
    info = c.fetchall()
    users = {}
    for item in info:
        users[item[0]] = item[1]
    db.close()
    return users


def get_all_users():
    '''returns all the users and hashed passwords in dict {user:pass}'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT username,password from users;"
    c.execute(command)
    info = c.fetchall()
    users = {}
    for item in info:
        users[item[0]] = item[1]
    db.close()
    return users

def add_Fav(user, timeid):
    '''adds the article to the favorites section of the user based on id and date'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    all_usernames = favDict()  ##dictionary of all the users and their saved articles
    list = show_Fav(user)
    added = False
    try:
        list.index(str(timeid))
    except:
        added = True
        if (all_usernames[user]): ##the string of saved articles for this user
            appendage = all_usernames[user] + "," + str(timeid)
        else:
            appendage = str(timeid)
        # command = "SELECT * FROM users;"
        # c.execute(command)
        # something = c.fetchall()
        # print(something)
        # print(user)
        # print(hashed_pass)
        command = "UPDATE users SET favorite='" + appendage + "'WHERE username='" + user + "';"
        c.execute(command)
        # print("added to favorites")
    db.commit()
    db.close()
    return added

def favDict():
    '''returns all the users and favorited articles in dict {user:article}'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT username,favorite from users;"
    c.execute(command)
    info = c.fetchall()
    users = {}
    for item in info:
        users[item[0]] = item[1]
    db.close()
    return users

def show_Fav(user):
    list = []          ## Start as an empty list
    dict = favDict()
    x = dict[user]
    if (x):
        list = x.split(",")
        for i in list:
            print (i)
    return list


# MAKE TABLES AND DATABASE IF THEY DONT EXIST
db = sqlite3.connect(DB)
c = db.cursor()
commands = []
commands += ["CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, question TEXT, answer TEXT, favorite TEXT)"]
commands += ["CREATE TABLE IF NOT EXISTS articles(date TEXT, content TEXT)"]
# commands += ["CREATE TABLE IF NOT EXISTS pages(link TEXT, weather TEXT, comic TEXT)"]
for command in commands:
    c.execute(command)
