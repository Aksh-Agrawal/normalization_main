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
        # Method 1: Look for course sections and course containers
        # These often have specific structure in Coursera profiles
        course_sections = []
        
        # Find all section headers that might indicate course lists
        section_headers = soup.find_all(['h2', 'h3'], string=lambda s: s and any(
            keyword in str(s).lower() for keyword in ['course', 'learning', 'certificate', 'completed']
        ))
        
        # For each potential section header, find nearby course containers
        for header in section_headers:
            # Look at siblings and parent's children
            parent = header.parent
            if parent:
                # Look for divs or sections that might contain course listings
                container = parent.find_next(['div', 'section'])
                if container:
                    course_sections.append(container)
        
        # If no specific sections found, try the main content area
        if not course_sections:
            main_content = soup.find('main')
            if main_content:
                course_sections.append(main_content)
            else:
                # Look for any large containers that might hold courses
                for container in soup.find_all(['div', 'section'], class_=True):
                    # Skip small containers
                    if len(str(container)) > 1000:
                        course_sections.append(container)
        
        # Process each section to find course items
        for section in course_sections:
            # Look for items that might be course cards or course entries
            course_items = section.find_all(['div', 'article', 'li'], 
                                          attrs={'class': lambda c: c and any(
                                              keyword in str(c).lower() for keyword in 
                                              ['course', 'card', 'item', 'listing', 'entry', 'row']
                                          )})
            
            if not course_items:
                # If no class-based items found, try looking for structured divs
                course_items = section.find_all(['div'], recursive=False)
                
            # Process each potential course item
            for item in course_items:
                title_elem = None
                institution_elem = None
                date_elem = None
                certificate_link = None
                
                # Look for course title (usually in h3, h4, strong, or div with specific classes)
                title_candidates = item.find_all(['h3', 'h4', 'strong', 'div', 'span', 'p'], 
                                                limit=5,
                                                attrs={'class': lambda c: not c or not any(
                                                    nav in str(c).lower() for nav in 
                                                    ['time', 'date', 'institution', 'logo', 'partner', 'certificate']
                                                )})
                
                for candidate in title_candidates:
                    text = candidate.text.strip()
                    if text and len(text) > 5 and len(text) < 150:
                        # Skip navigation elements and common site sections
                        nav_terms = ['menu', 'search', 'browse', 'login', 'sign in', 'technical skills', 
                                    'analytical skills', 'business skills', 'career resources', 
                                    'community', 'learn anywhere', 'copyright', 'rights reserved']
                        if not any(term in text.lower() for term in nav_terms):
                            title_elem = candidate
                            break
                
                # If we found a title, extract the rest of the course data
                if title_elem:
                    # Look for institution (often near the title or in specific elements)
                    inst_candidates = item.find_all(['div', 'span', 'img', 'p'], limit=5)
                    for inst in inst_candidates:
                        # Check for common institution indicators
                        inst_text = inst.text.strip()
                        institution_keywords = ['university', 'institute', 'ibm', 'google', 'amazon', 'aws', 
                                            'microsoft', 'meta', 'coursera', 'deeplearning', 'stanford']
                        
                        if inst_text and any(keyword in inst_text.lower() for keyword in institution_keywords):
                            if inst_text != title_elem.text.strip():  # Avoid using the title as institution
                                institution_elem = inst
                                break
                    
                    # Look for completion date
                    date_candidates = item.find_all(['div', 'span', 'p'], 
                                                 string=lambda s: s and any(
                                                     date_word in str(s).lower() for date_word in 
                                                     ['completed', 'january', 'february', 'march', 'april', 'may', 'june', 
                                                      'july', 'august', 'september', 'october', 'november', 'december']
                                                 ))
                    if date_candidates:
                        date_elem = date_candidates[0]
                    
                    # Look for certificate link
                    for link in item.find_all('a'):
                        href = link.get('href', '')
                        link_text = link.text.strip().lower()
                        if 'certificate' in href or 'certificate' in link_text or 'view' in link_text:
                            certificate_link = link
                            break
                    
                    # Create the course data structure
                    course_data = {
                        "title": title_elem.text.strip(),
                        "institution": institution_elem.text.strip() if institution_elem else None,
                        "completion_date": date_elem.text.strip() if date_elem else None,
                        "duration": None,
                        "certificate_url": certificate_link.get('href') if certificate_link else None,
                        "course_url": None
                    }
                    
                    # Clean up the completion date to remove "Completed" prefix
                    if course_data["completion_date"] and "completed" in course_data["completion_date"].lower():
                        course_data["completion_date"] = re.sub(
                            r'completed\s*', '', course_data["completion_date"], flags=re.IGNORECASE
                        ).strip()
                    
                    # Add to our list if it's a valid course (has title and isn't in the list yet)
                    if course_data["title"] and course_data not in completed_courses:
                        completed_courses.append(course_data)
        
        # Method 2: If we still don't have courses, look for "View certificate" links
        if not completed_courses:
            for link in soup.find_all('a'):
                href = link.get('href', '')
                text = link.text.strip().lower()
                
                if 'certificate' in text or 'certificate' in href.lower() or 'view' in text.lower():
                    # Find the closest heading or strong text - likely a course title
                    parent = link.parent
                    
                    # Go up a few levels to find context
                    for _ in range(4):
                        if not parent:
                            break
                            
                        # Look for a title near this certificate link
                        title_elems = parent.find_all(['h3', 'h4', 'strong', 'div', 'p'])
                        for title_elem in title_elems:
                            title = title_elem.text.strip()
                            
                            # Is this a good course title?
                            if (title and title.lower() != 'certificate' and
                                title.lower() != 'view certificate' and
                                len(title) > 5 and len(title) < 150):
                                
                                # Create course data
                                course_data = {
                                    "title": title,
                                    "institution": None,
                                    "completion_date": None,
                                    "duration": None,
                                    "certificate_url": href if 'certificate' in href.lower() else None,
                                    "course_url": None
                                }
                                
                                # Look for institution name
                                for elem in parent.find_all(['span', 'div', 'p']):
                                    text = elem.text.strip()
                                    inst_keywords = ['university', 'institute', 'ibm', 'google', 'amazon',
                                                'microsoft', 'meta', 'coursera']
                                    if text and any(keyword in text.lower() for keyword in inst_keywords):
                                        if text != title:  # Don't use title as institution
                                            course_data["institution"] = text
                                            break
                                
                                # Look for completion date
                                for elem in parent.find_all(['span', 'div', 'p']):
                                    text = elem.text.strip().lower()
                                    if ('completed' in text or
                                        any(month in text for month in ['january', 'february', 'march', 'april', 'may', 'june',
                                                                   'july', 'august', 'september', 'october', 'november', 'december'])):
                                        if 'completed' in text:
                                            course_data["completion_date"] = text.replace('completed', '').strip()
                                        else:
                                            course_data["completion_date"] = text
                                        break
                                
                                # Add to our list if not already there
                                if course_data not in completed_courses:
                                    completed_courses.append(course_data)
                                break
                                
                        parent = parent.parent
        
        # Method 3: Look for course titles directly
        if not completed_courses:
            # Find all elements that might be course titles
            potential_titles = []
            
            # Common course keywords
            course_keywords = [
                'python', 'machine learning', 'data science', 'ai', 'artificial intelligence',
                'programming', 'development', 'web', 'app', 'mobile', 'cloud', 'security',
                'devops', 'deep learning', 'statistics', 'analytics', 'engineering', 'design',
                'leadership', 'management', 'business', 'marketing', 'finance', 'blockchain',
                'specialization', 'certificate', 'professional'
            ]
            
            # Find elements that might contain course titles
            for elem in soup.find_all(['h3', 'h4', 'strong', 'div', 'p']):
                text = elem.text.strip()
                
                if (text and len(text) > 10 and len(text) < 150 and
                    any(keyword in text.lower() for keyword in course_keywords)):
                    
                    # Avoid navigation elements
                    parent = elem.parent
                    is_navigation = False
                    if parent:
                        parent_classes = parent.get('class', [])
                        if parent_classes:
                            parent_class_str = ' '.join(parent_classes).lower()
                            if any(nav in parent_class_str for nav in ['nav', 'menu', 'header', 'footer']):
                                is_navigation = True
                    
                    if not is_navigation:
                        potential_titles.append(elem)
            
            # Process each potential title
            for title_elem in potential_titles:
                title = title_elem.text.strip()
                
                # Create course data
                course_data = {
                    "title": title,
                    "institution": None,
                    "completion_date": None,
                    "duration": None,
                    "certificate_url": None,
                    "course_url": None
                }
                
                # Look for related information in nearby elements
                parent = title_elem.parent
                if parent:
                    # Find institution
                    for sibling in list(parent.next_siblings)[:5] + list(parent.previous_siblings)[:5]:
                        if hasattr(sibling, 'text'):
                            text = sibling.text.strip()
                            inst_keywords = ['university', 'institute', 'ibm', 'google', 'amazon',
                                        'microsoft', 'meta', 'coursera']
                            if text and any(keyword in text.lower() for keyword in inst_keywords):
                                if text != title:  # Avoid using title as institution
                                    course_data["institution"] = text
                                    break
                    
                    # Find completion date
                    for sibling in list(parent.next_siblings)[:5] + list(parent.previous_siblings)[:5]:
                        if hasattr(sibling, 'text'):
                            text = sibling.text.strip().lower()
                            if ('completed' in text or
                                any(month in text for month in ['january', 'february', 'march', 'april', 'may', 'june',
                                                           'july', 'august', 'september', 'october', 'november', 'december'])):
                                if 'completed' in text:
                                    course_data["completion_date"] = text.replace('completed', '').strip()
                                else:
                                    course_data["completion_date"] = text
                                break
                
                # Only add if not a duplicate
                if course_data not in completed_courses:
                    completed_courses.append(course_data)
                
    except Exception as e:
        logger.error(f"Error extracting completed courses: {e}")
    
    return completed_courses
