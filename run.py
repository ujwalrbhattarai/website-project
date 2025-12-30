"""
Application Entry Point
Run this file to start the Flask application
"""
from app import create_app, db
from app.models import User, Course, Video, Enrollment, Payment

# Create application instance
app = create_app()

# Shell context for flask shell command
@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'User': User,
        'Course': Course,
        'Video': Video,
        'Enrollment': Enrollment,
        'Payment': Payment
    }

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
