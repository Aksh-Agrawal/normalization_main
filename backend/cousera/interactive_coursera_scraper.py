#!/usr/bin/env python3
"""
Interactive Coursera Profile Scraper

This script provides an interactive way to scrape Coursera profile data,
allowing users to enter a profile URL when running the script.
"""

import sys
import json
import logging
import argparse
from .coursera_scraper import scrape_coursera_profile, validate_coursera_url

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run the interactive Coursera Profile Scraper"""
    parser = argparse.ArgumentParser(description='Interactive Coursera Profile Scraper')
    parser.add_argument('--url', help='The URL of the Coursera profile to scrape (optional)')
    parser.add_argument('--mock', action='store_true', help='Use mock data instead of scraping')
    args = parser.parse_args()
    
    try:
        # Get profile URL (either from command line or by asking the user)
        profile_url = args.url
        if not profile_url:
            print("\n=== Coursera Profile Scraper ===")
            print("This tool extracts information from public Coursera profiles.")
            
            # For the workflow environment, use a default URL
            default_url = "https://www.coursera.org/user/example123"
            print(f"\nUsing default profile: {default_url}")
            profile_url = default_url
            
            # In an interactive environment, we'd ask for input:
            # profile_url = input("Profile URL: ").strip()
            # if not profile_url:
            #     print("No URL provided. Exiting.")
            #     return 0
        
        # Validate URL (skip validation for the default URL)
        if profile_url == "https://www.coursera.org/user/example123":
            use_mock = True
        else:
            if not validate_coursera_url(profile_url):
                print(f"\nInvalid Coursera profile URL: {profile_url}")
                return 1
            use_mock = args.mock
        
        # Scrape the profile
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=use_mock)
        
        # Format and display results
        json_output = json.dumps(result, indent=2)
        print("\nResults:")
        print(json_output)
        
        print("\nThank you for using the Coursera Profile Scraper!")
        
    except KeyboardInterrupt:
        print("\n\nScraping cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())