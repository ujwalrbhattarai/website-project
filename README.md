# Educational Institute Website

A comprehensive educational institution website built with Flask, featuring separate portals for Students, Faculty, and Admins. The system supports video course management, payment tracking, and student progress monitoring with prices displayed in Nepali Rupees (NPR).

## Features

### 🎓 Student Portal
- Browse and enroll in courses
- Watch video lectures
- Track learning progress
- View payment history
- Course completion tracking

### 👨‍🏫 Faculty/Teacher Portal
- Create and manage courses
- Upload video content
- Track student enrollments
- Manage course materials

### 👨‍💼 Admin Portal
- User management (Students, Faculty)
- Course oversight
- Payment tracking and revenue reports
- System-wide analytics
- Monitor enrollments and activity

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite (easily switchable to MySQL/PostgreSQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Authentication**: Flask session management with password hashing
- **Icons**: Font Awesome 6

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Initialize the Database**
   ```powershell
   python init_db.py
   ```
   This will create sample data including:
   - Admin user (username: admin, password: admin123)
   - Faculty user (username: teacher1, password: teacher123)
   - Student user (username: student1, password: student123)
   - Sample courses with videos

3. **Run the Application**
   ```powershell
   python app.py
   ```

4. **Access the Website**
   Open your browser and navigate to: `http://localhost:5000`

## Default Login Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`

### Faculty Account
- Username: `teacher1`
- Password: `teacher123`

### Student Account
- Username: `student1`
- Password: `student123`

**⚠️ IMPORTANT: Change these passwords in production!**

## Database Configuration

The application uses SQLite by default. To switch to MySQL or PostgreSQL:

1. Install the appropriate database driver:
   ```powershell
   # For MySQL
   pip install pymysql
   
   # For PostgreSQL
   pip install psycopg2
   ```

2. Update the database URI in `app.py`:
   ```python
   # For MySQL
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
   
   # For PostgreSQL
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
   ```

## Project Structure

```
project/
│
├── app.py                          # Main application file
├── init_db.py                      # Database initialization script
├── requirements.txt                # Python dependencies
│
├── templates/                      # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Homepage
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   │
│   ├── student/                   # Student portal templates
│   │   ├── dashboard.html
│   │   ├── courses.html
│   │   ├── course_detail.html
│   │   └── watch_video.html
│   │
│   ├── faculty/                   # Faculty portal templates
│   │   ├── dashboard.html
│   │   ├── add_course.html
│   │   ├── course_detail.html
│   │   └── add_video.html
│   │
│   └── admin/                     # Admin portal templates
│       ├── dashboard.html
│       ├── users.html
│       ├── courses.html
│       └── payments.html
│
└── static/                        # Static files (created automatically)
    └── uploads/                   # Uploaded content
        └── videos/                # Video files
```

## Features in Detail

### Video Management
- Support for YouTube embedded videos
- Local video file support
- Video progress tracking
- Watch time monitoring

### Payment System
- Course enrollment with payment
- Payment history tracking
- Revenue analytics for admin
- All prices in Nepali Rupees (NPR)

### Student Progress Tracking
- Course completion percentage
- Video watch history
- Last watched timestamp
- Study duration tracking

## Customization

### Changing Currency Symbol
The NPR symbol (रू) is implemented via CSS. To change it, update the `.npr-symbol::before` in `templates/base.html`.

### Styling
The application uses Bootstrap 5 with custom CSS variables. Modify the `:root` variables in `templates/base.html` to change colors:
```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --success-color: #27ae60;
    --npr-color: #dc143c;
}
```

## Security Notes

1. **Change the SECRET_KEY** in `app.py` before deploying to production
2. **Update default passwords** immediately after setup
3. **Use HTTPS** in production environment
4. **Implement proper payment gateway** integration for real transactions
5. **Add email verification** for user registration
6. **Enable CSRF protection** for forms

## Future Enhancements

- [ ] Real payment gateway integration (eSewa, Khalti, etc.)
- [ ] Email notifications for enrollments
- [ ] Quiz and assignment features
- [ ] Certificate generation
- [ ] Discussion forums
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## Troubleshooting

### Database Issues
If you encounter database errors, delete the existing database file and reinitialize:
```powershell
Remove-Item educational_institute.db
python init_db.py
```

### Port Already in Use
If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, port=5001)
```

## Support

For issues, questions, or contributions, please create an issue in the repository.

## License

This project is created for educational purposes.
