#!/usr/bin/env python3
"""
Mock data generation for the Coursera Profile Scraper.

This module provides functionality to generate realistic mock data 
when scraping is not possible or during testing.
"""

import random
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

def generate_mock_data(profile_url: str) -> Dict[str, Any]:
    """
    Generate realistic mock data for a Coursera profile.
    
    Args:
        profile_url (str): The URL of the Coursera profile to generate mock data for.
        
    Returns:
        Dict[str, Any]: A dictionary containing mock profile data.
    """
    logger.info(f"Using mock data instead of scraping {profile_url}")
    
    # Extract user ID from URL
    user_id = profile_url.rsplit('/', 1)[-1]
    
    # Generate user info
    user_info = generate_mock_user_info(user_id)
    
    # Generate completed courses
    completed_courses = generate_mock_courses(3)
    
    # Create the final result object
    result = {
        "profile_url": profile_url,
        "user_info": user_info,
        "completed_courses": completed_courses,
        "scraped_successfully": True,
        "is_mock_data": True
    }
    
    return result

def generate_mock_user_info(user_id: str) -> Dict[str, Any]:
    """
    Generate mock user information.
    
    Args:
        user_id (str): The user ID to base the mock data on.
        
    Returns:
        Dict[str, Any]: A dictionary containing mock user information.
    """
    return {
        "name": "Alex Martinez",
        "bio": "Lifelong learner interested in AI, Public Health, and Cloud Computing.",
        "location": "Austin, TX",
        "profile_picture_url": f"https://www.coursera.org/static/images/user-profiles/{random.randint(0, 1000)}.jpg",
        "learning_info": {
            "courses_completed": 21,
            "specializations_completed": 2
        }
    }

def generate_mock_courses(num_courses: int) -> List[Dict[str, Any]]:
    """
    Generate mock completed courses.
    
    Args:
        num_courses (int): The number of courses to generate.
        
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing mock course information.
    """
    courses = [
        {
            "title": "Deep Learning Specialization",
            "institution": "deeplearning.ai",
            "completion_date": "April 2025",
            "duration": "10 weeks",
            "certificate_url": "https://www.coursera.org/verify/certification/861397",
            "course_url": f"https://www.coursera.org/learn/{random.randint(0, 10000)}",
            "skills": ["Deep Learning", "Neural Networks", "Machine Learning"]
        },
        {
            "title": "Data Science: R Basics",
            "institution": "Harvard University",
            "completion_date": "December 2024",
            "duration": "Approximately 24 hours",
            "certificate_url": "https://www.coursera.org/verify/certification/809641",
            "course_url": f"https://www.coursera.org/learn/{random.randint(0, 10000)}",
            "skills": ["R Programming", "Data Science", "Statistics"]
        },
        {
            "title": "Music Production",
            "institution": "Berklee College of Music",
            "completion_date": "August 2023",
            "duration": "4 months",
            "certificate_url": "https://www.coursera.org/verify/certification/804377",
            "course_url": f"https://www.coursera.org/learn/{random.randint(0, 10000)}",
            "skills": ["Music Production", "Audio Engineering", "Digital Audio Workstations"]
        }
    ]
    
    return courses[:num_courses]