import datetime
import secrets
from project.server import db, bcrypt
from flask import current_app as app
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(60), default='teller', nullable=True)
    parcels = db.relationship('Parcel', backref='booked_by', lazy=True)

    def __init__(self, first_name, last_name, email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return f'Parcel dispatch by {self.first_name} {self.last_name}'


class Parcel(db.Model):
    __tablename__ = 'parcel'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item = db.Column(db.String(255), nullable=False)
    dispatch_date = db.Column(db.String(60), nullable=False)
    arrival_date = db.Column(db.String(60), nullable=True)
    delivered_date = db.Column(db.String(60), nullable=True)
    delivered = db.Column(db.Boolean, default=False, nullable=True)
    cost = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    teller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)

    def __init__(self, item, dispatch_date, arrival_date, delivered_date, delivered, sender_id, receiver_id, cost, quantity, teller_id):
        self.item = item
        self.dispatch_date = dispatch_date
        self.arrival_date = arrival_date
        self.delivered_date = delivered_date
        self.delivered = delivered
        self.cost = cost
        self.quantity = quantity
        self.teller_id = teller_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id

    def __repr__(self):
        return f'Parcel {self.item}'

class Sender(db.Model):
    __tablename__ = 'senders'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    center = db.Column(db.String(255), nullable=False)

    def __init__(self, full_name, email, center, phone):
        self.full_name = full_name
        self.email = email
        self.center = center
        self.phone = phone

    def __repr__(self):
        return f'Parcel sent by {self.full_name}'


class Receiver(db.Model):
    __tablename__ = 'receivers'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    center = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)

    def __init__(self, full_name, email, center, phone):
        self.full_name = full_name
        self.email = email
        self.center = center
        self.phone = phone

    def __repr__(self):
        return f'Parcel sent to {self.full_name}'