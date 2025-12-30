# 📁 Project Structure

This document explains the organized structure of the Educational Institute Platform.

## 🏗️ Architecture Overview

The project follows a **modular MVC (Model-View-Controller)** architecture with clear separation of concerns:

```
website-project/
├── app/                          # Main application package
│   ├── __init__.py              # App factory & initialization
│   ├── constants.py             # Application constants
│   │
│   ├── models/                   # Database models (organized by domain)
│   │   ├── __init__.py          # Model exports
│   │   ├── user.py              # User model
│   │   ├── course.py            # Course model
│   │   ├── video.py             # Video model
│   │   ├── enrollment.py        # Enrollment, Payment, StudyHistory
│   │   ├── schedule.py          # OnlineClass, TodoItem
│   │   └── support.py           # SupportTicket, TicketResponse, Certificate
│   │
│   ├── routes/                   # Route blueprints (organized by user role)
│   │   ├── __init__.py          # Blueprint exports
│   │   ├── auth.py              # Authentication routes
│   │   ├── student.py           # Student portal routes
│   │   ├── faculty.py           # Faculty portal routes
│   │   ├── admin.py             # Admin panel routes
│   │   ├── management.py        # Management portal routes
│   │   └── payment.py           # Payment processing routes
│   │
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py          # Utility exports
│   │   ├── decorators.py        # Route decorators (@login_required, etc.)
│   │   ├── filters.py           # Jinja2 template filters
│   │   ├── helpers.py           # Helper functions
│   │   ├── validators.py        # Input validation functions
│   │   └── error_handlers.py   # Error page handlers
│   │
│   ├── static/                   # Static assets (CSS, JS)
│   │   ├── css/
│   │   │   └── custom.css       # Custom styles
│   │   └── js/
│   │       └── custom.js        # Custom JavaScript
│   │
│   └── templates/               # Error page templates
│       └── errors/
│           ├── 403.html         # Forbidden error
│           ├── 404.html         # Not found error
│           └── 500.html         # Server error
│
├── templates/                    # Main application templates
│   ├── base.html                # Base template
│   ├── index.html               # Landing page
│   ├── login.html               # Login page
│   ├── register.html            # Registration page
│   ├── student/                 # Student portal templates
│   ├── faculty/                 # Faculty portal templates
│   ├── admin/                   # Admin panel templates
│   ├── management/              # Management portal templates
│   └── payment/                 # Payment templates
│
├── static/                       # User uploads
│   └── uploads/                 # Uploaded files (videos, images, etc.)
│
├── instance/                     # Instance-specific files
│   └── educational_institute.db # SQLite database
│
├── logs/                         # Application logs (created automatically)
│   └── app.log                  # Main log file
│
├── config.py                     # Application configuration
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # Main documentation
└── QUICK_REFERENCE.md           # Developer quick reference
```

## 📦 Package Organization

### `app/` - Main Application Package

#### `app/__init__.py` - Application Factory
- Creates Flask app instance
- Initializes extensions (database, logging)
- Registers blueprints, error handlers, filters
- Sets up directories and logging

#### `app/constants.py` - Application Constants
Centralized constants for:
- User roles (Student, Faculty, Admin, Management)
- Enrollment statuses
- Payment statuses and methods
- Support ticket statuses
- Priority levels
- File upload settings
- Grade levels

### `app/models/` - Database Models

**Organized by domain/feature:**

| File | Models | Purpose |
|------|--------|---------|
| `user.py` | User | Authentication & profiles |
| `course.py` | Course | Course management |
| `video.py` | Video | Video content |
| `enrollment.py` | Enrollment, Payment, StudyHistory | Student-course relationships |
| `schedule.py` | OnlineClass, TodoItem | Scheduling & tasks |
| `support.py` | SupportTicket, TicketResponse, Certificate | Support & certifications |

**Benefits:**
- ✅ Easy to find specific models
- ✅ Related models grouped together
- ✅ Clear dependencies and relationships
- ✅ Better code maintainability

### `app/routes/` - Route Blueprints

**Organized by user role:**

| Blueprint | Prefix | Purpose |
|-----------|--------|---------|
| `auth.py` | `/` | Login, register, logout |
| `student.py` | `/student` | Student dashboard, courses, videos |
| `faculty.py` | `/faculty` | Faculty courses, uploads, analytics |
| `admin.py` | `/admin` | User management, reports |
| `management.py` | `/management` | Reports, oversight |
| `payment.py` | `/payment` | Payment processing |

