from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import urllib, json, sqlite3
from json import loads
app = Flask(__name__)
DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

app.secret_key = os.urandom(32)

@app.route("/")
def root():
    # if 'username' in session:
    #     return redirect('/menu')
    return redirect('/login')

# @app.route('/logout')
# def logout():
#     session.pop('username')
#     session.pop('password')
#     flash('You were successfully logged out!')
#     return redirect('/')

@app.route("/login")
def login():
    return render_template('login.html')

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

@app.route("/home")
def home():
    return "LOGGED IN"

@app.route("/signup")
def signup():
    # u = urllib.request.urlopen("https://restcountries.eu/rest/v2/all")
    # response = json.loads(u.read())
    # allcountries=[]
    # for country in response:
    #     allcountries.append(country['name'])
    return render_template("signup.html")

# @app.route("/signupcheck", methods=["POST"])
# def signupcheck():
#     username=request.form['username']
#     password=request.form['password']
#     confirm=request.form['confirmation']
#     response = json.loads(u.read())
#     if(username=="" or password=="" or confirm==""):
#         flash('Please fill out all fields!', 'red')
#         return render_template("signup.html", username=username,password=password)
#     if (confirm!=password):
#         flash('Passwords do not match!', 'red')
#         return render_template("signup.html", username=username,password=password)
#     added = db_manager.addUser(username,password,flag)
#     if (not added):
#         flash('Username taken!', 'red')
#         return render_template("signup.html", username=username,password=password)
#     flash('You have successfully created an account! Please log in!')
#     return redirect("/login")

if __name__ == "__main__":
    app.debug = True
    app.run()
