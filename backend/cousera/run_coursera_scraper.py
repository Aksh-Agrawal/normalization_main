#!/usr/bin/env python3
"""
Run Coursera Profile Scraper

This script provides an interactive interface for the Coursera Profile Scraper,
prompting the user for a profile URL and displaying the results.
"""

import sys
import json
from coursera_scraper import scrape_coursera_profile, validate_coursera_url

def main():
    # Welcome message
    print("\n=== Coursera Profile Scraper ===")
    print("This tool extracts information from public Coursera profiles.")
    print("Enter a Coursera profile URL to begin (e.g., https://www.coursera.org/user/123456)\n")
    
    try:
        # Get profile URL from user
        profile_url = input("Profile URL: ").strip()
        if not profile_url:
            print("No URL provided. Exiting.")
            return 0
        
        # Validate URL
        while not validate_coursera_url(profile_url):
            print(f"\nInvalid Coursera profile URL: {profile_url}")
            print("URL should be in the format: https://www.coursera.org/user/...")
            profile_url = input("\nPlease enter a valid Coursera profile URL: ").strip()
            if not profile_url:
                print("No URL provided. Exiting.")
                return 0
        
        # Scrape the profile
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=False)
        
        # Format and display results
        json_output = json.dumps(result, indent=2)
        print("\nResults:")
        print(json_output)
        
        # Option to save results
        save = input("\nDo you want to save these results to a file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            filename = input("Enter filename (or press Enter for default 'coursera_profile.json'): ").strip()
            if not filename:
                filename = "coursera_profile.json"
            
            with open(filename, 'w') as f:
                f.write(json_output)
            print(f"Results saved to {filename}")
        
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