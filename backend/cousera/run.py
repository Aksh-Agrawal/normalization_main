#!/usr/bin/env python3
"""
Coursera Profile Scraper and Bonus Calculator

This enhanced script runs both the Coursera Profile Scraper and Bonus Calculator in sequence.
It prompts the user for a Coursera profile URL, displays the scraped data,
and then calculates and displays bonus points for each course.
"""

import sys
import json
import time
import logging
from .interactive_scraper import main as scraper_main
from bonus_calculatorF.bonus_calculator import calculate_from_scraper_result, print_bonus_summary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(profile_url):
    """
    Run the Coursera Profile Scraper and Bonus Calculator in sequence.
    First scrape the profile, then calculate bonus points for the courses.
    
    Args:
        profile_url (str): The URL of the Coursera profile to analyze
    """
    try:
        # Welcome message
        print("\n=== Coursera Profile Analyzer ===")
        print("This tool extracts information from public Coursera profiles")
        print("and calculates bonus points for each course based on multiple factors.")
        
        # Run the scraper to get profile data
        profile_data = run_scraper(profile_url)
        
        if profile_data:
            # Calculate bonus points
            print("\n=== Calculating Bonus Points ===")
            print("Analyzing courses for their career value and market relevance...")
            enhanced_data = calculate_from_scraper_result(profile_data)
            
            # Print bonus summary
            print_bonus_summary(enhanced_data)
            
            # Option to save results
            try:
                save = input("\nDo you want to save these results to a file? (y/n): ").strip().lower()
                if save in ['y', 'yes']:
                    try:
                        filename = input("Enter filename (or press Enter for default 'coursera_profile_with_bonus.json'): ").strip()
                        if not filename:
                            filename = "coursera_profile_with_bonus.json"
                    except EOFError:
                        # Default filename if running in non-interactive mode
                        filename = "coursera_profile_with_bonus.json"
                        print(f"Using default filename: {filename}")
                    
                    with open(filename, 'w') as f:
                        json.dump(enhanced_data, f, indent=2)
                    print(f"Results saved to {filename}")
            except EOFError:
                # Save the results automatically in non-interactive mode
                filename = "coursera_profile_with_bonus.json"
                with open(filename, 'w') as f:
                    json.dump(enhanced_data, f, indent=2)
                print(f"Results automatically saved to {filename} (non-interactive mode)")
            
            print("\nThank you for using the Coursera Profile Analyzer!")
        
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user.")
        return 1
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    
    return 0

def run_scraper(profile_url):
    """Run the interactive scraper and return the profile data"""
    # We'll create a custom scraper function that returns the data instead of displaying it
    from .coursera_scraper import scrape_coursera_profile, validate_coursera_url
    
    try:
        # Get profile URL from user
        print("\n=== Coursera Profile Scraper ===")
        # print("Enter a Coursera profile URL to begin (e.g., https://www.coursera.org/user/123456)")
        # print("Or press Enter to use a demo profile\n")
        
        try:
            profile_url = profile_url.strip()
        except EOFError:
            # If we get EOF error (e.g., when running in an automated environment)
            print("Using demo profile due to input error")
            profile_url = ""
        
        # If empty, use demo profile
        if not profile_url:
            profile_url = "https://www.coursera.org/user/example123"
            print(f"Using demo profile: {profile_url}")
            use_mock = True
        else:
            use_mock = "--mock" in sys.argv
            
            # Validate URL
            while not validate_coursera_url(profile_url):
                print(f"\nInvalid Coursera profile URL: {profile_url}")
                print("URL should be in the format: https://www.coursera.org/user/...")
                try:
                    profile_url = input("\nPlease enter a valid Coursera profile URL (or press Enter for demo): ").strip()
                    if not profile_url:
                        profile_url = "https://www.coursera.org/user/example123"
                        print(f"Using demo profile: {profile_url}")
                        use_mock = True
                        break
                except EOFError:
                    profile_url = "https://www.coursera.org/user/example123"
                    print(f"Using demo profile: {profile_url}")
                    use_mock = True
                    break
        
        # Scrape the profile
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=use_mock)
        
        # Display basic profile info
        print("\nProfile successfully scraped!")
        if "user_info" in result and "name" in result["user_info"]:
            print(f"User: {result['user_info']['name']}")
        
        if "completed_courses" in result:
            print(f"Courses found: {len(result['completed_courses'])}")
        
        return result
    except Exception as e:
        print(f"Error during scraping: {e}")
        # If there's an error, return mock data for the demo profile
        print("Using demo profile due to error")
        return scrape_coursera_profile("https://www.coursera.org/user/example123", use_mock=True)

def run_interactive(profile_url):
    return main(profile_url)

if __name__ == "__main__":
    sys.exit(run_interactive())
