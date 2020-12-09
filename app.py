"""Blogly application."""

from flask import Flask, redirect, render_template, session, request, flash
from models import User, db, connect_db

app = Flask(__name__)
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
def show_add_form():
    """ display POST form to add new user """

    return render_template('new-user.html')
