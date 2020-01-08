import sqlite3
from utl.db_builder import exec

#====================================================

#validates if the user exists in the database
def userValid(username,password):
    q = "SELECT username FROM user_tbl;"
    data = exec(q)
    for uName in data:
        if uName[0] == username:
            p = "SELECT password FROM user_tbl WHERE username = '" + username + "';"
            data2 = exec(p)
            for passW in data2:
                if (passW[0] == password):
                    return True
    return False

#add user-provided credentials to database
def addUser(username, password, flag):
    q = "SELECT * FROM user_tbl WHERE username = '%s';" % username
    data = exec(q).fetchone()
    if (data is None):
        q = "INSERT INTO user_tbl VALUES('%s', '%s', '', '', '', 200, \"%s\", '', 0);" % (username, password, flag)
        exec(q)
        return True
    return False #if username already exists

#turns tuple into a list
def formatFetch(results):
    collection=[]
    for item in results:
        if str(item) not in collection:
            collection.append(str(item)[2:-3])
    return collection

#====================================================
def makeDict(results):
    dictionary={}
    for pair in results:
        if(pair[0]!=None):
            if(pair[1]==None):
                value=0
            else:
                value=pair[1]
            if value not in dictionary.keys():
                list=[pair[0]]
                dictionary[value]=list
            else:
                dictionary[value].append(pair[0])
    for key in dictionary:
        dictionary[key]=sorted(dictionary[key])
    print(dictionary)
    return dictionary
