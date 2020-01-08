#JoseMAD
# Michael "Bob" Zhang
# Michael "William" Lin
# Pratham Rawat
# Jesse "McCree" Chen

import sqlite3   #enable control of an sqlite database
import csv

DB_FILE= "data/foldoverdata.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#================================================

# tables

#================================================
db.commit()
db.close()