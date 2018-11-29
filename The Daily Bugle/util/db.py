import sqlite3
DB = "data/accounts.db"


def add_user(username, hashed_pass):
    '''adds users to use table'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "INSERT INTO users (username,password)VALUES(?,?);"
    c.execute(command,(username,hashed_pass))
    db.commit()
    db.close()

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


#MAKE TABLES AND DATABASE IF THEY DONT EXIST
db = sqlite3.connect(DB)
c = db.cursor()
commands = []
commands += ["CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"]
for command in commands:
    c.execute(command)
