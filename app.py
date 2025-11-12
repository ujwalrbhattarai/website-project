from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, admin, faculty
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    payments = db.relationship('Payment', backref='student', lazy=True)
    study_history = db.relationship('StudyHistory', backref='student', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_npr = db.Column(db.Float, nullable=False)
    duration_hours = db.Column(db.Integer)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    demo_video_url = db.Column(db.String(300))  # Demo video for preview
    thumbnail_url = db.Column(db.String(300))  # Course thumbnail image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    instructor = db.relationship('User', foreign_keys=[instructor_id], backref='courses_taught')
    videos = db.relationship('Video', backref='course', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    payments = db.relationship('Payment', backref='course', lazy=True)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(300), nullable=False)
    duration_minutes = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    study_histories = db.relationship('StudyHistory', backref='video', lazy=True)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_percentage = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    amount_npr = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id = db.Column(db.String(100))

class StudyHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    watch_duration = db.Column(db.Integer, default=0)  # in seconds
    completion_percentage = db.Column(db.Float, default=0.0)  # percentage watched
    is_completed = db.Column(db.Boolean, default=False)  # True if >= 70%
    completed = db.Column(db.Boolean, default=False)
    last_watched = db.Column(db.DateTime, default=datetime.utcnow)

class OnlineClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    meeting_link = db.Column(db.String(500))  # Zoom/Google Meet link
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    course = db.relationship('Course', backref='online_classes')
    creator = db.relationship('User', backref='created_classes')

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    student = db.relationship('User', backref='todo_items')

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, in_progress, closed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    category = db.Column(db.String(50))  # technical, payment, course, other
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='submitted_tickets')
    assigned_user = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_tickets')

class TicketResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ticket = db.relationship('SupportTicket', backref='responses')
    user = db.relationship('User', backref='ticket_responses')

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    grade = db.Column(db.String(10))  # A+, A, B+, B, C+, C
    certificate_url = db.Column(db.String(500))  # Path to PDF certificate
    
    # Relationships
    student = db.relationship('User', backref='certificates')
    course = db.relationship('Course', backref='certificates')

