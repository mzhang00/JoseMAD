#JoseMAD
# Michael "Bob" Zhang
# Michael "William" Lin
# Pratham Rawat
# Jesse "McCree" Chen

import sqlite3   #enable control of an sqlite database
import csv

DB_FILE= "data/qaffle_data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#================================================

# Users table
users_command = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, waffles INT, qafs_joined BLOB)"
c.execute(users_command)

# Posts table (per QAF)
posts_command = "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, author_id INTEGER, title TEXT, content TEXT, qaf_id INTEGER, time_created BLOB)"
c.execute(posts_command)

# Comments table (per QAF post)
comments_command = "CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, author_id INTEGER, content TEXT, post_id INTEGER, qaf_id INTEGER, time_created BLOB)"
c.execute(comments_command)

# QAF table (containing all QAFs)
qafs_command = "CREATE TABLE IF NOT EXISTS qafs (id INTEGER PRIMARY KEY, name TEXT, owner_id INTEGER)"
c.execute(qafs_command)

#================================================
db.commit()
db.close()