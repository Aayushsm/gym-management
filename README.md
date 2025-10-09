# Gym Management System

A modern web-based gym management system built with Flask and MongoDB.

## Features

- 💪 Member Management Dashboard
- 🔐 User Authentication
- 📊 Member Statistics
- 💬 Interactive Chatbot Assistant
- 📅 Attendance Tracking (planned)
- 💰 Payment Management (planned)
- 📈 Reports and Analytics (planned)

## Project Structure

```
gym-management/
├── app.py                  # Main Flask application with routes
├── auth.py                 # Authentication logic and user management
├── config.py               # Configuration settings for different environments
├── database_connectivity.py # MongoDB database operations and connectivity
├── models.py               # Data models for Member, Payment, and Attendance
├── requirements.txt        # Python dependencies
├── static/                 # Static assets directory
│   ├── css/
│   │   └── chatbot.css     # Chatbot styling
│   └── js/
│       └── chatbot.js      # Chatbot functionality
└── templates/              # HTML templates directory
    └── dashboard.html      # Main dashboard template with gym statistics and charts
```

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MongoDB with Flask-PyMongo
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Authentication**: Flask-Login

## Database Structure

The application uses MongoDB with the following collections:

- **members**: Stores member information (name, email, phone, join date, expiration date)
- **payments**: Records payment transactions (member_id, amount, payment_type, date)
- **attendance**: Tracks gym check-ins (member_id, check_in_time)

## Development Setup

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
