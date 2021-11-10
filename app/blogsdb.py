
# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3

SETUP_SCRIPT = """
CREATE TABLE IF NOT EXISTS blogs (
    blog_title          TEXT,
    user_id             TEXT,
    num_blogs           INTEGER DEFAULT 1,
    blog_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
    last_edited    DATE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS posts (
    post_title          TEXT,
    post_text           TEXT,
    blog_id             TEXT,
    user_id             TEXT,
    post_id             TEXT PRIMARY KEY DEFAULT (hex(randomblob(8)))
);
"""

class BlogManager:
    def __init__(self, db_file):
        """
        connects to database (db), if none exists, creates one
        """
        self.con = sqlite3.connect(db_file,check_same_thread=False) # change to 'sqlite:///your_filename.db'
        self.cur = self.con.cursor()

    """
    begin private helper methods
    """

    def get_blogID(self, user_id, blogname):
        """
        helper method; returns blog id; requires user id and name of blog
        """
        self.cur.execute(f"SELECT blog_id FROM blogs WHERE blog_title LIKE '{blogname}%' AND user_id LIKE '{user_id}%'")
        blog_id = self.cur.fetchone()
        return blog_id[0]

    def get_postID(self, user_id, blogname, postname):
        """
        helper method; returns post id; requires user id, name of blog post is in, and name of post
        """
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute(f"SELECT post_id FROM posts WHERE blog_id LIKE '{blog_id}%' AND post_title LIKE '{postname}%'")
        post_id = self.cur.fetchone()
        return post_id[0]

    def check_name_exists(self, new_name, user_id, nametype, name_loc, postcheck):
        """
        helper method; returns True/False; see wrappers for specifications
        """
        self.cur.execute(f"SELECT {nametype} FROM {name_loc} WHERE user_id LIKE '{user_id}%'{postcheck}")
        names = [i[0] for i in self.cur.fetchall()]
        if new_name in names:
            return True
        return False

    def edit_post(self, edit_type, content, postname, user_id, blogname):
        """
        helper method; edits an existing post based on specifications; see wrappers for specifications
        """
        post_id = self.get_postID(user_id, blogname, postname)
        self.cur.execute(f"UPDATE posts SET {edit_type}='{content}' WHERE post_id LIKE '{post_id}%'")
        blog_id = self.get_blogID(user_id, blogname)
        self.update_datetime(blog_id)

    def update_datetime(self, blog_id):
        """
        helper method; edits datetime when blog or post from blog is edited; requires blog id
        """
        self.cur.execute(f"UPDATE blogs SET last_edited=datetime('now') WHERE blog_id LIKE '{blog_id}%'")

    """
    end private helper methods
    """

    def setup(self):
        """
        private method; sets up blogs and posts table in database; no parameters
        """
        self.cur.executescript(SETUP_SCRIPT)

    def check_blogname_exists(self, new_blogname, user_id):
        """
        checkname wrapper;
        checks if user already has a blog with the name they are trying to use;
        requires user id and title of blog user is trying to create;
        """
        return self.check_name_exists(new_blogname, user_id, "blog_title", "blogs", "")

    def check_postname_exists(self, new_postname, user_id, blogname):
        """
        checkname wrapper;
        checks if a post title already exists under that blog;
        requires user id, title of post user is trying to create, and name of blog post is being created in;
        """
        blog_id = self.get_blogID(user_id, blogname)
        return self.check_name_exists(new_postname, user_id, "post_title", "posts", f" AND blog_id LIKE '{blog_id}'")

    def add_blog_w_starter_post(self, blogname, user_id, postname, post_content):
        """
        public method; creates blog with one post; requires title of blog, user id, title of post, and content to be added into that post
        """
        self.cur.execute("INSERT INTO blogs(blog_title, user_id) VALUES(?,?)", [blogname, user_id])
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id, user_id])
        self.update_datetime(blog_id)

    def edit_blog_name(self, new_blogname, old_blogname, user_id):
        """
        public method; edits blog title; requires new blog title, old blog title, and user id
        """
        blog_id = self.get_blogID(user_id, old_blogname)
        self.cur.execute(f"UPDATE blogs SET blog_title='{new_blogname}' WHERE blog_id LIKE '{blog_id}%'")
        self.update_datetime(blog_id)


    def repr_blog(self, user_id, blogname):
        """
        public method; returns dictionary of post titles : post contents; requires user_id and blogname
        """
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute(f"SELECT post_title, post_text FROM posts WHERE blog_id='{blog_id}'") #currently equal to 1, needs to change
        postDict = {i[0]:i[1] for i in self.cur.fetchall()}
        return postDict

    def add_post(self, blogname, postname, post_content, user_id):
        """
        public method; adds post to existing blog; requires name of blog, title of post, content of post, and user id
        """
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute("INSERT INTO posts(post_title, post_text, blog_id, user_id) VALUES(?,?,?,?)", [postname, post_content, blog_id, user_id])
        self.cur.execute(f"UPDATE blogs SET num_blogs = num_blogs + 1 WHERE blog_id LIKE '{blog_id}%'")
        self.update_datetime(blog_id)

    def edit_post_content(self, post_content, postname, user_id, blogname):
        """
        public edit post wrapper; edits post content; requires post content, post title, user id, and blog title
        """
        self.edit_post("post_text", post_content, postname, user_id, blogname)

    def edit_post_title(self, new_postname, postname, user_id, blogname):
        """
        public edit post wrapper; edits post title; requries old post title, new post title, user id , and blog title
        """
        self.edit_post("post_title", new_postname, postname, user_id, blogname)

    def get_post_content(self, postname, user_id, blogname):
        """
        public method; return content in specified post; requires post title, user id, and blog title
        """
        post_id = self.get_postID(user_id, blogname, postname)
        self.cur.execute(f"SELECT post_text FROM posts WHERE post_id LIKE '{post_id}%'")
        content = self.cur.fetchone()
        return content[0]

    def del_post(self, blogname, postname, user_id):
        """
        public method; deletes post from existing blog; requires name of blog post is in, title of post, and user id
        """
        post_id = self.get_postID(user_id, blogname, postname)
        blog_id = self.get_blogID(user_id, blogname)
        self.cur.execute(f"DELETE FROM posts WHERE post_id LIKE '{post_id}'")
        self.cur.execute(f"UPDATE blogs SET num_blogs=num_blogs-1 WHERE blog_id LIKE '{blog_id}'") #lowers postcounter in that blog by one
        self.update_datetime(blog_id)

    def list_blogs_by_datetime(self):
        """
        public method; lists blogs based on when they were last edited; no parameters
        """
        self.cur.execute(f"SELECT blog_title, user_id FROM blogs ORDER BY datetime(last_edited) DESC")
        return [[i[0],i[1]] for i in self.cur.fetchall()]

    def close(self):
        """
        private method; commit changes and close cursor; no parameters
        """
        print("Closing BlogDB... ")
        self.con.commit()
        self.con.close()

    def __del__(self):
        """
        private method; close db; no parameters
        """
        self.close()
        print("BlogDB Closed")

#WORKS blog_manager.setup()
#WORKS blog_manager.add_blog_w_starter_post("testblog", "12345678", "blahpost", "blahblahblah")
#WORKS blog_manager.add_blog_w_starter_post("blog_for_editing", "23456789", "post_to_edit", "blahdiblah")
#WORKS blog_manager.add_post("testblog", "testpost", "it works!", "12345678")
#WORKS blog_manager.edit_post_title("timepostcheck", "blahpost", 12345678, "newblogname")
#WORKS blog_manager.edit_post_content("blahdoblah", "edited_post", 23456789, "blog_for_editing")
#WORKS print(blog_manager.get_post_content("testpost", "12345678", "testblog"))
#WORKS print(blog_manager.repr_blog("23456789", "blog_for_editing"))
#WORKS print(blog_manager.list_blogs_by_datetime())
#WORKS blog_manager.del_post("testblog", "added_post", "12345678")
#WORKS print(blog_manager.check_blogname_exists("testblog", "12345678"))
#WORKS print(blog_manager.check_postname_exists("testpost", "12345678", "testblog"))
#WORKS blog_manager.edit_blog_name("newblogname", "testblog", "12345678")
