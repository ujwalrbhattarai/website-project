"""
User Model
Handles user authentication and profile data
"""
from datetime import datetime
from app import db


class User(db.Model):
    """User model for students, faculty, admin, and management"""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, admin, faculty, management
    full_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')
    payments = db.relationship('Payment', backref='student', lazy='dynamic')
    study_history = db.relationship('StudyHistory', backref='student', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
