#!/usr/bin/env python3
"""
Interactive Coursera Profile Scraper (with command-line support)

This script provides a flexible way to scrape Coursera profile data,
accepting URLs from command-line arguments or prompting the user for input.
It works both in interactive and non-interactive environments.
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
    """Run the Coursera Profile Scraper with flexible command line handling"""
    # Parse command line, but ignore unrecognized arguments
    parser = argparse.ArgumentParser(description='Coursera Profile Scraper')
    parser.add_argument('--url', help='The URL of the Coursera profile to scrape (optional)')
    parser.add_argument('--mock', action='store_true', help='Use mock data instead of scraping')
    parser.add_argument('--output', '-o', help='Output file to save JSON results')
    
    # Parse known args only
    args, unknown = parser.parse_known_args()
    
    try:
        # Check if URL was provided in unknown args (as positional parameter)
        profile_url = args.url
        if not profile_url and unknown:
            # Take the first unrecognized arg that looks like a URL
            for arg in unknown:
                if 'coursera.org' in arg:
                    profile_url = arg
                    break
        
        # If still no URL, use default
        if not profile_url:
            print("\n=== Coursera Profile Scraper ===")
            print("This tool extracts information from public Coursera profiles.")
            print("\nUsing default profile: https://www.coursera.org/user/example123")
            profile_url = "https://www.coursera.org/user/example123"
            use_mock = True
        else:
            use_mock = args.mock or 'example123' in profile_url
        
        # Scrape the profile
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=use_mock)
        
        # Output the result
        json_output = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"\nResults saved to {args.output}")
        else:
            print("\nResults:")
            print(json_output)
            
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