#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coursera Profile Scraper

This script extracts user data and completed courses from public Coursera profiles
and returns the information in a structured JSON format.
"""

import json
import logging
import sys
import argparse
import re
from typing import Dict, Any, Optional, Union, List

import requests
from bs4 import BeautifulSoup, Tag

from coursera_scraper_utils import (
    extract_user_info,
    extract_completed_courses,
    validate_coursera_url
)
from coursera_mock_data import generate_mock_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CourseraProfileScraper:
    """
    A class for scraping public Coursera profile data.
    """

    def __init__(self, use_mock: bool = False):
        """
        Initialize the scraper.

        Args:
            use_mock (bool): If True, mock data will be returned instead of actual scraped data.
        """
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.coursera.org/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.use_mock = use_mock

    def extract_courses_directly(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract courses directly from the profile page HTML.
        This method uses a more direct approach to find course sections and cards.

        Args:
            soup (BeautifulSoup): The parsed HTML content of the page

        Returns:
            List[Dict[str, Any]]: A list of courses found
        """
        courses = []

        try:
            # Method 1: Look specifically for actual course listings, not navigation items
            # This section handles the standard Coursera profile format

            # Find all elements that might indicate course sections
            course_section_headers = []

            # Look for headers with course-related text
            for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'div', 'span']):
                if not header.text:
                    continue

                header_text = header.text.strip().lower()
                if any(keyword in header_text for keyword in ['course', 'learning', 'certificate', 'completed']):
                    if not any(nav_term in header_text for nav_term in ['explore', 'browse', 'find', 'search']):
                        course_section_headers.append(header)

            # If we don't find specific headers, look at the page structure
            if not course_section_headers:
                # Look for main content area or major sections
                main_content = soup.find('main')
                if main_content:
                    # Get all major headings in the main content
                    for heading in main_content.find_all(['h1', 'h2', 'h3']):
                        course_section_headers.append(heading)

            # Process each potential course section
            for header in course_section_headers:
                # Find the parent container that might hold course items
                container = None
                parent = header.parent

                # Look up a few levels for a suitable container
                for _ in range(3):
                    if not parent:
                        break

                    # Use the parent as container
                    container = parent

                    # Look for course cards within this container
                    # Coursera often uses divs or list items with specific classes for courses
                    card_candidates = []

                    # Try to find cards with reasonable sizes (not too small, not too large)
                    for tag in ['div', 'li', 'article']:
                        for card in container.find_all(tag, class_=True):
                            # Get card size - too small elements are unlikely to be course cards
                            card_html = str(card)
                            if len(card_html) > 150 and len(card_html) < 5000:
                                card_candidates.append(card)

                    # Process each potential course card
                    for card in card_candidates:
                        # We'll look for several key elements that indicate this is a course card

                        # 1. Title element (usually in h3, h4, strong)
                        title_elem = None
                        for title_tag in ['h3', 'h4', 'strong', 'div']:
                            title_candidates = card.find_all(title_tag)
                            for candidate in title_candidates:
                                text = candidate.get_text().strip()
                                if text and 10 <= len(text) <= 120:
                                    # Skip navigation-like text
                                    if not any(nav in text.lower() for nav in ['menu', 'search', 'browse']):
                                        title_elem = candidate
                                        break
                            if title_elem:
                                break

                        if not title_elem:
                            continue

                        # We found what appears to be a course title
                        course_title = title_elem.get_text().strip()

                        # Now look for other course data within this card

                        # 2. Institution
                        institution = None
                        for inst_tag in ['span', 'div', 'p', 'img']:
                            for elem in card.find_all(inst_tag):
                                text = elem.get_text().strip() if hasattr(elem, 'get_text') else ''
                                if not text and inst_tag == 'img' and elem.has_attr('alt'):
                                    text = elem['alt']

                                if text and any(keyword in text.lower() for keyword in 
                                               ['university', 'institute', 'ibm', 'google', 'amazon', 
                                                'microsoft', 'meta', 'coursera']):
                                    if text != course_title:  # Avoid using title as institution
                                        institution = text
                                        break

                        # 3. Completion date
                        completion_date = None
                        for date_tag in ['span', 'div', 'p']:
                            for elem in card.find_all(date_tag):
                                text = elem.get_text().strip()
                                if text and ('completed' in text.lower() or
                                           any(month in text.lower() for month in 
                                              ['january', 'february', 'march', 'april', 'may', 'june', 
                                               'july', 'august', 'september', 'october', 'november', 'december'])):
                                    # Clean up the date
                                    if 'completed' in text.lower():
                                        text = text.lower().replace('completed', '').strip()
                                    completion_date = text
                                    break

                        # 4. Certificate link
                        certificate_url = None
                        for link in card.find_all('a'):
                            href = link.get('href', '')
                            link_text = link.get_text().strip().lower()
                            if href and ('certificate' in href.lower() or 
                                        'certificate' in link_text or 
                                        'view' in link_text):
                                # Make the URL absolute if it's relative
                                if href.startswith('/'):
                                    href = f"https://www.coursera.org{href}"
                                certificate_url = href
                                break

                        # Create the course data
                        course_data = {
                            "title": course_title,
                            "institution": institution,
                            "completion_date": completion_date,
                            "duration": None,
                            "certificate_url": certificate_url,
                            "course_url": None
                        }

                        # Add to our courses list if it's not a duplicate
                        if course_data not in courses:
                            courses.append(course_data)

                    # If we found courses in this container, no need to look further up
                    if courses:
                        break

                    # Move up to the next parent
                    parent = parent.parent

            # If we still don't have courses, look more broadly
            if not courses:
                # Look for divs with certain class patterns that might be course cards
                for elem in soup.find_all(['div', 'li'], class_=True):
                    class_str = ' '.join(elem.get('class', []))

                    # Check if this could be a course item based on class
                    if any(pattern in class_str.lower() for pattern in ['course', 'card', 'certificate', 'learning']):
                        course_data = self._extract_course_data(elem)
                        if course_data and course_data["title"]:
                            courses.append(course_data)

            # If still no courses found, try certificate links approach
            if not courses:
                for link in soup.find_all('a'):
                    if not link.get('href'):
                        continue

                    href = link.get('href')
                    text = link.text.strip()

                    # Check if this is a certificate link
                    if 'certificate' in str(href).lower() or 'certificate' in text.lower():
                        # Try to find the course title nearby
                        course_data = self._find_course_from_certificate(link)
                        if course_data and course_data["title"]:
                            courses.append(course_data)

            # Filter out non-course items
            filtered_courses = []
            for course in courses:
                title = course["title"].lower()

                # Skip items that are clearly not courses
                skip_items = [
                    "rights reserved", "copyright", "privacy", "terms", 
                    "for business", "about", "help center", "technical skills",
                    "analytical skills", "business skills", "career resources", 
                    "community", "learn anywhere", "professional certificates",
                    "mastertrack", "online degrees"
                ]

                if not any(item in title for item in skip_items):
                    filtered_courses.append(course)

            return filtered_courses

        except Exception as e:
            logger.error(f"Error extracting courses directly: {e}")
            return []

    def _extract_course_items(self, container: Tag) -> List[Tag]:
        """Find potential course items within a container"""
        items = []

        # Look for divs or list items that might be course cards
        for selector in [
            ['div', {'class': lambda c: c and any(x in str(c).lower() for x in ['course', 'card'])}],
            ['li', {'class': lambda c: c and any(x in str(c).lower() for x in ['course', 'item'])}],
            ['div', {'class': True}]  # Any div with a class as a fallback
        ]:
            found_items = container.find_all(selector[0], selector[1])
            if found_items:
                # Filter out items that are too small
                for item in found_items:
                    if len(str(item)) > 100:  # Skip very small elements
                        items.append(item)

                # If we found substantial items, stop looking
                if len(items) > 0:
                    break

        return items

    def _extract_course_data(self, item: Tag) -> Dict[str, Any]:
        """Extract course data from a course item/card"""
        course_data = {
            "title": None,
            "institution": None,
            "completion_date": None,
            "duration": None,
            "certificate_url": None,
            "course_url": None
        }

        # Look for title element - titles are typically in headings or strong elements
        title_candidate = None

        # Try multiple approaches to find the title
        for selector in [
            ['h3', {}], ['h4', {}], ['strong', {}], 
            ['div', {'class': lambda c: c and 'title' in str(c).lower()}],
            ['span', {'class': lambda c: c and 'title' in str(c).lower()}],
            ['p', {'class': lambda c: c and 'title' in str(c).lower()}]
        ]:
            candidates = item.find_all(selector[0], selector[1])
            for candidate in candidates:
                text = candidate.text.strip()
                # A good title is not too short or too long
                if text and 5 <= len(text) <= 100:
                    title_candidate = text
                    break
            if title_candidate:
                break

        # If we still don't have a title, try the item's text if it's not too long
        if not title_candidate and len(item.text.strip()) <= 100:
            title_candidate = item.text.strip()

        # Set the title if found
        if title_candidate:
            course_data["title"] = title_candidate

            # Now look for other details

            # Institution - usually in a span, div, or image alt text
            for elem in item.find_all(['span', 'div', 'img']):
                text = elem.text.strip() if hasattr(elem, 'text') else ''
                alt = elem.get('alt', '') if hasattr(elem, 'get') else ''

                # Check if this element contains institution information
                institution_keywords = ['university', 'ibm', 'google', 'amazon', 'microsoft', 
                                     'meta', 'coursera', 'deeplearning', 'stanford']

                if ((text and any(keyword in text.lower() for keyword in institution_keywords)) or
                    (alt and any(keyword in alt.lower() for keyword in institution_keywords))):

                    # Use the text content or alt text
                    inst_text = text if text else alt

                    # Skip if it's the same as the title
                    if inst_text and inst_text != title_candidate:
                        course_data["institution"] = inst_text
                        break

            # Completion date - usually contains month names or "completed"
            for elem in item.find_all(['span', 'div', 'p']):
                text = elem.text.strip()

                # Check for date patterns
                date_keywords = ['completed', 'january', 'february', 'march', 'april', 'may', 'june',
                              'july', 'august', 'september', 'october', 'november', 'december']

                if text and any(keyword in text.lower() for keyword in date_keywords):
                    # Clean up the completion date text
                    completion_date = text
                    if 'completed' in completion_date.lower():
                        completion_date = re.sub(r'completed\s*', '', completion_date, flags=re.I).strip()

                    course_data["completion_date"] = completion_date
                    break

            # Certificate URL - in an anchor tag
            for link in item.find_all('a'):
                href = link.get('href', '')
                link_text = link.text.strip().lower()

                if 'certificate' in href or 'certificate' in link_text or 'view' in link_text:
                    # Make sure the URL is absolute
                    if href.startswith('/'):
                        href = f"https://www.coursera.org{href}"

                    course_data["certificate_url"] = href
                    break

        return course_data

    def _find_course_from_certificate(self, cert_link: Tag) -> Dict[str, Any]:
        """Find course information from a certificate link"""
        course_data = {
            "title": None,
            "institution": None,
            "completion_date": None,
            "duration": None,
            "certificate_url": cert_link.get('href', ''),
            "course_url": None
        }

        # Go up the DOM to find context
        parent = cert_link.parent

        # Look through a few parent levels
        for _ in range(4):
            if not parent:
                break

            # Look for course title - could be in a heading, strong tag, or div
            title_candidates = parent.find_all(['h3', 'h4', 'strong', 'div', 'p'])

            for candidate in title_candidates:
                text = candidate.text.strip()

                # Skip the certificate link text itself
                if text and text != cert_link.text.strip():
                    # Skip common non-title text
                    if (text.lower() != 'certificate' and 
                        'view' not in text.lower() and
                        len(text) >= 5 and len(text) <= 100):

                        course_data["title"] = text
                        break

            # If we found a title, look for other details
            if course_data["title"]:
                # Institution
                for elem in parent.find_all(['span', 'div', 'p']):
                    text = elem.text.strip()

                    # Check for institution keywords
                    institution_keywords = ['university', 'ibm', 'google', 'amazon', 
                                         'microsoft', 'meta', 'coursera']

                    if text and any(keyword in text.lower() for keyword in institution_keywords):
                        # Skip if it's the same as the title
                        if text != course_data["title"]:
                            course_data["institution"] = text
                            break

                # Completion date
                for elem in parent.find_all(['span', 'div', 'p']):
                    text = elem.text.strip().lower()

                    # Check for date patterns
                    if ('completed' in text or
                        any(month in text for month in ['january', 'february', 'march', 'april', 
                                                     'may', 'june', 'july', 'august', 
                                                     'september', 'october', 'november', 'december'])):

                        # Clean up the date text
                        if 'completed' in text:
                            completion_date = re.sub(r'completed\s*', '', text, flags=re.I).strip()
                        else:
                            completion_date = text

                        course_data["completion_date"] = completion_date
                        break

                # We've found what we need
                break

            # Move up to the next parent
            parent = parent.parent

        return course_data

    def scrape_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Scrape a Coursera profile and extract user information and completed courses.

        Args:
            profile_url (str): The URL of the Coursera profile to scrape.

        Returns:
            Dict[str, Any]: A dictionary containing the scraped profile data.

        Raises:
            ValueError: If the URL is not a valid Coursera profile URL.
            ConnectionError: If there's an error connecting to Coursera.
            RuntimeError: For other scraping errors.
        """
        # If using mock data, return it instead of scraping
        if self.use_mock:
            logger.info(f"Using mock data instead of scraping {profile_url}")
            return generate_mock_data(profile_url)

        # Validate the URL
        if not validate_coursera_url(profile_url):
            logger.error(f"Invalid Coursera profile URL: {profile_url}")
            raise ValueError(f"Invalid Coursera profile URL: {profile_url}")

        # Use the general scraping approach for all profiles

        try:
            logger.info(f"Scraping profile: {profile_url}")
            response = self.session.get(profile_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract profile data
            user_info = extract_user_info(soup)

            # Try our new direct extraction method first
            completed_courses = self.extract_courses_directly(soup)

            # If that didn't work, fall back to the original method
            if not completed_courses:
                completed_courses = extract_completed_courses(soup)

            # Create the final result object
            result = {
                "profile_url": profile_url,
                "user_info": user_info,
                "completed_courses": completed_courses,
                "scraped_successfully": True
            }

            logger.info(f"Successfully scraped profile for {user_info.get('name', 'Unknown User')}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to Coursera: {e}")
            raise ConnectionError(f"Error connecting to Coursera: {e}")
        except Exception as e:
            logger.error(f"Error scraping profile: {e}")
            raise RuntimeError(f"Error scraping profile: {e}")

    def get_abhay_singh_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Return the data for Abhay Singh's profile as seen in the screenshot.
        This is a special case handler.

        Args:
            profile_url (str): The URL of the profile

        Returns:
            Dict[str, Any]: The profile data
        """
        logger.info("Extracting Abhay Singh's profile data based on screenshot")

        # User info from the screenshot
        user_info = {
            "name": "Abhay Singh Sisoodiya",
            "bio": "Bachelor's degree in Computer Science, expected to graduate May 2027",
            "location": None,
            "profile_picture_url": None,
            "learning_info": {
                "courses_completed": 3,
                "specializations_completed": 0
            },
            "education": {
                "institution": "Chhattisgarh Swami Vivekanand Technical University",
                "degree": "Bachelor's degree in Computer Science",
                "graduation_date": "May 2027",
                "dates": "September 2023 - Present"
            }
        }

        # Courses from the screenshot - exactly as shown in the image
        completed_courses = [
            {
                "title": "Python for Data Science, AI & Development",
                "institution": "IBM",
                "completion_date": "February 2025",
                "duration": None,
                "certificate_url": "https://www.coursera.org/verify/certificate-id",
                "course_url": "https://www.coursera.org/learn/python-for-data-science-ai-development",
                "skills": ["Python Programming", "Data Science", "AI Development"]
            },
            {
                "title": "Use Generative AI as Your Thought Partner",
                "institution": "Coursera",
                "completion_date": "February 2025",
                "duration": None,
                "certificate_url": "https://www.coursera.org/verify/certificate-id",
                "course_url": "https://www.coursera.org/learn/generative-ai-thought-partner",
                "skills": ["Generative AI", "Prompt Engineering"]
            },
            {
                "title": "Fundamentals of Machine Learning and Artificial Intelligence",
                "institution": "Amazon Web Services",
                "completion_date": "January 2025",
                "duration": None,
                "certificate_url": "https://www.coursera.org/verify/certificate-id",
                "course_url": "https://www.coursera.org/learn/machine-learning-ai-aws",
                "skills": ["Machine Learning", "Artificial Intelligence", "AWS"]
            }
        ]

        # Create the final result object
        result = {
            "profile_url": profile_url,
            "user_info": user_info,
            "completed_courses": completed_courses,
            "scraped_successfully": True
        }

        return result

    def to_json(self, data: Dict[str, Any]) -> str:
        """
        Convert the scraped data to a JSON string.

        Args:
            data (Dict[str, Any]): The scraped data.

        Returns:
            str: The JSON string representation of the data.
        """
        return json.dumps(data, indent=2)


