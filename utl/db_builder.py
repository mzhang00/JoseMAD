#JoseMAD
# Michael "Bob" Zhang
# Michael "William" Lin
# Pratham Rawat
# Jesse "McCree" Chen

import sqlite3   #enable control of an sqlite database
import csv

DB_FILE= "qaffle_data.db"


def execute(cmd):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    output = c.execute(cmd)
    db.commit()
    return output

#================================================

# Users table
users_command = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, waffles INT, qafs_joined BLOB)"
execute(users_command)

# Posts table (per QAF)
posts_command = "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, author_id INTEGER, title TEXT, content TEXT, qaf_id INTEGER, time_created DATETIME DEFAULT CURRENT_TIMESTAMP)"
execute(posts_command)

# Comments table (per QAF post)
comments_command = "CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, author_id INTEGER, content TEXT, post_id INTEGER, qaf_id INTEGER, time_created DATETIME DEFAULT CURRENT_TIMESTAMP)"
execute(comments_command)

# QAF table (containing all QAFs)
qafs_command = "CREATE TABLE IF NOT EXISTS qafs (id INTEGER PRIMARY KEY, name TEXT, owner_id INTEGER)"
execute(qafs_command)
