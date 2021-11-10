# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3
import auth, blogsdb
from os import urandom
from flask import render_template, redirect, request, url_for, session, Flask

# from app import app
# from app.auth import auth_user, crt_user

app = Flask(__name__)
app.secret_key = urandom(32)

blog_manager = blogsdb.BlogManager("blogs.db")
blog_manager.setup()
#TESTING AUTH
auth.database()
# auth.crt_user("c","jafe")
# auth.crt_user("fe","ld")
# print(auth.validate_new_user("c"))
# print(auth.auth_user("c","jafe"))
# print(auth.auth_user("c","j"))
# print(auth.get_userid("c"))

@app.route("/", methods=['GET','POST'])
def start():
    if 'username' in session: #is someone logged in
        return render_template("homepage.html", username = session['username'])
    return render_template("login.html", register_message='')

@app.route("/register", methods=['GET','POST'])
def register():
    username = request.form['regular_username']
    password = request.form['regular_password']
    if(username==''):
        return render_template("login.html", register_message = "Username can't be blank." )
    if(password==''):
        return render_template("login.html", register_message = "Password can't be blank.")
    if(auth.validate_new_user(username)):
        auth.crt_user(username,password)
        return render_template("login.html", register_message = "Sucessfully registered! Login!")
    return render_template("login.html", register_message = "User already exists. Try again with a different username.")

@app.route("/authenticate", methods=['GET','POST'])
def authenticate():
    user = request.form['login_username']
    password = request.form['login_password']
    if(user==''):
        return render_template("login.html", register_message = "Username can't be blank." )
    if(password==''):
        return render_template("login.html", register_message = "Password can't be blank.")
    if(auth.auth_user(user,password)):
        session['username'] = user
        return render_template("homepage.html", username=user)
    return render_template("login.html", register_message = "Username or password is wrong. Try again.")

@app.route("/index", methods=['GET', 'POST'])
def index():
    """
    homepage creation
    """
    return render_template('homepage.html', username=session['username'])

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    login form + response
    """
    return render_template("login.html")

@app.route("/crt_blog", methods=["GET", "POST"])
def crt_blog():
    userid = auth.get_userid(session['username'])
    """
    webpage arrived at upon selecting "create blog"
    """
    return render_template('crt_blog.html')

@app.route("/new_post", methods=["GET", "POST"])
def new_blog():
    userid = auth.get_userid(session['username'])
    blog = request.args['blog']
    postname = request.args['postname']
    posttext = request.args['body']
    if(blog=="newblog"):
        blogname = request.args['blogname']
        blog_manager.add_blog_w_starter_post(blogname, userid, postname, posttext)
    else:
        blog_manager.add_post(blog,postname,posttext,userid)
    return render_template("homepage.html", username=session['username'])
    """
    returns user to landing page after creating new blog post
    """

@app.route("/view_blogs", methods=["GET", "POST"])
def view_blogs():
    userid = auth.get_userid(session['username'])
    """
    view blogs from other users
    """
    return render_template("view_blogs.html", bloglist=blog_manager.list_blogs_by_datetime())

@app.route("/edit_blog", methods=["GET", "POST"])
def edit_blog():
    userid = auth.get_userid(session['username'])
    """
    edit post on existing blog
    """
    bloglist = ["blog1", "blog2"]
    chosen_blogname = request.form.getlist("blogs")
    print(chosen_blogname)
    return render_template("edit_blog.html", bloglist=bloglist)

@app.route("/edit_post", methods = ["GET", "POST"])
def edit_post():
    chosen_blogname = "newblogname"
    userid = auth.get_userid(session['username'])
    #postDict = blog_manager.repr_blog(userid, chosen_blogname)
    #postlist=list(postDict.keys())
    postlist = ["post1", "post2"]
    #chosen_postname = request.form["posts"]
    #print(chosen_postname)
    return render_template("edit_post.html", postlist=postlist)

@app.route("/editing", methods=["GET","POST"])
def edit():
    user_id = auth.get_userid(session['username'])
    new_postname, content = request.form["postname"], request.form["body"]
    postname = new_postname if new_postname != None else NEED_OLD_POST_NAME
    if new_postname != None:
        blog_manager.edit_post_title(new_postname, NEED_OLD_POSTNAME, user_id, NEED_BLOGNAME)
    if content != None:
        blog_manager.edit_post_content(content, postname, user_id, NEED_BLOGNAME)
    return render_template("edit.html", postname=OLD_POST_NAME, post_content=OLD_POST_CONTENT)

@app.route("/edited", methods=["GET","POST"])
def edited():
    userid = auth.get_userid(session['username'])
    return render_template("homepage.html", username = session['username'])

@app.route("/out", methods=["GET","POST"])
def logout():
    session.pop("username", default=None)
    return render_template("login.html", register_message='')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
