import os
import random
from datetime import datetime, timedelta
from app import app, db
from models import User, Subject, Session, Goal, Friend, Reminder, Rating, Note

def add_presentation_data():
    with app.app_context():
        # Get users
        rahul = User.query.filter_by(email='rahul@gmail.com').first()
        priya = User.query.filter_by(email='priya@gmail.com').first()
        amit = User.query.filter_by(email='amit@gmail.com').first()
        samruddhi = User.query.filter_by(email='samruddhiwalunj1605@gmail.com').first()
        
        users_to_add_activity = [u for u in [rahul, priya, amit, samruddhi] if u is not None]
        
        if not users_to_add_activity:
            print("Could not find primary users to mock data.")
            return

        print("Adding sample activities (Sessions, Notes, Goals) for presentation...")
        
        today = datetime.utcnow()
        
        # 1. Add recent sessions for a rich graph
        for user in users_to_add_activity:
            # Let's ensure the user has subjects
            subjects = Subject.query.filter_by(user_id=user.user_id).all()
            if not subjects:
                # Add default subject
                s = Subject(user_id=user.user_id, subject_name='General presentation demo', description='Mock subject for presentation')
                db.session.add(s)
                db.session.commit()
                subjects = [s]
            
            # Add 5-7 sessions over the past 3 days to populate charts
            for i in range(7):
                days_ago = random.randint(0, 3)
                start_hour = random.randint(8, 20)
                duration = random.choice([30, 45, 60, 90, 120])
                start_time = today - timedelta(days=days_ago)
                start_time = start_time.replace(hour=start_hour, minute=0, second=0, microsecond=0)
                end_time = start_time + timedelta(minutes=duration)
                
                subject = random.choice(subjects)
                
                sess = Session(
                    user_id=user.user_id,
                    subject_id=subject.subject_id,
                    start_time=start_time,
                    end_time=end_time,
                    duration_minutes=duration,
                    status='completed'
                )
                db.session.add(sess)

            # Add an active session
            active_sess = Session(
                user_id=user.user_id,
                subject_id=subjects[0].subject_id,
                start_time=today - timedelta(minutes=45),
                end_time=None,
                duration_minutes=0,
                status='active'
            )
            try:
                # Catch integrity errors in case there's constraints on active sessions, just to be safe
                db.session.add(active_sess)
            except:
                db.session.rollback()

        # 2. Add some notes to show the note feature is active
        test_notes_data = [
            ("Machine Learning Overview", "ML involves algorithms that parse data, learn from that data, and then apply what they've learned to make informed decisions."),
            ("Python Data Structures", "Lists are mutable, tuples are immutable. Dictionaries use hash tables for O(1) lookups."),
            ("Important deadlines", "- Submit project by Friday\n- Prepare slides for weekend demo")
        ]
        
        mock_notes = []
        if rahul:
            for title, content in test_notes_data:
                note = Note(
                    user_id=rahul.user_id,
                    title=title,
                    content=content,
                    is_shared=False,
                    created_at=today - timedelta(hours=random.randint(1, 48))
                )
                db.session.add(note)
                mock_notes.append(note)
                
        # 3. Add more Goals
        for user in users_to_add_activity:
            goal1 = Goal(user_id=user.user_id, goal_type='daily', target_hours=5.0, status='active')
            goal2 = Goal(user_id=user.user_id, goal_type='weekly', target_hours=30.0, status='pending')
            db.session.add_all([goal1, goal2])
        
        # Finally commit all
        db.session.commit()

        # 4. Share some notes
        from models import SharedNote
        if rahul and priya and mock_notes:
            sn = SharedNote(note_id=mock_notes[0].note_id, user_id=priya.user_id)
            db.session.add(sn)
            db.session.commit()

        print("Sample data successfully added for presentation showcase!")

if __name__ == '__main__':
    add_presentation_data()
