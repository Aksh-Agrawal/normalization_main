"""
Enhanced User Input Handler - Handles all user interactions
"""
import getpass
from typing import Optional, Dict, List
from services.auth_service import AuthenticationService

class UserInputHandler:
    """Class to handle all user input operations"""
    
    def __init__(self, auth_service=None):
        """Initialize the input handler"""
        self.auth_service = auth_service or AuthenticationService()
    
    def display_welcome_message(self):
        """Display welcome message"""
        print("="*60)
        print("🚀 WELCOME TO UNIFIED RANKING SYSTEM")
        print("="*60)
        print("Track your coding platform ratings and course achievements!")
        print()
    
    def display_main_menu(self):
        """Display main menu options"""
        print("\n📋 MAIN MENU")
        print("-" * 30)
        print("1. 🔐 Login")
        print("2. 📝 Register")
        print("3. ❌ Exit")
        print("-" * 30)
    
    def display_user_menu(self):
        """Display user menu after login"""
        user = self.auth_service.get_current_user()
        print(f"\n👋 Welcome back, {user['username']}!")
        print("\n📋 USER MENU")
        print("-" * 40)
        print("1. 🎯 Add Platform Ratings")
        print("2. 🎓 Add Course Data")
        print("3. 📊 View My Profile")
        print("4. 🏆 Calculate Rankings")
        print("5. 📈 Generate Heatmap")
        print("6. 🔓 Logout")
        print("-" * 40)
    
    def get_menu_choice(self, max_option: int) -> int:
        """Get menu choice from user"""
        while True:
            try:
                choice = int(input(f"\nEnter your choice (1-{max_option}): "))
                if 1 <= choice <= max_option:
                    return choice
                else:
                    print(f"❌ Please enter a number between 1 and {max_option}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_user_credentials(self, is_registration: bool = False) -> Dict[str, str]:
        """Get user credentials for login/registration"""
        print(f"\n{'📝 REGISTRATION' if is_registration else '🔐 LOGIN'}")
        print("-" * 30)
        
        credentials = {}
        
        # Get email
        while True:
            email = input("📧 Email: ").strip()
            if email:
                credentials['email'] = email
                break
            print("❌ Email cannot be empty")
        
        # Get password
        while True:
            try:
                # Try using getpass first
                password = getpass.getpass("🔑 Password: ")
                if password:
                    credentials['password'] = password
                    break
                print("❌ Password cannot be empty")
            except Exception as e:
                # Fallback to regular input if getpass fails
                print("⚠️ Secure password input not available, using regular input")
                password = input("🔑 Password: ").strip()
                if password:
                    credentials['password'] = password
                    break
                print("❌ Password cannot be empty")
        
        # Get username for registration
        if is_registration:
            username = input("👤 Username (optional): ").strip()
            if username:
                credentials['username'] = username
        
        return credentials
    
    def handle_registration(self) -> bool:
        """Handle user registration"""
        credentials = self.get_user_credentials(is_registration=True)
        
        success, message = self.auth_service.register_user(
            credentials['email'],
            credentials['password'],
            credentials.get('username')
        )
        
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
    
    def handle_login(self) -> bool:
        """Handle user login"""
        credentials = self.get_user_credentials(is_registration=False)
        
        success, message, user_data = self.auth_service.login_user(
            credentials['email'],
            credentials['password']
        )
        
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
    
    def get_platform_data(self) -> Dict[str, str]:
        """Get platform data from user with automatic rating fetching"""
        print("\n🎯 ADD PLATFORM RATING")
        print("-" * 30)
        
        platforms = {
            "1": {"name": "Codeforces", "api": "fetch_codeforces_profile_api"},
            "2": {"name": "Leetcode", "api": "fetch_leetcode_profile"}, 
            "3": {"name": "CodeChef", "api": "fetch_codechef_profile"},
            "4": {"name": "AtCoder", "api": None},
            "5": {"name": "HackerRank", "api": None}
        }
        
        print("Available platforms:")
        for key, platform in platforms.items():
            status = "🚀 Auto-fetch" if platform["api"] else "✋ Manual entry"
            print(f"  {key}. {platform['name']} - {status}")
        
        while True:
            choice = input("\nSelect platform (1-5): ").strip()
            if choice in platforms:
                platform_info = platforms[choice]
                platform_name = platform_info["name"]
                api_function = platform_info["api"]
                break
            print("❌ Please select a valid platform (1-5)")
        
        handle = input(f"Enter your {platform_name} handle: ").strip()
        
        if api_function and handle:
            print(f"🔄 Fetching {platform_name} rating automatically...")
            
            try:
                # Import and call the appropriate API function
                if api_function == "fetch_codeforces_profile_api":
                    from rating_scraper_api.CodeForces_api import fetch_codeforces_profile_api
                    profile_data = fetch_codeforces_profile_api(handle)
                elif api_function == "fetch_leetcode_profile":
                    from rating_scraper_api.leetcode_api import fetch_leetcode_profile
                    profile_data = fetch_leetcode_profile(handle)
                elif api_function == "fetch_codechef_profile":
                    from rating_scraper_api.CodeChef_api import fetch_codechef_profile
                    profile_data = fetch_codechef_profile(handle)
                
                # Check if fetching was successful
                if profile_data and 'error' not in profile_data and profile_data.get('rating') != 'N/A':
                    rating = int(float(profile_data['rating']))
                    print(f"✅ Successfully fetched rating: {rating}")
                    
                    return {
                        'platform_name': platform_name,
                        'handle': handle,
                        'rating': rating
                    }
                else:
                    error_msg = profile_data.get('error', 'Could not fetch rating') if profile_data else 'No data returned'
                    print(f"⚠️ Auto-fetch failed: {error_msg}")
                    print("📝 Please enter rating manually:")
                    
            except Exception as e:
                print(f"⚠️ Auto-fetch failed: {e}")
                print("📝 Please enter rating manually:")
        
        # Manual rating entry (fallback or for platforms without API)
        if not api_function:
            print(f"ℹ️ {platform_name} requires manual rating entry")
        
        while True:
            try:
                rating = int(input(f"Enter your {platform_name} rating: "))
                break
            except ValueError:
                print("❌ Please enter a valid rating number")
        
        return {
            'platform_name': platform_name,
            'handle': handle,
            'rating': rating
        }
    
    def get_course_data(self) -> Dict[str, str]:
        """Get course data from user"""
        print("\n🎓 ADD COURSE DATA")
        print("-" * 30)
        
        course_name = input("Course name: ").strip()
        institution = input("Institution (optional): ").strip() or None
        completion_date = input("Completion date (YYYY-MM-DD, optional): ").strip() or None
        
        bonus_points = 0.0
        bonus_input = input("Bonus points (optional): ").strip()
        if bonus_input:
            try:
                bonus_points = float(bonus_input)
            except ValueError:
                print("❌ Invalid bonus points, setting to 0")
                bonus_points = 0.0
        
        return {
            'course_name': course_name,
            'institution': institution,
            'completion_date': completion_date,
            'bonus_points': bonus_points
        }
    
    def display_user_profile(self):
        """Display user profile with platforms and courses"""
        user = self.auth_service.get_current_user()
        platforms = self.auth_service.get_user_platforms()
        courses = self.auth_service.get_user_courses()
        
        print(f"\n👤 USER PROFILE: {user['username']}")
        print("="*50)
        print(f"📧 Email: {user['email']}")
        print(f"📅 Member since: {user['created_at']}")
        
        print(f"\n🎯 PLATFORM RATINGS ({len(platforms)} platforms)")
        print("-" * 50)
        if platforms:
            for platform in platforms:
                print(f"  • {platform['platform_name']}: {platform['rating']} ({platform['handle']})")
        else:
            print("  No platform ratings added yet")
        
        print(f"\n🎓 COMPLETED COURSES ({len(courses)} courses)")
        print("-" * 50)
        if courses:
            for course in courses:
                institution_info = f" - {course['institution']}" if course['institution'] else ""
                bonus_info = f" (+{course['bonus_points']} pts)" if course['bonus_points'] > 0 else ""
                print(f"  • {course['course_name']}{institution_info}{bonus_info}")
        else:
            print("  No courses added yet")
    
    def confirm_action(self, message: str) -> bool:
        """Get confirmation from user"""
        while True:
            response = input(f"{message} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' for yes or 'n' for no")
    
    def display_success_message(self, message: str):
        """Display success message"""
        print(f"✅ {message}")
    
    def display_error_message(self, message: str):
        """Display error message"""
        print(f"❌ {message}")
    
    def pause_for_user(self):
        """Pause and wait for user input"""
        input("\nPress Enter to continue...")
    
    def get_platform_handle(self, platform_name: str) -> Optional[str]:
        """Get platform handle from user"""
        handle = input(f"Enter {platform_name} handle (or press Enter to skip): ").strip()
        return handle if handle else None