# Decorators for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def faculty_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if user.role not in ['admin', 'faculty']:
            flash('Faculty access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def management_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if user.role not in ['admin', 'management']:
            flash('Management access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role', 'student')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            full_name=full_name,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Student Routes
@app.route('/student/dashboard')
@login_required
def student_dashboard():
    user = User.query.get(session['user_id'])
    enrollments = Enrollment.query.filter_by(student_id=user.id).all()
    payments = Payment.query.filter_by(student_id=user.id).order_by(Payment.payment_date.desc()).all()
    
    return render_template('student/dashboard.html', 
                         user=user, 
                         enrollments=enrollments,
                         payments=payments)

@app.route('/student/courses')
@login_required
def student_courses():
    user = User.query.get(session['user_id'])
    enrolled_course_ids = [e.course_id for e in user.enrollments]
    available_courses = Course.query.filter(~Course.id.in_(enrolled_course_ids)).all()
    
    return render_template('student/courses.html', courses=available_courses)

@app.route('/student/course/<int:course_id>')
@login_required
def student_course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    user = User.query.get(session['user_id'])
    
    # Check if enrolled
    enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    
    return render_template('student/course_detail.html', 
                         course=course, 
                         enrollment=enrollment)

@app.route('/student/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll_course(course_id):
    user = User.query.get(session['user_id'])
    
    # Prevent admin and management from enrolling in courses
    if user.role in ['admin', 'management']:
        flash('Administrators and management members cannot enroll in courses.', 'warning')
        return redirect(url_for('browse_courses'))
    
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    if existing:
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('student_course_detail', course_id=course_id))
    
    # Get payment method
    payment_method = request.form.get('payment_method', 'cash')
    
    # If eSewa or Khalti, redirect to payment gateway
    if payment_method in ['esewa', 'khalti']:
        # Store pending enrollment in session
        session['pending_enrollment'] = {
            'course_id': course_id,
            'payment_method': payment_method,
            'amount': course.price_npr
        }
        
        if payment_method == 'esewa':
            return redirect(url_for('initiate_esewa_payment', course_id=course_id))
        elif payment_method == 'khalti':
            return redirect(url_for('initiate_khalti_payment', course_id=course_id))
    
    # For cash/demo payment, process immediately
    # Create payment record
    payment = Payment(
        student_id=user.id,
        course_id=course_id,
        amount_npr=course.price_npr,
        payment_method=payment_method,
        status='completed',
        transaction_id=f'TXN-{payment_method.upper()}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    )
    db.session.add(payment)
    
    # Create enrollment
    enrollment = Enrollment(
        student_id=user.id,
        course_id=course_id
    )
    db.session.add(enrollment)
    db.session.commit()
    
    flash(f'🎉 Successfully enrolled in {course.title}! Payment via {payment_method.upper()} completed.', 'success')
    return redirect(url_for('student_course_detail', course_id=course_id))

@app.route('/payment/esewa/initiate/<int:course_id>')
@login_required
def initiate_esewa_payment(course_id):
    user = User.query.get(session['user_id'])
    course = Course.query.get_or_404(course_id)
    
    # eSewa Configuration (Test Mode)
    esewa_config = {
        'merchant_code': 'EPAYTEST',  # Use your eSewa merchant code
        'success_url': url_for('esewa_payment_success', _external=True),
        'failure_url': url_for('esewa_payment_failure', _external=True),
        'amount': course.price_npr,
        'tax_amount': 0,
        'service_charge': 0,
        'product_delivery_charge': 0,
        'total_amount': course.price_npr,
        'transaction_uuid': f'TXN-{user.id}-{course_id}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
        'product_code': f'COURSE-{course_id}',
        'product_service_charge': 0,
        'success_url': url_for('esewa_payment_success', _external=True),
        'failure_url': url_for('esewa_payment_failure', _external=True)
    }
    
    # Store transaction in session
    session['esewa_transaction'] = {
        'course_id': course_id,
        'transaction_uuid': esewa_config['transaction_uuid'],
        'amount': course.price_npr
    }
    
    return render_template('payment/esewa_redirect.html', config=esewa_config, course=course)

@app.route('/payment/esewa/success')
@login_required
def esewa_payment_success():
    # Get transaction details from query parameters
    transaction_code = request.args.get('refId')
    transaction_uuid = request.args.get('oid')
    amount = request.args.get('amt')
    
    # Get stored transaction from session
    esewa_transaction = session.get('esewa_transaction')
    
    if not esewa_transaction:
        flash('Payment verification failed. Transaction not found.', 'danger')
        return redirect(url_for('index'))
    
    course_id = esewa_transaction['course_id']
    user = User.query.get(session['user_id'])
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    if not existing:
        # Create payment record
        payment = Payment(
            student_id=user.id,
            course_id=course_id,
            amount_npr=course.price_npr,
            payment_method='esewa',
            status='completed',
            transaction_id=transaction_code or transaction_uuid
        )
        db.session.add(payment)
        
        # Create enrollment
        enrollment = Enrollment(
            student_id=user.id,
            course_id=course_id
        )
        db.session.add(enrollment)
        db.session.commit()
    
    # Clear session
    session.pop('esewa_transaction', None)
    session.pop('pending_enrollment', None)
    
    flash(f'🎉 Payment successful! You are now enrolled in {course.title}!', 'success')
    return redirect(url_for('student_course_detail', course_id=course_id))

@app.route('/payment/esewa/failure')
@login_required
def esewa_payment_failure():
    # Clear session
    session.pop('esewa_transaction', None)
    session.pop('pending_enrollment', None)
    
    flash('❌ Payment failed or was cancelled. Please try again.', 'danger')
    return redirect(url_for('student_courses'))

@app.route('/payment/khalti/initiate/<int:course_id>')
@login_required
def initiate_khalti_payment(course_id):
    user = User.query.get(session['user_id'])
    course = Course.query.get_or_404(course_id)
    
    # For now, just process as demo payment
    flash('Khalti payment integration coming soon! Processing as demo payment.', 'info')
    
    # Create payment record
    payment = Payment(
        student_id=user.id,
        course_id=course_id,
        amount_npr=course.price_npr,
        payment_method='khalti',
        status='completed',
        transaction_id=f'TXN-KHALTI-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    )
    db.session.add(payment)
    
    # Create enrollment
    enrollment = Enrollment(
        student_id=user.id,
        course_id=course_id
    )
    db.session.add(enrollment)
    db.session.commit()
    
    flash(f'🎉 Successfully enrolled in {course.title}!', 'success')
    return redirect(url_for('student_course_detail', course_id=course_id))

@app.route('/student/video/<int:video_id>')
@login_required
def watch_video(video_id):
    video = Video.query.get_or_404(video_id)
    user = User.query.get(session['user_id'])
    
    # Check if enrolled in course
    enrollment = Enrollment.query.filter_by(
        student_id=user.id, 
        course_id=video.course_id
    ).first()
    
    if not enrollment:
        flash('You need to enroll in this course first.', 'warning')
        return redirect(url_for('student_courses'))
    
    # Get or create study history
    history = StudyHistory.query.filter_by(
        student_id=user.id,
        video_id=video_id
    ).first()
    
    if not history:
        history = StudyHistory(student_id=user.id, video_id=video_id)
        db.session.add(history)
        db.session.commit()
    
    return render_template('student/watch_video.html', video=video, history=history)

@app.route('/student/update_progress/<int:video_id>', methods=['POST'])
@login_required
def update_progress(video_id):
    user = User.query.get(session['user_id'])
    data = request.json
    watch_duration = data.get('watch_duration', 0)
    total_duration = data.get('total_duration', 1)
    completed = data.get('completed', False)
    
    # Calculate completion percentage
    completion_percentage = (watch_duration / total_duration) * 100 if total_duration > 0 else 0
    
    history = StudyHistory.query.filter_by(
        student_id=user.id,
        video_id=video_id
    ).first()
    
    if history:
        history.watch_duration = watch_duration
        history.completion_percentage = completion_percentage
        history.is_completed = completion_percentage >= 70  # Mark completed if >= 70%
        history.completed = completed
        history.last_watched = datetime.utcnow()
        db.session.commit()
        return {'success': True, 'completion_percentage': completion_percentage, 'is_completed': history.is_completed}
    
    return {'success': False}, 404

@app.route('/student/recorded-videos')
@login_required
def recorded_videos():
    user = User.query.get(session['user_id'])
    
    # Get all enrolled courses
    enrollments = Enrollment.query.filter_by(student_id=user.id).all()
    enrolled_course_ids = [e.course_id for e in enrollments]
    
    # Get all videos from enrolled courses grouped by topic
    videos_by_topic = {}
    for course_id in enrolled_course_ids:
        course = Course.query.get(course_id)
        videos = Video.query.filter_by(course_id=course_id).order_by(Video.order).all()
        
        for video in videos:
            # Extract topic from video title (e.g., "Python Basics - Introduction")
            topic = video.title.split('-')[0].strip() if '-' in video.title else course.title
            if topic not in videos_by_topic:
                videos_by_topic[topic] = []
            
            # Get watch history
            history = StudyHistory.query.filter_by(student_id=user.id, video_id=video.id).first()
            
            videos_by_topic[topic].append({
                'video': video,
                'course': course,
                'history': history
            })
    
    return render_template('student/recorded_videos.html', videos_by_topic=videos_by_topic)

@app.route('/student/online-classes')
@login_required
def online_classes():
    user = User.query.get(session['user_id'])
    
    # Get all enrolled courses
    enrollments = Enrollment.query.filter_by(student_id=user.id).all()
    enrolled_course_ids = [e.course_id for e in enrollments]
    
    # Get upcoming and past classes
    now = datetime.utcnow()
    
    if enrolled_course_ids:
        upcoming_classes = OnlineClass.query.filter(
            OnlineClass.course_id.in_(enrolled_course_ids),
            OnlineClass.scheduled_at >= now
        ).order_by(OnlineClass.scheduled_at).all()
        
        past_classes = OnlineClass.query.filter(
            OnlineClass.course_id.in_(enrolled_course_ids),
            OnlineClass.scheduled_at < now
        ).order_by(OnlineClass.scheduled_at.desc()).limit(10).all()
    else:
        upcoming_classes = []
        past_classes = []
    
    return render_template('student/online_classes.html', 
                         upcoming_classes=upcoming_classes, 
                         past_classes=past_classes)

@app.route('/student/todo')
@login_required
def student_todo():
    user = User.query.get(session['user_id'])
    
    # Get all todos
    pending_todos = TodoItem.query.filter_by(student_id=user.id, is_completed=False).order_by(TodoItem.created_at.desc()).all()
    completed_todos = TodoItem.query.filter_by(student_id=user.id, is_completed=True).order_by(TodoItem.completed_at.desc()).all()
    
    return render_template('student/todo.html', pending_todos=pending_todos, completed_todos=completed_todos)

@app.route('/student/todo/add', methods=['POST'])
@login_required
def add_todo():
    user = User.query.get(session['user_id'])
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium')
    due_date_str = request.form.get('due_date')
    
    if not title:
        flash('Todo title is required.', 'danger')
        return redirect(url_for('student_todo'))
    
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except:
            pass
    
    todo = TodoItem(
        student_id=user.id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )
    db.session.add(todo)
    db.session.commit()
    
    flash('✅ Todo added successfully!', 'success')
    return redirect(url_for('student_todo'))

@app.route('/student/todo/<int:todo_id>/toggle', methods=['POST'])
@login_required
def toggle_todo(todo_id):
    user = User.query.get(session['user_id'])
    todo = TodoItem.query.get_or_404(todo_id)
    
    if todo.student_id != user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('student_todo'))
    
    todo.is_completed = not todo.is_completed
    if todo.is_completed:
        todo.completed_at = datetime.utcnow()
    else:
        todo.completed_at = None
    
    db.session.commit()
    
    return redirect(url_for('student_todo'))

@app.route('/student/todo/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete_todo(todo_id):
    user = User.query.get(session['user_id'])
    todo = TodoItem.query.get_or_404(todo_id)
    
    if todo.student_id != user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('student_todo'))
    
    db.session.delete(todo)
    db.session.commit()
    
    flash('🗑️ Todo deleted successfully!', 'success')
    return redirect(url_for('student_todo'))

@app.route('/student/settings')
@login_required
def student_settings():
    user = User.query.get(session['user_id'])
    return render_template('student/settings.html', user=user)

@app.route('/student/profile')
@login_required
def student_profile():
    user = User.query.get(session['user_id'])
    
    # Get user statistics
    total_enrollments = Enrollment.query.filter_by(student_id=user.id).count()
    total_payments = Payment.query.filter_by(student_id=user.id, status='completed').count()
    completed_videos = StudyHistory.query.filter_by(student_id=user.id, is_completed=True).count()
    
    # Get recent enrollments
    recent_enrollments = Enrollment.query.filter_by(student_id=user.id).order_by(Enrollment.enrollment_date.desc()).limit(5).all()
    
    return render_template('student/profile.html', 
                         user=user,
                         total_enrollments=total_enrollments,
                         total_payments=total_payments,
                         completed_videos=completed_videos,
                         recent_enrollments=recent_enrollments)

@app.route('/student/certificates')
@login_required
def student_certificates():
    user = User.query.get(session['user_id'])
    
    # Get all certificates for the student
    certificates = Certificate.query.filter_by(student_id=user.id).order_by(Certificate.issue_date.desc()).all()
    
    # Get eligible courses (completed >= 70%)
    enrollments = Enrollment.query.filter_by(student_id=user.id).all()
    eligible_courses = [e for e in enrollments if e.completion_percentage >= 70 and e.status == 'active']
    
    return render_template('student/certificates.html', 
                         user=user,
                         certificates=certificates,
                         eligible_courses=eligible_courses)

@app.route('/student/certificate/<int:certificate_id>')
@login_required
def view_certificate(certificate_id):
    user = User.query.get(session['user_id'])
    certificate = Certificate.query.get_or_404(certificate_id)
    
    if certificate.student_id != user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('student_certificates'))
    
    return render_template('student/certificate_view.html', 
                         user=user,
                         certificate=certificate)

@app.route('/student/certificate/request/<int:course_id>', methods=['POST'])
@login_required
def request_certificate(course_id):
    user = User.query.get(session['user_id'])
    
    # Check if enrollment exists and completion >= 70%
    enrollment = Enrollment.query.filter_by(student_id=user.id, course_id=course_id).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'danger')
        return redirect(url_for('student_certificates'))
    
    if enrollment.completion_percentage < 70:
        flash('You must complete at least 70% of the course to request a certificate.', 'warning')
        return redirect(url_for('student_certificates'))
    
    # Check if certificate already exists
    existing_cert = Certificate.query.filter_by(student_id=user.id, course_id=course_id).first()
    if existing_cert:
        flash('Certificate already issued for this course.', 'info')
        return redirect(url_for('student_certificates'))
    
    # Generate certificate number
    import random
    import string
    cert_number = f"TIG-{datetime.now().year}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
    
    # Determine grade based on completion percentage
    if enrollment.completion_percentage >= 95:
        grade = 'A+'
    elif enrollment.completion_percentage >= 90:
        grade = 'A'
    elif enrollment.completion_percentage >= 85:
        grade = 'B+'
    elif enrollment.completion_percentage >= 80:
        grade = 'B'
    elif enrollment.completion_percentage >= 75:
        grade = 'C+'
    else:
        grade = 'C'
    
    # Create certificate
    certificate = Certificate(
        student_id=user.id,
        course_id=course_id,
        certificate_number=cert_number,
        completion_date=datetime.utcnow(),
        grade=grade
    )
    
    db.session.add(certificate)
    db.session.commit()
    
    flash('🎓 Certificate generated successfully!', 'success')
    return redirect(url_for('student_certificates'))

