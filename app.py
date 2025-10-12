from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import config
import os
from database_connectivity import initialize_db, get_all_members, get_members_collection, get_payments_collection, get_attendance_collection
from auth import auth, login_manager
from workout_planner import WorkoutPlanner
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from models import Member, Payment, Attendance

app = Flask(__name__)
app.config.from_object(config['development'])

# Initialize database connection
db = initialize_db(app)

# Initialize database collections
members_col = get_members_collection()
payments_col = get_payments_collection()
attendance_col = get_attendance_collection()

# Initialize login manager
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Basic routes
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    # If user is a member, redirect to member dashboard
    if hasattr(current_user, 'role') and current_user.role == 'member':
        return redirect(url_for('member_dashboard'))
    
    total_members = members_col.count_documents({})
    active_members = members_col.count_documents({'expiration_date': {'$gt': datetime.now()}})
    expiring_soon = list(members_col.find({
        'expiration_date': {
            '$lte': datetime.now() + timedelta(days=30),
            '$gt': datetime.now()
        }
    }))

    # --- New: compute last 6 months attendance labels + counts ---
    def month_from_offset(dt, offset):
        # offset: negative for past months (e.g. -5..0)
        total_month = (dt.year * 12 + dt.month - 1) + offset
        y = total_month // 12
        m = total_month % 12 + 1
        return y, m

    attendance_labels = []
    attendance_data = []
    today = datetime.now()
    for offset in range(-5, 1):  # last 6 months (oldest -> newest)
        y, m = month_from_offset(today, offset)
        start = datetime(y, m, 1)
        if m == 12:
            next_start = datetime(y + 1, 1, 1)
        else:
            next_start = datetime(y, m + 1, 1)
        count = attendance_col.count_documents({
            'check_in_date': {'$gte': start, '$lt': next_start}
        })
        attendance_labels.append(start.strftime('%b %Y'))
        attendance_data.append(count)

    # --- New: build recent_activity from attendance, payments, new members ---
    recent_items = []

    # latest attendance
    for att in attendance_col.find().sort('check_in_date', -1).limit(6):
        member = members_col.find_one({'_id': att.get('member_id')})
        name = member.get('name') if member else 'Unknown'
        recent_items.append({
            'date': att['check_in_date'],
            'type': 'Check-in',
            'member_name': name,
            'action': 'checked in',
            'detail': f'{name} checked in',
            'badge': 'Check-in'
        })

    # latest payments
    for pay in payments_col.find().sort('payment_date', -1).limit(6):
        mem = None
        try:
            mem = members_col.find_one({'_id': pay.get('member_id')})
        except:
            mem = None
        name = mem.get('name') if mem else pay.get('member_name', 'Unknown')
        amount = pay.get('amount', 0)
        recent_items.append({
            'date': pay['payment_date'],
            'type': 'Payment',
            'member_name': name,
            'action': f'paid ₹{amount:.2f}',
            'detail': f'{name} paid ₹{amount:.2f}',
            'badge': 'Payment'
        })

    # latest new members
    for nm in members_col.find().sort('join_date', -1).limit(6):
        nm_name = nm.get('name', 'Unknown')
        recent_items.append({
            'date': nm['join_date'],
            'type': 'New Member',
            'member_name': nm_name,
            'action': 'joined',
            'detail': f'{nm_name} joined',
            'badge': 'New Member'
        })

    # sort by date descending and limit to 6-8 items
    recent_items.sort(key=lambda x: x['date'], reverse=True)
    recent_activity = recent_items[:6]

    return render_template('dashboard.html',
                         total_members=total_members,
                         active_members=active_members,
                         expiring_soon=expiring_soon,
                         attendance_labels=attendance_labels,
                         attendance_data=attendance_data,
                         recent_activity=recent_activity)

@app.route('/workout-planner')
@login_required
def workout_planner_page():
    """Render workout planner page"""
    return render_template('workout_planner.html')

@app.route('/members')
@login_required
def members():
    all_members = list(members_col.find())
    today = datetime.now()
    for member in all_members:
        # Check if member has an expiration date (members do, admins don't)
        if member.get('expiration_date'):
            member['renewal_needed'] = member['expiration_date'] < today + timedelta(days=30)
        else:
            # Admin users don't have expiration dates, so no renewal needed
            member['renewal_needed'] = False
    return render_template('members.html', members=all_members, now=datetime.now)

