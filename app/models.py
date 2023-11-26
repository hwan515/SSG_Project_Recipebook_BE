from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

bcrypt = Bcrypt()
db = SQLAlchemy()

post_liker = db.Table(
    'post_liker',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), primary_key=True)
)


comment_liker = db.Table(
    'comment_liker',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'), nullable=True)

    author = db.relationship('User', backref=db.backref('posts'))
    likers = db.relationship('User', secondary=post_liker, backref=db.backref('liked_posts'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    
    post = db.relationship('Post', backref=db.backref('comments'))
    author = db.relationship('User', backref=db.backref('comments'))
    likers = db.relationship('User', secondary=comment_liker, backref=db.backref('liked_comments'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=True)
    price = db.Column(db.Integer, unique=False, nullable=True)
    unit = db.Column(db.Integer, unique=False, nullable=True)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), unique=False, nullable=True)
    post_id = db.Column(db.Integer, nullable=False)
