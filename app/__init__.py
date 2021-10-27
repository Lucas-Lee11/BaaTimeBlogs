# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

from os import urandom
from flask import Flask

app = Flask(__name__)

# session key - 32 random bytes
app.secret_key = urandom(32)

from app import routes

app.run()
