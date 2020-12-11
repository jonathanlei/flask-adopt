"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
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

    posts_tags = db.relationship('PostTag', backref="post")


class Tag(db.Model):
    """ Create tags for posts """

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')


class PostTag(db.Model):
    """ Create table of posts and their tags """

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    tag = db.relationship('Tag', backref="posts_tags")


#USING IPYTHON TO SET UP POSTS, TAGS, POSTS_TAGS
# %run app.py
# User.query.get(7)
# user = User.query.get(7)
# post = Post.query.get(6)
# post2 = Post(title="TestTitle2", content="TestContent2")
# user.posts.append(post2)
# db.session.commit()
# tag = Tag(name="CodeHelpTag")
# from models import Tag
# from models import PostTag
# tag = Tag(name="CodeHelpTag")
# post
# post2
# post2.tags.append(tag)
# db.session.commit()
# post2.tags.append("joel")
# %history
# PostTag.query.all()
# %history