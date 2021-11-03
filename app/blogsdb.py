# Baa Time — Alejandro Alonso, Ivan Mijacika, Theodore Fahey, Emma Buller
# SoftDev
# P00
# 2021-10-27

import sqlite3

class Blog_DB:
    class Blog:
        pass
    
    def __init__(self, db_file):
        """
        connects to database (db), if none exists, creates one
        """

    def setup(self):
        """
        setup database - create the blogs table, and the posts table
        """

    def add_story(self):
        """
        add a db and return blog id
        """

    def get_story(self):
        """
        return visual representation of blog
        """

    def close(self):
        """
        commit changes and close cursor.
        """
        print("BlogDB closing...")
        self.con.commit()
        self.con.close()

    def __del__(self):
        """
        make sure db is closed
        """
        self.close()
        print("BlogDB deleted")