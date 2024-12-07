from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import func
from .models import User, Train, Booking
from . import db, bcrypt
from flask import current_app
routes = Blueprint('routes', __name__)


@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({"message": "Username or email already exists"}), 400
    
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'], 
        email=data['email'],  
        password_hash=hashed_password, 
        role='USER'  
    )
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Registration failed", "error": str(e)}), 500

# Login User
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        # Use a dictionary with a specific structure
        token = create_access_token(identity=str(user.id))
        return jsonify({
            "access_token": token,
            "username": user.username,
            "role": user.role
        }), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Add Train (Admin Only with API Key)
@routes.route('/add_train', methods=['POST'])
def add_train():
    # Enhanced API Key verification
    api_key = request.headers.get('X-API-Key')
    if api_key != current_app.config['SECRET_KEY']:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    train = Train(
        train_name=data['train_name'], 
        
        source=data['source'],
        destination=data['destination'], 
        total_seats=data['total_seats'],
        available_seats=data['total_seats']
    )
    
    try:
        db.session.add(train)
        db.session.commit()
        return jsonify({"message": "Train added successfully.", "train_id": train.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Train addition failed", "error": str(e)}), 500

# Improved Seat Availability with Performance Optimization
@routes.route('/seat_availability', methods=['GET'])
def seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    
    # Use a more efficient query
    trains = Train.query.filter(
        Train.source == source, 
        Train.destination == destination,
        Train.available_seats > 0,
        Train.is_active == True
    ).all()
    
    return jsonify([{
        "train_id": train.id,
        "train_name": train.train_name,
        
        "available_seats": train.available_seats
    } for train in trains]), 200

# Enhanced Seat Booking with Robust Race Condition Handling
@routes.route('/book_seat', methods=['POST'])
@jwt_required()
def book_seat():
    data = request.get_json()
    train_id = data['train_id']
    seat_count = data['seat_count']
    user_id = int(get_jwt_identity())
    print(user_id)

    try:
        # Use a transaction and row-level locking
        with db.session.begin_nested():
            # Pessimistic locking with 'SELECT FOR UPDATE'
            train = Train.query.with_for_update().filter_by(id=train_id).first()
            
            if not train:
                return jsonify({"message": "Train not found"}), 404
            
            if train.available_seats < seat_count:
                return jsonify({"message": "Not enough seats available"}), 400
            
            # Atomic update of available seats
            train.available_seats -= seat_count
            
            # Create booking
            booking = Booking(
                user_id=user_id, 
                train_id=train_id, 
                seat_count=seat_count,
                booking_status='CONFIRMED'
            )
            
            db.session.add(booking)
        
        # Commit the transaction
        db.session.commit()
        
        return jsonify({
            "message": "Seat booked successfully", 
            "booking_id": booking.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Booking failed", "error": str(e)}), 500

# Get Specific Booking Details
@routes.route('/booking_details', methods=['GET'])
@jwt_required()
def booking_details():
    user_id = get_jwt_identity()["id"]
    
    bookings = Booking.query.join(Train).filter(
        Booking.user_id == user_id,
        Booking.booking_status == 'CONFIRMED'
    ).all()
    
    if not bookings:
        return jsonify({"message": "No bookings found."}), 404

    booking_list = [{
        "booking_id": booking.id,
        "train_name": booking.train.train_name,
        
        "seat_count": booking.seat_count,
        "booking_time": booking.booking_time.isoformat()
    } for booking in bookings]

    return jsonify(booking_list), 200