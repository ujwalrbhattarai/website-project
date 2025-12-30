# 🎓 Educational Institute Platform

A modern, full-featured educational institute management system built with Flask. Features a modular MVC architecture, comprehensive logging, and modern UI design.

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment (optional)
cp .env.example .env
# Edit .env with your settings

# 3. Run the application
python run.py
```

Visit **http://localhost:5000** and login with default credentials below.

## 🔑 Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Faculty | teacher1 | teacher123 |
| Student | student1 | student123 |
| Management | manager1 | manager123 |

**⚠️ Change these passwords in production!**

## 📁 Project Structure

```
website-project/
├── app/                          # Application package
│   ├── __init__.py              # App factory, blueprints, logging
│   ├── constants.py             # Application constants & enums
│   ├── models/                   # Database models (split by domain)
│   │   ├── __init__.py          # Model exports
│   │   ├── user.py              # User model
│   │   ├── course.py            # Course model
│   │   ├── video.py             # Video model
│   │   ├── enrollment.py        # Enrollment, Payment, StudyHistory
│   │   ├── schedule.py          # OnlineClass, TodoItem
│   │   └── support.py           # SupportTicket, TicketResponse, Certificate
│   ├── routes/                   # Route blueprints
│   │   ├── __init__.py          # Blueprint exports
│   │   ├── auth.py              # Login, register, logout
│   │   ├── student.py           # Student dashboard, courses
│   │   ├── faculty.py           # Faculty courses, videos
│   │   ├── admin.py             # Admin panel
│   │   ├── management.py        # Management portal
│   │   └── payment.py           # eSewa, Khalti integration
│   └── utils/                    # Utilities
│       ├── __init__.py          # Utility exports
│       ├── decorators.py        # @login_required, @admin_required
│       ├── filters.py           # Jinja2 filters
│       ├── helpers.py           # Helper functions
│       ├── validators.py        # Input validation
│       └── error_handlers.py   # Error pages
├── templates/                    # HTML templates
├── static/uploads/              # User uploads
├── instance/                     # Instance folder
│   └── educational_institute.db # SQLite database
├── config.py                     # Configuration
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── QUICK_REFERENCE.md           # Developer quick reference
├── PROJECT_STRUCTURE.md         # Detailed architecture guide
└── .env.example                  # Environment template
```

**📖 See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture documentation.**

## ✨ Features

### 👨‍🎓 Student Portal
- View enrolled courses and progress
- Watch video lectures with progress tracking
- Access online classes and schedules
- Create and manage todo lists
- Download course certificates
- Submit and track support tickets
- Make payments via eSewa/Khalti

### 👨‍🏫 Faculty Portal
- Create and manage courses
- Upload video lectures
- View student enrollment and progress
- Monitor video watch statistics
- Manage course materials
- Respond to student support tickets

### 👨‍💼 Admin Portal
- Manage all users (create, edit, delete)
- Oversee all courses and content
- View detailed analytics and reports
- Monitor payment transactions
- Handle support tickets
- Generate revenue reports
- Issue student certificates

### 👔 Management Portal
- View all courses and enrollments
- Monitor student progress
- Access comprehensive reports
- Review payment records
- Manage support system

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/ujwalrbhattarai/website-project.git
cd website-project
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment** (optional)
```bash
cp .env.example .env
# Edit .env file with your settings
```

5. **Run the application**
```bash
python run.py
```

The app will be available at **http://localhost:5000**

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Security
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///educational_institute.db

# Environment
FLASK_ENV=development

# Email (optional - for production)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Payment (configure for production)
ESEWA_MERCHANT_ID=your-esewa-id
KHALTI_SECRET_KEY=your-khalti-key
```

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🎨 Customization

### Change UI Colors

Edit `app/static/css/custom.css`:
```css
:root {
    --primary-color: #4f46e5;      /* Change to your color */
    --secondary-color: #06b6d4;    /* Change to your color */
    --success-color: #10b981;      /* Change to your color */
}
```

### Add New Features

1. **Create route** in appropriate blueprint (`app/routes/`)
2. **Add template** in `templates/` folder
3. **Update model** if needed in `app/models/__init__.py`
4. **Add helper functions** in `app/utils/helpers.py`

## 🐛 Debugging

### View Logs
```bash
# Real-time log viewing (created automatically on first run)
tail -f logs/app.log

# Or on Windows PowerShell
Get-Content logs\app.log -Wait
```

### Common Issues

**Database errors**
- Delete `instance/educational_institute.db` and restart

**Import errors**
- Verify all dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (3.8+ required)

**Template not found**
- Check template path in `render_template()`
- Verify template exists in `templates/` folder

**Permission denied (403)**
- Check user role matches route decorator
- Verify login status

## 🚀 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Configure email service (SMTP)
- [ ] Set up payment gateways (eSewa, Khalti)
- [ ] Enable HTTPS/SSL
- [ ] Set up automated backups
- [ ] Configure logging rotation
- [ ] Change default passwords

### Deploy with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using PostgreSQL

Update `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost/dbname
```

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

## 📚 Development Guide

### Adding a New Route

```python
# app/routes/student.py
from flask import render_template, session
from app.utils.decorators import login_required, student_required
import logging

logger = logging.getLogger(__name__)

@bp.route('/my-feature')
@student_required
def my_feature():
    try:
        user_id = session['user_id']
        logger.info(f"User {user_id} accessed my-feature")
        
        # Your logic here
        
        return render_template('student/my_feature.html')
    except Exception as e:
        logger.error(f"Error in my_feature: {str(e)}", exc_info=True)
        flash('An error occurred', 'danger')
        return redirect(url_for('student.dashboard'))
```

### Creating a Database Model

```python
# app/models/__init__.py
class MyModel(db.Model):
    __tablename__ = 'my_model'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MyModel {self.name}>'
```

### Using Decorators

```python
from app.utils.decorators import login_required, admin_required

@app.route('/admin/only')
@admin_required
def admin_only():
    # Only admins can access this
    pass

@app.route('/protected')
@login_required
def protected():
    # Any logged-in user can access this
    pass
```

## 📖 Quick Reference

### Essential Commands

```bash
# Start app
python run.py

# Install new package
pip install package-name
pip freeze > requirements.txt

# View logs
tail -f logs/app.log  # Linux/Mac
Get-Content logs\app.log -Wait  # Windows
```

### File Locations

| Task | File |
|------|------|
| Add student route | `app/routes/student.py` |
| Add faculty route | `app/routes/faculty.py` |
| Add admin route | `app/routes/admin.py` |
| Add database model | `app/models/__init__.py` |
| Add helper function | `app/utils/helpers.py` |
| Add template filter | `app/utils/filters.py` |
| Customize CSS | `app/static/css/custom.css` |
| Customize JS | `app/static/js/custom.js` |
| Configure app | `config.py` or `.env` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:
1. Check `logs/app.log` for error details
2. Review this README
3. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for more details
4. Open an issue on GitHub

## 🎯 Roadmap

- [ ] Real-time chat support
- [ ] Mobile app (React Native)
- [ ] API endpoints for external integrations
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] Quiz and assignment system
- [ ] Live video streaming

---

**Built with ❤️ using Flask**