@app.route('/student/support')
@login_required
def student_support():
    user = User.query.get(session['user_id'])
    tickets = SupportTicket.query.filter_by(student_id=user.id).order_by(SupportTicket.created_at.desc()).all()
    return render_template('student/support.html', user=user, tickets=tickets)

@app.route('/student/support/new', methods=['GET', 'POST'])
@login_required
def student_support_new():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        category = request.form.get('category', 'other')
        
        ticket = SupportTicket(
            student_id=session['user_id'],
            title=title,
            description=description,
            priority=priority,
            category=category
        )
        db.session.add(ticket)
        db.session.commit()
        
        flash('Support ticket submitted successfully!', 'success')
        return redirect(url_for('student_support'))
    
    user = User.query.get(session['user_id'])
    return render_template('student/support_new.html', user=user)

@app.route('/student/support/<int:ticket_id>')
@login_required
def student_support_detail(ticket_id):
    user = User.query.get(session['user_id'])
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    # Make sure the student can only view their own tickets
    if ticket.student_id != user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student_support'))
    
    return render_template('student/support_detail.html', user=user, ticket=ticket)

@app.route('/student/support/<int:ticket_id>/respond', methods=['POST'])
@login_required
def student_support_respond(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    user = User.query.get(session['user_id'])
    
    if ticket.student_id != user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('student_support'))
    
    message = request.form.get('message')
    if message:
        response = TicketResponse(
            ticket_id=ticket_id,
            user_id=session['user_id'],
            message=message
        )
        db.session.add(response)
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Response added successfully!', 'success')
    
    return redirect(url_for('student_support_detail', ticket_id=ticket_id))

