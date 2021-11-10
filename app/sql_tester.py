#a Python script for interacting with an SQLite db:
import sqlite3 #enable SQLite operations
import blogsdb
#open db if exists, otherwise create
db = sqlite3.connect("blogs.db") 

cur = db.cursor() #facilitate db ops

#blog_manager=blogsdb.BlogManager("blogs.db")
#blog_manager.add_blog_w_starter_post("newblogname", "84E2D0F4CAC38AAA", "oldpostname", "oldpostcontent")

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