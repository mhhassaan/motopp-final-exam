from flask_login import UserMixin
from motopp import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(1000))

    def __repr__(self):
        return '<User %r>' % self.email


class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    make = db.Column(db.String(1000))
    model = db.Column(db.String(1000))
    year = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('bikes', lazy=True))

    def __repr__(self):
        return '<Bike %r>' % self.name


class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    external_url = db.Column(db.String(255))

    def __repr__(self):
        return '<Part %r>' % self.name


class UserPart(db.Model):
    __tablename__ = 'users_parts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    part_id = db.Column(db.Integer)
    type = db.Column(db.String(100))

    def __repr__(self):
        return '<UserPart %r>' % self.id
