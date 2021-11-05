#a Python script for interacting with an SQLite db:
import sqlite3 #enable SQLite operations

#open db if exists, otherwise create
db = sqlite3.connect("discobandit.db") 

c = db.cursor() #facilitate db ops

SETUP = """
CREATE TABLE IF NOT EXISTS blogs (
    blog_title          TEXT
    user_id             INTEGER
    num_blogs           INTEGER DEFAULT 0
    blog_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8)))
    last_date_edited    DATE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS posts (
    post_title          TEXT
    post_text           TEXT
    blog_id             INTEGER
    user_id             INTEGER
    post_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8)))
    last_date_edited    DATE DEFAULT CURRENT_TIMESTAMP
);
"""

def setup():
        """
        setup database - create the blogs table, and the posts table
        """
        c.executescript(SETUP)

def add_blog_w_starter_post(blogname, user_id, postname, post_content):
    """
    add a blog and return blog id
    """
    c.execute("INSERT INTO blogs(blog_title, user_id) VALUES(?,?)", [blogname, user_id])
    c.execute("SELECT blog_title, user_id, blog_id FROM blogs")
    blogdata = c.fetchall()
    for blog in blogdata:
        if blogname in blog and user_id in blog:
            blog_id = blog[2]
            break
    c.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id, user_id])
    c.execute("SELECT * from blogs")
    print(c.fetchall())
    c.execute("SELECT * from blogs")
    print(c.fetchall())

setup()
add_blog_w_starter_post("testblog", 12345678, "testpost", "blahblahblahblah")

db.close()