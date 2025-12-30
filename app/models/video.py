"""
Video Model
Handles video content and metadata
"""
from datetime import datetime
from app import db


class Video(db.Model):
    """Video model for course content"""
    __tablename__ = 'video'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(300), nullable=False)
    duration_minutes = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    is_free = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    study_histories = db.relationship('StudyHistory', backref='video', lazy='dynamic')
    
    def __repr__(self):
        return f'<Video {self.title}>'
