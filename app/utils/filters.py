"""
Custom Jinja2 Template Filters
"""
from datetime import datetime

def format_currency(value):
    """Format number as NPR currency"""
    try:
        return f"रू {value:,.2f}"
    except (ValueError, TypeError):
        return f"रू 0.00"

def time_ago(dt):
    """
    Convert datetime to human-readable 'time ago' format
    Example: '2 hours ago', '3 days ago'
    """
    if not dt:
        return ""
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 2592000:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 31536000:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''} ago"

def format_duration(minutes):
    """
    Convert minutes to hours and minutes format
    Example: 90 -> '1h 30m'
    """
    if not minutes:
        return "0m"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0:
        return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"
    return f"{mins}m"

def truncate_text(text, length=100, suffix='...'):
    """Truncate text to specified length"""
    if not text or len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix

def format_percentage(value):
    """Format number as percentage"""
    try:
        return f"{value:.1f}%"
    except (ValueError, TypeError):
        return "0%"