**Benefits:**
- ✅ Clear separation by user role
- ✅ Easy permission management
- ✅ Independent testing
- ✅ Scalable architecture

### `app/utils/` - Utilities

**Reusable functions and helpers:**

| File | Purpose | Key Functions |
|------|---------|---------------|
| `decorators.py` | Route protection | @login_required, @admin_required |
| `filters.py` | Template formatting | format_currency, time_ago |
| `helpers.py` | Common operations | generate_unique_filename, sanitize_string |
| `validators.py` | Input validation | validate_email, validate_password |
| `error_handlers.py` | Error pages | 404, 500, 403 handlers |

**Benefits:**
- ✅ DRY (Don't Repeat Yourself)
- ✅ Centralized validation
- ✅ Consistent error handling
- ✅ Reusable across routes

## 🔄 Data Flow

### Request Flow
```
User Request
    ↓
Flask Router
    ↓
Blueprint Route (@login_required decorator)
    ↓
Validators (validate input)
    ↓
Models (database operations)
    ↓
Helpers (process data)
    ↓
Template (render response)
    ↓
Response to User
```

### Example: Student Viewing a Course

1. **User visits** `/student/course/1`
2. **Route decorator** checks authentication (@login_required)
3. **Route handler** in `app/routes/student.py` processes request
4. **Model query** fetches Course from database
5. **Helper functions** format data
6. **Template** renders `templates/student/course_detail.html`
7. **Filters** format currency, dates in template
8. **Response** sent to browser

## 🎯 Design Principles

### 1. Separation of Concerns
- **Models**: Data structure and relationships
- **Routes**: Request handling and business logic
- **Templates**: Presentation layer
- **Utils**: Reusable functionality

### 2. Modularity
- Each blueprint is independent
- Models split by domain
- Utilities organized by purpose
- Easy to test and maintain

### 3. DRY (Don't Repeat Yourself)
- Validators centralized in `validators.py`
- Decorators for common checks
- Template filters for formatting
- Helper functions for operations

### 4. Security
- Input validation before processing
- SQL injection protection (SQLAlchemy ORM)
- Password hashing (Werkzeug)
- Role-based access control (decorators)

## 📚 How to Navigate the Codebase

### Finding Specific Functionality

**Want to add a new student feature?**
1. Add route in `app/routes/student.py`
2. Create template in `templates/student/`
3. Add model if needed in `app/models/`
4. Use decorators from `app/utils/decorators.py`

**Want to add validation?**
1. Add validator in `app/utils/validators.py`
2. Use in route handlers
3. Import from `app.utils.validators`

**Want to add a template filter?**
1. Add filter in `app/utils/filters.py`
2. Register in `app/__init__.py` → `register_filters()`
3. Use in templates: `{{ value|your_filter }}`

**Want to add a new model?**
1. Create file in `app/models/` (e.g., `notification.py`)
2. Import in `app/models/__init__.py`
3. Add relationships to existing models if needed

## 🔧 Configuration

### Constants (`app/constants.py`)
- All magic strings in one place
- Easy to update values
- Type-safe with classes
- Better IDE autocomplete

### Environment Variables (`.env`)
- Secrets and credentials
- Environment-specific settings
- Never committed to git

### Config (`config.py`)
- Application configuration
- Database settings
- Upload paths
- Email settings

## 🚀 Benefits of This Structure

### For Developers
- ✅ Easy to find code
- ✅ Clear responsibilities
- ✅ Simple to test
- ✅ Better IDE support
- ✅ Less merge conflicts

### For Teams
- ✅ Multiple developers can work simultaneously
- ✅ Clear code ownership
- ✅ Easier code reviews
- ✅ Simpler onboarding

### For Maintenance
- ✅ Changes isolated to specific files
- ✅ Clear impact analysis
- ✅ Easy to debug
- ✅ Better logging

### For Scaling
- ✅ Add new features without touching existing code
- ✅ Extract to microservices if needed
- ✅ Easy to optimize specific parts
- ✅ Clear performance bottlenecks

## 📖 Related Documentation

- **README.md** - Installation and usage guide
- **QUICK_REFERENCE.md** - Day-to-day developer reference
- **config.py** - Configuration options

---

**This structure follows industry best practices and is ready for production use!** 🎉
