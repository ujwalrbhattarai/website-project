# 🚀 Quick Reference Guide

## Essential Commands

### Start the Application
```bash
python run.py
```

### Database Operations
```bash
# Reset database (WARNING: Deletes all data!)
# Delete the database file and restart the app
rm instance/educational_institute.db
python run.py  # Will recreate database automatically
```

### View Logs
```bash
# View logs in real-time
tail -f logs/app.log

# Or on Windows PowerShell
Get-Content logs\app.log -Wait

# Search for errors
grep "ERROR" logs/app.log
# Or on Windows
Select-String -Path logs\app.log -Pattern "ERROR"
```

## 📁 Quick File Finder

| Want to... | Edit this file |
|------------|---------------|
| Add a new route for students | `app/routes/student.py` |
| Add a new route for faculty | `app/routes/faculty.py` |
| Add a new route for admin | `app/routes/admin.py` |
| Add authentication logic | `app/routes/auth.py` |
| Add payment processing | `app/routes/payment.py` |
| Define User model | `app/models/user.py` |
| Define Course model | `app/models/course.py` |
| Define Video model | `app/models/video.py` |
| Define Payment/Enrollment | `app/models/enrollment.py` |
| Define Support/Certificate | `app/models/support.py` |
| Add a helper function | `app/utils/helpers.py` |
| Add input validation | `app/utils/validators.py` |
| Add a template filter | `app/utils/filters.py` |
| Add a route decorator | `app/utils/decorators.py` |
| Define application constants | `app/constants.py` |
| Customize error pages | `app/templates/errors/` |
| Change CSS styling | `app/static/css/custom.css` |
| Add JavaScript features | `app/static/js/custom.js` |
| Configure app settings | `config.py` |
| Set environment variables | `.env` |
| Change app initialization | `app/__init__.py` |

## 🎯 Common Code Patterns

### Creating a New Route
```python
# app/routes/student.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import User, Course
from app.utils.decorators import login_required, student_required
import logging

bp = Blueprint('student', __name__, url_prefix='/student')
logger = logging.getLogger(__name__)

@bp.route('/my-feature')
@student_required
def my_feature():
    """Description of what this route does"""
    try:
        user = User.query.get(session['user_id'])
        logger.info(f"User {user.username} accessed my-feature")
        
        # Your logic here
        
        return render_template('student/my_feature.html', user=user)
        
    except Exception as e:
        logger.error(f"My feature error: {str(e)}", exc_info=True)
        flash('An error occurred.', 'danger')
        return redirect(url_for('student.dashboard'))
```

### Creating a Database Model
```python
# Choose the appropriate file based on domain:
# - app/models/user.py - User-related
# - app/models/course.py - Course-related
# - app/models/enrollment.py - Enrollment/Payment
# - app/models/schedule.py - Scheduling/Tasks
# - app/models/support.py - Support/Certificates

# Example: Adding to app/models/support.py
from datetime import datetime
from app import db

class Notification(db.Model):
    """Notification model for user alerts"""
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id}>'

# Then add to app/models/__init__.py:
from app.models.support import Notification
__all__ = [..., 'Notification']
```

### Adding a Helper Function
```python
# app/utils/helpers.py
def my_helper_function(param):
    """
    Description of what this function does
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    try:
        # Your logic here
        result = process(param)
        return result
    except Exception as e:
        logger.error(f"Helper function error: {str(e)}")
        return None
```

### Adding a Template Filter
```python
# app/utils/filters.py
def my_filter(value):
    """Description of what this filter does"""
    try:
        # Your processing here
        return processed_value
    except (ValueError, TypeError):
        return value

# Then register in app/__init__.py:
app.jinja_env.filters['myfilter'] = my_filter
```

### Using in Template
```jinja2
{{ some_value|myfilter }}
```

## 🔍 Debugging Checklist

### Application Won't Start
- [ ] Check Python is installed: `python --version`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Check for syntax errors in recent changes
- [ ] Review logs: `logs/app.log`

### Database Errors
- [ ] Run migration: `python migrate_db.py`
- [ ] Check database exists: `ls *.db`
- [ ] Verify database URL in `config.py` or `.env`
- [ ] Check model definitions in `app/models/__init__.py`

### Import Errors
- [ ] Check file is in correct directory
- [ ] Verify `__init__.py` exists in directories
- [ ] Check circular imports
- [ ] Verify blueprint registration in `app/__init__.py`

### Template Not Found
- [ ] Check template path: `templates/folder/file.html`
- [ ] Verify template exists
- [ ] Check spelling in `render_template('path/to/template.html')`

### 404 Errors
- [ ] Check route decorator: `@bp.route('/path')`
- [ ] Verify blueprint prefix: `url_prefix='/prefix'`
- [ ] Check URL: `url_for('blueprint.function_name')`
- [ ] Verify blueprint is registered

