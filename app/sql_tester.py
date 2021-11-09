#a Python script for interacting with an SQLite db:
import sqlite3 #enable SQLite operations

#open db if exists, otherwise create
db = sqlite3.connect("blogs.db") 

cur = db.cursor() #facilitate db ops

def tester():
    """
    add a blog and return blog id
    """
    cur.execute("SELECT * from blogs")
    print(cur.fetchall())
    cur.execute("SELECT * from posts")
    print(cur.fetchall())

tester()

db.close()