#!/usr/bin/env python3
"""
Simple Interactive Coursera Profile Scraper

This script provides an interactive interface for the Coursera Profile Scraper,
prompting the user to enter a profile URL and displaying the results.
"""

import sys
import json
import logging
from coursera_scraper import scrape_coursera_profile, validate_coursera_url

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the Coursera Profile Scraper interactively"""
    
    # Demo URL to use if no URL is provided
    default_url = "https://www.coursera.org/user/example123"
    
    # Welcome message
    print("\n=== Coursera Profile Scraper ===")
    print("This tool extracts information from public Coursera profiles.")
    print("\nEnter a Coursera profile URL or press Enter to use the demo profile.")
    
    try:
        # Get URL from user or use default
        profile_url = input("Profile URL (or press Enter for demo): ").strip()
        if not profile_url:
            profile_url = default_url
            print(f"Using demo profile: {profile_url}")
            
        # Scrape the profile (use demo mode for the demo URL)
        use_mock = (profile_url == default_url)
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=use_mock)
        
        # Display results
        print("\nResults:")
        print(json.dumps(result, indent=2))
        
        print("\nThank you for using the Coursera Profile Scraper!")
        return 0
        
    except KeyboardInterrupt:
        print("\n\nScraping cancelled by user.")
        return 0
    except Exception as e:
        logger.error(f"Error scraping profile: {str(e)}")
        print(f"\nError: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())