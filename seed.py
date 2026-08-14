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
            email='admin@studytrack.com',
            password=bcrypt.generate_password_hash('admin123').decode('utf-8')
        )
        db.session.add(admin)

        print("Creating Users...")
        pass_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        user1 = User(name='Alice Wonderland', email='alice@example.com', password=pass_hash, phone_no='1234567890')
        user2 = User(name='Bob Builder', email='bob@example.com', password=pass_hash, phone_no='0987654321', is_admin=False)
        user3 = User(name='Charlie Chaplin', email='charlie@example.com', password=pass_hash)
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()

        print("Creating Subjects...")
        sub1 = Subject(user_id=user1.user_id, subject_name='Advanced Mathematics', description='Calculus and Linear Algebra topics.')
        sub2 = Subject(user_id=user1.user_id, subject_name='Computer Science 101', description='Intro to Python and Algorithms.')
        db.session.add_all([sub1, sub2])
        db.session.commit()

        print("Creating Goals...")
        g1 = Goal(user_id=user1.user_id, goal_type='weekly', target_hours=15.0, status='active')
        g2 = Goal(user_id=user1.user_id, goal_type='daily', target_hours=2.5, status='completed')
        db.session.add_all([g1, g2])
        
        print("Creating Study Sessions (Past 7 days)...")
        today = datetime.utcnow()
        sessions = []
        import random
        for i in range(7):
            d = today - timedelta(days=i)
            # Random 1-3 sessions per day
            for _ in range(random.randint(1, 3)):
                duration = random.randint(30, 120)
                start = d.replace(hour=random.randint(9, 20), minute=0, second=0)
                end = start + timedelta(minutes=duration)
                s = Session(
                    user_id=user1.user_id,
                    subject_id=random.choice([sub1.subject_id, sub2.subject_id]),
                    start_time=start,
                    end_time=end,
                    duration_minutes=duration,
                    status='completed'
                )
                sessions.append(s)
                
        db.session.add_all(sessions)

        print("Creating Friendships...")
        f1 = Friend(sender_id=user1.user_id, receiver_id=user2.user_id, status='accepted')
        f2 = Friend(sender_id=user3.user_id, receiver_id=user1.user_id, status='pending')
        db.session.add_all([f1, f2])

        print("Creating Reminders...")
        r1 = Reminder(user_id=user1.user_id, message='Complete CS Project', time=today + timedelta(days=2))
        db.session.add(r1)

        print("Creating Ratings...")
        rat1 = Rating(user_id=user1.user_id, rating=5, feedback='Amazing platform! Super helpful.')
        rat2 = Rating(user_id=user2.user_id, rating=4, feedback='Needs more graph types, but overall great.')
        db.session.add_all([rat1, rat2])

        db.session.commit()
        print("Database seeded successfully! Try logging in with: alice@example.com / password123")

if __name__ == '__main__':
    seed_database()
