# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3, hashlib

SETUP="""
CREATE TABLE IF NOT EXISTS users (
    username            TEXT,
    password            TEXT,
    user_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    num_blogs           INTEGER DEFAULT 0
);
"""

#example: cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", [username, password])
DB_FILE = "users.db"


def database():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.executescript(SETUP)

def hash(password: str) -> str:
    #  """
    #  hash pwd with SHA512
    #  """
    return hashlib.sha512(password.encode()).hexdigest()

def validate_new_user(user):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    rows = cursor.execute("SELECT username FROM users WHERE username LIKE '" + user[0] + "%'").fetchall()
    for i in rows:
        x = ''.join(i)
        if (x == user):
            return False
    return True

    # """
    # validates inputs for creating a new user
    # """

def crt_user(user, pw):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    password = hash(pw)
    cursor.execute("INSERT INTO users(username, password) VALUES(?, ?)", [user, password])
    db.commit()
    db.close()
    # """
    # if all inputs pass, create new user with inputs
    # """

def get_userid(user):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    rows = cursor.execute("SELECT username FROM users WHERE username LIKE '" + user[0] + "%'").fetchall()
    id = cursor.execute("SELECT user_id FROM users WHERE username LIKE '" + user[0] + "%'").fetchall()
    for i in range(len(rows)):
        x = ''.join(rows[i])
        if (x == user):
            userid = ''.join(id[i])
            return userid
    # """
    # return user id num
    # """

def auth_user(user,pw):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    p = hash(pw)
    up = user+p
    rows = cursor.execute("SELECT username, password FROM users WHERE username LIKE '" + user[0] + "%'").fetchall()
    for i in rows:
        x = ''.join(i)
        if (x == up):
            return True
    return False
    #
    # """
    # authenticates user based off of username & pwd
    # """
    # pass
