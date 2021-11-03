# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

from flask import Flask, render_template, request, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST']) #, methods=['GET', 'POST'])
def index():
    """
    create the basic login page, if session active auto-sign in
    """
    return render_template('homepage.html', username="user1")

@app.route("/crt_blog")
def crt_blog():
    return render_template('crt_blog.html')

@app.route("/new_blog")
def new_blog():
    return render_template("homepage.html", username='user1')
@app.route("/edit_blog")
def edit_blog():
    return render_template("edit_blog.html")
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