### Permission Errors (403)
- [ ] Check decorator: `@admin_required`, `@student_required`, etc.
- [ ] Verify user role in database
- [ ] Check session data: `session.get('role')`

## 🎨 Quick CSS Customization

### Change Colors
Edit `app/static/css/custom.css`:
```css
:root {
    --primary-color: #4f46e5;      /* Your color here */
    --secondary-color: #06b6d4;    /* Your color here */
    --success-color: #10b981;      /* Your color here */
}
```

### Change Fonts
```css
body {
    font-family: 'Your Font', sans-serif;
}
```

## 📝 Logging Quick Reference

```python
import logging
logger = logging.getLogger(__name__)

# Different log levels
logger.debug("Detailed debugging information")      # Only in debug mode
logger.info("General informational messages")       # Normal operation
logger.warning("Warning messages")                  # Something unexpected
logger.error("Error messages")                      # Something failed
logger.critical("Critical problems")                # System failure

# Log with exception info
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {str(e)}", exc_info=True)
```

## 🔐 Environment Variables

### Create .env file
```bash
# Development
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///educational_institute.db
FLASK_ENV=development

# Production (example)
SECRET_KEY=generate-strong-random-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
FLASK_ENV=production
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Generate Secret Key
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Deployment Quick Guide

### Production Checklist
- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Set `DEBUG=False` in config
- [ ] Configure proper email service
- [ ] Set up HTTPS/SSL
- [ ] Configure payment gateways
- [ ] Set up automated backups

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🔗 Useful URLs

| Description | URL |
|-------------|-----|
| Application | http://localhost:5000 |
| Student Dashboard | http://localhost:5000/student/dashboard |
| Faculty Dashboard | http://localhost:5000/faculty/dashboard |
| Admin Dashboard | http://localhost:5000/admin/dashboard |
| Management Dashboard | http://localhost:5000/management/dashboard |

## 📞 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Faculty | teacher1 | teacher123 |
| Student | student1 | student123 |
| Management | manager1 | manager123 |

## 🛠️ Development Workflow

### Adding a New Feature
1. **Plan**: Decide which blueprint it belongs to
2. **Model**: Add database model if needed (`app/models/__init__.py`)
3. **Route**: Add route function (`app/routes/<blueprint>.py`)
4. **Template**: Create HTML template (`templates/<folder>/<file>.html`)
5. **Test**: Test the feature manually
6. **Log**: Add appropriate logging
7. *PROJECT_STRUCTURE.md** - Detailed architecture documentation
- ***Document**: Update relevant documentation

### Making Changes
1. **Backup**: Commit current working code to git
2. **Edit**: Make your changes
3. **Test**: Run and test thoroughly
4. **Log**: Check logs for errors
5. **Commit**: Commit working changes

## 📚 Documentation Files

- **README.md** - Complete user and developer guide
- **QUICK_REFERENCE.md** - This file - your daily reference guide!
- **.env.example** - Environment variable template

## 🎓 Learning Path

### For Beginners
1. Start with `README_NEW.md`
2. Run the application and explore
3. Read `QUICK_REFERENCE.md` (this file)
4. Make small changes.md` - Quick Start section
2. Run the application and explore
3. Read `QUICK_REFERENCE.md` (this file)
4. Make small changes to see effects

### For Developers
1. Read `PROJECT_STRUCTURE.md` for architecture details
3. Explore `app/routes/` to see patterns
4. Check `app/utils/` for reusable code
5. Study models in `app/models/le code
4. Study `app/models/__init__.py` for data structure

### For Advanced
1. Review entire architecture in code

## 🆘 Getting Help

1. **Check Logs**: `logs/app.log` - Most errors are logged here (created on first run)
2. **Read Docs**: Check README.md
3. **Search Code**: Use grep/search to find similar implementations
4. **Debug**: Add logging to track down issues
5. **Test**: Isolate the problem in a minimal test case

## ⚡ Pro Tips

### Speed Up Development
- Use `logger.debug()` instead of `print()`
- Create reusable utilities in `app/utils/helpers.py`
- Use decorators for common checks
- Follow existing code patterns

### Avoid Common Mistakes
- Always use `@login_required` on protected routes
- Never hardcode secrets - use environment variables
- Always log errors with `exc_info=True`
- Test with different user roles
- Check logs after every change

### Best Practices
- Write descriptive commit messages
- Add docstrings to functions
- Use type hints where appropriate
- Keep functions small and focused
- DRY - Don't Repeat Yourself

## 🎯 Quick Wins

### Make It Your Own
1. Change colors in `app/static/css/custom.css`
2. Update site name in templates
3. Add your logo
4. Customize email templates

### Impress Users
1. Add loading spinners
2. Improve error messages
3. Add success animations
4. Enhance mobile responsiveness

### Improve Code
1. Add more logging
2. Write utility functions
3. Add input validation
4. Improve error handling

---

**Keep this file handy - it's your day-to-day reference!** 📖
