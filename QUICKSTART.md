# Quick Start Guide

## Getting Started (3 Simple Steps)

### Option 1: Automated Setup (Recommended)
```powershell
.\setup_and_run.ps1
```

### Option 2: Manual Setup
```powershell
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Initialize database
python init_db.py

# Step 3: Run the application
python app.py
```

Then open your browser to: http://localhost:5000

## Default Login Credentials

| Role    | Username  | Password    |
|---------|-----------|-------------|
| Admin   | admin     | admin123    |
| Faculty | teacher1  | teacher123  |
| Student | student1  | student123  |

## Common Tasks

### Adding a New Course (Faculty)
1. Login as faculty user
2. Click "Add Course" button
3. Fill in course details (title, description, price in NPR, duration)
4. Click "Create Course"
5. Add videos to the course from the course detail page

### Enrolling in a Course (Student)
1. Login as student user
2. Browse available courses
3. Click "View Details" on desired course
4. Click "Enroll Now" button
5. Start learning!

### Managing Users (Admin)
1. Login as admin user
2. Navigate to "Users" from the navigation menu
3. View all registered users and their roles
4. Monitor user activity

### Tracking Payments (Admin)
1. Login as admin user
2. Navigate to "Payments" from the navigation menu
3. View all payment transactions
4. Filter by status (completed, pending, failed)

## Video Integration

### YouTube Videos
Use the embed URL format:
```
https://www.youtube.com/embed/VIDEO_ID
```

### Local Videos
1. Place video file in `static/uploads/videos/` folder
2. Use relative path:
```
/static/uploads/videos/your-video.mp4
```

## Database Management

### Reset Database
```powershell
Remove-Item educational_institute.db
python init_db.py
```

### Backup Database
```powershell
Copy-Item educational_institute.db educational_institute_backup.db
```

### Switch to MySQL
1. Install MySQL driver:
```powershell
pip install pymysql
```

2. Update `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
```

3. Create database in MySQL:
```sql
CREATE DATABASE educational_institute;
```

4. Run initialization:
```powershell
python init_db.py
```

## Customization

### Change Currency
Edit `templates/base.html`, find `.npr-symbol::before` and change:
```css
.npr-symbol::before {
    content: "$";  /* Change to your currency symbol */
}
```

### Change Colors
Edit `templates/base.html`, modify CSS variables:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
}
```

### Add Payment Gateway

For eSewa integration:
1. Get merchant credentials from eSewa
2. Update `config.py` with your credentials
3. Implement payment verification endpoint
4. Update enrollment route to use eSewa API

For Khalti integration:
1. Get API keys from Khalti
2. Update `config.py` with your credentials
3. Add Khalti JavaScript SDK
4. Implement payment verification

## Troubleshooting

### Port 5000 already in use
Change port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Database locked error
Close all connections to database file:
```powershell
# Restart the application
```

### Template not found error
Ensure you're running from the project root directory:
```powershell
cd "d:\college\4th sem\python\project"
python app.py
```

### Static files not loading
Clear browser cache or use Ctrl+Shift+R to hard refresh

## Project Structure
```
project/
├── app.py                      # Main application
├── config.py                   # Configuration
├── init_db.py                  # Database initialization
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── QUICKSTART.md              # This file
├── setup_and_run.ps1          # Setup script
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student/               # Student templates
│   ├── faculty/               # Faculty templates
│   └── admin/                 # Admin templates
│
└── static/                     # Static files
    └── uploads/
        └── videos/
```

## Security Checklist for Production

- [ ] Change SECRET_KEY in config.py
- [ ] Change all default passwords
- [ ] Enable HTTPS
- [ ] Use environment variables for sensitive data
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Enable SQL injection protection (already done via SQLAlchemy)
- [ ] Implement file upload validation
- [ ] Add backup strategy
- [ ] Configure proper error handling
- [ ] Use production WSGI server (gunicorn, uWSGI)

## Next Steps

1. ✅ Set up the application
2. ✅ Login with default credentials
3. ✅ Explore different user portals
4. 📝 Customize for your institution
5. 🎨 Modify styling and branding
6. 💳 Integrate payment gateway
7. 📧 Add email notifications
8. 🚀 Deploy to production

## Need Help?

- Check README.md for detailed documentation
- Review code comments in app.py
- Check console output for error messages
- Ensure all dependencies are installed

## Tips

- Use Chrome/Firefox Developer Tools (F12) to debug frontend issues
- Check Flask console output for backend errors
- Test with different user roles to understand the system
- Start with sample data, then modify as needed
- Keep database backups before making changes

Happy Learning! 🎓
