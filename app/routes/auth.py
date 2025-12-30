"""
Authentication Routes Blueprint
Handles login, logout, and registration
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Course
from app.utils.helpers import validate_email, sanitize_string
import logging

bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@bp.route('/courses')
def courses():
    """Public courses listing page"""
    courses_list = Course.query.filter_by(is_active=True).all()
    return render_template('courses.html', courses=courses_list)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        try:
            # Get form data
            username = sanitize_string(request.form.get('username', '').strip())
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            full_name = sanitize_string(request.form.get('full_name', '').strip())
            role = request.form.get('role', 'student')
            
            # Validation
            if not all([username, email, password, full_name]):
                flash('All fields are required.', 'danger')
                return render_template('register.html')
            
            if not validate_email(email):
                flash('Invalid email address.', 'danger')
                return render_template('register.html')
            
            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return render_template('register.html')
            
            if len(password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return render_template('register.html')
            
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return render_template('register.html')
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return render_template('register.html')
            
            # Create new user
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                full_name=full_name,
                role=role
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"New user registered: {username} ({role})")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            
            if not username or not password:
                flash('Username and password are required.', 'danger')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                if not user.is_active:
                    flash('Your account has been deactivated. Contact support.', 'danger')
                    return render_template('login.html')
                
                # Set session
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session['full_name'] = user.full_name
                
                logger.info(f"User logged in: {username} ({user.role})")
                flash(f'Welcome back, {user.full_name}!', 'success')
                
                # Redirect based on role
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user.role == 'faculty':
                    return redirect(url_for('faculty.dashboard'))
                elif user.role == 'management':
                    return redirect(url_for('management.dashboard'))
                else:  # student
                    return redirect(url_for('student.dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
                logger.warning(f"Failed login attempt for username: {username}")
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {username}")
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
