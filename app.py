from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import urllib, json, sqlite3
from util.user import User
from json import loads
app = Flask(__name__)

app.secret_key = os.urandom(64)

def current_user():
    if 'user_id' in session:
        return User(session['user_id'])
    return None

@app.route('/')
def root():
    if current_user() != None:
        return redirect('/welcome')
    return redirect('/home')

@app.route('/welcome')
def welcome():
    return render_template("home.html")

@app.route('/home')
def home():
    return render_template("index.html", title = "WELCOME TO QAFFLE", current_user = current_user())

@app.route('/my_posts')
def my_posts():
    if current_user() == None: # have to be logged in to make an entry
      flash('You must be logged in to access this page', 'warning')
      return redirect( url_for( 'login'))
    return render_template("my_posts.html", title = "My Posts", current_user = current_user())

@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if form was submitted
    form = request.form.keys()
    if 'username' in form and 'password' in form:
        # read the data from the form
        # we can use [] now since we know the key exists
        username = request.form['username']
        password = request.form['password']

        # make sure that the form data is valid
        valid = True

        to_login = User.get_user(username) # gets user object using username

        auth_valid = True

        if to_login is None: # if a user with that username doesn't exist
            flash('That username does not belong to a registered account!','danger')
            auth_valid = False
        elif to_login.password != password: # if they typed in the wrong password
            flash('Incorrect password!','danger')
            auth_valid = False

        if valid and auth_valid:
            session['user_id'] = to_login.id
            message = 'Successfully logged in'
            flash(message, 'success')
            return redirect(url_for('welcome'))
    return render_template("login.html", title = "Log In", current_user = current_user())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # check if form was submitted
    form = request.form.keys()
    if 'username' in form and 'password' in form and 'password_repeat' in form:

        # read the data from the form
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        # make sure that the form data is valid
        valid = True

        if not password == password_repeat: # if they typed in a different password in repeat
            flash('Passwords do not match!', 'danger')
            valid = False

        if not User.username_avaliable(username): # checks database if username already exists
            flash('Username already taken!', 'danger')
            valid = False

        if valid:
            User.new_user(username, password)
            flash("Account successfully created!", "success")
            return redirect('login')
    return render_template('signup.html', title = 'Sign Up', current_user = current_user())

if __name__ == "__main__":
    app.debug = True
    app.run()
