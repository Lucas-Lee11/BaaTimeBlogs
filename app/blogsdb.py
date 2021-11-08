# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3

SETUP = """
CREATE TABLE IF NOT EXISTS blogs (
    blog_title          TEXT,
    user_id             INTEGER,
    num_blogs           INTEGER DEFAULT 1,
    blog_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    last_date_edited    DATE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS posts (
    post_title          TEXT,
    post_text           TEXT,
    blog_id             TEXT,
    user_id             INTEGER,
    post_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    last_date_edited    DATE DEFAULT CURRENT_TIMESTAMP
);
"""

class BlogManager:
    def __init__(self, db_file):
        """
        connects to database (db), if none exists, creates one
        """
        self.con = sqlite3.connect("blogs.db") # change to 'sqlite:///your_filename.db'
        self.cur = self.con.cursor()

    def setup(self):
        """
        setup database - create the blogs table, and the posts table
        """
        self.cur.executescript(SETUP)

    def check_blogname_exists(self, new_blogname, user_id, postname, post_content):
        """
        check if blog title exists in user's blogs, if not then run add_blog_w_starter_post
        """
        self.cur.execute(f"SELECT blogname FROM blogs WHERE user_id LIKE '{user_id}%'")
        blognames = self.cur.fetchall()
        if new_blogname in blognames:
            return True
        return False

    def add_blog_w_starter_post(self, blogname, user_id, postname, post_content):
        """
        add a blog and return blog id
        """
        self.cur.execute("INSERT INTO blogs(blog_title, user_id) VALUES(?,?)", [blogname, user_id])
        self.cur.execute(f"SELECT blog_id FROM blogs WHERE blog_title LIKE '{blogname}%' AND user_id LIKE '{user_id}%'")
        blog_id = self.cur.fetchone()
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id[0], user_id])

    def repr_blog(self, blog_id):
        self.cur.execute(f'SELECT post_text FROM posts WHERE blog_id={blog_id}') #currently equal to 1, needs to change
        postList = self.cur.fetchall()
        return postList

    def add_post(self, blog_id, postname, post_content, user_id):
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id, user_id])

    def close(self):
        """
        commit changes and close cursor.
        """
        print("Closing BlogDB... ")
        self.con.commit()
        self.con.close()

    def __del__(self):
        """
        make sure db is closed
        """
        self.close()
        print("BlogDB Closed")

blog_manager=BlogManager("discobandit.db")
blog_manager.setup()
blog_manager.add_blog_w_starter_post("testblog", 12345678, "testpost", "blahblahblahblah")