# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3
import auth
from flask import render_template, redirect, request, url_for, session, Flask

# from app import app
# from app.auth import auth_user, crt_user

app = Flask(__name__)

auth.database()

@app.route("/")
def yes():
    return render_template("homepage.html", username = "user1")

@app.route("/index") #, methods=['GET', 'POST'])
def index():
    """
    homepage creation
    """
    return render_template('homepage.html', username="user1")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    login form + response
    """
    return render_template("login.html")

@app.route("/crt_blog", methods=["GET", "POST"])
def crt_blog():
    """
    webpage arrived at upon selecting "create blog"
    """
    return render_template('crt_blog.html')

@app.route("/new_blog", methods=["GET", "POST"])
def new_blog():
    """
    returns user to landing page after creating new blog post
    """
    return render_template("homepage.html", username='user1')

@app.route("/edit_blog", methods=["GET", "POST"])
def edit_blog():
    """
    edit post on existing blog
    """
    return render_template("edit_blog.html")

@app.route("/view_blogs", methods=["GET", "POST"])
def view_blogs():
    """
    view blogs from other users
    """
    return render_template("view_blogs.html")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
