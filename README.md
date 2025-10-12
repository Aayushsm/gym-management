# FitLife Gym Management System

A comprehensive web-based gym management system built with Flask, MongoDB, and AI-powered features. The system supports both gym members and administrative staff with role-based access control.

## Features

### Authentication & User Management
- Role-based authentication for gym members and admin staff
- Member registration with automatic signup fee (₹2,000)
- Admin/staff registration without membership fees
- Secure login/logout with password hashing and session management
- Profile management for all users

### Admin Dashboard Features
- Real-time analytics for members, attendance, and revenue
- Member management: add, view, edit, and delete member accounts
- Attendance tracking with daily check-in and duplicate prevention
- Payment processing for renewals and additional payments
- Advanced search by ID, name, or email
- Reports and analytics: monthly statistics and attendance trends
- Membership expiry alerts

### Member Dashboard Features
- Personal dashboard with activity overview
- Attendance charts (monthly gym visits)
- Membership status and renewal alerts
- Activity history (check-ins and payment history)

### AI-Powered Workout Planner
- Google Gemini integration for personalized workout plans
- Goal-specific training: Fat Loss, Muscle Gain, Strength, Endurance
- Experience levels: Beginner, Intermediate, Advanced
- Equipment customization: Full gym, bodyweight
- Detailed plans with exercises, sets, reps, rest periods
- Nutrition guidance and progress tracking
- Plan storage and retrieval

### Interactive Chatbot Assistant
- Rule-based chatbot for gym information (members only)
- Quick replies for common questions
- Help with membership, facilities, schedules, training, and search

### Modern UI/UX
- Responsive design (Bootstrap 5)
- Custom styling with professional gym-themed design
- Interactive charts (Chart.js)
- Flash messages for user feedback
- Font Awesome icons

### Indian Rupee Integration
- All pricing in Indian Rupees (₹)
- Membership pricing:
  - 1 Month: ₹2,500
  - 3 Months: ₹7,000
  - 6 Months: ₹12,500
  - 12 Months: ₹22,500
- Signup fee: ₹2,000 (members only)
- Personal training: ₹1,000/session

### Database Integration
- MongoDB collections:
  - `members` - User accounts with role-based access
  - `payments` - Transaction records and renewals
  - `attendance` - Check-in tracking with timestamps
  - `workout_plans` - AI-generated fitness plans

### Security Features
- Password hashing (Werkzeug)
- Role-based route protection
- Session management (Flask-Login)
- Input validation

### Reports & Export
- Monthly statistics, expiring memberships, recent payments, attendance trends
- Export reports as CSV or PDF (admin/staff only)

## Planned Features

- Payment gateway integration for online payments

## Tech Stack

- Backend: Python 3.8+ / Flask
- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5
- Database: MongoDB with PyMongo
- AI Integration: Google Gemini 2.5 Flash API
- Authentication: Flask-Login
- Charts: Chart.js
- Icons: Font Awesome 6

## Project Structure

```
gym-management/
├── app.py                     # Main Flask application
├── auth.py                    # Authentication blueprint
├── config.py                  # Configuration settings
├── database_connectivity.py   # MongoDB operations
├── models.py                  # Data models
├── workout_planner.py         # AI workout generation
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── static/                    # Static assets
│   ├── css/
│   │   └── chatbot.css
│   ├── js/
│   │   └── chatbot.js
│   └── styles.css
└── templates/                 # HTML templates
    ├── base.html
    ├── dashboard.html
    ├── member_dashboard.html
    ├── workout_planner.html
    ├── login.html
    ├── register.html
    └── [other templates]
```

## Development Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB 4.0 or higher
- Google Gemini API Key

### Installation

1. Clone the repository
    ```bash
    cd gym-management
    ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables
    ```bash
    cp .env.example .env
    # Edit .env and add your Google Gemini API key
    ```

4. Start MongoDB
    ```bash
    sudo systemctl start mongod
    ```

5. Run the application
    ```bash
    python app.py
    ```

6. Access the application
    - Open `http://localhost:5000` in your browser
    - Register as admin or member
    - Explore the features

## License

MIT License - Feel free to use and modify for your gym management needs.
