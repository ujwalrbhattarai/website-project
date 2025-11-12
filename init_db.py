"""
Database Initialization Script
This script creates the database and populates it with sample data
"""

from app import app, db, User, Course, Video, Enrollment, Payment, StudyHistory, OnlineClass, TodoItem, SupportTicket, TicketResponse, Certificate
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Drop all tables and recreate them
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create Admin User
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@eduinstitute.edu.np',
            password=generate_password_hash('admin123'),
            full_name='System Administrator',
            role='admin'
        )
        db.session.add(admin)
        
        # Create Faculty Users
        print("Creating faculty users...")
        faculty1 = User(
            username='teacher1',
            email='teacher1@eduinstitute.edu.np',
            password=generate_password_hash('teacher123'),
            full_name='Dr. Ramesh Kumar',
            role='faculty'
        )
        
        faculty2 = User(
            username='teacher2',
            email='teacher2@eduinstitute.edu.np',
            password=generate_password_hash('teacher123'),
            full_name='Prof. Sita Sharma',
            role='faculty'
        )
        
        db.session.add(faculty1)
        db.session.add(faculty2)
        
        # Create Management User
        print("Creating management user...")
        management = User(
            username='manager1',
            email='manager@eduinstitute.edu.np',
            password=generate_password_hash('manager123'),
            full_name='Prakash Subedi',
            role='management'
        )
        db.session.add(management)
        
        # Create Student Users
        print("Creating student users...")
        students = []
        student_names = [
            'Aayush Thapa', 'Priya Shrestha', 'Bikash Adhikari',
            'Anjali Rai', 'Suresh Tamang', 'Kritika Gurung'
        ]
        
        for i, name in enumerate(student_names, 1):
            student = User(
                username=f'student{i}',
                email=f'student{i}@eduinstitute.edu.np',
                password=generate_password_hash('student123'),
                full_name=name,
                role='student'
            )
            students.append(student)
            db.session.add(student)
        
        db.session.commit()
        
        # Create Courses
        print("Creating courses...")
        
        course1 = Course(
            title='Python Programming Fundamentals',
            description='Learn Python from scratch. This comprehensive course covers variables, data types, control structures, functions, and object-oriented programming. Perfect for beginners in Nepal looking to start their programming journey.',
            price_npr=2500.00,
            duration_hours=40,
            instructor_id=faculty1.id,
            demo_video_url='https://www.youtube.com/embed/rfscVS0vtbw',
            thumbnail_url='https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400'
        )
        
        course2 = Course(
            title='Web Development with Flask',
            description='Master web development using Flask framework. Build dynamic websites and web applications. Learn about routing, templates, databases, and deployment. Suitable for intermediate Python developers.',
            price_npr=3500.00,
            duration_hours=50,
            instructor_id=faculty1.id,
            demo_video_url='https://www.youtube.com/embed/Z1RJmh_OqeA',
            thumbnail_url='https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400'
        )
        
        course3 = Course(
            title='Data Science with Python',
            description='Dive into data science using Python. Learn pandas, numpy, matplotlib, and machine learning basics. Work with real-world datasets and create insightful visualizations. Ideal for aspiring data scientists.',
            price_npr=4500.00,
            duration_hours=60,
            instructor_id=faculty2.id,
            demo_video_url='https://www.youtube.com/embed/ua-CiDNNj30',
            thumbnail_url='https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400'
        )
        
        course4 = Course(
            title='Digital Marketing Essentials',
            description='Master digital marketing strategies for the Nepali market. Learn SEO, social media marketing, content marketing, and analytics. Perfect for entrepreneurs and marketing professionals.',
            price_npr=3000.00,
            duration_hours=35,
            instructor_id=faculty2.id,
            demo_video_url='https://www.youtube.com/embed/nU-IIXBWlS4',
            thumbnail_url='https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400'
        )
        
        db.session.add_all([course1, course2, course3, course4])
        db.session.commit()
        
        # Create Videos for Courses
        print("Creating course videos...")
        
        # Videos for Python Programming
        python_videos = [
            {
                'title': 'Introduction to Python',
                'description': 'Welcome to Python! Learn what Python is and why it is popular.',
                'video_url': 'https://www.youtube.com/embed/Y8Tko2YC5hA',
                'duration_minutes': 15,
                'order': 1
            },
            {
                'title': 'Variables and Data Types',
                'description': 'Understanding variables, integers, floats, strings, and booleans.',
                'video_url': 'https://www.youtube.com/embed/Z1Yd7upQsXY',
                'duration_minutes': 25,
                'order': 2
            },
            {
                'title': 'Control Flow - If/Else',
                'description': 'Learn conditional statements and decision making.',
                'video_url': 'https://www.youtube.com/embed/PqFKRqpHrjw',
                'duration_minutes': 20,
                'order': 3
            },
            {
                'title': 'Loops in Python',
                'description': 'Master for loops and while loops for iteration.',
                'video_url': 'https://www.youtube.com/embed/94UHCEmprCY',
                'duration_minutes': 30,
                'order': 4
            }
        ]
        
        for video_data in python_videos:
            video = Video(course_id=course1.id, **video_data)
            db.session.add(video)
        
        # Videos for Flask
        flask_videos = [
            {
                'title': 'Flask Introduction',
                'description': 'Getting started with Flask web framework.',
                'video_url': 'https://www.youtube.com/embed/Z1RJmh_OqeA',
                'duration_minutes': 18,
                'order': 1
            },
            {
                'title': 'Routing and Views',
                'description': 'Creating routes and handling requests.',
                'video_url': 'https://www.youtube.com/embed/mqhxxeeTbu0',
                'duration_minutes': 22,
                'order': 2
            },
            {
                'title': 'Templates with Jinja2',
                'description': 'Dynamic HTML generation using templates.',
                'video_url': 'https://www.youtube.com/embed/bxhXQG1qJPM',
                'duration_minutes': 28,
                'order': 3
            }
        ]
        
        for video_data in flask_videos:
            video = Video(course_id=course2.id, **video_data)
            db.session.add(video)
        
        # Videos for Data Science
        ds_videos = [
            {
                'title': 'Data Science Overview',
                'description': 'Introduction to data science concepts and tools.',
                'video_url': 'https://www.youtube.com/embed/ua-CiDNNj30',
                'duration_minutes': 20,
                'order': 1
            },
            {
                'title': 'Pandas Basics',
                'description': 'Working with dataframes and series.',
                'video_url': 'https://www.youtube.com/embed/vmEHCJofslg',
                'duration_minutes': 35,
                'order': 2
            }
        ]
        
        for video_data in ds_videos:
            video = Video(course_id=course3.id, **video_data)
            db.session.add(video)
        
        # Videos for Digital Marketing
        dm_videos = [
            {
                'title': 'Digital Marketing Introduction',
                'description': 'Overview of digital marketing channels.',
                'video_url': 'https://www.youtube.com/embed/nU-IIXBWlS4',
                'duration_minutes': 16,
                'order': 1
            },
            {
                'title': 'SEO Fundamentals',
                'description': 'Search engine optimization basics.',
                'video_url': 'https://www.youtube.com/embed/hF515-0Tduk',
                'duration_minutes': 25,
                'order': 2
            }
        ]
        
        for video_data in dm_videos:
            video = Video(course_id=course4.id, **video_data)
            db.session.add(video)
        
        db.session.commit()
        
        # Create Enrollments and Payments
        print("Creating sample enrollments and payments...")
        
        courses = [course1, course2, course3, course4]
        
        for student in students[:4]:  # First 4 students get enrollments
            # Enroll in 1-2 random courses
            num_courses = random.randint(1, 2)
            selected_courses = random.sample(courses, num_courses)
            
            for course in selected_courses:
                # Create enrollment
                enrollment = Enrollment(
                    student_id=student.id,
                    course_id=course.id,
                    enrollment_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    completion_percentage=random.uniform(10, 90),
                    status='active'
                )
                db.session.add(enrollment)
                
                # Create payment
                payment = Payment(
                    student_id=student.id,
                    course_id=course.id,
                    amount_npr=course.price_npr,
                    payment_method='online',
                    status='completed',
                    payment_date=enrollment.enrollment_date,
                    transaction_id=f'TXN{random.randint(100000, 999999)}'
                )
                db.session.add(payment)
        
        db.session.commit()
        
        # Create sample online classes
        print("Creating sample online classes...")
        
        now = datetime.utcnow()
        
        # Upcoming classes
        online_class1 = OnlineClass(
            course_id=course1.id,
            title='Python Live Q&A Session',
            description='Join us for a live question and answer session about Python programming.',
            meeting_link='https://zoom.us/j/123456789',
            scheduled_at=now + timedelta(days=2, hours=14),
            duration_minutes=90,
            created_by=faculty1.id
        )
        
        online_class2 = OnlineClass(
            course_id=course2.id,
            title='Flask Project Demo',
            description='Live demonstration of building a complete Flask application.',
            meeting_link='https://meet.google.com/abc-defg-hij',
            scheduled_at=now + timedelta(days=5, hours=16),
            duration_minutes=120,
            created_by=faculty1.id
        )
        
        online_class3 = OnlineClass(
            course_id=course3.id,
            title='Data Visualization Workshop',
            description='Interactive workshop on creating visualizations with matplotlib and seaborn.',
            meeting_link='https://zoom.us/j/987654321',
            scheduled_at=now + timedelta(days=7, hours=15),
            duration_minutes=90,
            created_by=faculty2.id
        )
        
        # Past classes
        past_class1 = OnlineClass(
            course_id=course1.id,
            title='Python Setup and Installation',
            description='Getting Python installed and configured on your system.',
            meeting_link='https://zoom.us/j/111222333',
            scheduled_at=now - timedelta(days=5, hours=14),
            duration_minutes=60,
            created_by=faculty1.id
        )
        
        past_class2 = OnlineClass(
            course_id=course4.id,
            title='Social Media Marketing Strategies',
            description='Effective social media marketing for Nepali businesses.',
            meeting_link='https://meet.google.com/xyz-uvw-rst',
            scheduled_at=now - timedelta(days=10, hours=16),
            duration_minutes=90,
            created_by=faculty2.id
        )
        
        db.session.add_all([online_class1, online_class2, online_class3, past_class1, past_class2])
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\nDefault Login Credentials:")
        print("\nAdmin:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nManagement:")
        print("  Username: manager1")
        print("  Password: manager123")
        print("\nFaculty:")
        print("  Username: teacher1")
        print("  Password: teacher123")
        print("\nStudent:")
        print("  Username: student1")
        print("  Password: student123")
        print("\n" + "="*50)
        print("\nYou can now run the application using: python app.py")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
