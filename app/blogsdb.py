# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3

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

class Blog_DB:
    class Blog:
        def __init__(self, db, keys, values):
            self.db = db
            self.keys = keys
            self.values = list(values)
            #need a way to acces columns
        
        def __repr__(self):
            """
            string represenation of blog objs
            """

        def repr_blog(self):
            """
            returns full blog text - all posts
            """

        def add_post(self, author_id, post):
            """
            add post to blog
            """

        def update(self):
            """
            requests data from database for updating
            """
    
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

    def get_blog(self, db, userid, blog):
        """
        return visual representation of blog
        """
        self.cur.execute("")

    def add_blog_w_starter_post(self, blogname, user_id, postname, post_content):
        """
        add a blog and return blog id
        """
        self.cur.execute("INSERT INTO blogs(blog_title, user_id) VALUES(?,?)", [blogname, user_id])
        self.cur.execute("SELECT blog_title, user_id, blog_id FROM blogs")
        blogdata = self.cur.fetchall()
        for blog in blogdata:
            if blogname in blog and user_id in blog:
                blog_id = blog[2]
                break
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id, user_id])
        self.cur.execute("SELECT * from blogs")
        print(self.cur.fetchall())
        self.cur.execute("SELECT * from blogs")
        print(self.cur.fetchall())

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