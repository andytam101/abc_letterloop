from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, DateTime

db = SQLAlchemy()

class User(db.Model):
    userId = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String, nullable=False)
    email = db.Column(String, nullable=False, unique=True)
    password = db.Column(String, nullable=False)
    replied = db.Column(Boolean, nullable=False)
    asked = db.relationship('Question', backref='user', lazy=False)
    answered = db.relationship('Answer', backref='user', lazy=False)

class Question(db.Model):
    quesId = db.Column(Integer, primary_key=True)
    content = db.Column(String, nullable=False)
    issueId = db.Column(Integer, db.ForeignKey('issue.issueId'), nullable=False)
    userId = db.Column(Integer, db.ForeignKey('user.userId'), nullable=False)
    answer_to = db.relationship('Answer', backref='question', lazy=False)

class Issue(db.Model):
    issueId = db.Column(Integer, primary_key=True)
    theme = db.Column(String)
    q_dl = db.Column(DateTime, nullable=False)
    a_dl = db.Column(DateTime, nullable=False)
    userId = db.Column(Integer, db.ForeignKey('user.userId'))
    questions = db.relationship('Question', backref='issue', lazy=False)

class Answer(db.Model):
    answerId = db.Column(Integer, primary_key=True)
    content = db.Column(String, nullable=False)
    userId = db.Column(Integer, db.ForeignKey('user.userId'), nullable=False)
    quesId = db.Column(Integer, db.ForeignKey('question.quesId'), nullable=False)
    