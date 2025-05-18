#!/usr/bin/env python3
"""
Friendly Coursera Profile Scraper

A simple, interactive scraper for Coursera profiles that accepts command-line arguments
but also works without them, prompting for user input when needed.
"""

import sys
import json
from .coursera_scraper import scrape_coursera_profile, validate_coursera_url

def main():
    """Main entry point for the interactive Coursera scraper"""
    print("\n=== Coursera Profile Scraper ===")
    print("This tool extracts information from public Coursera profiles.")
    
    # Check if a URL was provided as a command-line argument
    if len(sys.argv) > 1 and "coursera.org" in sys.argv[1]:
        profile_url = sys.argv[1]
        print(f"\nUsing provided URL: {profile_url}")
    else:
        # No URL provided, use a default one
        profile_url = "https://www.coursera.org/user/example123"
        print(f"\nUsing demo profile: {profile_url}")
    
    # Determine if we should use mock data
    use_mock = "example123" in profile_url
    
    # Scrape the profile
    print(f"\nScraping profile: {profile_url}...")
    result = scrape_coursera_profile(profile_url, use_mock=use_mock)
    
    # Display the results
    print("\nResults:")
    print(json.dumps(result, indent=2))
    
    print("\nThank you for using the Coursera Profile Scraper!")
    return 0

if __name__ == "__main__":
    sys.exit(main())