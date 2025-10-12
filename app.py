from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user
from config import config
import os
from database_connectivity import initialize_db, get_all_members
from auth import auth, login_manager
from workout_planner import WorkoutPlanner
from datetime import datetime
from bson.objectid import ObjectId

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

@app.route('/workout-planner')
def workout_planner_page():
    """Render workout planner page"""
    return render_template('workout_planner.html')

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

# Initialize workout planner
planner = WorkoutPlanner()

@app.route('/api/workout-planner', methods=['POST'])
def generate_workout_plan():
    """Generate AI-powered workout plan"""
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        # Generate plan using Gemini AI
        workout_plan = planner.generate_plan(data)
        print(f"Generated plan successfully")  # Debug log
        
        # Save to MongoDB
        plan_document = {
            'member_id': data.get('member_id'),
            'user_inputs': {
                'goal': data.get('goal'),
                'experience': data.get('experience'),
                'days_per_week': data.get('days_per_week'),
                'duration': data.get('duration'),
                'equipment': data.get('equipment'),
                'age': data.get('age'),
                'weight': data.get('weight'),
                'height': data.get('height'),
                'health_conditions': data.get('health_conditions', '')
            },
            'workout_plan': workout_plan,
            'created_at': datetime.utcnow(),
            'status': 'active'
        }
        
        # Insert into database
        result = db.workout_plans.insert_one(plan_document)
        print(f"Saved to DB with ID: {result.inserted_id}")  # Debug log
        
        return jsonify({
            'success': True,
            'plan': workout_plan,
            'plan_id': str(result.inserted_id)
        }), 200
        
    except Exception as e:
        print(f"ERROR in workout planner: {str(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full stack trace
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/workout-plans/<member_id>', methods=['GET'])
def get_member_plans(member_id):
    """Get all workout plans for a member"""
    try:
        plans = list(db.workout_plans.find(
            {'member_id': member_id}
        ).sort('created_at', -1))
        
        # Convert ObjectId to string
        for plan in plans:
            plan['_id'] = str(plan['_id'])
        
        return jsonify({
            'success': True,
            'plans': plans
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
