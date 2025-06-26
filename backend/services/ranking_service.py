"""
Enhanced Ranking System with Database Integration
"""
from logic_formulas.formula_main import UnifiedRankingSystem, User
from rating_scraper_api.CodeForces_api import fetch_codeforces_profile_api
from rating_scraper_api.leetcode_api import fetch_leetcode_profile
from rating_scraper_api.CodeChef_api import fetch_codechef_profile
from bonus_calculatorF import bonus_calculator
from services.auth_service import AuthenticationService
from typing import Dict, List, Tuple, Optional

class EnhancedRankingSystem:
    """Enhanced ranking system with user management and database integration"""
    
    def __init__(self, auth_service: AuthenticationService):
        """Initialize the enhanced ranking system"""
        self.auth_service = auth_service
        self.ranking_system = UnifiedRankingSystem()
        self.platform_configs = {
            "Codeforces": {"max_rating": 3000, "api_func": fetch_codeforces_profile_api},
            "Leetcode": {"max_rating": 2500, "api_func": fetch_leetcode_profile},
            "CodeChef": {"max_rating": 1800, "api_func": fetch_codechef_profile},
            "AtCoder": {"max_rating": 2800, "api_func": None},
            "HackerRank": {"max_rating": 2000, "api_func": None}
        }
        self._setup_platforms()
    
    def _setup_platforms(self):
        """Setup all available platforms"""
        for platform_name, config in self.platform_configs.items():
            self.ranking_system.add_platform(platform_name, config["max_rating"])
    
    def fetch_platform_rating(self, platform_name: str, handle: str) -> Optional[int]:
        """Fetch rating from platform API"""
        if platform_name not in self.platform_configs:
            return None
        
        api_func = self.platform_configs[platform_name]["api_func"]
        if not api_func:
            return None
        
        try:
            profile_data = api_func(handle)
            if profile_data and profile_data.get("rating") != 'N/A':
                return int(profile_data["rating"])
        except Exception as e:
            print(f"Error fetching {platform_name} rating: {e}")
        
        return None
    
    def add_user_platform_rating(self, platform_name: str, handle: str, rating: Optional[int] = None) -> bool:
        """Add platform rating for current user"""
        try:
            self.auth_service.require_authentication()
            user = self.auth_service.get_current_user()
            user_id = str(user['id'])
            
            # Try to fetch rating from API if not provided
            if rating is None:
                fetched_rating = self.fetch_platform_rating(platform_name, handle)
                if fetched_rating is not None:
                    rating = fetched_rating
                    print(f"✅ Fetched {platform_name} rating: {rating}")
                else:
                    print(f"⚠️ Could not fetch {platform_name} rating automatically")
                    return False
            
            # Add user to ranking system if not exists
            if user_id not in self.ranking_system.users:
                self.ranking_system.add_user(user_id)
            
            # Update platform stats
            self.ranking_system.update_platform_stats(
                platform_name,
                difficulty=2100,  # Default difficulty
                participation=0.8,  # Default participation
                current_ratings={user_id: rating}
            )
            
            # Save to database
            max_rating = self.platform_configs[platform_name]["max_rating"]
            self.auth_service.save_user_platform(platform_name, handle, rating, max_rating)
            
            return True
            
        except Exception as e:
            print(f"Error adding platform rating: {e}")
            return False
    
    def add_manual_platform_rating(self, platform_name: str, handle: str, rating: int) -> bool:
        """Manually add platform rating for current user"""
        try:
            self.auth_service.require_authentication()
            user = self.auth_service.get_current_user()
            user_id = str(user['id'])
            
            # Add user to ranking system if not exists
            if user_id not in self.ranking_system.users:
                self.ranking_system.add_user(user_id)
            
            # Update platform stats
            self.ranking_system.update_platform_stats(
                platform_name,
                difficulty=2100,
                participation=0.8,
                current_ratings={user_id: rating}
            )
            
            # Save to database
            max_rating = self.platform_configs[platform_name]["max_rating"]
            self.auth_service.save_user_platform(platform_name, handle, rating, max_rating)
            
            print(f"✅ Added {platform_name} rating: {rating}")
            return True
            
        except Exception as e:
            print(f"Error adding manual platform rating: {e}")
            return False
    
    def load_user_data_from_database(self):
        """Load user's platform data from database into ranking system"""
        try:
            self.auth_service.require_authentication()
            user = self.auth_service.get_current_user()
            user_id = str(user['id'])
            
            # Get user's platform data from database
            platforms = self.auth_service.get_user_platforms()
            
            if not platforms:
                print("ℹ️ No platform data found in database")
                return
            
            # Add user to ranking system
            if user_id not in self.ranking_system.users:
                self.ranking_system.add_user(user_id)
            
            # Load each platform's data
            for platform_data in platforms:
                platform_name = platform_data['platform_name']
                rating = platform_data['rating']
                
                if platform_name in self.platform_configs:
                    self.ranking_system.update_platform_stats(
                        platform_name,
                        difficulty=2100,
                        participation=0.8,
                        current_ratings={user_id: rating}
                    )
            
            print(f"✅ Loaded {len(platforms)} platform ratings from database")
            
        except Exception as e:
            print(f"Error loading user data: {e}")
    
    def calculate_user_ranking(self) -> Dict:
        """Calculate ranking for current user"""
        try:
            self.auth_service.require_authentication()
            user = self.auth_service.get_current_user()
            user_id = str(user['id'])
            
            # Load data from database first
            self.load_user_data_from_database()
            
            if user_id not in self.ranking_system.users:
                return {"error": "No platform data found for user"}
            
            ranking_user = self.ranking_system.users[user_id]
            
            # Calculate course bonus (if available)
            course_bonus = 0.0
            courses = self.auth_service.get_user_courses()
            for course in courses:
                course_bonus += course.get('bonus_points', 0.0)
            
            # Update total rating
            ranking_user.course_bonus = course_bonus
            ranking_user.total_rating = ranking_user.unified_rating + course_bonus
            
            return {
                "user_id": user_id,
                "username": user['username'],
                "platform_rating": ranking_user.unified_rating,
                "course_bonus": course_bonus,
                "total_rating": ranking_user.total_rating,
                "platform_details": ranking_user.platform_ratings,
                "weights": self.ranking_system.final_weights
            }
            
        except Exception as e:
            print(f"Error calculating ranking: {e}")
            return {"error": str(e)}
    
    def display_ranking_results(self, ranking_data: Dict):
        """Display ranking results in a formatted way"""
        if "error" in ranking_data:
            print(f"❌ Error: {ranking_data['error']}")
            return
        
        print("\n" + "="*60)
        print("🏆 UNIFIED RANKING RESULTS")
        print("="*60)
        
        print(f"👤 User: {ranking_data['username']}")
        print(f"🎯 Platform Rating: {ranking_data['platform_rating']:.1f}")
        print(f"🎓 Course Bonus: {ranking_data['course_bonus']:.1f}")
        print(f"🏆 Total Rating: {ranking_data['total_rating']:.1f}")
        
        print(f"\n📊 PLATFORM BREAKDOWN")
        print("-"*40)
        
        for platform, rating in ranking_data['platform_details'].items():
            weight = ranking_data['weights'].get(platform, 0)
            print(f"  • {platform:<12}: {rating:>4} (weight: {weight:.4f})")
        
        # Calculate percentage score
        max_possible = sum(self.platform_configs[p]["max_rating"] for p in ranking_data['platform_details'].keys())
        if max_possible > 0:
            percentage = (ranking_data['platform_rating'] / max_possible) * 100
            print(f"\n📈 Performance: {percentage:.1f}% of maximum possible rating")
    
    def get_available_platforms(self) -> List[str]:
        """Get list of available platforms"""
        return list(self.platform_configs.keys())
    
    def get_platform_info(self, platform_name: str) -> Optional[Dict]:
        """Get information about a specific platform"""
        if platform_name in self.platform_configs:
            return {
                "name": platform_name,
                "max_rating": self.platform_configs[platform_name]["max_rating"],
                "has_api": self.platform_configs[platform_name]["api_func"] is not None
            }
        return None
