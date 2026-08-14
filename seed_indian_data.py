import os
from flask import Flask
from datetime import datetime, timedelta
from app import app, db, bcrypt
from models import User, Admin, Subject, Session, Goal, Friend, Reminder, Rating

def seed_database():
    with app.app_context():
        # Drop and recreate all to start fresh
        db.drop_all()
        db.create_all()

        print("Creating Admin...")
        admin = Admin(
            email='admin@study.com',
            password=bcrypt.generate_password_hash('1234').decode('utf-8')
        )
        db.session.add(admin)

        print("Creating Users...")
        pass_hash = bcrypt.generate_password_hash('1234').decode('utf-8')
        users_data = [
            ('Rahul Sharma', 'rahul@gmail.com', '9876543210'),
            ('Priya Patil', 'priya@gmail.com', '9876543211'),
            ('Amit Kulkarni', 'amit@gmail.com', '9876543212'),
            ('Sneha Joshi', 'sneha@gmail.com', '9876543213'),
            ('Rohan Deshmukh', 'rohan@gmail.com', '9876543214'),
            ('Anjali Singh', 'anjali@gmail.com', '9876543215'),
            ('Vikram Kumar', 'vikram@gmail.com', '9876543216'),
            ('Pooja Patel', 'pooja@gmail.com', '9876543217'),
            ('Aditya Verma', 'aditya@gmail.com', '9876543218'),
            ('Riya Gupta', 'riya@gmail.com', '9876543219')
        ]
        
        users = []
        for name, email, phone in users_data:
            user = User(name=name, email=email, password=pass_hash, phone_no=phone, is_admin=False)
            db.session.add(user)
            users.append(user)
            
        db.session.commit()

        u1, u2, u3, u4, u5, u6, u7, u8, u9, u10 = users

        print("Creating Subjects...")
        s1 = Subject(user_id=u1.user_id, subject_name='DBMS', description='Core concepts of SQL, Normalization, and Transactions.')
        s2 = Subject(user_id=u1.user_id, subject_name='Java Programming', description='Object-Oriented Programming and advanced Java concepts.')
        s3 = Subject(user_id=u2.user_id, subject_name='Operating Systems', description='Processes, Memory Management, and Concurrency.')
        s4 = Subject(user_id=u2.user_id, subject_name='Computer Networks', description='OSI model, TCP/IP protocols, and network security.')
        s5 = Subject(user_id=u3.user_id, subject_name='Artificial Intelligence', description='Search algorithms, machine learning basics.')
        s6 = Subject(user_id=u4.user_id, subject_name='Python Programming', description='Data structures, APIs, and scripting using Python.')
        s7 = Subject(user_id=u5.user_id, subject_name='Web Development', description='HTML, CSS, JavaScript, and backend frameworks.')
        s8 = Subject(user_id=u6.user_id, subject_name='Software Engineering', description='SDLC, Agile methodologies, and project planning.')
        s9 = Subject(user_id=u7.user_id, subject_name='Machine Learning', description='Supervised vs unsupervised learning models.')
        s10 = Subject(user_id=u8.user_id, subject_name='Data Structures', description='Arrays, Linked Lists, Trees, and Graphs theory.')
        s11 = Subject(user_id=u9.user_id, subject_name='Cloud Computing', description='AWS, Azure, and Google Cloud services overview.')
        s12 = Subject(user_id=u10.user_id, subject_name='Cyber Security', description='Network vulnerabilities, cryptography, and ethical hacking.')
        
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12])
        db.session.commit()

        print("Creating Study Sessions...")
        today = datetime.utcnow()
        sessions = [
            Session(user_id=u1.user_id, subject_id=s1.subject_id, start_time=today - timedelta(days=7, hours=2), end_time=today - timedelta(days=7), duration_minutes=120, status='completed'),
            Session(user_id=u1.user_id, subject_id=s2.subject_id, start_time=today - timedelta(days=6, hours=2.5), end_time=today - timedelta(days=6), duration_minutes=150, status='completed'),
            Session(user_id=u2.user_id, subject_id=s3.subject_id, start_time=today - timedelta(days=5, hours=2), end_time=today - timedelta(days=5), duration_minutes=120, status='completed'),
            Session(user_id=u2.user_id, subject_id=s4.subject_id, start_time=today - timedelta(days=4, hours=3), end_time=today - timedelta(days=4), duration_minutes=180, status='completed'),
            Session(user_id=u3.user_id, subject_id=s5.subject_id, start_time=today - timedelta(days=3, hours=1.5), end_time=today - timedelta(days=3), duration_minutes=90, status='completed'),
            Session(user_id=u4.user_id, subject_id=s6.subject_id, start_time=today - timedelta(days=2, hours=2), end_time=today - timedelta(days=2), duration_minutes=120, status='completed'),
            Session(user_id=u5.user_id, subject_id=s7.subject_id, start_time=today - timedelta(days=1, hours=3), end_time=today - timedelta(days=1), duration_minutes=180, status='completed'),
        ]
        db.session.add_all(sessions)

        print("Creating Goals...")
        goals = [
            Goal(user_id=u1.user_id, goal_type='daily', target_hours=4.0, status='pending'),
            Goal(user_id=u2.user_id, goal_type='weekly', target_hours=20.0, status='active'),
            Goal(user_id=u3.user_id, goal_type='monthly', target_hours=80.0, status='completed'),
        ]
        db.session.add_all(goals)

        print("Creating Friendships...")
        f1 = Friend(sender_id=u1.user_id, receiver_id=u2.user_id, status='accepted')
        f2 = Friend(sender_id=u2.user_id, receiver_id=u3.user_id, status='accepted')
        f3 = Friend(sender_id=u3.user_id, receiver_id=u4.user_id, status='pending')
        f4 = Friend(sender_id=u4.user_id, receiver_id=u5.user_id, status='accepted')
        f5 = Friend(sender_id=u1.user_id, receiver_id=u5.user_id, status='accepted')
        db.session.add_all([f1, f2, f3, f4, f5])

        print("Creating Reminders and Ratings...")
        rem1 = Reminder(user_id=u1.user_id, message='Revise DBMS normal forms', time=today + timedelta(days=2))
        rat1 = Rating(user_id=u1.user_id, rating=5, feedback='Very useful app for tracking study sessions.')
        rat2 = Rating(user_id=u2.user_id, rating=4, feedback='Great interface and easy to use.')
        
        db.session.add_all([rem1, rat1, rat2])

        db.session.commit()
        print("Database seeded successfully with explicit python Flask-Bcrypt Hashes! Try logging in with: rahul@gmail.com / 1234")

if __name__ == '__main__':
    seed_database()
