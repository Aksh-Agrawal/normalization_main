#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for the Coursera Profile Scraper.
"""

import re
import logging
import json
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_coursera_url(url: str) -> bool:
    """
    Validate that the given URL is a Coursera profile URL.
    
    Args:
        url (str): The URL to validate.
        
    Returns:
        bool: True if the URL is a valid Coursera profile URL, False otherwise.
    """
    if not url or not isinstance(url, str):
        return False
    
    parsed = urlparse(url)
    
    # Check if domain is coursera.org
    if not parsed.netloc or not parsed.netloc.endswith('coursera.org'):
        return False
    
    # Check if path contains /user/ or /~
    if not parsed.path or (not '/user/' in parsed.path and not '/~' in parsed.path):
        return False
    
    return True


def extract_user_info(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Extract user information from the Coursera profile page.
    
    Args:
        soup (BeautifulSoup): The parsed HTML of the profile page.
        
    Returns:
        Dict[str, Any]: A dictionary containing the user's information.
    """
    user_info = {
        "name": "Unknown",
        "bio": None,
        "location": None,
        "profile_picture_url": None,
        "learning_info": {
            "courses_completed": 0,
            "specializations_completed": 0
        }
    }
    
    try:
        # Check if profile exists
        not_found_text = "profile you're looking for can't be found"
        page_text = soup.get_text()
        if not_found_text in page_text:
            user_info["name"] = "Profile not found"
            user_info["profile_exists"] = False
            return user_info
            
        # Extract name - using simpler selectors to improve compatibility
        name_tags = soup.find_all(['h1', 'h2', 'h3'])
        for tag in name_tags:
            if tag.text and len(tag.text.strip()) > 0:
                name = tag.text.strip()
                # Skip generic page titles and navigation elements
                skip_phrases = ["coursera", "home", "browse", "log in", "sign in", "join", "page not found"]
                if name and not any(phrase in name.lower() for phrase in skip_phrases):
                    user_info["name"] = name
                    break
                    
        # Extract bio - look for paragraphs or divs that might contain bio
        bio_candidates = soup.find_all(['p', 'div'], limit=15)
        for candidate in bio_candidates:
            text = candidate.text.strip()
            # A bio typically has more than 20 chars but less than 1000
            if text and 20 <= len(text) <= 1000:
                # Skip elements that are clearly navigation, headers, or generic text
                skip_phrases = ["home", "sign in", "log in", "join", "browse", "for business", "copyright"]
                if not any(phrase in text.lower() for phrase in skip_phrases):
                    user_info["bio"] = text
                    break
        
        # Extract location - find small text elements that might contain location
        for elem in soup.find_all(['span', 'small', 'div'], limit=20):
            text = elem.text.strip()
            # Locations are typically short and often contain a comma (City, Country)
            if text and 3 <= len(text) <= 50 and ',' in text:
                # Skip obvious non-location text
                skip_phrases = ["copyright", "terms", "privacy"]
                if not any(phrase in text.lower() for phrase in skip_phrases):
                    user_info["location"] = text
                    break
        
        # Extract profile picture
        for img in soup.find_all('img', limit=15):
            src = img.get('src')
            if src and ('profile' in src.lower() or 'avatar' in src.lower() or 'user' in src.lower()):
                user_info["profile_picture_url"] = src
                break
                    
        # Extract course count from text - more specific pattern matching to avoid false positives
        text_content = soup.get_text().lower()
        # Look for patterns like "5 courses completed" or "completed 5 courses"
        course_patterns = [
            r'(\d+)\s*course[s]?\s*completed',
            r'completed\s*(\d+)\s*course[s]?',
            r'(\d+)\s*course[s]?\s*[\w\s]{0,20}certificate'
        ]
        
        for pattern in course_patterns:
            match = re.search(pattern, text_content)
            if match:
                try:
                    count = int(match.group(1))
                    # Avoid extracting years or extremely large numbers
                    if count > 0 and count < 1000:
                        user_info["learning_info"]["courses_completed"] = count
                        break
                except (ValueError, IndexError):
                    pass
                    
        # Look for specialization counts
        spec_patterns = [
            r'(\d+)\s*specialization[s]?\s*completed',
            r'completed\s*(\d+)\s*specialization[s]?',
            r'(\d+)\s*specialization[s]?\s*[\w\s]{0,20}certificate'
        ]
        
        for pattern in spec_patterns:
            match = re.search(pattern, text_content)
            if match:
                try:
                    count = int(match.group(1))
                    # Avoid extracting years or extremely large numbers
                    if count > 0 and count < 100:  # A more reasonable upper limit for specializations
                        user_info["learning_info"]["specializations_completed"] = count
                        break
                except (ValueError, IndexError):
                    pass
    
    except Exception as e:
        logger.error(f"Error extracting user info: {e}")
    
    return user_info


def extract_completed_courses(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Extract completed courses information from the Coursera profile page.
    
    Args:
        soup (BeautifulSoup): The parsed HTML of the profile page.
        
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing information about a completed course.
    """
    completed_courses = []
    
    try:
        # Look for course links - these are most reliable indicators of courses
        course_links = []
        
        # Find all links on the page
        all_links = soup.find_all('a')
        for link in all_links:
            href = link.get('href', '')
            text = link.text.strip()
            
            # Only process links with text and href
            if href and text and len(text) > 3:
                # Coursera course links typically have these patterns
                if ('learn/' in href or '/course/' in href or 'certificate' in href):
                    # Skip links that are clearly not course-related
                    if not any(skip in text.lower() for skip in ['sign in', 'log in', 'register', 'forgot', 'help', 'settings']):
                        course_links.append(link)
        
        # Process found links to extract course information
        for link in course_links:
            href = link.get('href', '')
            title = link.text.strip()
            
            # Basic validation to avoid empty/too short titles
            if title and len(title) > 3:
                # Create course data structure
                course_data = {
                    "title": title,
                    "institution": None,
                    "completion_date": None,
                    "duration": None,
                    "certificate_url": href if 'certificate' in href.lower() else None,
                    "course_url": href if 'certificate' not in href.lower() else None
                }
                
                # Try to find institution by looking at nearby elements
                parent = link.parent
                if parent:
                    # Look for institution in siblings or parent's siblings
                    for sibling in list(parent.next_siblings)[:3]:
                        if hasattr(sibling, 'text'):
                            sib_text = sibling.text.strip()
                            # Institution names are typically shorter
                            if sib_text and 3 <= len(sib_text) <= 50:
                                course_data["institution"] = sib_text
                                break
                
                # Look for completion date in nearby text
                if parent:
                    parent_text = parent.get_text()
                    # Try to find dates using regex
                    date_patterns = [
                        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}',  # Month Year
                        r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY
                        r'\d{4}-\d{1,2}-\d{1,2}'  # YYYY-MM-DD
                    ]
                    
                    for pattern in date_patterns:
                        match = re.search(pattern, parent_text)
                        if match:
                            course_data["completion_date"] = match.group(0)
                            break
                
                # Add the course data to our list if it has at least a title and URL
                if course_data["title"] and (course_data["certificate_url"] or course_data["course_url"]):
                    # Avoid duplicates
                    if course_data not in completed_courses:
                        completed_courses.append(course_data)
                
    except Exception as e:
        logger.error(f"Error extracting completed courses: {e}")
    
    return completed_courses
