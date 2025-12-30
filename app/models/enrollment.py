"""
Enrollment, Payment, and Study History Models
Handles student-course relationships and tracking
"""
from datetime import datetime
from app import db


class Enrollment(db.Model):
    """Enrollment model for student-course relationship"""
    __tablename__ = 'enrollment'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_percentage = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)
    
    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} Course:{self.course_id}>'


class Payment(db.Model):
    """Payment model for course purchases"""
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    amount_npr = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # esewa, khalti, cash
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id = db.Column(db.String(100), unique=True)
    
    def __repr__(self):
        return f'<Payment {self.transaction_id}>'


class StudyHistory(db.Model):
    """Study history for tracking video progress"""
    __tablename__ = 'study_history'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    watch_duration = db.Column(db.Integer, default=0)  # in seconds
    completion_percentage = db.Column(db.Float, default=0.0)
    is_completed = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    last_watched = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<StudyHistory Student:{self.student_id} Video:{self.video_id}>'
