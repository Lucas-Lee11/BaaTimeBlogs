# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3, hashlib

def hash(password: str) -> str:
    """
    hash pwd with SHA512
    """
    return hashlib.sha512(password.encode()).hexdigest()

def validate_new_user():
    """
    validates inputs for creating a new user
    """

def crt_user():
    """
    if all inputs pass, create new user with inputs
    """
    pass

def get_userid():
    """
    return user id num
    """
    pass

def auth_user():
    """
    authenticates user based off of username & pwd
    """
    pass