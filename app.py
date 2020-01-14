from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import urllib, json, sqlite3

from util.user import User
from util.post import Post
from util.qaf import Qaf
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

@app.route('/shop')
def shop():
    return render_template("shop.html", current_user = current_user())

@app.route('/welcome')
def welcome():
    if current_user() == None:
        return redirect('/home')
    qafs_joined = current_user().qafs_joined.split(',')[:-1]
    qaf_list = [Qaf(qaf_id) for qaf_id in qafs_joined]
    return render_template("home.html", current_user = current_user(), qaf_list = qaf_list)

@app.route('/logout')
def logout():
    session.clear()
    flash('You were successfully logged out.', 'alert-success')
    return redirect('/')

@app.route('/home')
def home():
    return render_template("index.html", title = "WELCOME TO QAFFLE", current_user = current_user())

@app.route('/my_posts')
def my_posts():
    if current_user() == None: # have to be logged in to make an entry
      flash('You must be logged in to access this page', 'warning')
      return redirect( url_for( 'login'))
    return render_template("my_posts.html", title = "My Posts", current_user = current_user())

@app.route('/create_qaf', methods=['GET', 'POST'])
def create_qaf():
    if current_user() == None: # have to be logged in to make an entry
        flash('You must log in to access this page')
        return redirect( url_for( 'login'))
    if (request.form):
        entry = request.form
        new_qaf = Qaf.new_qaf(entry['name'], current_user().id)
        current_user().join_qaf(new_qaf)
        flash("QAF created successfully")
        return redirect(url_for('welcome'))
    return render_template('create_qaf.html', title = "Create QAF", current_user = current_user())

@app.route("/settings")
def settings():
    return render_template('settings.html');

@app.route("/qaf/<id>", methods=['GET', 'POST'])
def show_qaf(id):
    qaf = Qaf(id)
    posts = qaf.get_posts()
    return render_template('qaf.html', title = qaf.name,current_user = current_user(), qaf = qaf, posts = posts)

@app.route("/qaf/<id>/create_post", methods=['GET', 'POST'])
def create_post(id):
    if current_user() == None: # have to be logged in to make an entry
        flash('You must log in to access this page')
        return redirect( url_for( 'login'))
    if (request.form):
        entry = request.form
        Post.new_post(current_user().id,entry['title'],entry['content'],id)
        return redirect("/qaf/"+str(id))
    return render_template("create_post.html", title = "Create Post", current_user = current_user())

@app.route("/qaf/<qaf_id>/<post_id>", methods=['GET', 'POST'])
def show_post(qaf_id,post_id):
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if form was submitted
    if(current_user()):
        return redirect('/welcome');
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

        #TODO:Update the 'danger' and 'success' tags for foundation (not bootstrap)

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
