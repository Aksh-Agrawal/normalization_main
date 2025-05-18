#!/usr/bin/env python3
"""
Interactive Coursera Profile Scraper Wrapper

This script provides a direct, interactive interface for the Coursera Profile Scraper,
prompting the user to enter a profile URL and displaying the results.
"""

import sys
import json
from .coursera_scraper import scrape_coursera_profile, validate_coursera_url
import time

def main():
    """Main function to run the Coursera Profile Scraper interactively"""
    # Display welcome message
    print("\n=== Coursera Profile Scraper ===")
    print("This tool extracts information from public Coursera profiles.")
    
    # Default URL (used if no input is provided or for testing)
    default_url = "https://www.coursera.org/user/example123"
    
    # Ask for profile URL
    print("\nEnter a Coursera profile URL (e.g., https://www.coursera.org/user/123456)")
    print("Or press Enter to scrape a demo profile.")
    
    try:
        profile_url = input("Profile URL: ").strip()
        if not profile_url:
            profile_url = default_url
            print(f"Using default profile: {profile_url}")
        
        # Validate URL
        while not validate_coursera_url(profile_url):
            print(f"\nInvalid Coursera profile URL: {profile_url}")
            print("URL should be in the format: https://www.coursera.org/user/...")
            profile_url = input("\nPlease enter a valid Coursera profile URL: ").strip()
            if not profile_url:
                profile_url = default_url
                print(f"Using default profile: {profile_url}")
                break
        
        # Scrape the profile (using real data, not mock)
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=False)
        
        # Format and display results
        json_output = json.dumps(result, indent=2)
        print("\nResults:")
        print(json_output)
        
        # Option to save results
        save = input("\nDo you want to save these results to a file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            timestamp = int(time.time())
            default_filename = f"coursera_profile_{timestamp}.json"
            filename = input(f"Enter filename (or press Enter for '{default_filename}'): ").strip()
            if not filename:
                filename = default_filename
            
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