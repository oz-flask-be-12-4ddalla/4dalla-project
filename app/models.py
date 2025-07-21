from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

def get_korea_time():
    return datetime.now().replace(tzinfo=ZoneInfo('Asia/Seoul'))

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10),nullable=False)
    age = db.Column(db.Enum('teen','twenty','thirty','forty','fifty'), nullable=False)
    gender = db.Column(db.Enum('male','female'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_korea_time)
    updated_at = db.Column(db.DateTime, default=get_korea_time, onupdate=get_korea_time)

    answers = db.relationship('Answer', backref='user', lazy=True)

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    choice_id = db.Column(db.Integer,db.ForeignKey('choices.id'))
    created_at = db.Column(db.DateTime, default=get_korea_time)
    updated_at = db.Column(db.DateTime, default=get_korea_time, onupdate=get_korea_time)


class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=get_korea_time)
    updated_at = db.Column(db.DateTime, default=get_korea_time, onupdate=get_korea_time)

    answers = db.relationship('Answer', backref='choice', lazy=True)
    question = db.relationship('Question', backref='choices', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=get_korea_time)
    updated_at = db.Column(db.DateTime, default=get_korea_time, onupdate=get_korea_time)

    image = db.relationship('Image', backref='questions', lazy=True)

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum('main','sub'), nullable=False)
    created_at = db.Column(db.DateTime, default=get_korea_time)

