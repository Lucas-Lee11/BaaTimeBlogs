# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3

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

    def setup(self):
        """
        setup database - create the blogs table, and the posts table
        """

    def get_story(self):
        """
        return visual representation of blog
        """

    def add_story(self):
        """
        add a db and return blog id
        """

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