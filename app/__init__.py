# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST']) #, methods=['GET', 'POST'])
def index():
    """
    create the basic login page, currently going straight to homepage
    """
    return render_template('homepage.html', username="user1")

@app.route("/crt_blog")
def crt_blog():
    """
    webpage arrived at upon selecting "create blog"
    """
    return render_template('crt_blog.html')

@app.route("/new_blog")
def new_blog():
    """
    returns user to landing page after creating new blog post
    """
    return render_template("homepage.html", username='user1')

@app.route("/edit_blog")
def edit_blog():
    """
    edit post on existing blog
    """
    return render_template("edit_blog.html")

@app.route("/view_blogs")
def view_blogs():
    """
    view blogs from other users
    """
    return render_template("view_blogs.html")

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
