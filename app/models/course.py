"""
Course Model
Handles course data and relationships
"""
from datetime import datetime
from app import db


class Course(db.Model):
    """Course model for educational content"""
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_npr = db.Column(db.Float, nullable=False)
    duration_hours = db.Column(db.Integer)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    demo_video_url = db.Column(db.String(300))
    thumbnail_url = db.Column(db.String(300))
    category = db.Column(db.String(100))
    level = db.Column(db.String(50))  # beginner, intermediate, advanced
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    instructor = db.relationship('User', foreign_keys=[instructor_id], backref='courses_taught')
    videos = db.relationship('Video', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic')
    payments = db.relationship('Payment', backref='course', lazy='dynamic')
    
    def __repr__(self):
        return f'<Course {self.title}>'
    
    @property
    def enrollment_count(self):
        """Get total number of enrollments"""
        return self.enrollments.count()
    
    @property
    def video_count(self):
        """Get total number of videos"""
        return self.videos.count()
    
    def to_dict(self):
        """Convert course object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price_npr': self.price_npr,
            'duration_hours': self.duration_hours,
            'instructor': self.instructor.full_name if self.instructor else None,
            'enrollment_count': self.enrollment_count,
            'video_count': self.video_count
        }
