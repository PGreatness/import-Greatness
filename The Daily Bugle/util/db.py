import sqlite3
DB = "data/database.db"


def add_user(username, hashed_pass):
    '''adds users to use table'''
    db = sqlite3.connect(DB)
    c = db.cursor()
    command = "INSERT INTO users (username,password_hash)VALUES(?,?);"
    c.execute(command,(username,password_hash))
    db.commit()
    db.close()



print('hi')
#MAKE TABLES AND DATABASE IF THEY DONT EXIST