@app.route('/member_dashboard')
@login_required
def member_dashboard():
    # Restrict access to members only
    if not hasattr(current_user, 'role') or current_user.role != 'member':
        flash('Access denied. This page is for members only.')
        return redirect(url_for('index'))
        
    member = members_col.find_one({'_id': ObjectId(current_user.id)})
    
    # Ensure member has an expiration date (should always be true for members)
    if not member.get('expiration_date'):
        flash('Error: Member account missing expiration date. Please contact support.')
        return redirect(url_for('index'))
    
    # Get attendance data for chart
    attendance = list(attendance_col.find({'member_id': ObjectId(current_user.id)})
                     .sort('check_in_date', -1))
    
    # Process attendance for chart
    attendance_by_month = {}
    for record in attendance:
        month = record['check_in_date'].strftime('%Y-%m')
        attendance_by_month[month] = attendance_by_month.get(month, 0) + 1
    
    attendance_labels = list(attendance_by_month.keys())[-6:]  # Last 6 months
    attendance_data = [attendance_by_month[month] for month in attendance_labels]
    
    # Get recent activity
    recent_activity = []
    
    # Add attendance records
    for att in attendance[:5]:
        recent_activity.append({
            'date': att['check_in_date'],
            'type': 'Check-in',
            'details': 'Gym visit'
        })
    
    # Add payment records
    payments = list(payments_col.find({'member_id': ObjectId(current_user.id)})
                   .sort('payment_date', -1))
    for payment in payments[:5]:
        recent_activity.append({
            'date': payment['payment_date'],
            'type': 'Payment',
            'details': f"₹{payment['amount']:.2f} - {payment.get('note', '')}"
        })
    
    # Sort combined activity by date
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('member_dashboard.html',
                         expiration_date=member['expiration_date'],
                         renewal_needed=member['expiration_date'] < datetime.now() + timedelta(days=30),
                         attendance_labels=attendance_labels,
                         attendance_data=attendance_data,
                         recent_activity=recent_activity[:10])

@app.route('/add_member', methods=['GET', 'POST'])
@login_required
def add_member():
    # Restrict to admin/staff only
    if hasattr(current_user, 'role') and current_user.role == 'member':
        flash('Access denied. Only staff can add members.')
        return redirect(url_for('member_dashboard'))
        
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form.get('password', '')  # Password might be optional
        
        # Check if user already exists
        if members_col.find_one({'email': email}):
            flash('Email address already exists')
            return redirect(url_for('add_member'))
            
        join_date = datetime.now()
        expiration_date = join_date + timedelta(days=365)  # 1 year default
        
        password_hash = generate_password_hash(password) if password else None

        member_id = members_col.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'password': password_hash,
            'join_date': join_date,
            'expiration_date': expiration_date,
            'role': 'member',  # Always create as member through this route
            'active': True
        }).inserted_id

        # Initial signup fee for members added by staff (₹2000 in Indian Rupees)
        payments_col.insert_one({
            'member_id': member_id,
            'amount': 2000.0,
            'payment_date': join_date,
            'note': 'Signup fee',
            'payment_type': 'signup'
        })

        flash('Member added successfully! Signup fee: ₹2000 applied.')
        return redirect(url_for('members'))
    return render_template('add_member.html')

@app.route('/member/<id>')
@login_required
def member_detail(id):
    member = members_col.find_one({'_id': ObjectId(id)})
    if not member:
        flash('Member not found!')
        return redirect(url_for('members'))

    payments = list(payments_col.find({'member_id': ObjectId(id)}).sort('payment_date', -1))
    attendance = list(attendance_col.find({'member_id': ObjectId(id)}).sort('check_in_date', -1))

    # Check if renewal needed
    renewal_needed = member['expiration_date'] < datetime.now() + timedelta(days=30)  # Warn 30 days before expiry

    return render_template('member_detail.html', member=member, payments=payments, attendance=attendance, renewal_needed=renewal_needed)

