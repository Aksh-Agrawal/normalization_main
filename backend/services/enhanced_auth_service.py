"""
Enhanced Authentication Service - Updated for new database schema
"""
import re
import bcrypt
import json
from typing import Optional, Dict, Tuple, List
from datetime import datetime
import sqlite3

class EnhancedAuthService:
    """Enhanced Authentication Service with improved database integration"""
    
    def __init__(self, db_path: str = "users.db"):
        """Initialize enhanced authentication service"""
        self.db_path = db_path
        self.current_user = None
        self.current_session_id = None
        
        # Initialize database if not exists
        self._ensure_database_ready()
    
    def _ensure_database_ready(self):
        """Ensure database is ready with enhanced schema"""
        try:
            from enhanced_db_model import EnhancedUserModel
            # This will create/migrate the database if needed
            EnhancedUserModel(self.db_path)
        except ImportError:
            print("⚠️  Enhanced database model not available, using basic initialization")
            self._basic_init()
    
    def _basic_init(self):
        """Basic database initialization fallback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        conn.close()
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            # Fallback for old SHA-256 hashes
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username: str) -> Tuple[bool, str]:
        """Validate username"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        if len(username) > 30:
            return False, "Username must be no more than 30 characters long"
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        return True, "Username is valid"
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if len(password) > 128:
            return False, "Password must be no more than 128 characters long"
        
        checks = [
            (r'[A-Z]', "at least one uppercase letter"),
            (r'[a-z]', "at least one lowercase letter"),
            (r'\d', "at least one digit")
        ]
        
        for pattern, message in checks:
            if not re.search(pattern, password):
                return False, f"Password must contain {message}"
        
        return True, "Password is valid"
    
    def register_user(self, email: str, password: str, username: str = None, full_name: str = None) -> Tuple[bool, str]:
        """Register a new user with enhanced validation"""
        # Validate email
        if not self.validate_email(email):
            return False, "Invalid email format"
        
        # Generate username if not provided
        if not username:
            username = email.split('@')[0]
            # Make username unique if it exists
            base_username = username
            counter = 1
            while self._username_exists(username):
                username = f"{base_username}{counter}"
                counter += 1
        
        # Validate username
        is_valid, message = self.validate_username(username)
        if not is_valid:
            return False, message
        
        # Check if username already exists
        if self._username_exists(username):
            return False, "Username already exists"
        
        # Validate password
        is_valid, message = self.validate_password(password)
        if not is_valid:
            return False, message
        
        # Create user
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self._hash_password(password)
            
            # Check if using new schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_new'")
            if cursor.fetchone():
                cursor.execute('''
                    INSERT INTO users_new (email, password_hash, username, full_name, email_verified)
                    VALUES (?, ?, ?, ?, ?)
                ''', (email, password_hash, username, full_name, 0))
            else:
                # Fallback to old schema
                cursor.execute('''
                    INSERT INTO users (email, password_hash, username)
                    VALUES (?, ?, ?)
                ''', (email, password_hash, username))
            
            conn.commit()
            conn.close()
            
            # Log system analytics
            self._log_analytics("user_registration", 1, {"email_domain": email.split('@')[1]})
            
            return True, "User registered successfully"
            
        except sqlite3.IntegrityError as e:
            if "email" in str(e):
                return False, "Email already exists"
            elif "username" in str(e):
                return False, "Username already exists"
            else:
                return False, "Registration failed due to data conflict"
        except Exception as e:
            print(f"Registration error: {e}")
            return False, "Registration failed due to system error"
    
    def login_user(self, email: str, password: str, remember_me: bool = False) -> Tuple[bool, str, Optional[Dict]]:
        """Enhanced user login with session tracking"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if using new schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_new'")
            use_new_schema = cursor.fetchone() is not None
            
            if use_new_schema:
                cursor.execute('''
                    SELECT id, email, username, full_name, password_hash, login_count, is_active
                    FROM users_new 
                    WHERE email = ? AND is_active = 1
                ''', (email,))
            else:
                cursor.execute('''
                    SELECT id, email, username, password_hash, is_active
                    FROM users 
                    WHERE email = ? AND is_active = 1
                ''', (email,))
            
            user_data = cursor.fetchone()
            
            if not user_data:
                conn.close()
                return False, "Invalid email or password", None
            
            # Verify password
            if use_new_schema:
                user_id, email, username, full_name, password_hash, login_count, is_active = user_data
            else:
                user_id, email, username, password_hash, is_active = user_data
                full_name = None
                login_count = 0
            
            if not self._verify_password(password, password_hash):
                conn.close()
                return False, "Invalid email or password", None
            
            # Update login information
            if use_new_schema:
                cursor.execute('''
                    UPDATE users_new 
                    SET last_login = CURRENT_TIMESTAMP, 
                        last_active = CURRENT_TIMESTAMP,
                        login_count = login_count + 1
                    WHERE id = ?
                ''', (user_id,))
                
                # Create session record
                cursor.execute('''
                    INSERT INTO user_sessions (user_id, session_start, actions_performed)
                    VALUES (?, CURRENT_TIMESTAMP, 0)
                ''', (user_id,))
                self.current_session_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user_id,))
            
            conn.commit()
            conn.close()
            
            # Set current user
            self.current_user = {
                'id': user_id,
                'email': email,
                'username': username,
                'full_name': full_name,
                'login_count': login_count + 1
            }
            
            # Log analytics
            self._log_analytics("user_login", 1, {"remember_me": remember_me})
            
            return True, "Login successful", self.current_user
            
        except Exception as e:
            print(f"Login error: {e}")
            return False, "Login failed due to system error", None
    
    def logout_user(self):
        """Enhanced logout with session cleanup"""
        if self.current_user and self.current_session_id:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Close session
                cursor.execute('''
                    UPDATE user_sessions 
                    SET session_end = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (self.current_session_id,))
                
                conn.commit()
                conn.close()
                
                # Log analytics
                self._log_analytics("user_logout", 1)
                
            except Exception as e:
                print(f"Logout error: {e}")
        
        self.current_user = None
        self.current_session_id = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        return self.current_user
    
    def require_authentication(self):
        """Require authentication for protected operations"""
        if not self.is_logged_in():
            raise PermissionError("User must be logged in to perform this action")
    
    def save_user_platform(self, platform_name: str, handle: str, rating: int, 
                          max_rating: int = None, contests: int = 0, problems: int = 0):
        """Save platform data with enhanced tracking"""
        self.require_authentication()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get platform ID
            cursor.execute("SELECT id FROM platforms WHERE LOWER(name) = LOWER(?)", (platform_name,))
            platform_result = cursor.fetchone()
            
            if not platform_result:
                # Platform doesn't exist, insert it
                cursor.execute('''
                    INSERT INTO platforms (name, display_name, max_rating, difficulty_weight, supports_auto_fetch)
                    VALUES (?, ?, ?, ?, ?)
                ''', (platform_name.lower(), platform_name, max_rating or 3000, 1.0, 0))
                platform_id = cursor.lastrowid
            else:
                platform_id = platform_result[0]
            
            # Check if using new schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_platforms_new'")
            use_new_schema = cursor.fetchone() is not None
            
            if use_new_schema:
                # Check for existing record
                cursor.execute('''
                    SELECT id, current_rating FROM user_platforms_new 
                    WHERE user_id = ? AND platform_id = ?
                ''', (self.current_user['id'], platform_id))
                
                existing = cursor.fetchone()
                
                if existing:
                    old_rating = existing[1]
                    # Update existing record
                    cursor.execute('''
                        UPDATE user_platforms_new 
                        SET handle = ?, current_rating = ?, 
                            max_rating_achieved = COALESCE(MAX(max_rating_achieved, ?), ?),
                            contests_participated = ?, problems_solved = ?,
                            last_updated = CURRENT_TIMESTAMP,
                            verification_status = 'verified'
                        WHERE user_id = ? AND platform_id = ?
                    ''', (handle, rating, rating, rating, contests, problems, 
                          self.current_user['id'], platform_id))
                    
                    # Record rating history if rating changed
                    if old_rating != rating:
                        cursor.execute('''
                            INSERT INTO rating_history (user_platform_id, old_rating, new_rating, rating_change, source)
                            VALUES (?, ?, ?, ?, 'manual')
                        ''', (existing[0], old_rating, rating, rating - old_rating))
                else:
                    # Insert new record
                    cursor.execute('''
                        INSERT INTO user_platforms_new 
                        (user_id, platform_id, handle, current_rating, max_rating_achieved, 
                         contests_participated, problems_solved, verification_status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'verified')
                    ''', (self.current_user['id'], platform_id, handle, rating, rating, contests, problems))
            else:
                # Fallback to old schema
                cursor.execute('''
                    INSERT OR REPLACE INTO user_platforms 
                    (user_id, platform_name, handle, rating, max_rating)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.current_user['id'], platform_name, handle, rating, max_rating))
            
            conn.commit()
            conn.close()
            
            # Log analytics
            self._log_analytics("platform_added", 1, {"platform": platform_name, "rating": rating})
            
        except Exception as e:
            print(f"Error saving platform data: {e}")
            raise
    
    def save_user_course(self, course_name: str, institution: str = None, 
                        completion_date: str = None, bonus_points: float = 0.0,
                        course_url: str = None, skills: List[str] = None):
        """Save course data with enhanced tracking"""
        self.require_authentication()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get or create institution
            institution_id = None
            if institution:
                cursor.execute("SELECT id FROM institutions WHERE name = ? OR short_name = ?", (institution, institution))
                inst_result = cursor.fetchone()
                if inst_result:
                    institution_id = inst_result[0]
                else:
                    # Create new institution
                    cursor.execute('''
                        INSERT INTO institutions (name, prestige_score, institution_type)
                        VALUES (?, 5.0, 'online_platform')
                    ''', (institution,))
                    institution_id = cursor.lastrowid
            
            # Check if using new schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_courses_new'")
            use_new_schema = cursor.fetchone() is not None
            
            if use_new_schema:
                skills_json = json.dumps(skills) if skills else None
                cursor.execute('''
                    INSERT INTO user_courses_new 
                    (user_id, course_name, course_url, institution_id, completion_date, 
                     institution_bonus, skills_learned, verification_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'verified')
                ''', (self.current_user['id'], course_name, course_url, institution_id, 
                      completion_date, bonus_points, skills_json))
            else:
                # Fallback to old schema
                cursor.execute('''
                    INSERT INTO user_courses 
                    (user_id, course_name, institution, completion_date, bonus_points)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.current_user['id'], course_name, institution, completion_date, bonus_points))
            
            conn.commit()
            conn.close()
            
            # Log analytics
            self._log_analytics("course_added", 1, {
                "institution": institution, 
                "bonus_points": bonus_points,
                "skills_count": len(skills) if skills else 0
            })
            
        except Exception as e:
            print(f"Error saving course data: {e}")
            raise
    
    def get_user_platforms(self) -> List[Dict]:
        """Get user platforms with enhanced data"""
        self.require_authentication()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check schema and get appropriate data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_platforms_new'")
        if cursor.fetchone():
            cursor.execute('''
                SELECT p.display_name, up.handle, up.current_rating, up.max_rating_achieved,
                       up.contests_participated, up.problems_solved, up.rating_percentile,
                       up.last_updated, p.max_rating, p.difficulty_weight
                FROM user_platforms_new up
                JOIN platforms p ON up.platform_id = p.id
                WHERE up.user_id = ?
                ORDER BY up.current_rating DESC
            ''', (self.current_user['id'],))
            
            platforms = []
            for row in cursor.fetchall():
                platforms.append({
                    'platform_name': row[0],
                    'handle': row[1],
                    'rating': row[2],
                    'max_rating': row[3],
                    'contests': row[4],
                    'problems': row[5],
                    'percentile': row[6],
                    'last_updated': row[7],
                    'platform_max': row[8],
                    'weight': row[9]
                })
        else:
            # Fallback to old schema
            cursor.execute('''
                SELECT platform_name, handle, rating, max_rating, last_updated
                FROM user_platforms
                WHERE user_id = ?
            ''', (self.current_user['id'],))
            
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
    
    def get_user_courses(self) -> List[Dict]:
        """Get user courses with enhanced data"""
        self.require_authentication()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check schema and get appropriate data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_courses_new'")
        if cursor.fetchone():
            cursor.execute('''
                SELECT uc.course_name, i.name, uc.completion_date, uc.total_bonus,
                       uc.course_url, uc.skills_learned, uc.difficulty_level,
                       uc.course_type, i.prestige_score
                FROM user_courses_new uc
                LEFT JOIN institutions i ON uc.institution_id = i.id
                WHERE uc.user_id = ?
                ORDER BY uc.total_bonus DESC, uc.completion_date DESC
            ''', (self.current_user['id'],))
            
            courses = []
            for row in cursor.fetchall():
                skills = json.loads(row[5]) if row[5] else []
                courses.append({
                    'course_name': row[0],
                    'institution': row[1],
                    'completion_date': row[2],
                    'bonus_points': row[3],
                    'course_url': row[4],
                    'skills': skills,
                    'difficulty': row[6],
                    'type': row[7],
                    'institution_prestige': row[8]
                })
        else:
            # Fallback to old schema
            cursor.execute('''
                SELECT course_name, institution, completion_date, bonus_points
                FROM user_courses
                WHERE user_id = ?
            ''', (self.current_user['id'],))
            
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
    
    def get_user_summary(self) -> Dict:
        """Get comprehensive user summary"""
        self.require_authentication()
        
        try:
            from enhanced_db_model import EnhancedUserModel
            db = EnhancedUserModel(self.db_path)
            return db.get_user_statistics(self.current_user['id'])
        except ImportError:
            # Fallback to basic summary
            return {
                'user_info': self.current_user,
                'platforms': self.get_user_platforms(),
                'courses': self.get_user_courses()
            }
    
    def _username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check both old and new schema
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_new'")
        if cursor.fetchone():
            cursor.execute("SELECT 1 FROM users_new WHERE username = ?", (username,))
        else:
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    def _log_analytics(self, metric_name: str, value: float, metadata: Dict = None):
        """Log analytics data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if analytics table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='system_analytics'")
            if cursor.fetchone():
                metadata_json = json.dumps(metadata) if metadata else None
                cursor.execute('''
                    INSERT INTO system_analytics (metric_name, metric_value, metadata)
                    VALUES (?, ?, ?)
                ''', (metric_name, value, metadata_json))
                conn.commit()
            
            conn.close()
        except Exception:
            pass  # Don't fail operations due to analytics errors
