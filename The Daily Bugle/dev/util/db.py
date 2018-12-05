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
    command = "SELECT * FROM users;"
    c.execute(command)
    something = c.fetchall()
    print(something)
    print(user)
    print(hashed_pass)
    command = "UPDATE users SET password='" + hashed_pass + "'WHERE username='" + user + "';"
    c.execute(command)
    print("passwords updated")
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

def save_article(date, content):
    '''adds articles to articles table'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "INSERT INTO articles(date, content)VALUES(?,?);"
    c.execute(command, (date, content))
    db.commit()
    db.close()

def get_articles():
    '''returns all the articles in dict {date:content}'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "SELECT date,content from articles;"
    c.execute(command)
    info = c.fetchall()
    articles = {}
    for item in info:
        articles[item[0]] = item[1]
    db.close()
    return articles


# MAKE TABLES AND DATABASE IF THEY DONT EXIST
db = sqlite3.connect(DB)
c = db.cursor()
commands = []
commands += ["CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, question TEXT, answer TEXT)"]
commands += ["CREATE TABLE IF NOT EXISTS articles(date TEXT, content TEXT)"]
# commands += ["CREATE TABLE IF NOT EXISTS pages(link TEXT, weather TEXT, comic TEXT)"]
for command in commands:
    c.execute(command)
