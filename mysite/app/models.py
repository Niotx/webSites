from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    saved_foods = db.relationship('Food', backref='user', lazy=True)
    saved_bmi = db.relationship('BMI', backref='user', lazy=True)
    saved_energy = db.relationship('Energy', backref='user', lazy=True)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class BMI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Energy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    kcal = db.Column(db.Float, nullable=False)
    kj = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
