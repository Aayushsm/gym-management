from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from models import Member
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Member.get_by_id(user_id)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        member = Member.get_by_email(email)
        
        if not member or not check_password_hash(member.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
            
        login_user(member)
        
        # Direct members to their dashboard and staff to the admin dashboard
        if hasattr(member, 'role') and member.role == 'member':
            return redirect(url_for('member_dashboard'))
        return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        # Validation
        if not all([name, email, phone, password, confirm_password, role]):
            flash('All fields are required.')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('auth.register'))
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long.')
            return redirect(url_for('auth.register'))
            
        if role not in ['member', 'admin']:
            flash('Please select a valid account type.')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        user = Member.get_by_email(email)
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
            
        # Create new user with role
        from database_connectivity import get_members_collection, get_payments_collection
        from datetime import datetime, timedelta
        
        members_col = get_members_collection()
        payments_col = get_payments_collection()
        
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        join_date = datetime.now()
        # Only members get expiration dates, admins don't expire
        expiration_date = join_date + timedelta(days=365) if role == 'member' else None
        
        member_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password_hash,
            "join_date": join_date,
            "expiration_date": expiration_date,
            "active": True,
            "role": role
        }
        
        result = members_col.insert_one(member_data)
        member_id = str(result.inserted_id)
        
        # Add initial signup fee ONLY for members, not for admins
        if role == 'member':
            payments_col.insert_one({
                'member_id': result.inserted_id,
                'amount': 2000.0,  # ₹2000 signup fee in Indian Rupees
                'payment_date': join_date,
                'note': 'Signup fee',
                'payment_type': 'signup'
            })
        
        if member_id:
            if role == 'member':
                flash('Member registration successful! Signup fee: ₹2000. Please log in.')
            else:
                flash('Admin account created successfully! Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.')
            
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('auth.login'))
