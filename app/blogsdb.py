# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3

SETUP = """
CREATE TABLE IF NOT EXISTS blogs (
    blog_title          TEXT,
    user_id             TEXT,
    num_blogs           INTEGER DEFAULT 1,
    blog_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    last_date_edited    DATE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS posts (
    post_title          TEXT,
    post_text           TEXT,
    blog_id             TEXT,
    user_id             TEXT,
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

    """
    begin helper methods
    """

    def check_name_exists(self, new_name, user_id):
        """
        check if blog title exists in user's blogs, if not then run add_blog_w_starter_post
        """
        self.cur.execute(f"SELECT blogname FROM blogs WHERE user_id LIKE '{user_id}%'")
        blognames = self.cur.fetchall()
        if new_name in blognames:
            return True
        return False
    
    def check_blogname_exists(self, new_blogname, user_id):
        self.check_name_exists(new_blogname, user_id)

    def check_postname_exists(self, new_postname, user_id):
        self.check_name_exists(self, new_postname, user_id)
    
    def get_blogID(self, user_id, blogname):
        self.cur.execute(f"SELECT blog_id FROM blogs WHERE blog_title LIKE '{blogname}%' AND user_id LIKE '{user_id}%'")
        blog_id = self.cur.fetchone()
        return blog_id[0]
    
    def get_postID(self, user_id, blogname, postname):
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute(f"SELECT post_id FROM posts WHERE blog_id LIKE '{blog_id}%' AND post_title LIKE '{postname}%'")
        post_id = self.cur.fetchone()
        return post_id[0]

    """
    end helper methods
    """

    def setup(self):
        """
        setup database - create the blogs table, and the posts table
        """
        self.cur.executescript(SETUP)

    def add_blog_w_starter_post(self, blogname, user_id, postname, post_content):
        """
        add a blog and return blog id
        """
        self.cur.execute("INSERT INTO blogs(blog_title, user_id) VALUES(?,?)", [blogname, user_id])
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id[0], user_id])

    def add_post(self, blogname, postname, post_content, user_id):
        blog_id = self.get_blogID(user_id, blogname)
        print(blog_id)
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id, user_id])
    
    def get_post_content(self, postname, user_id, blogname):
        post_id = self.get_postID(user_id, blogname, postname)
        self.cur.execute(f"SELECT post_text FROM posts WHERE post_id LIKE '{post_id}%'")
        content = self.cur.fetchone()
        return content[0]

    def edit_post(self, edit_type, content, postname, user_id, blogname):
        post_id = self.get_postID(user_id, blogname, postname)
        self.cur.execute(f"UPDATE posts SET {edit_type}='{content}' WHERE post_id LIKE '{post_id}%'")

    def edit_post_content(self, post_content, postname, user_id, blogname):
        self.edit_post("post_text", post_content, postname, user_id, blogname)    

    def edit_post_title(self, new_postname, postname, user_id, blogname):
        self.edit_post("post_title", new_postname, postname, user_id, blogname)    

    def repr_blog(self, user_id, blogname):
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute(f"SELECT post_title, post_text FROM posts WHERE blog_id='{blog_id}'") #currently equal to 1, needs to change
        postDict = {i[0]:i[1] for i in self.cur.fetchall()}
        return postDict
        
    def list_blogs_by_datetime(self):
        self.cur.execute(f"SELECT * FROM blogs ORDER BY date(last_date_edited) DESC")
        return self.cur.fetchall()

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

#WORKS blog_manager.setup()
#WORKS blog_manager.add_blog_w_starter_post("testblog", "12345678", "testpost", "blahblahblahblah") 
#WORKS blog_manager.add_blog_w_starter_post("blog_for_editing", "23456789", "post_to_edit", "blahdiblah")
#WORKS blog_manager.add_post("blog_for_editing", "added_post", "it works!", "23456789")
#WORKS blog_manager.edit_post_title("edited_post", "post_to_edit", 23456789, "blog_for_editing")
#WORKS blog_manager.edit_post_content("blahdoblah", "edited_post", 23456789, "blog_for_editing")
#WORKS print(blog_manager.get_post_content("testpost", "12345678", "testblog"))
#WORKS print(blog_manager.repr_blog("23456789", "blog_for_editing"))
print(blog_manager.list_blogs_by_datetime())