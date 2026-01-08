"""
Database migration to add security fields to users table
Run this after updating the User model
"""
from sqlalchemy import text
from app.db.database import get_db

def migrate_users_table():
    """
    Add password_hash, role, and is_active columns to existing users table
    """
    db = next(get_db())
    
    try:
        # Check if columns already exist
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name IN ('password_hash', 'role', 'is_active')
        """))
        existing_columns = [row[0] for row in result]
        
        # Add password_hash column
        if 'password_hash' not in existing_columns:
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN password_hash VARCHAR
            """))
            print("✓ Added password_hash column")
        
        # Add role column
        if 'role' not in existing_columns:
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR DEFAULT 'user'
            """))
            print("✓ Added role column")
        
        # Add is_active column
        if 'is_active' not in existing_columns:
            db.execute(text("""
                ALTER TABLE users 
                ADD COLUMN is_active BOOLEAN DEFAULT true
            """))
            print("✓ Added is_active column")
        
        db.commit()
        print("✅ Migration completed successfully")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Migration failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_users_table()
