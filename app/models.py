from . import db
from datetime import datetime
from sqlalchemy import Enum

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('USER', 'ADMIN', name='user_role_types'), nullable=False, default='USER')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    train_name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    seat_count = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    booking_status = db.Column(Enum('CONFIRMED', 'PENDING', 'CANCELLED', name='booking_status_types'), default='PENDING')

    
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    train = db.relationship('Train', backref=db.backref('bookings', lazy=True))