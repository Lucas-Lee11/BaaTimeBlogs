# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

from os import urandom

from flask import Flask

app = Flask(__name__)

# after Flask app init to avoid circular imports
from app import main

# secret key for session (32 random bytes)
app.secret_key = urandom(32)

# false in deliverable
app.debug = False
app.run()
