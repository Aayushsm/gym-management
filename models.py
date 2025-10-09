from datetime import datetime, timedelta
from flask_login import UserMixin
from database_connectivity import get_member_by_id, get_member_by_email
from bson.objectid import ObjectId

class Member(UserMixin):
    def __init__(self, id, name, email, phone, password=None, join_date=None, 
                 expiration_date=None, active=True, role="member"):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.join_date = join_date or datetime.now()
        self.expiration_date = expiration_date or (self.join_date + timedelta(days=365))
        self.active = active
        self.role = role

    @staticmethod
    def get_by_id(user_id):
        # Get user from MongoDB
        user_data = get_member_by_id(user_id)
        if not user_data:
            return None
        
        return Member(
            id=str(user_data['_id']),
            name=user_data['name'],
            email=user_data['email'],
            phone=user_data['phone'],
            password=user_data.get('password'),
            join_date=user_data.get('join_date'),
            expiration_date=user_data.get('expiration_date'),
            active=user_data.get('active', True),
            role=user_data.get('role', 'member')
        )

    @staticmethod
    def get_by_email(email):
        # Get user from MongoDB
        user_data = get_member_by_email(email)
        if not user_data:
            return None
        
        return Member(
            id=str(user_data['_id']),
            name=user_data['name'],
            email=user_data['email'],
            phone=user_data['phone'],
            password=user_data.get('password'),
            join_date=user_data.get('join_date'),
            expiration_date=user_data.get('expiration_date'),
            active=user_data.get('active', True),
            role=user_data.get('role', 'member')
        )

class Payment:
    def __init__(self, member_id, amount, payment_type="membership", description="", payment_date=None, id=None):
        self.id = id
        self.member_id = member_id
        self.amount = amount
        self.payment_type = payment_type
        self.description = description
        self.payment_date = payment_date or datetime.now()
        
    @classmethod
    def from_dict(cls, payment_data):
        return cls(
            id=str(payment_data['_id']),
            member_id=str(payment_data['member_id']),
            amount=payment_data['amount'],
            payment_type=payment_data.get('payment_type', 'membership'),
            description=payment_data.get('description', ''),
            payment_date=payment_data.get('payment_date')
        )

class Attendance:
    def __init__(self, member_id, check_in_time=None, id=None):
        self.id = id
        self.member_id = member_id
        self.check_in_time = check_in_time or datetime.now()
        
    @classmethod
    def from_dict(cls, attendance_data):
        return cls(
            id=str(attendance_data['_id']),
            member_id=str(attendance_data['member_id']),
            check_in_time=attendance_data.get('check_in_time')
        )
