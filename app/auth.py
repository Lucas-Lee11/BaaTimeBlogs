# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3, hashlib

SETUP="""
CREATE TABLE IF NOT EXISTS users (
    username            TEXT
    password            TEXT
    user_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8)))
    num_blogs           INTEGER DEFAULT 0
);
"""

def hash(password: str) -> str:
    """
    hash pwd with SHA512
    """
    return hashlib.sha512(password.encode()).hexdigest()

def validate_new_user(user):
	rows = cursor.execute("SELECT user FROM users").fetchall()
	for i in rows:
		if (i == user):
			return false
	return true
		
    """
    validates inputs for creating a new user
    """
	
def crt_user(user, pw):
	cursor.execute("INSERT INTO users VALUES('" + user +"','" + pw + "',NULL");
    """
    if all inputs pass, create new user with inputs
    """
    pass

def get_userid():
    """
    return user id num
    """
    pass

def auth_user(user,pw):
	rows = cursor.execute("SELECT user, pass FROM users").fetchall()
	up = "('" + user +"', '" + pw + "')")
	for i in rows:
		if (i[0] == up):
			return true
	return false
		
    """
    authenticates user based off of username & pwd
    """
    pass
