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
        return redirect(url_for('index'))
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Check if user already exists
        user = Member.get_by_email(email)
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
            
        # Create new user
        from database_connectivity import create_member
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        member_id = create_member(name, email, phone, password_hash)
        
        if member_id:
            flash('Registration successful! Please log in.')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.')
            
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