@app.route('/renew/<id>', methods=['POST'])
@login_required
def renew(id):
    months = int(request.form['months'])
    member = members_col.find_one({'_id': ObjectId(id)})
    
    # Calculate price based on months (in Indian Rupees)
    prices = {1: 2500, 3: 7000, 6: 12500, 12: 22500}  # ₹2500/month base rate
    amount = prices.get(months, months * 2500)  # Default to ₹2500 per month if not in price table
    
    # Calculate new expiration date
    current_expiry = member['expiration_date']
    # If membership has expired, start from today
    if current_expiry < datetime.now():
        current_expiry = datetime.now()
    
    new_expiry = current_expiry + timedelta(days=30 * months)
    
    # Update member record
    members_col.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'expiration_date': new_expiry}}
    )
    
    # Record payment
    payments_col.insert_one({
        'member_id': ObjectId(id),
        'amount': amount,
        'payment_date': datetime.now(),
        'end_date': new_expiry,
        'note': f'{months}-month renewal',
        'payment_type': 'renewal'
    })
    
    flash(f'Membership renewed successfully for {months} months! Amount: ₹{amount}')
    return redirect(url_for('member_detail', id=id))

@app.route('/log_attendance/<id>', methods=['POST'])
@login_required
def log_attendance(id):
    attendance_col.insert_one({
        'member_id': ObjectId(id),
        'check_in_date': datetime.now(),
        'recorded_by': current_user.id,
        'recorded_by_name': current_user.name
    })
    flash('Attendance logged!')
    return redirect(url_for('member_detail', id=id))

