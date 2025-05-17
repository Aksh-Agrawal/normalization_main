from platform import UnifiedRankingSystem, User
from CodeForces_api import fetch_codeforces_profile_api
from leetcode_api import fetch_leetcode_profile
from CodeChef_api import fetch_codechef_profile
# from course_credential_manager import CourseCredentialManager

def run():
    ranking_system = UnifiedRankingSystem()
    # course_manager = CourseCredentialManager()
    user_id = None

    # Add all platforms first
    ranking_system.add_platform("Codeforces", max_rating=3000)
    ranking_system.add_platform("Leetcode", max_rating=2500)
    ranking_system.add_platform("Atcoder", max_rating=2800)
    ranking_system.add_platform("CodeChef", max_rating=1800)

    # Fetch CodeForces profile
    handle_CF = input("Enter Codeforces handle: ")
    profile_data_CF = fetch_codeforces_profile_api(handle_CF)
    
    # Use the first valid handle as the user_id
    user_id = handle_CF
    # Add the user to the system
    ranking_system.add_user(user_id)
    
    # Process Codeforces
    cf_rating = None
    if profile_data_CF and profile_data_CF["rating"] != 'N/A':
        cf_rating = int(profile_data_CF["rating"])
        print(f"Codeforces Rating: {cf_rating}")
    else:
        print("Could not retrieve valid Codeforces rating. Imputing value.")
        # Create a temporary user with platform ratings to impute this value
        temp_user = User(user_id)
        cf_rating = ranking_system._impute_missing_rating(temp_user, "Codeforces")
        print(f"Imputed Codeforces Rating: {cf_rating}")

    # Update Codeforces with real or imputed rating
    ranking_system.update_platform_stats(
        "Codeforces",
        difficulty=2100,
        participation=0.8,
        current_ratings={user_id: cf_rating}
    )

    # Fetch Leetcode profile
    handle_LC = input("Enter Leetcode handle: ")
    profile_data_LC = fetch_leetcode_profile(handle_LC)
    lc_rating = None
    if profile_data_LC and profile_data_LC["rating"] != 'N/A':
        lc_rating = int(profile_data_LC["rating"])
        print(f"Leetcode Rating: {lc_rating}")
    else:
        print("Could not retrieve valid Leetcode rating. Imputing value.")
        lc_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "Leetcode")
        print(f"Imputed Leetcode Rating: {lc_rating}")

    # Update Leetcode with real or imputed rating
    ranking_system.update_platform_stats(
        "Leetcode",
        difficulty=2100,
        participation=0.8,
        current_ratings={user_id: lc_rating}
    )

    # Fetch CodeChef profile
    handle_CC = input("Enter CodeChef handle: ")
    profile_data_CC = fetch_codechef_profile(handle_CC)
    cc_rating = None
    if profile_data_CC and profile_data_CC["rating"] != 'N/A':
        cc_rating = int(profile_data_CC["rating"])
        print(f"CodeChef Rating: {cc_rating}")
    else:
        print("Could not retrieve valid CodeChef rating. Imputing value.")
        cc_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "CodeChef")
        print(f"Imputed CodeChef Rating: {cc_rating}")

    # Update CodeChef with real or imputed rating
    ranking_system.update_platform_stats(
        "CodeChef",
        difficulty=3100,
        participation=0.5,
        current_ratings={user_id: cc_rating}
    )

    # Handle AtCoder - Using imputation by default for this example
    print("No AtCoder API implemented, using imputation for AtCoder rating.")
    atcoder_rating = ranking_system._impute_missing_rating(ranking_system.users[user_id], "Atcoder")
    print(f"Imputed AtCoder Rating: {atcoder_rating}")

    # Update AtCoder with imputed rating
    ranking_system.update_platform_stats(
        "Atcoder",
        difficulty=3500,
        participation=0.6,
        current_ratings={user_id: atcoder_rating}
    )

    # Course bonus section
    # print("\n===== Course Credentials =====")
    # print("Would you like to connect your educational platforms for course bonus points?")
    # if input("(y/n): ").lower() == 'y':
    #     # Connect course platforms
    #     platforms = ["coursera", "edx", "udacity"]
    #     for platform in platforms:
    #         print(f"\nWould you like to connect your {platform.capitalize()} account?")
    #         if input("(y/n): ").lower() == 'y':
    #             course_manager.authenticate(platform)
        
    #     # Calculate and apply course bonus
    #     # course_bonus = course_manager.calculate_course_bonus(user_id)
    #     print(f"\nTotal Course Bonus for {user_id}: {course_bonus:.2f} points")
        
    #     # Apply course bonus to the user in the ranking system
    #     ranking_system.users[user_id].course_bonus = course_bonus
    #     ranking_system.users[user_id].total_rating = ranking_system.users[user_id].unified_rating + course_bonus
    # else:
    #     print("Skipping course bonus calculation.")

    # Final Output
    print("\n===== Final Rankings =====")
    print(f"{'Rank':<5} {'User ID':<15} {'Platform Rating':<18} {'Course Bonus':<15} {'Total Rating':<15}")
    for i, (user_id, platform_rating, course_bonus, total) in enumerate(ranking_system.get_rankings(), 1):
        print(f"{i:<5} {user_id:<15} {platform_rating:<18.1f} {course_bonus:<15.1f} {total:<15.1f}")
    
    # Show detailed ratings per platform
    user = ranking_system.users[user_id]
    print("\n===== Detailed Ratings =====")
    for platform, rating in user.platform_ratings.items():
        weight = ranking_system.final_weights.get(platform, 0)
        print(f"{platform}: Rating = {rating}, Weight = {weight:.4f}")
    
    print("\n===== Component Breakdown =====")
    print(f"Base Platform Rating: {user.unified_rating:.1f}")
    print(f"Course Bonus: {user.course_bonus:.1f}")
    print(f"Total Rating: {user.total_rating:.1f}")

if __name__ == "__main__":
    run()