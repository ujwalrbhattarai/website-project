"""
Database Models Package
Centralized imports for all database models
"""

# Import all models for easy access
from app.models.user import User
from app.models.course import Course
from app.models.video import Video
from app.models.enrollment import Enrollment, Payment, StudyHistory
from app.models.schedule import OnlineClass, TodoItem
from app.models.support import SupportTicket, TicketResponse, Certificate

# Export all models
__all__ = [
    'User',
    'Course',
    'Video',
    'Enrollment',
    'Payment',
    'StudyHistory',
    'OnlineClass',
    'TodoItem',
    'SupportTicket',
    'TicketResponse',
    'Certificate'
]
