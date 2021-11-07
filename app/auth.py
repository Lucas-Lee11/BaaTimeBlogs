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
    rows = cursor.execute("SELECT username FROM users").fetchall()
    print(rows)
    u = "('" + user + "',)"
    for i in rows:
        print(i)
        if (i == u):
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
    # """
    # if all inputs pass, create new user with inputs
    # """

def get_userid(username):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    rows = cursor.execute("SELECT username FROM users").fetchall()
    id = cursor.execute("SELECT user_id FROM users").fetchall()
    u = "('" + user + "')"
    for i in range(len(rows)):
        if (rows[i] == u):
            return id[i][2:len(id)-2]
    # """
    # return user id num
    # """

def auth_user(user,pw):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    p = hash(pw)
    up = "('" + user + "', '" + p + "')"
    rows = cursor.execute("SELECT user, password FROM users").fetchall()
    for i in rows:
        if (i == up):
            return true
    return false
    #
    # """
    # authenticates user based off of username & pwd
    # """
    # pass
