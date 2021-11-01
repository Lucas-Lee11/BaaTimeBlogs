# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

from flask import Flask, render_template, request
from os import urandom

app = Flask(__name__)

app.secret_key = urandom(32)

@app.route("/", methods=['GET', 'POST']) #, methods=['GET', 'POST'])
def index():
    """
    create the basic login page, if session active auto-sign in
    """
    return render_template('homepage.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run() 