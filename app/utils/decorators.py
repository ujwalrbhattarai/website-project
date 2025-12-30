"""
Authentication and Authorization Decorators
"""
from functools import wraps
from flask import session, redirect, url_for, flash, abort
from app.models import User

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific role(s) for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                flash(f'Access denied. Required role: {", ".join(roles)}', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require admin access"""
    return role_required('admin')(f)

def faculty_required(f):
    """Decorator to require faculty or admin access"""
    return role_required('admin', 'faculty')(f)

def management_required(f):
    """Decorator to require management or admin access"""
    return role_required('admin', 'management')(f)

def student_required(f):
    """Decorator to require student access"""
    return role_required('student')(f)
