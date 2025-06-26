"""
Simple Main Application - Fixes password input issues
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from services.enhanced_auth_service import EnhancedAuthService
from services.simple_input_handler import SimpleUserInputHandler

# Import Coursera scraping functionality
try:
    from cousera.coursera_scraper import scrape_coursera_profile, validate_coursera_url
    from bonus_calculatorF.bonus_calculator import calculate_from_scraper_result
    COURSERA_AVAILABLE = True
except ImportError:
    COURSERA_AVAILABLE = False

class SimpleUnifiedRankingApp:
    """Simple version of the main application with fixed password input"""
    
    def __init__(self):
        """Initialize the application"""
        print("🔄 Initializing simple application...")
        self.auth_service = EnhancedAuthService()
        self.input_handler = SimpleUserInputHandler(self.auth_service)  # Pass the same auth service
        
        # Try to initialize ranking service for auto-fetch capability
        try:
            from services.ranking_service import EnhancedRankingSystem
            self.ranking_service = EnhancedRankingSystem(self.auth_service)
            print("✅ Ranking service initialized - auto-fetch enabled")
        except Exception as e:
            print(f"⚠️ Ranking service not available: {e}")
            self.ranking_service = None
        
        self.running = True
        print("✅ Application initialized successfully")
    
    def run(self):
        """Main application loop"""
        self.input_handler.display_welcome_message()
        
        while self.running:
            try:
                if not self.auth_service.is_logged_in():
                    print("\n🔓 Not logged in - showing authentication menu...")
                    self._handle_authentication_flow()
                else:
                    print("\n✅ User is logged in - showing user menu...")
                    self._handle_user_flow()
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using Unified Ranking System!")
                self.running = False
                break
            except EOFError:
                print("\n\n👋 Input stream closed. Exiting...")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                try:
                    continue_app = input("\nDo you want to continue? (y/n): ").strip().lower()
                    if continue_app != 'y':
                        self.running = False
                except:
                    self.running = False
    
    def _handle_authentication_flow(self):
        """Handle user authentication (login/register)"""
        try:
            self.input_handler.display_main_menu()
            choice = self.input_handler.get_menu_choice(3)
            
            if choice == 1:  # Login
                self._handle_login()
            elif choice == 2:  # Register
                self._handle_registration()
            elif choice == 3:  # Exit
                print("\n👋 Thank you for using Unified Ranking System!")
                self.running = False
        except Exception as e:
            print(f"❌ Error in authentication flow: {e}")
            self.input_handler.pause_for_user()
    
    def _handle_user_flow(self):
        """Handle authenticated user operations"""
        try:
            self.input_handler.display_user_menu()
            choice = self.input_handler.get_menu_choice(6)
            
            if choice == 1:  # Add Platform Ratings
                self._handle_add_platform_ratings()
            elif choice == 2:  # Add Course Data
                self._handle_add_course_data()
            elif choice == 3:  # View Profile
                self._handle_view_profile()
            elif choice == 4:  # Calculate Rankings
                self._handle_calculate_rankings()
            elif choice == 5:  # Generate Heatmap
                self._handle_generate_heatmap()
            elif choice == 6:  # Logout
                self._handle_logout()
        except Exception as e:
            print(f"❌ Error in user flow: {e}")
            self.input_handler.pause_for_user()
    
    def _handle_login(self):
        """Handle user login"""
        try:
            if self.input_handler.handle_login():
                print("🎉 Successfully logged in!")
                print("📋 You can now access the user menu...")
            else:
                print("❌ Login failed. Please try again.")
            self.input_handler.pause_for_user()
        except Exception as e:
            print(f"❌ Error during login: {e}")
            self.input_handler.pause_for_user()
    
    def _handle_registration(self):
        """Handle user registration"""
        try:
            if self.input_handler.handle_registration():
                print("🎉 Registration successful! You can now log in.")
            self.input_handler.pause_for_user()
        except Exception as e:
            print(f"❌ Error during registration: {e}")
            self.input_handler.pause_for_user()
    
    def _handle_add_platform_ratings(self):
        """Handle adding platform ratings with auto-fetch support"""
        try:
            print("\n🎯 ADD PLATFORM RATINGS")
            print("="*40)
            
            if self.ranking_service:
                print("🚀 Auto-fetch enabled for supported platforms")
                
                # Use the enhanced flow with ranking service
                platforms_info = {
                    "Codeforces": {"max_rating": 3000, "has_api": True},
                    "Leetcode": {"max_rating": 2500, "has_api": True},
                    "CodeChef": {"max_rating": 1800, "has_api": True},
                    "AtCoder": {"max_rating": 2800, "has_api": False},
                    "HackerRank": {"max_rating": 2000, "has_api": False}
                }
                
                print("Available platforms:")
                for i, (platform, info) in enumerate(platforms_info.items(), 1):
                    status = "🚀 Auto-fetch" if info["has_api"] else "✋ Manual entry"
                    print(f"  {i}. {platform} (Max: {info['max_rating']}) - {status}")
                
                # Get platform selection
                while True:
                    try:
                        choice = int(input(f"\nSelect platform (1-{len(platforms_info)}): "))
                        if 1 <= choice <= len(platforms_info):
                            selected_platform = list(platforms_info.keys())[choice - 1]
                            break
                        else:
                            print(f"❌ Please enter a number between 1 and {len(platforms_info)}")
                    except ValueError:
                        print("❌ Please enter a valid number")
                    except (EOFError, KeyboardInterrupt):
                        print("\n❌ Input cancelled")
                        return
                
                # Get platform handle
                handle = input(f"Enter your {selected_platform} handle: ").strip()
                if not handle:
                    print("❌ Handle cannot be empty")
                    self.input_handler.pause_for_user()
                    return
                
                # Try automatic fetching using ranking service
                print(f"🔄 Attempting to fetch {selected_platform} rating automatically...")
                success = self.ranking_service.add_user_platform_rating(selected_platform, handle)
                
                if not success:
                    print("⚠️ Auto-fetch failed. Please enter rating manually.")
                    max_rating = platforms_info[selected_platform]["max_rating"]
                    while True:
                        try:
                            rating = int(input(f"Enter your {selected_platform} rating (0-{max_rating}): "))
                            if 0 <= rating <= max_rating:
                                break
                            else:
                                print(f"❌ Rating must be between 0 and {max_rating}")
                        except ValueError:
                            print("❌ Please enter a valid number")
                        except (EOFError, KeyboardInterrupt):
                            print("\n❌ Input cancelled")
                            return
                    
                    success = self.ranking_service.add_manual_platform_rating(selected_platform, handle, rating)
                
                if success:
                    print(f"✅ {selected_platform} rating added successfully!")
                else:
                    print("❌ Failed to add platform rating")
            else:
                # Fallback to simple input handler
                print("⚠️ Using manual entry mode")
                platform_data = self.input_handler.get_platform_data()
                
                if not platform_data:
                    print("❌ No platform data entered")
                    self.input_handler.pause_for_user()
                    return
                
                self.auth_service.save_user_platform(
                    platform_data['platform_name'],
                    platform_data['handle'],
                    platform_data['rating']
                )
                print(f"✅ {platform_data['platform_name']} rating saved successfully!")
            
        except Exception as e:
            print(f"❌ Failed to add platform data: {e}")
        
        self.input_handler.pause_for_user()
    
    def _handle_add_course_data(self):
        """Handle adding course data with options for manual entry or Coursera web scraping"""
        try:
            print("\n📚 ADD COURSE DATA")
            print("="*40)
            print("Choose how to add course data:")
            
            options = ["2. ✏️ Manual entry", "3. ⬅️ Back to main menu"]
            if COURSERA_AVAILABLE:
                options.insert(0, "1. 🌐 Scrape from Coursera profile URL")
                max_choice = 3
            else:
                print("⚠️ Coursera scraping not available")
                max_choice = 2
            
            for option in options:
                print(option)
            
            while True:
                try:
                    choice = int(input(f"\nSelect option (1-{max_choice}): "))
                    if 1 <= choice <= max_choice:
                        break
                    else:
                        print(f"❌ Please enter a number between 1 and {max_choice}")
                except ValueError:
                    print("❌ Please enter a valid number")
                except:
                    print("❌ Invalid input")
                    return
            
            if COURSERA_AVAILABLE and choice == 1:
                self._handle_coursera_scraping()
            elif (COURSERA_AVAILABLE and choice == 2) or (not COURSERA_AVAILABLE and choice == 1):
                self._handle_manual_course_entry()
            else:  # Back to main menu
                return
                
        except Exception as e:
            print(f"❌ Failed to add course data: {e}")
        
        self.input_handler.pause_for_user()
    
    def _handle_coursera_scraping(self):
        """Handle Coursera profile scraping for course data"""
        try:
            print("\n🌐 COURSERA PROFILE SCRAPING")
            print("="*40)
            print("Extract course data from your public Coursera profile")
            print("Example URL: https://www.coursera.org/user/your-username")
            
            # Get Coursera profile URL
            profile_url = input("\nEnter your Coursera profile URL: ").strip()
            
            if not profile_url:
                print("❌ URL cannot be empty")
                return
            
            # Validate URL
            if not validate_coursera_url(profile_url):
                print("❌ Invalid Coursera profile URL")
                print("URL should be in the format: https://www.coursera.org/user/...")
                return
            
            print(f"\n🔄 Scraping profile: {profile_url}")
            print("This may take a few moments...")
            
            # Scrape the profile
            try:
                profile_data = scrape_coursera_profile(profile_url, use_mock=False)
                
                if not profile_data:
                    print("❌ Failed to scrape profile or no data found")
                    return
                
                # Display basic profile info
                print("\n✅ Profile successfully scraped!")
                
                if "user_info" in profile_data and "name" in profile_data["user_info"]:
                    print(f"👤 User: {profile_data['user_info']['name']}")
                
                completed_courses = profile_data.get('completed_courses', [])
                if not completed_courses:
                    print("📚 No completed courses found")
                    return
                
                print(f"📚 Found {len(completed_courses)} completed courses")
                
                # Calculate bonus points for courses
                print("\n🔄 Calculating course bonus points...")
                enhanced_data = calculate_from_scraper_result(profile_data)
                
                # Save each course to the database
                saved_count = 0
                total_bonus = 0
                
                for course in enhanced_data.get('completed_courses', []):
                    try:
                        # Try to get course name from 'title' first (Coursera format), then 'name' (fallback)
                        course_name = course.get('title') or course.get('name', 'Unknown Course')
                        institution = course.get('institution', 'Coursera')
                        completion_date = course.get('completion_date', 'Unknown')
                        bonus_points = course.get('bonus_points', 0)
                        
                        # Save to database
                        self.auth_service.save_user_course(
                            course_name,
                            institution,
                            completion_date,
                            bonus_points
                        )
                        
                        saved_count += 1
                        total_bonus += bonus_points
                        
                        print(f"✅ Saved: {course_name} (+{bonus_points:.1f} bonus)")
                        
                    except Exception as e:
                        course_title = course.get('title') or course.get('name', 'Unknown')
                        print(f"⚠️ Failed to save course '{course_title}': {e}")
                
                print(f"\n🎉 Successfully saved {saved_count} courses!")
                print(f"💰 Total bonus points: {total_bonus:.1f}")
                
                # Display summary of top courses by bonus
                if saved_count > 0:
                    print("\n🏆 Top courses by bonus points:")
                    sorted_courses = sorted(
                        enhanced_data.get('completed_courses', []), 
                        key=lambda x: x.get('bonus_points', 0), 
                        reverse=True
                    )[:5]
                    
                    for i, course in enumerate(sorted_courses, 1):
                        name = (course.get('title') or course.get('name', 'Unknown'))[:50] 
                        if len(course.get('title', '') or course.get('name', '')) > 50:
                            name += '...'
                        bonus = course.get('bonus_points', 0)
                        print(f"  {i}. {name} (+{bonus:.1f})")
                
            except Exception as e:
                print(f"❌ Error during scraping: {e}")
                print("💡 Tip: Make sure your Coursera profile is public")
                
        except Exception as e:
            print(f"❌ Error in Coursera scraping: {e}")
    
    def _handle_manual_course_entry(self):
        """Handle manual course entry"""
        try:
            course_data = self.input_handler.get_course_data()
            
            if not course_data:
                print("❌ No course data entered")
                return
            
            self.auth_service.save_user_course(
                course_data['course_name'],
                course_data['institution'],
                course_data['completion_date'],
                course_data['bonus_points']
            )
            print("✅ Course data added successfully!")
        except Exception as e:
            print(f"❌ Failed to add course data: {e}")
    
    def _handle_view_profile(self):
        """Handle viewing user profile"""
        try:
            self.input_handler.display_user_profile()
        except Exception as e:
            print(f"❌ Failed to load profile: {e}")
        
        self.input_handler.pause_for_user()
    
    def _handle_logout(self):
        """Handle user logout"""
        try:
            user = self.auth_service.get_current_user()
            self.auth_service.logout_user()
            print(f"👋 Goodbye, {user['username']}!")
        except Exception as e:
            print(f"❌ Error during logout: {e}")
        
        self.input_handler.pause_for_user()
    
    def _handle_calculate_rankings(self):
        """Handle calculating and displaying rankings"""
        try:
            if not self.ranking_service:
                print("❌ Ranking service is not available")
                print("📊 Please add platform ratings first to enable ranking calculations")
                self.input_handler.pause_for_user()
                return
                
            print("\n🔄 Calculating unified rankings...")
            
            try:
                ranking_data = self.ranking_service.calculate_user_ranking()
                self.ranking_service.display_ranking_results(ranking_data)
                print("✅ Rankings calculated successfully!")
            except Exception as e:
                print(f"❌ Failed to calculate rankings: {e}")
                print("ℹ️ Make sure you have added platform ratings first")
        except Exception as e:
            print(f"❌ Error calculating rankings: {e}")
        
        self.input_handler.pause_for_user()
    
    def _handle_generate_heatmap(self):
        """Handle generating coding activity heatmap"""
        try:
            print("\n📈 GENERATE ACTIVITY HEATMAP")
            print("="*40)
            
            # Get user's platform data
            platforms = self.auth_service.get_user_platforms()
            if not platforms:
                print("❌ No platform data found. Please add platform ratings first.")
                self.input_handler.pause_for_user()
                return
            
            print(f"Found {len(platforms)} platforms in your profile")
            
            # Import heatmap functions
            try:
                from heatmap.heat_map import (
                    get_codeforces_heatmap,
                    get_leetcode_heatmap,
                    get_codechef_heatmap,
                    combine_heatmaps,
                    draw_github_style_heatmap,
                )
            except ImportError as e:
                print(f"❌ Heatmap functionality not available: {e}")
                self.input_handler.pause_for_user()
                return
            
            heatmaps = []
            
            for platform_data in platforms:
                platform_name = platform_data['platform_name']
                handle = platform_data['handle']
                
                print(f"🔄 Fetching {platform_name} heatmap for {handle}...")
                
                try:
                    if platform_name.lower() == 'codeforces':
                        heatmap_data = get_codeforces_heatmap(handle)
                        if heatmap_data:
                            heatmaps.append(heatmap_data)
                            print(f"✅ {platform_name} heatmap data retrieved")
                        else:
                            print(f"⚠️ No {platform_name} heatmap data available")
                    elif platform_name.lower() == 'leetcode':
                        heatmap_data = get_leetcode_heatmap(handle)
                        if heatmap_data:
                            heatmaps.append(heatmap_data)
                            print(f"✅ {platform_name} heatmap data retrieved")
                        else:
                            print(f"⚠️ No {platform_name} heatmap data available")
                    elif platform_name.lower() == 'codechef':
                        heatmap_data = get_codechef_heatmap(handle)
                        if heatmap_data:
                            heatmaps.append(heatmap_data)
                            print(f"✅ {platform_name} heatmap data retrieved")
                        else:
                            print(f"⚠️ No {platform_name} heatmap data available")
                    else:
                        print(f"⚠️ Heatmap not available for {platform_name}")
                        
                except Exception as e:
                    print(f"❌ Failed to fetch {platform_name} heatmap: {e}")
            
            if heatmaps:
                print("🔄 Combining heatmaps...")
                try:
                    # Fix: Pass individual heatmaps as arguments, not as a list
                    combined_heatmap = combine_heatmaps(*heatmaps)
                    
                    print("🔄 Generating visualization...")
                    draw_github_style_heatmap(combined_heatmap)
                    print("✅ Heatmap generated successfully!")
                except Exception as e:
                    print(f"❌ Failed to generate heatmap visualization: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("❌ No heatmap data available")
                print("ℹ️ Make sure your platform handles are correct and you have activity on these platforms")
                
        except Exception as e:
            print(f"❌ Failed to generate heatmap: {e}")
        
        self.input_handler.pause_for_user()

def main():
    """Main entry point"""
    try:
        print("🚀 Starting Simple Unified Ranking System...")
        print("ℹ️ This version uses visible password input for compatibility")
        print("🎯 Full features: Auto-fetch, Rankings, Heatmaps, Course tracking")
        app = SimpleUnifiedRankingApp()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
