from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3
app = Flask(__name__)
DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

app.secret_key = os.urandom(32)

db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

db.execute("CREATE TABLE IF NOT EXISTS posts (username TEXT, postID INTEGER ,verID INTEGER,title TEXT,content TEXT)")

@app.route('/')

def root():
    return "hello"
# from flask import Flask , render_template,request, redirect, url_for, session, flash
# import urllib, json, sqlite3
# from json import loads
# from utl import db_builder, db_manager
# import os
# app = Flask(__name__)
# app.secret_key = os.urandom(32)
#
# DB_FILE = "trivia.db"
#
# @app.route("/")
# def root():
#     if 'username' in session:
#         return redirect('/menu')
#     return redirect('/login')
#
# @app.route('/logout')
# def logout():
#     session.pop('username')
#     session.pop('password')
#     flash('You were successfully logged out!')
#     return redirect('/')
#
# @app.route("/login")
# def login():
#     return render_template('login.html')
#
# @app.route("/auth", methods=["POST"])
# def auth():
#     enteredU = request.form['username']
#     enteredP = request.form['password']
#     if(enteredU=="" or enteredP==""):
#         flash('Please fill out all fields!', 'red')
#         return render_template("login.html")
#     if (db_manager.userValid(enteredU,enteredP)):
#         flash('You were successfully logged in!')
#         return redirect('/home')
#     else:
#         flash('Wrong Credentials!', 'red')
#         return render_template("login.html")
#
# @app.route("/home")
# def home():
#     return "LOGGED IN"
#
# @app.route("/signup")
# def signup():
#     u = urllib.request.urlopen("https://restcountries.eu/rest/v2/all")
#     response = json.loads(u.read())
#     allcountries=[]
#     for country in response:
#         allcountries.append(country['name'])
#     return render_template("signup.html",options=allcountries)
#
# @app.route("/signupcheck", methods=["POST"])
# def signupcheck():
#     username=request.form['username']
#     password=request.form['password']
#     confirm=request.form['confirmation']
#     flag=request.form['flag']
#     u = urllib.request.urlopen("https://restcountries.eu/rest/v2/all")
#     response = json.loads(u.read())
#     if(username=="" or password=="" or confirm==""):
#         flash('Please fill out all fields!', 'red')
#         return render_template("signup.html", username=username,password=password,confirm=confirm,flag=flag,options=allcountries)
#     if (confirm!=password):
#         flash('Passwords do not match!', 'red')
#         return render_template("signup.html", username=username,password=password,confirm=confirm,flag=flag,options=allcountries)
#     added = db_manager.addUser(username,password,flag)
#     if (not added):
#         flash('Username taken!', 'red')
#         return render_template("signup.html", username=username,password=password,confirm=confirm,flag=flag,options=allcountries)
#     flash('You have successfully created an account! Please log in!')
#     return redirect("/login")
