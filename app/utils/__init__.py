"""
Utilities Package
Provides decorators, filters, helpers, validators, and error handlers
"""

from app.utils.decorators import login_required, admin_required, faculty_required, student_required, role_required
from app.utils.filters import format_currency, time_ago, format_duration, truncate_text
from app.utils.helpers import (
    allowed_file,
    generate_unique_filename,
    sanitize_string,
    calculate_completion_percentage,
    generate_certificate_number,
    validate_email,
    format_file_size,
    get_file_extension
)
from app.utils.validators import (
    validate_password,
    validate_username,
    validate_image_file,
    validate_video_file,
    validate_document_file,
    validate_price,
    validate_phone,
    sanitize_input
)

__all__ = [
    # Decorators
    'login_required',
    'admin_required',
    'faculty_required',
    'student_required',
    'role_required',
    
    # Filters
    'format_currency',
    'time_ago',
    'format_duration',
    'truncate_text',
    
    # Helpers
    'allowed_file',
    'generate_unique_filename',
    'sanitize_string',
    'calculate_completion_percentage',
    'generate_certificate_number',
    'validate_email',
    'format_file_size',
    'get_file_extension',
    
    # Validators
    'validate_password',
    'validate_username',
    'validate_image_file',
    'validate_video_file',
    'validate_document_file',
    'validate_price',
    'validate_phone',
    'sanitize_input',
]
