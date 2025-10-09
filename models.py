from datetime import datetime, timedelta
from flask_login import UserMixin

class Member(UserMixin):
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.join_date = datetime.now()
        self.expiration_date = self.join_date + timedelta(days=365)

    @staticmethod
    def get_by_id(user_id):
        # Placeholder for database query
        return None

    @staticmethod
    def get_by_email(email):
        # Placeholder for database query
        return None

class Payment:
    def __init__(self, member_id, amount):
        self.member_id = member_id
        self.amount = amount
        self.payment_date = datetime.now()

class Attendance:
    def __init__(self, member_id):
        self.member_id = member_id
        self.check_in_date = datetime.now()
