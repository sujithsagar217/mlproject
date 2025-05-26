from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class UserSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sex = db.Column(db.Integer)
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    bmi = db.Column(db.Float)
    hypertension = db.Column(db.Integer)
    diabetes = db.Column(db.Integer)
    level = db.Column(db.Integer)
    fitness_goal = db.Column(db.Integer)
    fitness_type = db.Column(db.Integer)
    predicted_exercise = db.Column(db.Text)
    predicted_diet = db.Column(db.Text)
