from flask_pymongo import PyMongo
from flask import current_app
from pymongo.collection import Collection
from bson.objectid import ObjectId
from datetime import datetime

# MongoDB connection instance
mongo = PyMongo()

def initialize_db(app):
    """Initialize MongoDB connection with the Flask app"""
    app.config["MONGO_URI"] = app.config.get("MONGODB_URI", "mongodb://localhost:27017/gym_management")
    mongo.init_app(app)
    return mongo.db

# Database collections
def get_members_collection() -> Collection:
    """Get the members collection from MongoDB"""
    return mongo.db.members

def get_payments_collection() -> Collection:
    """Get the payments collection from MongoDB"""
    return mongo.db.payments

def get_attendance_collection() -> Collection:
    """Get the attendance collection from MongoDB"""
    return mongo.db.attendance

# Member database operations
def create_member(name, email, phone, password_hash):
    """Create a new member in the database"""
    member_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password_hash,
        "join_date": datetime.now(),
        "expiration_date": datetime.now().replace(year=datetime.now().year + 1),
        "active": True,
        "role": "member"
    }
    
    result = get_members_collection().insert_one(member_data)
    return str(result.inserted_id)

def get_member_by_id(member_id):
    """Get member by ID from the database"""
    if not ObjectId.is_valid(member_id):
        return None
    
    member_data = get_members_collection().find_one({"_id": ObjectId(member_id)})
    return member_data

def get_member_by_email(email):
    """Get member by email from the database"""
    return get_members_collection().find_one({"email": email})

def update_member(member_id, update_data):
    """Update member information in the database"""
    if not ObjectId.is_valid(member_id):
        return False
    
    result = get_members_collection().update_one(
        {"_id": ObjectId(member_id)},
        {"$set": update_data}
    )
    
    return result.modified_count > 0

def get_all_members():
    """Get all members from the database"""
    return list(get_members_collection().find())

# Payment database operations
def record_payment(member_id, amount, payment_type="membership", description=""):
    """Record a payment in the database"""
    if not ObjectId.is_valid(member_id):
        return False
    
    payment_data = {
        "member_id": ObjectId(member_id),
        "amount": amount,
        "payment_type": payment_type,
        "description": description,
        "payment_date": datetime.now()
    }
    
    result = get_payments_collection().insert_one(payment_data)
    return str(result.inserted_id)

def get_member_payments(member_id):
    """Get all payments for a specific member"""
    if not ObjectId.is_valid(member_id):
        return []
    
    return list(get_payments_collection().find({"member_id": ObjectId(member_id)}))

# Attendance database operations
def record_attendance(member_id):
    """Record member attendance in the database"""
    if not ObjectId.is_valid(member_id):
        return False
    
    attendance_data = {
        "member_id": ObjectId(member_id),
        "check_in_time": datetime.now()
    }
    
    result = get_attendance_collection().insert_one(attendance_data)
    return str(result.inserted_id)

def get_member_attendance(member_id):
    """Get attendance records for a specific member"""
    if not ObjectId.is_valid(member_id):
        return []
    
    return list(get_attendance_collection().find({"member_id": ObjectId(member_id)}))

def get_daily_attendance(date=None):
    """Get attendance records for a specific date"""
    if date is None:
        date = datetime.now()
    
    start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0)
    end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
    
    return list(get_attendance_collection().find({
        "check_in_time": {
            "$gte": start_of_day,
            "$lte": end_of_day
        }
    }))