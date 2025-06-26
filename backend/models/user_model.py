"""
User Model - Handles user data and authentication
"""
import hashlib
import sqlite3
from datetime import datetime
from typing import Optional, Dict, List
import os

class UserModel:
    """Model class for handling user data and database operations"""
    
    def __init__(self, db_path: str = "users.db"):
        """Initialize the user model with database connection"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create user_platforms table for storing platform ratings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_platforms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                platform_name TEXT NOT NULL,
                handle TEXT,
                rating INTEGER,
                max_rating INTEGER,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, platform_name)
            )
        ''')
        
        # Create user_courses table for storing course data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course_name TEXT NOT NULL,
                institution TEXT,
                completion_date DATE,
                bonus_points REAL DEFAULT 0.0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, email: str, password: str, username: str = None) -> bool:
        """Create a new user account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (email, password_hash, username)
                VALUES (?, ?, ?)
            ''', (email, password_hash, username or email.split('@')[0]))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # Email already exists
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self._hash_password(password)
        
        cursor.execute('''
            SELECT id, email, username, created_at
            FROM users 
            WHERE email = ? AND password_hash = ? AND is_active = 1
        ''', (email, password_hash))
        
        user_data = cursor.fetchone()
        
        if user_data:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (user_data[0],))
            conn.commit()
            
            conn.close()
            return {
                'id': user_data[0],
                'email': user_data[1],
                'username': user_data[2],
                'created_at': user_data[3]
            }
        
        conn.close()
        return None
    
    def save_platform_data(self, user_id: int, platform_name: str, handle: str, rating: int, max_rating: int = None):
        """Save platform rating data for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_platforms 
            (user_id, platform_name, handle, rating, max_rating, last_updated)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, platform_name, handle, rating, max_rating))
        
        conn.commit()
        conn.close()
    
    def get_user_platforms(self, user_id: int) -> List[Dict]:
        """Get all platform data for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT platform_name, handle, rating, max_rating, last_updated
            FROM user_platforms
            WHERE user_id = ?
        ''', (user_id,))
        
        platforms = []
        for row in cursor.fetchall():
            platforms.append({
                'platform_name': row[0],
                'handle': row[1],
                'rating': row[2],
                'max_rating': row[3],
                'last_updated': row[4]
            })
        
        conn.close()
        return platforms
    
    def save_course_data(self, user_id: int, course_name: str, institution: str = None, 
                        completion_date: str = None, bonus_points: float = 0.0):
        """Save course completion data for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_courses 
            (user_id, course_name, institution, completion_date, bonus_points)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, course_name, institution, completion_date, bonus_points))
        
        conn.commit()
        conn.close()
    
    def get_user_courses(self, user_id: int) -> List[Dict]:
        """Get all course data for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT course_name, institution, completion_date, bonus_points
            FROM user_courses
            WHERE user_id = ?
        ''', (user_id,))
        
        courses = []
        for row in cursor.fetchall():
            courses.append({
                'course_name': row[0],
                'institution': row[1],
                'completion_date': row[2],
                'bonus_points': row[3]
            })
        
        conn.close()
        return courses
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user data by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, username, created_at, last_login
            FROM users
            WHERE id = ? AND is_active = 1
        ''', (user_id,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return {
                'id': user_data[0],
                'email': user_data[1],
                'username': user_data[2],
                'created_at': user_data[3],
                'last_login': user_data[4]
            }
        return None
