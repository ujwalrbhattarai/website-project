"""
Utility Helper Functions
Reusable utility functions for common operations
"""
import os
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
from app.utils.validators import (
    validate_email as _validate_email,
    validate_file_extension,
    sanitize_input
)


def allowed_file(filename, allowed_extensions=None):
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file to check
        allowed_extensions: Set of allowed extensions (optional)
        
    Returns:
        bool: True if allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())
    
    return validate_file_extension(filename, allowed_extensions)


def generate_unique_filename(filename):
    """
    Generate unique filename with timestamp and random string
    
    Args:
        filename: Original filename
        
    Returns:
        str: Unique filename with timestamp and random component
    """
    name, ext = os.path.splitext(secure_filename(filename))
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_str = secrets.token_hex(4)
    return f"{name}_{timestamp}_{random_str}{ext}"


def sanitize_string(text):
    """
    Sanitize string for safe storage (wrapper for backward compatibility)
    
    Args:
        text: Text to sanitize
        
    Returns:
        str: Sanitized text
    """
    return sanitize_input(text)


def calculate_completion_percentage(videos_total, videos_completed):
    """
    Calculate course completion percentage
    
    Args:
        videos_total: Total number of videos
        videos_completed: Number of completed videos
        
    Returns:
        float: Completion percentage
    """
    if videos_total == 0:
        return 0.0
    return round((videos_completed / videos_total) * 100, 2)


def generate_certificate_number():
    """
    Generate unique certificate number
    
    Returns:
        str: Unique certificate number in format CERT-YYYYMMDDHHMMSS-RANDOM
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = secrets.token_hex(4).upper()
    return f"CERT-{timestamp}-{random_part}"


def validate_email(email):
    """
    Validate email format (wrapper for backward compatibility)
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return _validate_email(email)


def format_file_size(size_bytes):
    """
    Convert bytes to human readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        str: Human-readable file size (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_file_extension(filename):
    """
    Get file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension (lowercase, without dot)
    """
    if not filename or '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()
