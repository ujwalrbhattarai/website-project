from app import app, db, User
from werkzeug.security import check_password_hash

with app.app_context():
    print("=" * 60)
    print("USER VERIFICATION REPORT")
    print("=" * 60)
    
    # Check all users
    all_users = User.query.all()
    print(f"\nTotal Users in Database: {len(all_users)}")
    print("-" * 60)
    
    # Check each user
    for user in all_users:
        print(f"\nUser ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Full Name: {user.full_name}")
        print(f"Role: {user.role}")
        print(f"Created: {user.created_at}")
    
    print("\n" + "=" * 60)
    print("FACULTY USERS CHECK")
    print("=" * 60)
    
    # Check faculty users specifically
    faculty_users = User.query.filter_by(role='faculty').all()
    print(f"\nTotal Faculty Users: {len(faculty_users)}")
    
    if faculty_users:
        for teacher in faculty_users:
            print(f"\n  Username: {teacher.username}")
            print(f"  Email: {teacher.email}")
            print(f"  Full Name: {teacher.full_name}")
            
            # Test password
            test_password = "teacher123"
            password_works = check_password_hash(teacher.password, test_password)
            print(f"  Password 'teacher123' works: {password_works}")
    else:
        print("\n  ⚠️  NO FACULTY USERS FOUND!")
        print("  Run init_db.py to create teacher accounts")
    
    print("\n" + "=" * 60)
    print("PASSWORD TEST")
    print("=" * 60)
    
    # Try to find teacher1
    teacher1 = User.query.filter_by(username='teacher1').first()
    if teacher1:
        print(f"\n✓ Found 'teacher1'")
        print(f"  Role: {teacher1.role}")
        print(f"  Testing password 'teacher123'...")
        if check_password_hash(teacher1.password, 'teacher123'):
            print("  ✓ Password 'teacher123' is CORRECT")
        else:
            print("  ✗ Password 'teacher123' is INCORRECT")
    else:
        print("\n✗ 'teacher1' NOT FOUND in database")
        print("  Please run: python init_db.py")
    
    print("\n" + "=" * 60)
