from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import backref

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(128), unique=True)
    email = db.Column(db.VARCHAR(128), unique=True)
    password = db.Column(db.VARCHAR(128))
    uploads = db.relationship('Uploads', backref='users')

    def __init__(self, username, email, password, uploads):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'{self.username}:{self.email}:{self.password}:{self.uploads}'

class Uploads(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.VARCHAR(512))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, image_url, user_id):
        self.image_url = image_url
        self.user_id = user_id

    def __repr__(self):
        return f'{self.image_url}:{self.user_id}'