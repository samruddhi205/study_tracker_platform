# Study Tracker

Study Tracker is a Flask-based web application that helps students organise their studies, track learning time, set goals, manage notes, and connect with friends.

## Features

- User registration and secure login
- Personal study dashboard with progress analytics
- Add, edit, and delete subjects
- Track study sessions and duration
- Set daily, weekly, or monthly study goals
- Create reminders for important study tasks
- Add notes and upload attachments
- Share notes with friends
- Send and accept friend requests
- Chat with accepted friends
- Give ratings and feedback
- Admin dashboard for managing users and viewing student progress

## Built With

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- SQLite
- HTML, CSS, JavaScript

## Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd study_tracker
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

5. Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Sample Data

To add sample users, subjects, study sessions, goals, and reminders:

```bash
python seed.py
```

Sample student login:

```text
Email: alice@example.com
Password: password123
```

Sample admin login:

```text
Email: admin@studytrack.com
Password: admin123
```

You can also add Indian student sample data:

```bash
python seed_indian_data.py
```

Sample login:

```text
Email: rahul@gmail.com
Password: 1234
```

> Note: The seed scripts reset the database before adding sample data.

## Project Structure

```text
study_tracker/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── templates/
├── static/
├── seed.py
├── seed_indian_data.py
├── add_sample_activities.py
├── make_friends.py
├── schema.sql
└── sample_data.sql
```

## Future Improvements

- Email notifications for reminders
- Password reset functionality
- Better charts and reports
- Mobile-responsive enhancements
- Cloud database deployment
- Real-time chat updates

## License

This project is created for educational purposes.
