"""
OnlineClass and TodoItem Models
Handles scheduling and task management
"""
from datetime import datetime
from app import db


class OnlineClass(db.Model):
    """Online class scheduling"""
    __tablename__ = 'online_class'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    meeting_link = db.Column(db.String(500))
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    course = db.relationship('Course', backref='online_classes')
    creator = db.relationship('User', backref='created_classes')
    
    def __repr__(self):
        return f'<OnlineClass {self.title}>'


class TodoItem(db.Model):
    """Todo items for students"""
    __tablename__ = 'todo_item'
    
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
    
    def __repr__(self):
        return f'<TodoItem {self.title}>'
