"""
Authentication Service - Handles user registration and login
"""
import re
from typing import Optional, Dict, Tuple
from models.user_model import UserModel

class AuthenticationService:
    """Service class for handling user authentication operations"""
    
    def __init__(self, db_path: str = "users.db"):
        """Initialize authentication service"""
        self.user_model = UserModel(db_path)
        self.current_user = None
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, "Password is valid"
    
    def register_user(self, email: str, password: str, username: str = None) -> Tuple[bool, str]:
        """Register a new user"""
        # Validate email
        if not self.validate_email(email):
            return False, "Invalid email format"
        
        # Validate password
        is_valid, message = self.validate_password(password)
        if not is_valid:
            return False, message
        
        # Create user
        success = self.user_model.create_user(email, password, username)
        if success:
            return True, "User registered successfully"
        else:
            return False, "Email already exists or registration failed"
    
    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """Login user"""
        user_data = self.user_model.authenticate_user(email, password)
        if user_data:
            self.current_user = user_data
            return True, "Login successful", user_data
        else:
            return False, "Invalid email or password", None
    
    def logout_user(self):
        """Logout current user"""
        self.current_user = None
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged in user"""
        return self.current_user
    
    def require_authentication(self):
        """Decorator to require authentication"""
        if not self.is_logged_in():
            raise PermissionError("User must be logged in to perform this action")
    
    def save_user_platform(self, platform_name: str, handle: str, rating: int, max_rating: int = None):
        """Save platform data for current user"""
        self.require_authentication()
        self.user_model.save_platform_data(
            self.current_user['id'], platform_name, handle, rating, max_rating
        )
    
    def get_user_platforms(self) -> list:
        """Get platform data for current user"""
        self.require_authentication()
        return self.user_model.get_user_platforms(self.current_user['id'])
    
    def save_user_course(self, course_name: str, institution: str = None, 
                        completion_date: str = None, bonus_points: float = 0.0):
        """Save course data for current user"""
        self.require_authentication()
        self.user_model.save_course_data(
            self.current_user['id'], course_name, institution, completion_date, bonus_points
        )
    
    def get_user_courses(self) -> list:
        """Get course data for current user"""
        self.require_authentication()
        return self.user_model.get_user_courses(self.current_user['id'])
