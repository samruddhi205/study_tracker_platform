import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from config import Config
from models import db, User, Admin

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Support both Admin and User loading using prefix
    if str(user_id).startswith('admin_'):
        admin_id = int(str(user_id).split('_')[1])
        return Admin.query.get(admin_id)
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        password = request.form.get('password')

        # Basic validation
        if not name or not email or not password:
            flash('Please fill out required fields', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password, phone_no=phone_no)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check Admin
        admin = Admin.query.filter_by(email=email).first()
        if admin and bcrypt.check_password_hash(admin.password, password):
            login_user(admin)
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
            
        # Check User
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
            
        flash('Invalid email or password', 'danger')
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

from sqlalchemy import func
from datetime import datetime, timedelta

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    
    # Calculate stats
    total_minutes = db.session.query(func.sum(Session.duration_minutes)).filter_by(user_id=current_user.user_id).scalar() or 0
    total_hours = round(total_minutes / 60, 2)
    
    # Cleaned out unused line chart data logic
    
    # Subject Time Breakdown (Pie Chart 1)
    subject_stats = db.session.query(
        Subject.subject_name,
        func.sum(Session.duration_minutes)
    ).join(Session).filter(Session.user_id == current_user.user_id).group_by(Subject.subject_name).all()
    
    subject_labels = [s[0] for s in subject_stats]
    subject_data = [round(s[1] / 60, 2) for s in subject_stats] # in hours
    
    # Goals Breakdown (Pie Chart 2)
    active_goals = Goal.query.filter_by(user_id=current_user.user_id, status='active').count()
    completed_goals = Goal.query.filter_by(user_id=current_user.user_id, status='completed').count()
    goals_labels = ['Active', 'Completed']
    goals_data = [active_goals, completed_goals]
    
    # Recent Sessions List (Added details)
    recent_sessions = Session.query.filter_by(user_id=current_user.user_id).order_by(Session.start_time.desc()).limit(5).all()
        
    return render_template('dashboard.html', 
                          total_hours=total_hours,
                          subject_labels=subject_labels,
                          subject_data=subject_data,
                          goals_labels=goals_labels,
                          goals_data=goals_data,
                          recent_sessions=recent_sessions)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.get_id().startswith('admin_') and not getattr(current_user, 'is_admin', False):
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))
        
    users = User.query.all()
    feedbacks = Rating.query.all()
    total_sessions = Session.query.count()
    
    return render_template('admin.html', users=users, feedbacks=feedbacks, total_sessions=total_sessions)

@app.route('/admin/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if not current_user.get_id().startswith('admin_') and not getattr(current_user, 'is_admin', False):
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_user/<int:id>', methods=['POST'])
@login_required
def edit_user_admin(id):
    if not current_user.get_id().startswith('admin_') and not getattr(current_user, 'is_admin', False):
        return redirect(url_for('dashboard'))
    user = User.query.get_or_404(id)
    user.name = request.form.get('name')
    user.email = request.form.get('email')
    user.phone_no = request.form.get('phone_no')
    db.session.commit()
    flash(f'User {user.name} updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/user_progress/<int:id>')
@login_required
def admin_user_progress(id):
    if not current_user.get_id().startswith('admin_') and not getattr(current_user, 'is_admin', False):
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))
        
    user = User.query.get_or_404(id)
    
    # Calculate stats
    total_minutes = db.session.query(func.sum(Session.duration_minutes)).filter_by(user_id=id).scalar() or 0
    total_hours = round(total_minutes / 60, 2)
    
    recent_sessions = Session.query.filter_by(user_id=id).order_by(Session.start_time.desc()).limit(10).all()
    goals = Goal.query.filter_by(user_id=id).all()
    
    return render_template('admin_user_progress.html', 
                            user_detail=user, 
                            total_hours=total_hours, 
                            sessions=recent_sessions, 
                            goals=goals)


from models import db, User, Admin, Subject, Session, Goal

