"""
Routes Package
Blueprint registrations and route organization
"""

from app.routes.auth import bp as auth_bp
from app.routes.student import bp as student_bp
from app.routes.faculty import bp as faculty_bp
from app.routes.admin import bp as admin_bp
from app.routes.management import bp as management_bp
from app.routes.payment import bp as payment_bp

__all__ = [
    'auth_bp',
    'student_bp',
    'faculty_bp',
    'admin_bp',
    'management_bp',
    'payment_bp'
]