# Admin Routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_faculty = User.query.filter_by(role='faculty').count()
    total_courses = Course.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter_by(status='completed').scalar() or 0
    
    recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(10).all()
    recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_courses=total_courses,
                         total_revenue=total_revenue,
                         recent_enrollments=recent_enrollments,
                         recent_payments=recent_payments)

@app.route('/admin/profile')
@admin_required
def admin_profile():
    user = User.query.get(session['user_id'])
    
    # Get admin statistics
    total_students = User.query.filter_by(role='student').count()
    total_faculty = User.query.filter_by(role='faculty').count()
    total_courses = Course.query.count()
    total_revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter_by(status='completed').scalar() or 0
    total_tickets = SupportTicket.query.count()
    open_tickets = SupportTicket.query.filter_by(status='open').count()
    
    # Recent activities
    recent_users = User.query.filter_by(role='student').order_by(User.id.desc()).limit(5).all()
    recent_tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).limit(5).all()
    
    return render_template('admin/profile.html',
                         user=user,
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_courses=total_courses,
                         total_revenue=total_revenue,
                         total_tickets=total_tickets,
                         open_tickets=open_tickets,
                         recent_users=recent_users,
                         recent_tickets=recent_tickets)

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/add', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        role = request.form.get('role')
        
        # Validation
        if not all([username, email, password, full_name, role]):
            flash('All fields are required!', 'danger')
            return redirect(url_for('admin_add_user'))
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('admin_add_user'))
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('admin_add_user'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            full_name=full_name,
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'✅ User {username} added successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/add_user.html')