# --- SUBJECT MANAGEMENT ROUTES ---
@app.route('/subjects', methods=['GET', 'POST'])
@login_required
def subjects():
    if request.method == 'POST':
        subject_name = request.form.get('subject_name')
        description = request.form.get('description')
        if not subject_name:
            flash('Subject name is required', 'danger')
        else:
            new_sub = Subject(user_id=current_user.user_id, subject_name=subject_name, description=description)
            db.session.add(new_sub)
            db.session.commit()
            flash('Subject added successfully!', 'success')
        return redirect(url_for('subjects'))
        
    user_subjects = Subject.query.filter_by(user_id=current_user.user_id).all()
    return render_template('subjects.html', subjects=user_subjects)

@app.route('/subject/edit/<int:id>', methods=['POST'])
@login_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.user_id != current_user.user_id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('subjects'))
        
    subject.subject_name = request.form.get('subject_name')
    subject.description = request.form.get('description')
    db.session.commit()
    flash('Subject updated successfully', 'success')
    return redirect(url_for('subjects'))

@app.route('/subject/delete/<int:id>', methods=['POST'])
@login_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.user_id == current_user.user_id:
        db.session.delete(subject)
        db.session.commit()
        flash('Subject deleted', 'success')
    return redirect(url_for('subjects'))

# --- SESSION TRACKER ROUTES ---
@app.route('/tracker')
@login_required
def tracker():
    user_subjects = Subject.query.filter_by(user_id=current_user.user_id).all()
    recent_sessions = Session.query.filter_by(user_id=current_user.user_id).order_by(Session.start_time.desc()).limit(10).all()
    return render_template('tracker.html', subjects=user_subjects, sessions=recent_sessions)

@app.route('/api/session/save', methods=['POST'])
@login_required
def save_session():
    data = request.json
    subject_id = data.get('subject_id')
    start_time_str = data.get('start_time') # Keep simple, expects string ISO format
    end_time_str = data.get('end_time')
    duration = data.get('duration_minutes', 0)
    
    # Needs datetime parsing
    from datetime import datetime
    try:
        start_dt = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
    except Exception as e:
        return {'status': 'error', 'message': 'Invalid dates'}, 400
        
    new_session = Session(
        user_id=current_user.user_id,
        subject_id=subject_id,
        start_time=start_dt,
        end_time=end_dt,
        duration_minutes=duration,
        status='completed'
    )
    db.session.add(new_session)
    db.session.commit()
    return {'status': 'success', 'message': 'Session saved'}

# --- GOAL MANAGEMENT ROUTES ---
@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        goal_type = request.form.get('goal_type')
        target_hours = request.form.get('target_hours')
        
        if not target_hours:
            flash('Target hours are required', 'danger')
        else:
            try:
                hours = float(target_hours)
                new_goal = Goal(user_id=current_user.user_id, goal_type=goal_type, target_hours=hours)
                db.session.add(new_goal)
                db.session.commit()
                flash('Goal added!', 'success')
            except ValueError:
                flash('Invalid target hours', 'danger')
        return redirect(url_for('goals'))
        
    user_goals = Goal.query.filter_by(user_id=current_user.user_id).all()
    return render_template('goals.html', goals=user_goals)

@app.route('/goal/delete/<int:id>', methods=['POST'])
@login_required
def delete_goal(id):
    goal = Goal.query.get_or_404(id)
    if goal.user_id == current_user.user_id:
        db.session.delete(goal)
        db.session.commit()
        flash('Goal deleted', 'success')
    return redirect(url_for('goals'))

from models import Friend, Reminder, Rating

# --- FRIENDS SYSTEM ROUTES ---
@app.route('/friends', methods=['GET'])
@login_required
def friends():
    search_query = request.args.get('search', '')
    search_results = []
    if search_query:
        search_results = User.query.filter(User.email.ilike(f'%{search_query}%'), User.user_id != current_user.user_id).all()
        
    # Get friends (accepted)
    friends_list = []
    accepted_requests = Friend.query.filter(
        db.or_(Friend.sender_id == current_user.user_id, Friend.receiver_id == current_user.user_id),
        Friend.status == 'accepted'
    ).all()
    
    for req in accepted_requests:
        friends_list.append(req.receiver if req.sender_id == current_user.user_id else req.sender)
        
    # Get pending requests received
    pending_requests = Friend.query.filter_by(receiver_id=current_user.user_id, status='pending').all()
    
    return render_template('friends.html', 
                           search_results=search_results, 
                           friends_list=friends_list, 
                           pending_requests=pending_requests)

