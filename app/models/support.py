"""
SupportTicket and Certificate Models
Handles support system and certifications
"""
from datetime import datetime
from app import db


class SupportTicket(db.Model):
    """Support tickets for student queries"""
    __tablename__ = 'support_ticket'
    
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
    
    def __repr__(self):
        return f'<SupportTicket {self.title}>'


class TicketResponse(db.Model):
    """Responses to support tickets"""
    __tablename__ = 'ticket_response'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ticket = db.relationship('SupportTicket', backref='responses')
    user = db.relationship('User', backref='ticket_responses')
    
    def __repr__(self):
        return f'<TicketResponse {self.id}>'


class Certificate(db.Model):
    """Course completion certificates"""
    __tablename__ = 'certificate'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime)
    grade = db.Column(db.String(10))  # A+, A, B+, B, C+, C
    certificate_url = db.Column(db.String(500))
    
    # Relationships
    student = db.relationship('User', backref='certificates')
    course = db.relationship('Course', backref='certificates')
    
    def __repr__(self):
        return f'<Certificate {self.certificate_number}>'
