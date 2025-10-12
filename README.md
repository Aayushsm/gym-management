# Gym Management System

A modern web-based gym management system built with Flask, MongoDB, and AI-powered features.

## Features

- 💪 Member Management Dashboard
- 🔐 User Authentication
- 🤖 AI-Powered Workout Planner
  - Personalized workout plans using Google Gemini 2.5 Flash AI
  - Goal-specific training (Fat Loss, Muscle Gain, Strength, Endurance)
  - Experience-level adjustments (Beginner, Intermediate, Advanced)
  - Equipment-based customization (Full Gym, Home Gym, Bodyweight)
  - Weekly schedule with detailed exercises, sets, reps, and rest periods
  - Nutrition tips and progress tracking guidance
  - MongoDB storage for saved workout plans
- 📊 Member Statistics
- 💬 Interactive Chatbot Assistant
- 📅 Attendance Tracking (planned)
- 💰 Payment Management (planned)
- 📈 Reports and Analytics (planned)

## Project Structure

```
gym-management/
├── app.py # Main Flask application with routes
├── auth.py # Authentication logic and user management
├── config.py # Configuration settings
├── database_connectivity.py # MongoDB database operations
├── models.py # Data models for Member, Payment, Attendance
├── workout_planner.py # AI workout planner module (Gemini API)
├── requirements.txt # Python dependencies
├── .env # Environment variables (API keys) - DO NOT COMMIT
├── .gitignore # Git ignore rules
├── static/ # Static assets directory
│ ├── css/
│ │ └── chatbot.css # Chatbot styling
│ └── js/
│ └── chatbot.js # Chatbot functionality
└── templates/ # HTML templates directory
├── dashboard.html # Main dashboard with statistics and charts
└── workout_planner.html # AI workout planner page statistics and charts
```

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MongoDB with Flask-PyMongo
- **AI**: Google Gemini 2.5 Flash API
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Authentication**: Flask-Login

## Database Structure

The application uses MongoDB with the following collections:

- **members**: Stores member information (name, email, phone, join_date, expiration_date)
- **payments**: Records payment transactions (member_id, amount, payment_type, date)
- **attendance**: Tracks gym check-ins (member_id, check_in_time)
- **workout_plans**: Stores AI-generated workout plans (member_id, user_inputs, workout_plan, created_at)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB 4.0 or higher
- Google Gemini API Key (free - get it at https://aistudio.google.com/apikey)

1. Clone the repository:
```bash
git clone <repository-url>
cd gym-management
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure MongoDB is installed and running:
```bash
# Check MongoDB status
sudo systemctl status mongod

# If not running, start MongoDB
sudo systemctl start mongod
```

4. Run the development server:
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Current Status

- ✅ Basic project structure
- ✅ Frontend dashboard template
- ✅ Chatbot implementation
- ✅ Authentication blueprint
- ✅ MongoDB database integration
- 🚧 Member management features (in progress)
- 🚧 Payment system (pending)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License