@app.route('/friend/request/<int:id>', methods=['POST'])
@login_required
def add_friend(id):
    if id == current_user.user_id:
        flash("You cannot add yourself.", "warning")
        return redirect(url_for('friends'))
        
    existing_req = Friend.query.filter(
        db.or_(
            db.and_(Friend.sender_id == current_user.user_id, Friend.receiver_id == id),
            db.and_(Friend.sender_id == id, Friend.receiver_id == current_user.user_id)
        )
    ).first()
    
    if existing_req:
        flash("Friend request already exists.", "warning")
    else:
        new_req = Friend(sender_id=current_user.user_id, receiver_id=id)
        db.session.add(new_req)
        db.session.commit()
        flash("Friend request sent!", "success")
        
    return redirect(url_for('friends'))

@app.route('/friend/accept/<int:id>', methods=['POST'])
@login_required
def accept_friend(id):
    req = Friend.query.get_or_404(id)
    if req.receiver_id == current_user.user_id:
        req.status = 'accepted'
        db.session.commit()
        flash("Friend request accepted!", "success")
    return redirect(url_for('friends'))

# --- REMINDERS ROUTES ---
@app.route('/reminders', methods=['GET', 'POST'])
@login_required
def reminders():
    if request.method == 'POST':
        message = request.form.get('message')
        reminder_time = request.form.get('time')
        
        if message and reminder_time:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(reminder_time)
                new_reminder = Reminder(user_id=current_user.user_id, message=message, time=dt)
                db.session.add(new_reminder)
                db.session.commit()
                flash('Reminder added!', 'success')
            except ValueError:
                flash('Invalid date format', 'danger')
        return redirect(url_for('reminders'))
        
    user_reminders = Reminder.query.filter_by(user_id=current_user.user_id).order_by(Reminder.time).all()
    return render_template('reminders.html', reminders=user_reminders)

@app.route('/reminder/delete/<int:id>', methods=['POST'])
@login_required
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if reminder.user_id == current_user.user_id:
        db.session.delete(reminder)
        db.session.commit()
        flash('Reminder deleted', 'success')
    return redirect(url_for('reminders'))

# --- FEEDBACK ROUTES ---
@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        rating_val = request.form.get('rating')
        text = request.form.get('feedback')
        try:
            r = int(rating_val)
            if 1 <= r <= 5:
                new_feedback = Rating(user_id=current_user.user_id, rating=r, feedback=text)
                db.session.add(new_feedback)
                db.session.commit()
                flash('Thank you for your feedback!', 'success')
        except (ValueError, TypeError):
            flash('Invalid rating', 'danger')
        return redirect(url_for('feedback'))
    return render_template('feedback.html')

from werkzeug.utils import secure_filename
from models import Note, Friend, SharedNote

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads', 'notes')

# --- NOTES ROUTES ---
@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('file')
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('notes'))
            
        file_path = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            uniq_filename = f"{current_user.user_id}_{int(datetime.utcnow().timestamp())}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq_filename)
            file.save(save_path)
            file_path = f"uploads/notes/{uniq_filename}" # relative path for static serving
            
        new_note = Note(user_id=current_user.user_id, title=title, content=content, file_path=file_path)
        db.session.add(new_note)
        db.session.commit()
        flash('Note created successfully!', 'success')
        return redirect(url_for('notes'))
        
    user_notes = Note.query.filter_by(user_id=current_user.user_id).order_by(Note.created_at.desc()).all()
    
    # Get friends for sharing modal
    friends_list = []
    accepted_requests = Friend.query.filter(
        db.or_(Friend.sender_id == current_user.user_id, Friend.receiver_id == current_user.user_id),
        Friend.status == 'accepted'
    ).all()
    
    for req in accepted_requests:
        friends_list.append(req.receiver if req.sender_id == current_user.user_id else req.sender)
        
    return render_template('notes.html', notes=user_notes, friends=friends_list)