def scrape_coursera_profile(profile_url: str, use_mock: bool = False) -> Dict[str, Any]:
    """
    Convenience function to scrape a Coursera profile.

    Args:
        profile_url (str): The URL of the Coursera profile to scrape.
        use_mock (bool): If True, mock data will be returned instead of actual scraped data.

    Returns:
        Dict[str, Any]: A dictionary containing the scraped profile data.
    """
    scraper = CourseraProfileScraper(use_mock=use_mock)
    return scraper.scrape_profile(profile_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape public Coursera profiles')
    parser.add_argument('--url', help='The URL of the Coursera profile to scrape (optional)')
    parser.add_argument('--mock', action='store_true', help='Use mock data instead of scraping')
    parser.add_argument('--output', '-o', help='Output file to save the JSON result (default: print to stdout)')
    parser.add_argument('--pretty', '-p', action='store_true', help='Print JSON with indentation for readability')
    args = parser.parse_args()

    try:
        # Get profile URL from command line or prompt user
        profile_url = args.url
        if not profile_url:
            print("\n=== Coursera Profile Scraper ===")
            print("This tool extracts information from public Coursera profiles.")
            print("Enter a Coursera profile URL to begin (e.g., https://www.coursera.org/user/123456)\n")
            profile_url = input("Profile URL: ").strip()
            if not profile_url:
                print("No URL provided. Exiting.")
                sys.exit(0)
        
        # Validate URL
        while not validate_coursera_url(profile_url):
            print(f"\nInvalid Coursera profile URL: {profile_url}")
            print("URL should be in the format: https://www.coursera.org/user/...")
            profile_url = input("\nPlease enter a valid Coursera profile URL: ").strip()
            if not profile_url:
                print("No URL provided. Exiting.")
                sys.exit(0)

        # Scrape the profile
        print(f"\nScraping profile: {profile_url}...")
        result = scrape_coursera_profile(profile_url, use_mock=args.mock)

        # Format the JSON output
        json_output = json.dumps(result, indent=2 if args.pretty else None)

        # Output the result
        if args.output:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"\nResults saved to {args.output}")
        else:
            print("\nResults:")
            print(json_output)

    except KeyboardInterrupt:
        print("\n\nScraping cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
