"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Create user profiles for blogly site """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False, default='')
    image_url = db.Column(db.String, nullable=False, default='')
    posts = db.relationship("Post", backref="user")

    def __repr__(self):
        """ representation of instances """

        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

    @property
    def full_name(self):
        """ return a full name string """
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """ Create Blog Posts for users"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)