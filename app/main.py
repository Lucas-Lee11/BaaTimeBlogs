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
    bloglist = blog_manager.list_blogs_from_user(userid)
    """
    webpage arrived at upon selecting "create blog"
    """
    return render_template('crt_blog.html', blogs=bloglist)

@app.route("/new_post", methods=["GET", "POST"])
def new_blog():
    userid = auth.get_userid(session['username'])
    bloglist = blog_manager.list_blogs_from_user(userid)
    postname = request.form['postname']
    if(postname==''):
        return render_template("crt_blog.html", error="Postname can't be empty", blogs=bloglist)
    posttext = request.form['body']
    print(posttext + "nnnn")
    if(posttext==' '):
        return render_template("crt_blog.html", error="Post text can't be empty", blogs=bloglist)
    newblog = request.form.get('newblog')
    if(newblog is not None):
        blogname = request.form['blogname']
        if(blogname==''):
            return render_template("crt_blog.html", error="Blogname can't be empty", blogs=bloglist)
        elif(blog_manager.check_blogname_exists(blogname,userid)):
            return render_template("crt_blog.html", error="Blogname already exists. Input a new one", blogs=bloglist)
        else:
            blog_manager.add_blog_w_starter_post(blogname, userid, postname, posttext)
    else:
        blog = request.form.get('blog')
        if(blog is None):
            return render_template("crt_blog.html", error="You have no blogs to add on. Create a new one", blogs=bloglist)
        if(blog_manager.check_postname_exists(postname,userid,blog)):
            bloglist = blog_manager.list_blogs_from_user(userid)
            return render_template("crt_blog.html", error="Postname already exists. Input a new one", blogs=bloglist)
        else:
            blog_manager.add_post(blog,postname,posttext,userid)
    return render_template("homepage.html", username=session['username'])
    """
    returns user to landing page after creating new blog post
    """

global correctBlog
@app.route("/view_blogs", methods=["GET", "POST"])
def view_blogs():
    global correctBlog
    correctBlog = None
    userid = auth.get_userid(session['username'])
    """
    view blogs from other users
    """
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    list=blog_manager.list_blogs_by_datetime()
    for i in list:
        id = i[1];
        cursor.execute(f"SELECT username FROM users WHERE user_id like '{id}'")
        user = cursor.fetchone()
        i.append(user[0])

    return render_template("view_blogs.html", bloglist=list)

@app.route("/view_posts",methods=["GET", "POST"])
def view_posts():
    if(len(request.form.getlist("blog"))==0):
        db = sqlite3.connect("users.db")
        cursor = db.cursor()
        list=blog_manager.list_blogs_by_datetime()
        for i in list:
            id = i[1];
            cursor.execute(f"SELECT username FROM users WHERE user_id like '{id}'")
            user = cursor.fetchone()
            i.append(user[0])
        return render_template("view_blogs.html", bloglist=list, error="Please select a blog to view.")
    global correctBlog
    correctBlog = None
    if (correctBlog is None):
        correctBlog = (request.form.getlist("blog"))
    db = sqlite3.connect("blogs.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM blogs WHERE blog_title like '{correctBlog[0]}'")
    user = cursor.fetchone()
    #userid = auth.get_userid(session['username'])
    new_dict = blog_manager.repr_blog(user[0],correctBlog[0])
    return render_template("view_posts.html", postDict = new_dict, blogname = correctBlog[0])

@app.route("/edit_blog", methods=["GET", "POST"])
def edit_blog():
    userid = auth.get_userid(session['username'])
    """
    edit post on existing blog
    """
    bloglist = blog_manager.list_blogs_from_user(userid)
    return render_template("edit_blog.html", bloglist=bloglist)

#needed for edit funcs
global chosen_blogname, chosen_post, old_post_content

@app.route("/edit_post", methods = ["GET", "POST"])
def edit_post():
    global chosen_blogname
    userid = auth.get_userid(session['username'])
    if(len(request.form.getlist("blogs"))==0):
        bloglist = blog_manager.list_blogs_from_user(userid)
        return render_template("edit_blog.html", bloglist=bloglist, error="Please select a blog to edit")
    else:
        chosen_blogname = request.form.getlist("blogs")[0]
        postlist = blog_manager.list_posts_from_blog(userid, chosen_blogname)
        return render_template("edit_post.html", postlist=postlist)

@app.route("/editing", methods=["GET","POST"])
def edit():
    global chosen_post, old_post_content
    userid = auth.get_userid(session['username'])
    if(len(request.form.getlist("posts"))==0):
        postlist = blog_manager.list_posts_from_blog(userid, chosen_blogname)
        return render_template("edit_post.html", postlist=postlist, error="Please select a post to edit")
    else:
        chosen_post = request.form.getlist("posts")[0]
        old_post_content = blog_manager.get_post_content(chosen_post, userid, chosen_blogname)
        return render_template("edit.html", blogname=chosen_blogname, error="", postname=chosen_post, post_content=old_post_content)

@app.route("/edited", methods=["GET","POST"])
def edited():
    userid = auth.get_userid(session['username'])
    new_blogname, new_postname, content = request.form["blogname"], request.form["postname"], request.form["body"]
    postname, blogname = chosen_post, chosen_blogname
    if new_postname != chosen_post and not blog_manager.check_postname_exists(new_postname, userid, chosen_blogname):
        blog_manager.edit_post_title(new_postname, chosen_post, userid, chosen_blogname)
        postname=new_postname
    elif new_postname != chosen_post:
        return render_template("edit.html", error="Post title already exists in this blog.", blogname=new_blogname, postname=chosen_post, post_content=old_post_content)
    if new_blogname != chosen_blogname and not blog_manager.check_blogname_exists(new_blogname, userid):
        blog_manager.edit_blog_name(new_blogname, chosen_blogname, userid)
        blogname=new_blogname
    elif new_blogname != chosen_blogname:
        return render_template("edit.html", error="Blog title already exists in this blog.", blogname=new_blogname, postname=chosen_post, post_content=old_post_content)
    blog_manager.edit_post_content(content, postname, userid, blogname)
    return render_template("homepage.html", username = session['username'])

@app.route("/out", methods=["GET","POST"])
def logout():
    session.pop("username", default=None)
    return render_template("login.html", register_message='')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
