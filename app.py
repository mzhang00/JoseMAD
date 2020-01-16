from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
import os
import urllib, json, sqlite3

from util.db_builder import execute
from util.user import User
from util.post import Post
from util.qaf import Qaf
from util.comment import Comment
from json import loads
app = Flask(__name__)

app.secret_key = os.urandom(64)

def current_user():
    if 'user_id' in session:
        return User(session['user_id'])
    return None

@app.context_processor
def make_template_globals():
    return dict(current_user=current_user())

@app.route('/')
def root():
    if current_user() != None:
        return redirect('/welcome')
    return redirect('/home')

@app.route('/shop')
def shop():
    return render_template("shop.html", title = "Shop")

@app.route('/welcome')
def welcome():
    if current_user() == None:
        return redirect('/home')
    return render_template("home.html", title = "Welcome")

@app.route('/logout')
def logout():
    session.clear()
    flash('You were successfully logged out.', 'alert-success')
    return redirect('/')

@app.route("/qafSearch")
def qafSearch():
    input = request.args.get("input", 0, type=str)
    if(input == ""):
        return jsonify(result = "");
    output = execute(f"""SELECT * FROM 'qafs' WHERE name LIKE '%{input}%';""").fetchall()
    print(output)
    return jsonify(result = output);

@app.route('/home')
def home():
    return render_template("index.html", title = "WELCOME TO QAFFLE")

@app.route('/my_posts')
def my_posts():
    if current_user() == None: # have to be logged in to make an entry
      flash('You must be logged in to access this page', 'warning')
      return redirect( url_for( 'login'))
    return render_template("my_posts.html", title = "My Posts")

@app.route("/settings", methods=['GET','POST'])
def settings():
    if current_user() == None: # have to be logged in to change settings
        flash('You must log in to access this page')
        return redirect(url_for('login'))
    form = request.form.keys()
    if 'oldpass' in form and 'newpass' in form and 'confirm' in form:
        entry = request.form
        if entry['newpass'] != entry['confirm']:
            flash("Confirmation password does not match. Please resubmit!")
        elif current_user().password != entry['oldpass']:
            flash("Old password does not match. Please resubmit!")
        else:
            current_user().change_password(entry['newpass'])
            flash("Password updated successfully!")
            return redirect(url_for('settings'))
    return render_template('settings.html', title = "Settings")

@app.route('/my_qafs')
def my_qafs():
    if current_user() == None:
      flash('You must be logged in to access this page', 'warning')
      return redirect( url_for( 'login'))
    qaf_list = current_user().get_qafs_joined()
    return render_template("my_qafs.html", title = "My Qafs", qaf_list = qaf_list)

@app.route('/create_qaf', methods=['GET', 'POST'])
def create_qaf():
    if current_user() == None:
        flash('You must log in to access this page')
        return redirect( url_for( 'login'))
    if (request.form):
        entry = request.form
        new_qaf = Qaf.new_qaf(entry['name'], current_user().id)
        current_user().join_qaf(new_qaf)
        flash("QAF created successfully")
        return redirect(url_for('my_qafs'))
    return render_template('create_qaf.html', title = "Create QAF")

@app.route("/qaf/<id>", methods=['GET', 'POST'])
def show_qaf(id):
    if current_user() == None:
      flash('You must be logged in to access this page', 'warning')
      return redirect( url_for( 'login'))
    qaf = Qaf(id)
    posts = qaf.get_posts()
    return render_template('qaf.html', title = qaf.name, qaf = qaf, posts = posts)

@app.route("/qaf/<id>/create_post", methods=['GET', 'POST'])
def create_post(id):
    if current_user() == None: # have to be logged in to make an entry
        flash('You must log in to access this page')
        return redirect( url_for( 'login'))
    if (request.form):
        entry = request.form
        Post.new_post(current_user().id,entry['title'],entry['content'],id, entry['tags'])
        return redirect("/qaf/"+str(id))
    return render_template("create_post.html", title = "Create Post")

@app.route("/qaf/<qaf_id>/<post_id>", methods=['GET', 'POST'])
def show_post(qaf_id,post_id):
    if current_user() == None:
      flash('You must be logged in to access this page', 'warning')
      return redirect( url_for( 'login'))
    if ('comment' in request.form):
        entry = request.form
        Comment.new_comment(current_user().id, entry['comment'], post_id, qaf_id)
    post = Post(post_id)
    comments = post.get_comments()
    return render_template('post.html', title = post.title, post = post, comments = comments, author = User(post.author_id).username)

# @app.route("/qaf/<qaf_id>/<post_id>/create_comment", methods=['GET', 'POST'])
# def create_comment(qaf_id,post_id):

#     return render_template('create_comment.html', title = "Create Comment", current_user = current_user(), post = post)

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
    return render_template("login.html", title = "Log In")

@app.route('/upvotePost')
def upvotePost():
    input = request.args.get("input", 0, type=str);
    print(input)
    Post(int(input)).upvoted()
    return jsonify(result = input);

@app.route('/downvotePost')
def downvotePost():
    input = request.args.get("input", 0, type=str);
    print(input)
    Post(int(input)).downvoted()
    return jsonify(result = input);

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
    return render_template('signup.html', title = 'Sign Up')

if __name__ == "__main__":
    app.debug = True
    app.run()
