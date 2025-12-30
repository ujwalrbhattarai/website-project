"""
Application Constants
Centralized configuration values and magic strings
"""

# User Roles
class UserRole:
    STUDENT = 'student'
    FACULTY = 'faculty'
    ADMIN = 'admin'
    MANAGEMENT = 'management'
    
    ALL = [STUDENT, FACULTY, ADMIN, MANAGEMENT]


# Enrollment Status
class EnrollmentStatus:
    ACTIVE = 'active'
    COMPLETED = 'completed'
    SUSPENDED = 'suspended'
    
    ALL = [ACTIVE, COMPLETED, SUSPENDED]


# Payment Status
class PaymentStatus:
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    
    ALL = [PENDING, COMPLETED, FAILED]


# Payment Methods
class PaymentMethod:
    ESEWA = 'esewa'
    KHALTI = 'khalti'
    CASH = 'cash'
    
    ALL = [ESEWA, KHALTI, CASH]


# Support Ticket Status
class TicketStatus:
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'
    
    ALL = [OPEN, IN_PROGRESS, CLOSED]


# Priority Levels
class Priority:
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
    ALL = [LOW, MEDIUM, HIGH]


# Support Categories
class SupportCategory:
    TECHNICAL = 'technical'
    PAYMENT = 'payment'
    COURSE = 'course'
    OTHER = 'other'
    
    ALL = [TECHNICAL, PAYMENT, COURSE, OTHER]


# Course Levels
class CourseLevel:
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    
    ALL = [BEGINNER, INTERMEDIATE, ADVANCED]


# File Upload Settings
class FileUpload:
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
    MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB


# Grade Levels
class Grade:
    A_PLUS = 'A+'
    A = 'A'
    B_PLUS = 'B+'
    B = 'B'
    C_PLUS = 'C+'
    C = 'C'
    D = 'D'
    F = 'F'
    
    ALL = [A_PLUS, A, B_PLUS, B, C_PLUS, C, D, F]


# Alert Messages
class AlertType:
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'


# Pagination
class Pagination:
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
