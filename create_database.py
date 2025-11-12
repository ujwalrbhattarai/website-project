"""
Create PostgreSQL Database
This script creates the 'the_innovative_group' database
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    print("=" * 60)
    print("PostgreSQL Database Creation")
    print("=" * 60)
    print()
    
    # Connection parameters
    db_params = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'Biratnagar-8'
    }
    
    database_name = 'the_innovative_group'
    
    try:
        # Connect to default 'postgres' database
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(**db_params, database='postgres')
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        print(f"Checking if database '{database_name}' exists...")
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database_name,)
        )
        
        exists = cursor.fetchone()
        
        if exists:
            print(f"✓ Database '{database_name}' already exists!")
            print()
            print("You can now run:")
            print("  1. python init_db.py  (to create tables)")
            print("  2. python app.py      (to start the app)")
        else:
            # Create database
            print(f"Creating database '{database_name}'...")
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
            )
            print(f"✓ Database '{database_name}' created successfully!")
            print()
            print("Next steps:")
            print("  1. python init_db.py  (to create tables and sample data)")
            print("  2. python app.py      (to start the application)")
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 60)
        
    except psycopg2.OperationalError as e:
        error_str = str(e)
        print("✗ Connection failed!")
        print()
        
        if "authentication failed" in error_str:
            print("ERROR: Invalid username or password")
            print("→ Check password in create_database.py (line 20)")
            print("→ Current password: Biratnagar-8")
        elif "could not connect to server" in error_str:
            print("ERROR: Cannot connect to PostgreSQL server")
            print("→ Check if PostgreSQL is running:")
            print("  Windows: Services → postgresql-x64-xx → Start")
        else:
            print(f"ERROR: {error_str}")
        
        return False
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    try:
        create_database()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