@app.route('/attendance/<id>')
@login_required
def member_attendance(id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = {'member_id': ObjectId(id)}
    
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        query['check_in_date'] = {'$gte': start}
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if 'check_in_date' in query:
            query['check_in_date']['$lte'] = end
        else:
            query['check_in_date'] = {'$lte': end}
    
    attendance = list(attendance_col.find(query).sort('check_in_date', -1))
    member = members_col.find_one({'_id': ObjectId(id)})
    
    return render_template('member_attendance.html', 
                         attendance=attendance, 
                         member=member,
                         start_date=start_date,
                         end_date=end_date)

@app.route('/add_payment/<id>', methods=['POST'])
@login_required
def add_payment(id):
    amount = float(request.form['amount'])
    note = request.form.get('note', '')
    payment_date = datetime.now()
    
    # Record general payment (non-renewal)
    payment_id = payments_col.insert_one({
        'member_id': ObjectId(id),
        'amount': amount,
        'payment_date': payment_date,
        'note': note,
        'payment_type': 'other'  # To distinguish from renewals
    }).inserted_id
    
    if payment_id:
        flash(f'Payment of ₹{amount:.2f} recorded successfully for {note}', 'success')
    else:
        flash('Error recording payment. Please try again.', 'danger')
    
    return redirect(url_for('member_detail', id=id))

@app.route('/delete_member/<id>')
@login_required
def delete_member(id):
    members_col.delete_one({'_id': ObjectId(id)})
    payments_col.delete_many({'member_id': ObjectId(id)})
    attendance_col.delete_many({'member_id': ObjectId(id)})
    flash('Member deleted!')
    return redirect(url_for('members'))

@app.route('/check_in', methods=['GET', 'POST'])
@login_required
def check_in():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        try:
            member = members_col.find_one({'_id': ObjectId(member_id)})
            if not member:
                flash('Member not found', 'danger')
                return redirect(url_for('check_in'))
            
            # Check if THIS member has checked in today
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            existing_checkin = attendance_col.find_one({
                'member_id': ObjectId(member_id),
                'check_in_date': {
                    '$gte': today_start,
                    '$lt': today_end
                }
            })
            
            if existing_checkin:
                flash(f'Member {member["name"]} has already checked in today', 'warning')
            else:
                # Check if membership is active
                if member['expiration_date'] < datetime.now():
                    flash('Membership has expired! Please renew.', 'danger')
                else:
                    # Log attendance
                    attendance_col.insert_one({
                        'member_id': ObjectId(member_id),
                        'check_in_date': datetime.now(),
                        'recorded_by': current_user.id,
                        'recorded_by_name': current_user.name  # Add this to track who recorded
                    })
                    flash(f'Check-in recorded for {member["name"]}', 'success')
        
        except Exception as e:
            flash('Invalid member ID', 'danger')
    
    # Get today's check-ins
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    
    todays_checkins = list(attendance_col.find({
        'check_in_date': {
            '$gte': today_start,
            '$lt': today_end
        }
    }).sort('check_in_date', -1))
    
    # Get member details for each check-in
    checkins_with_members = []
    for checkin in todays_checkins:
        member = members_col.find_one({'_id': checkin['member_id']})
        if member:
            checkins_with_members.append({
                'time': checkin['check_in_date'],
                'member_name': member['name'],
                'member_id': str(member['_id']),
                'recorded_by': checkin.get('recorded_by_name', 'System')
            })
    
    return render_template('check_in.html', checkins=checkins_with_members)

@app.route('/search_member', methods=['GET'])
@login_required
def search_member():
    query = request.args.get('query', '').strip()
    members = []
    
    if query:
        # Try to find by ID first
        try:
            if len(query) == 24:  # MongoDB ID length
                member = members_col.find_one({'_id': ObjectId(query)})
                if member:
                    members = [member]
        except:
            pass
        
        # If no member found by ID, search by name or email
        if not members:
            members = list(members_col.find({
                '$or': [
                    {'name': {'$regex': query, '$options': 'i'}},
                    {'email': {'$regex': query, '$options': 'i'}}
                ]
            }))
    
    return render_template('search_member.html', members=members, query=query)

@app.route('/reports')
@login_required
def reports():
    # Get monthly statistics
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    
    monthly_stats = {
        'new_members': members_col.count_documents({'join_date': {'$gte': start_of_month}}),
        'renewals': payments_col.count_documents({
            'payment_date': {'$gte': start_of_month},
            'note': {'$regex': 'renewal', '$options': 'i'}
        }),
        'total_payments': sum(p['amount'] for p in payments_col.find({
            'payment_date': {'$gte': start_of_month}
        })),
        'attendance': attendance_col.count_documents({
            'check_in_date': {'$gte': start_of_month}
        })
    }
    
    # Get expiring memberships
    expiring_soon = list(members_col.find({
        'expiration_date': {
            '$lte': today + timedelta(days=30),
            '$gt': today
        }
    }).sort('expiration_date', 1))
    
    # Get payment history
    recent_payments = list(payments_col.find().sort('payment_date', -1).limit(10))
    
    # Get attendance trends
    attendance_data = list(attendance_col.aggregate([
        {
            '$group': {
                '_id': {
                    'year': {'$year': '$check_in_date'},
                    'month': {'$month': '$check_in_date'}
                },
                'count': {'$sum': 1}
            }
        },
        {'$sort': {'_id': 1}},
        {'$limit': 6}
    ]))
    
    return render_template('reports.html',
                         monthly_stats=monthly_stats,
                         expiring_soon=expiring_soon,
                         recent_payments=recent_payments,
                         attendance_data=attendance_data)

@app.route('/update_profile/<id>', methods=['GET', 'POST'])
@login_required
def update_profile(id):
    if request.method == 'POST':
        updates = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone']
        }
        
        if request.form.get('new_password'):
            updates['password'] = generate_password_hash(request.form['new_password'])
        
        members_col.update_one(
            {'_id': ObjectId(id)},
            {'$set': updates}
        )
        flash('Profile updated successfully!')
        return redirect(url_for('member_dashboard'))
        
    member = members_col.find_one({'_id': ObjectId(id)})
    return render_template('update_profile.html', member=member)

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
        }, 200)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.context_processor
def utility_processor():
    def today_stats():
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        try:
            total_payments = sum(p['amount'] for p in payments_col.find({
                'payment_date': {'$gte': today_start, '$lt': today_end}
            }))
        except:
            total_payments = 0

        stats = {
            'checkins': attendance_col.count_documents({
                'check_in_date': {'$gte': today_start, '$lt': today_end}
            }),
            'payments': total_payments,
            'new_members': members_col.count_documents({
                'join_date': {'$gte': today_start, '$lt': today_end}
            })
        }
        return stats
    
    return dict(today_stats=today_stats, now=datetime.now)

if __name__ == '__main__':
    app.run(debug=True)
