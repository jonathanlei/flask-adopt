"""Blogly application."""

from flask import Flask, redirect, render_template, session, request, flash
from models import User, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def send_to_users():
    """ redirects to users route """

    return redirect('/users')


@app.route('/users')
def show_users():
    """ display list of users with links to individual pages
        also have link to add user form """

    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_new_user_form():
    """ display POST form to add new user """

    return render_template('new-user.html')


@app.route('/users/new', methods=["POST"])
def new_user_submission():
    """ handle new user form submission, create new user instance
     and redirect to users page """

    first_name = request.form["first_name"]
    if not first_name:
        flash('Please enter a first name.')
        return redirect('/users/new')
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """show user information based on the id,
       redirect to 404 if id not found"""

    user = User.query.get_or_404(user_id)
    return render_template("user-info.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """ show the edit information form for the given user id"""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_info(user_id):
    """ collect form data and update user information in the database,
    redirect to user info page"""

    user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    if not first_name:
        flash('Please enter a first name.')
        return redirect(f"/users/{user_id}/edit")
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ delete a user from database and redirect to users page"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
