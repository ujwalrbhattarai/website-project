"""
Error Handlers for HTTP Errors
"""
from flask import render_template
import logging

logger = logging.getLogger(__name__)

def page_not_found(e):
    """Handle 404 errors"""
    logger.warning(f"404 error: {e}")
    return render_template('errors/404.html'), 404

def internal_server_error(e):
    """Handle 500 errors"""
    logger.error(f"500 error: {e}", exc_info=True)
    return render_template('errors/500.html'), 500

def forbidden(e):
    """Handle 403 errors"""
    logger.warning(f"403 error: {e}")
    return render_template('errors/403.html'), 403

def bad_request(e):
    """Handle 400 errors"""
    logger.warning(f"400 error: {e}")
    return render_template('errors/400.html'), 400