@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.full_name = request.form.get('full_name')
        user.role = request.form.get('role')
        
        # Update password only if provided
        new_password = request.form.get('password')
        if new_password:
            user.password = generate_password_hash(new_password)
        
        db.session.commit()
        flash(f'✅ User {user.username} updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting yourself
    if user.id == session['user_id']:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'🗑️ User {user.username} deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/courses')
@admin_required
def admin_courses():
    courses = Course.query.all()
    return render_template('admin/courses.html', courses=courses)

@app.route('/admin/payments')
@admin_required
def admin_payments():
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    return render_template('admin/payments.html', payments=payments)

@app.route('/admin/reports')
@admin_required
def admin_reports():
    # Analytics data
    all_courses = Course.query.all()
    all_students = User.query.filter_by(role='student').all()
    all_payments = Payment.query.filter_by(status='completed').all()
    all_enrollments = Enrollment.query.all()
    
    # Calculate totals
    total_revenue = sum(payment.amount_npr for payment in all_payments)
    
    return render_template('admin/reports.html',
                         courses=all_courses,
                         students=all_students,
                         payments=all_payments,
                         enrollments=all_enrollments,
                         total_revenue=total_revenue)

@app.route('/admin/support')
@admin_required
def admin_support():
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    faculty_members = User.query.filter_by(role='faculty').all()
    return render_template('admin/support.html', tickets=tickets, faculty_members=faculty_members)