@app.route('/note/share/<int:id>', methods=['POST'])
@login_required
def share_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id == current_user.user_id:
        friend_id = request.form.get('friend_id')
        if friend_id == 'all':
            note.is_shared = not note.is_shared
            db.session.commit()
            status = "globally shared" if note.is_shared else "globally unshared"
            flash(f'Note {status} successfully.', 'success')
        elif friend_id:
            # Check if it's an unshare request
            action = request.form.get('action')
            if action == 'unshare':
                sn = SharedNote.query.filter_by(note_id=note.note_id, user_id=friend_id).first()
                if sn:
                    db.session.delete(sn)
                    db.session.commit()
                    flash('Note unshared with friend.', 'success')
            else:
                existing = SharedNote.query.filter_by(note_id=note.note_id, user_id=friend_id).first()
                if not existing:
                    sn = SharedNote(note_id=note.note_id, user_id=friend_id)
                    db.session.add(sn)
                    db.session.commit()
                    flash('Note shared with friend.', 'success')
                else:
                    flash('Note is already shared with this friend.', 'info')
    return redirect(url_for('notes'))

@app.route('/note/delete/<int:id>', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id == current_user.user_id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted.', 'success')
    return redirect(url_for('notes'))

# --- FRIEND PROFILE ROUTE ---
@app.route('/friend/<int:id>')
@login_required
def friend_profile(id):
    if id == current_user.user_id:
        return redirect(url_for('dashboard'))
        
    # Check if they are friends
    is_friend = Friend.query.filter(
        db.or_(
            db.and_(Friend.sender_id == current_user.user_id, Friend.receiver_id == id),
            db.and_(Friend.sender_id == id, Friend.receiver_id == current_user.user_id)
        ),
        Friend.status == 'accepted'
    ).first()
    
    if not is_friend:
        flash("You are not friends with this user.", "danger")
        return redirect(url_for('friends'))
        
    friend_user = User.query.get_or_404(id)
    
    # Calculate stats
    total_minutes = db.session.query(func.sum(Session.duration_minutes)).filter_by(user_id=id).scalar() or 0
    total_hours = round(total_minutes / 60, 2)
    
    recent_sessions = Session.query.filter_by(user_id=id).order_by(Session.start_time.desc()).limit(10).all()
    goals = Goal.query.filter_by(user_id=id, status='active').all()
    
    # Notes globally shared OR explicitly shared with current user
    shared_notes = Note.query.filter(
        Note.user_id == id,
        db.or_(
            Note.is_shared == True,
            Note.note_id.in_(
                db.session.query(SharedNote.note_id).filter_by(user_id=current_user.user_id)
            )
        )
    ).order_by(Note.created_at.desc()).all()
    
    return render_template('friend_profile.html', 
                            friend=friend_user, 
                            total_hours=total_hours, 
                            sessions=recent_sessions, 
                            goals=goals, 
                            notes=shared_notes)

from models import Message

@app.route('/chat/<int:id>', methods=['GET', 'POST'])
@login_required
def chat(id):
    if id == current_user.user_id:
        return redirect(url_for('friends'))
        
    # Check if they are friends
    is_friend = Friend.query.filter(
        db.or_(
            db.and_(Friend.sender_id == current_user.user_id, Friend.receiver_id == id),
            db.and_(Friend.sender_id == id, Friend.receiver_id == current_user.user_id)
        ),
        Friend.status == 'accepted'
    ).first()
    
    if not is_friend:
        flash("You can only chat with your friends.", "danger")
        return redirect(url_for('friends'))
        
    friend_user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        content = request.form.get('content')
        if content and content.strip():
            new_msg = Message(sender_id=current_user.user_id, receiver_id=id, content=content.strip())
            db.session.add(new_msg)
            db.session.commit()
        return redirect(url_for('chat', id=id))

    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.user_id, Message.receiver_id == id),
            db.and_(Message.sender_id == id, Message.receiver_id == current_user.user_id)
        )
    ).order_by(Message.created_at.asc()).all()

    return render_template('chat.html', friend=friend_user, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
