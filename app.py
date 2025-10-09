from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from config import config
import os
from database_connectivity import initialize_db, get_all_members
from auth import auth, login_manager

app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize database connection
db = initialize_db(app)

# Initialize login manager
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Basic routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/members')
@login_required
def members():
    # Get members from database
    members_list = get_all_members()
    return render_template('members.html', members=members_list)

@app.route('/check-in')
@login_required
def check_in():
    return render_template('check_in.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True)