@app.route('/admin/support/<int:ticket_id>')
@admin_required
def admin_support_detail(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    faculty_members = User.query.filter_by(role='faculty').all()
    return render_template('admin/support_detail.html', ticket=ticket, faculty_members=faculty_members)

@app.route('/admin/support/<int:ticket_id>/assign', methods=['POST'])
@admin_required
def admin_support_assign(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    assigned_to = request.form.get('assigned_to')
    status = request.form.get('status')
    
    if assigned_to:
        ticket.assigned_to = int(assigned_to)
    if status:
        ticket.status = status
    
    ticket.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Ticket updated successfully!', 'success')
    return redirect(url_for('admin_support_detail', ticket_id=ticket_id))

@app.route('/admin/support/<int:ticket_id>/respond', methods=['POST'])
@admin_required
def admin_support_respond(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    message = request.form.get('message')
    
    if message:
        response = TicketResponse(
            ticket_id=ticket_id,
            user_id=session['user_id'],
            message=message
        )
        db.session.add(response)
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Response added successfully!', 'success')
    
    return redirect(url_for('admin_support_detail', ticket_id=ticket_id))

@app.route('/admin/management')
@admin_required
def admin_management():
    management_users = User.query.filter(User.role.in_(['admin', 'faculty', 'management'])).all()
    return render_template('admin/management.html', management_users=management_users)

@app.route('/admin/management/add', methods=['POST'])
@admin_required
def admin_management_add():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    role = request.form.get('role', 'faculty')
    
    # Check if user already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        flash('User with this username or email already exists!', 'danger')
        return redirect(url_for('admin_management'))
    
    # Create new management user
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        role=role,
        password=generate_password_hash(password)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    flash(f'{role.capitalize()} member added successfully!', 'success')
    return redirect(url_for('admin_management'))

@app.route('/admin/management/<int:user_id>/remove', methods=['POST'])
@admin_required
def admin_management_remove(user_id):
    user = User.query.get_or_404(user_id)
    
    # Prevent removing yourself
    if user.id == session['user_id']:
        flash('You cannot remove yourself!', 'danger')
        return redirect(url_for('admin_management'))
    
    # Prevent removing if user has active data
    if user.role == 'faculty':
        course_count = Course.query.filter_by(instructor_id=user.id).count()
        if course_count > 0:
            flash('Cannot remove faculty member with active courses!', 'danger')
            return redirect(url_for('admin_management'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Management member removed successfully!', 'success')
    return redirect(url_for('admin_management'))

# Faculty Routes
@app.route('/faculty/dashboard')
@faculty_required
def faculty_dashboard():
    user = User.query.get(session['user_id'])
    my_courses = Course.query.filter_by(instructor_id=user.id).all()
    
    return render_template('faculty/dashboard.html', 
                         user=user, 
                         courses=my_courses)

@app.route('/faculty/profile')
@faculty_required
def faculty_profile():
    user = User.query.get(session['user_id'])
    
    # Get faculty statistics
    total_courses = Course.query.filter_by(instructor_id=user.id).count()
    total_students = db.session.query(db.func.count(db.func.distinct(Enrollment.student_id))).join(Course).filter(Course.instructor_id == user.id).scalar() or 0
    total_videos = db.session.query(db.func.count(Video.id)).join(Course).filter(Course.instructor_id == user.id).scalar() or 0
    assigned_tickets = SupportTicket.query.filter_by(assigned_to=user.id).count()
    open_tickets = SupportTicket.query.filter_by(assigned_to=user.id, status='open').count()
    
    # Recent activities
    my_courses = Course.query.filter_by(instructor_id=user.id).order_by(Course.id.desc()).limit(5).all()
    my_tickets = SupportTicket.query.filter_by(assigned_to=user.id).order_by(SupportTicket.created_at.desc()).limit(5).all()
    
    return render_template('faculty/profile.html',
                         user=user,
                         total_courses=total_courses,
                         total_students=total_students,
                         total_videos=total_videos,
                         assigned_tickets=assigned_tickets,
                         open_tickets=open_tickets,
                         my_courses=my_courses,
                         my_tickets=my_tickets)

@app.route('/faculty/course/add', methods=['GET', 'POST'])
@faculty_required
def faculty_add_course():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price_npr = float(request.form.get('price_npr'))
        duration_hours = int(request.form.get('duration_hours', 0))
        demo_video_url = request.form.get('demo_video_url', '')
        thumbnail_url = request.form.get('thumbnail_url', '')
        
        course = Course(
            title=title,
            description=description,
            price_npr=price_npr,
            duration_hours=duration_hours,
            instructor_id=session['user_id'],
            demo_video_url=demo_video_url,
            thumbnail_url=thumbnail_url
        )
        db.session.add(course)
        db.session.commit()
        
        flash('Course created successfully!', 'success')
        return redirect(url_for('faculty_dashboard'))
    
    return render_template('faculty/add_course.html')

@app.route('/faculty/course/<int:course_id>')
@faculty_required
def faculty_course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    videos = Video.query.filter_by(course_id=course_id).order_by(Video.order).all()
    
    return render_template('faculty/course_detail.html', course=course, videos=videos)

@app.route('/faculty/support')
@faculty_required
def faculty_support():
    user = User.query.get(session['user_id'])
    tickets = SupportTicket.query.filter_by(assigned_to=user.id).order_by(SupportTicket.created_at.desc()).all()
    return render_template('faculty/support.html', tickets=tickets, user=user)

@app.route('/faculty/support/<int:ticket_id>')
@faculty_required
def faculty_support_detail(ticket_id):
    user = User.query.get(session['user_id'])
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    # Make sure faculty can only view tickets assigned to them
    if ticket.assigned_to != user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('faculty_support'))
    
    return render_template('faculty/support_detail.html', ticket=ticket, user=user)

@app.route('/faculty/support/<int:ticket_id>/respond', methods=['POST'])
@faculty_required
def faculty_support_respond(ticket_id):
    user = User.query.get(session['user_id'])
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    if ticket.assigned_to != user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('faculty_support'))
    
    message = request.form.get('message')
    if message:
        response = TicketResponse(
            ticket_id=ticket_id,
            user_id=session['user_id'],
            message=message
        )
        db.session.add(response)
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Response added successfully!', 'success')
    
    return redirect(url_for('faculty_support_detail', ticket_id=ticket_id))

# Management Routes
@app.route('/management/dashboard')
@management_required
def management_dashboard():
    user = User.query.get(session['user_id'])
    
    # Get overview statistics
    total_students = User.query.filter_by(role='student').count()
    total_faculty = User.query.filter_by(role='faculty').count()
    total_courses = Course.query.count()
    total_tickets = SupportTicket.query.count()
    
    # Recent activities
    recent_tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).limit(10).all()
    recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(10).all()
    
    return render_template('management/dashboard.html',
                         user=user,
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_courses=total_courses,
                         total_tickets=total_tickets,
                         recent_tickets=recent_tickets,
                         recent_enrollments=recent_enrollments)

@app.route('/management/profile')
@management_required
def management_profile():
    user = User.query.get(session['user_id'])
    
    # Get management statistics
    total_students = User.query.filter_by(role='student').count()
    total_faculty = User.query.filter_by(role='faculty').count()
    total_courses = Course.query.count()
    total_tickets = SupportTicket.query.count()
    open_tickets = SupportTicket.query.filter_by(status='open').count()
    total_revenue = db.session.query(db.func.sum(Payment.amount_npr)).filter_by(status='completed').scalar() or 0
    
    # Recent activities
    recent_tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).limit(5).all()
    recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(5).all()
    
    return render_template('management/profile.html',
                         user=user,
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_courses=total_courses,
                         total_tickets=total_tickets,
                         open_tickets=open_tickets,
                         total_revenue=total_revenue,
                         recent_tickets=recent_tickets,
                         recent_enrollments=recent_enrollments)

@app.route('/management/reports')
@management_required
def management_reports():
    user = User.query.get(session['user_id'])
    
    # Analytics data
    all_courses = Course.query.all()
    all_payments = Payment.query.filter_by(status='completed').all()
    
    return render_template('management/reports.html',
                         user=user,
                         courses=all_courses,
                         payments=all_payments)

@app.route('/management/students')
@management_required
def management_students():
    user = User.query.get(session['user_id'])
    students = User.query.filter_by(role='student').order_by(User.full_name).all()
    
    return render_template('management/students.html',
                         user=user,
                         students=students)

@app.route('/management/courses')
@management_required
def management_courses():
    user = User.query.get(session['user_id'])
    courses = Course.query.all()
    
    return render_template('management/courses.html',
                         user=user,
                         courses=courses)

@app.route('/management/support')
@management_required
def management_support():
    user = User.query.get(session['user_id'])
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    
    return render_template('management/support.html',
                         user=user,
                         tickets=tickets)

@app.route('/management/support/<int:ticket_id>')
@management_required
def management_support_detail(ticket_id):
    user = User.query.get(session['user_id'])
    ticket = SupportTicket.query.get_or_404(ticket_id)
    
    return render_template('management/support_detail.html',
                         user=user,
                         ticket=ticket)

@app.route('/faculty/course/<int:course_id>/add_video', methods=['GET', 'POST'])
@faculty_required
def faculty_add_video(course_id):
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        duration_minutes = int(request.form.get('duration_minutes', 0))
        order = int(request.form.get('order', 0))
        
        video = Video(
            title=title,
            description=description,
            video_url=video_url,
            duration_minutes=duration_minutes,
            course_id=course_id,
            order=order
        )
        db.session.add(video)
        db.session.commit()
        
        flash('Video added successfully!', 'success')
        return redirect(url_for('faculty_course_detail', course_id=course_id))
    
    return render_template('faculty/add_video.html', course=course)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
