# FitLife Gym Management System

A comprehensive web-based gym management system built with Flask, MongoDB, and AI-powered features. The system supports both gym members and administrative staff with role-based access control.

## 🌟 Features

### Completed Features ✅

#### **Authentication & User Management**
- 🔐 **Role-Based Authentication** - Separate login/registration for gym members and admin staff
- 👥 **Member Registration** - Public registration with automatic signup fee (₹2,000) for members only
- 👨‍💼 **Admin Registration** - Staff account creation without membership fees
- 🔄 **Secure Login/Logout** - Password hashing and session management
- ✏️ **Profile Management** - Users can update their personal information

#### **Admin Dashboard Features**
- 📊 **Comprehensive Analytics** - Real-time stats for members, attendance, and revenue
- 👥 **Member Management** - Add, view, edit, and delete member accounts
- 🏃‍♂️ **Attendance Tracking** - Daily check-in system with duplicate prevention
- 💰 **Payment Processing** - Membership renewals and additional payments
- 🔍 **Advanced Search** - Find members by ID, name, or email
- 📈 **Reports & Analytics** - Monthly statistics and attendance trends
- ⏰ **Membership Expiry Alerts** - Track and notify expiring memberships

#### **Member Dashboard Features**
- 🏠 **Personal Dashboard** - Member-specific view with activity overview
- 📊 **Attendance Charts** - Visual representation of monthly gym visits
- 💳 **Membership Status** - View expiration dates and renewal alerts
- 📅 **Activity History** - Track check-ins and payment history

#### **AI-Powered Workout Planner**
- 🤖 **Google Gemini Integration** - AI-generated personalized workout plans
- 🎯 **Goal-Specific Training** - Fat Loss, Muscle Gain, Strength, Endurance
- 💪 **Experience Levels** - Beginner, Intermediate, Advanced programs
- 🏋️ **Equipment Customization** - Full gym, bodyweight, home gym options
- 📝 **Detailed Plans** - Complete with exercises, sets, reps, rest periods
- 🥗 **Nutrition Guidance** - AI-generated nutrition tips and tracking advice
- 💾 **Plan Storage** - Save and retrieve workout plans from database

#### **Interactive Chatbot Assistant**
- 💬 **Smart Chatbot** - Rule-based AI assistant for gym information
- ❓ **Quick Replies** - Fast access to common questions
- 📋 **Comprehensive Help** - Membership info, facilities, schedules, training
- 🔍 **Member Search Assistance** - Guide users through search functionality

#### **Modern UI/UX**
- 📱 **Responsive Design** - Mobile-friendly Bootstrap 5 interface
- 🎨 **Custom Styling** - Professional gym-themed design with animations
- 📊 **Interactive Charts** - Chart.js integration for data visualization
- 🔔 **Flash Messages** - User feedback for all actions
- 🌐 **Font Awesome Icons** - Professional iconography throughout

### **Indian Rupee Integration**
- 💱 **Currency Support** - All pricing in Indian Rupees (₹)
- 💰 **Membership Pricing**:
  - 1 Month: ₹2,500
  - 3 Months: ₹7,000
  - 6 Months: ₹12,500
  - 12 Months: ₹22,500
- 💳 **Signup Fee**: ₹2,000 (members only, not applied to admin accounts)

### **Database Integration**
- 🗄️ **MongoDB Collections**:
  - `members` - User accounts with role-based access
  - `payments` - Transaction records and renewals
  - `attendance` - Check-in tracking with timestamps
  - `workout_plans` - AI-generated fitness plans

### **Security Features**
- 🔒 **Password Security** - Werkzeug password hashing
- 🛡️ **Access Control** - Role-based route protection
- 🔐 **Session Management** - Flask-Login integration
- ✅ **Input Validation** - Form validation and sanitization

## 🚧 Planned Features (Future Development)

1. **Advanced Reporting**
   - Revenue analytics and forecasting
   - Member retention statistics
   - Equipment usage tracking

2. **Class Management**
   - Group fitness class scheduling
   - Instructor management
   - Class booking system

3. **Mobile App**
   - Native mobile application
   - QR code check-ins
   - Push notifications

4. **Equipment Management**
   - Equipment maintenance tracking
   - Usage analytics
   - Booking system for equipment

5. **Advanced AI Features**
   - Progress tracking with AI insights
   - Nutrition plan generation
   - Injury prevention recommendations

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ / Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MongoDB with PyMongo
- **AI Integration**: Google Gemini 2.5 Flash API
- **Authentication**: Flask-Login with password hashing
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6

## 📁 Project Structure

```
gym-management/
├── app.py                     # Main Flask application
├── auth.py                    # Authentication blueprint
├── config.py                  # Configuration settings
├── database_connectivity.py   # MongoDB operations
├── models.py                  # Data models
├── workout_planner.py         # AI workout generation
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
├── static/                   # Static assets
│   ├── css/
│   │   └── chatbot.css      # Chatbot styling
│   ├── js/
│   │   └── chatbot.js       # Chatbot functionality
│   └── styles.css           # Main stylesheet
└── templates/                # HTML templates
    ├── base.html            # Base template
    ├── dashboard.html       # Admin dashboard
    ├── member_dashboard.html # Member dashboard
    ├── workout_planner.html # AI workout planner
    ├── login.html           # Login page
    ├── register.html        # Registration page
    └── [other templates]    # Various feature pages
```

## 🚀 Development Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB 4.0 or higher
- Google Gemini API Key

### Installation

1. **Clone the repository**
```bash
cd gym-management
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

4. **Start MongoDB**
```bash
sudo systemctl start mongod
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
- Open `http://localhost:5000` in your browser
- Register as admin or member
- Explore the features!

## 💳 Pricing Structure

### Membership Plans (Monthly)
- **Basic**: ₹750/month - Gym access + fitness assessment
- **Premium**: ₹1,250/month - Gym + classes + locker
- **Elite**: ₹2,000/month - All features + personal training

### One-time Fees
- **Signup Fee**: ₹2,000 (members only)
- **Personal Training**: ₹1,000/session

### Renewal Discounts
- 3 months: ₹7,000 (save ₹500)
- 6 months: ₹12,500 (save ₹2,500)
- 12 months: ₹22,500 (save ₹7,500)

## 🎯 Current Status

**Version**: 1.0 Beta
**Status**: Feature-complete MVP with AI integration
**Last Updated**: December 2024

The system is production-ready for small to medium-sized gyms with all core features implemented and tested.

## 📄 License

MIT License - Feel free to use and modify for your gym management needs.
