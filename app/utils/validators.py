"""
Input Validators
Reusable validation functions for forms and API inputs
"""
import re
from app.constants import FileUpload


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 100:
        return False, "Password must be less than 100 characters"
    
    return True, ""


def validate_username(username):
    """
    Validate username format
    
    Args:
        username: Username string to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if len(username) > 80:
        return False, "Username must be less than 80 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""


def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def validate_image_file(filename):
    """Validate image file extension"""
    return validate_file_extension(filename, FileUpload.ALLOWED_IMAGE_EXTENSIONS)


def validate_video_file(filename):
    """Validate video file extension"""
    return validate_file_extension(filename, FileUpload.ALLOWED_VIDEO_EXTENSIONS)


def validate_document_file(filename):
    """Validate document file extension"""
    return validate_file_extension(filename, FileUpload.ALLOWED_DOCUMENT_EXTENSIONS)


def validate_price(price):
    """
    Validate price value
    
    Args:
        price: Price value to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        price_float = float(price)
        if price_float < 0:
            return False, "Price cannot be negative"
        if price_float > 1000000:
            return False, "Price exceeds maximum allowed value"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid price format"


def validate_phone(phone):
    """
    Validate phone number (Nepal format)
    
    Args:
        phone: Phone number string
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return False
    # Nepal phone: 10 digits starting with 9
    pattern = r'^9\d{9}$'
    return re.match(pattern, phone) is not None


def sanitize_input(text, max_length=None):
    """
    Sanitize user input by removing dangerous characters
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Truncate if max_length specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text
