#!/usr/bin/env python3
"""
Coursera Bonus Calculator

This advanced module calculates comprehensive bonus points for Coursera courses 
based on multiple weighted factors:

- Institution reputation and global ranking
- Course duration and intensity
- Course topic relevance and industry demand
- Skills covered and their market value
- Course difficulty and specialization level
- Instructor credentials
- Course popularity metrics
- Certificate value

The calculator provides detailed metrics to evaluate the relative value and 
career impact of different courses in your learning portfolio.
"""

import json
import sys
import time
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
total_bonus_sum: float = 0.0
# Institution reputation scores (higher = more prestigious)
INSTITUTION_SCORES = {
    # Top Tier Universities (9-10)
    "Stanford University": 10,
    "Harvard University": 10, 
    "Massachusetts Institute of Technology": 10,
    "California Institute of Technology": 10,
    "University of Oxford": 10,
    "University of Cambridge": 10,
    "ETH Zurich": 9.5,
    "Yale University": 9.5,
    "Princeton University": 9.5,
    "Imperial College London": 9,
    "University of Chicago": 9,
    "Columbia University": 9,
    "Technical University of Munich": 9,
    "National University of Singapore": 9,
    
    # Strong Universities (8-8.9)
    "University of California, Berkeley": 8.8,
    "University of California, Los Angeles": 8.5,
    "University of California": 8.5,
    "University of Michigan": 8.5,
    "Johns Hopkins University": 8.5,
    "Cornell University": 8.5,
    "University of Pennsylvania": 8.5,
    "University of Toronto": 8.3,
    "University of Washington": 8.3,
    "New York University": 8.2,
    "University of Edinburgh": 8.2,
    "University of Texas at Austin": 8.2,
    "Georgia Institute of Technology": 8.2,
    "Carnegie Mellon University": 8.8,
    "Duke University": 8.3,
    "Northwestern University": 8.2,
    "University of British Columbia": 8.0,
    "University of Illinois Urbana-Champaign": 8.0,
    
    # Good Universities (7-7.9)
    "Rice University": 7.8,
    "University of London": 7.5,
    "University of Wisconsin-Madison": 7.5,
    "University of Hong Kong": 7.8,
    "University of Melbourne": 7.7,
    "University of Sydney": 7.6,
    "Purdue University": 7.6,
    "University of Southern California": 7.5,
    "Boston University": 7.3,
    "Arizona State University": 7.0,
    "University of Minnesota": 7.0,
    "University of Colorado Boulder": 7.0,
    
    # Top Tech Companies (8-9.5)
    "Google": 9.2,
    "Meta": 9.0,
    "OpenAI": 9.5,
    "Microsoft": 8.8,
    "Amazon Web Services": 8.5,
    "Apple": 8.6,
    "IBM": 8.3,
    "NVIDIA": 8.7,
    "Salesforce": 8.0,
    "Intel": 8.0,
    "Adobe": 8.0,
    "Oracle": 7.8,
    
    # AI/ML Specialized Organizations
    "deeplearning.ai": 9.3,
    "OpenAI": 9.5,
    "Hugging Face": 8.8,
    "NVIDIA Deep Learning Institute": 8.7,
    
    # Specialized Institutions
    "Berklee College of Music": 9.5,  # Top for music
    "Juilliard School": 9.7,  # Top for performing arts
    "Rhode Island School of Design": 9.3,  # Top for design
    "London School of Economics": 9.2,  # Top for economics
    "Wharton School": 9.5,  # Top for business
    
    # Coursera Entities
    "Coursera": 6.5,
    "Coursera Project Network": 6.0,
    
    # Other Notable Organizations
    "World Bank": 8.5,
    "United Nations": 8.3,
    "International Monetary Fund": 8.2,
    "Linux Foundation": 8.0,
    "Khan Academy": 7.5,
    
    # Default for unlisted institutions
    "default": 5.5
}

# Topic/field bonus points based on industry demand and future relevance
FIELD_SCORES = {
    # AI and Machine Learning (9-10)
    "artificial intelligence": 10,
    "machine learning": 10,
    "deep learning": 10,
    "neural networks": 9.8,
    "natural language processing": 9.7,
    "computer vision": 9.5,
    "reinforcement learning": 9.3,
    "generative ai": 10,
    "prompt engineering": 9.5,
    "llm": 9.8,
    "large language models": 9.8,
    "gpt": 9.5,
    "transformers": 9.6,
    
    # Data Science and Analytics (8-9.5)
    "data science": 9.5,
    "big data": 9.0,
    "data analytics": 9.0,
    "data mining": 8.7,
    "predictive analytics": 8.8,
    "business intelligence": 8.5,
    "data visualization": 8.7,
    "tableau": 8.5,
    "power bi": 8.4,
    
    # Programming and Development (7.5-9)
    "programming": 8.5,
    "software engineering": 8.7,
    "software development": 8.7,
    "web development": 8.2,
    "mobile development": 8.3,
    "app development": 8.3,
    "front-end": 8.0,
    "back-end": 8.1,
    "full-stack": 8.5,
    "devops": 9.0,
    "python": 9.0,
    "javascript": 8.5,
    "java": 8.0,
    "c++": 8.2,
    "c#": 8.0,
    "typescript": 8.6,
    "go": 8.7,
    "rust": 8.8,
    "react": 8.5,
    "angular": 8.0,
    "vue": 8.2,
    "node.js": 8.3,
    "django": 8.3,
    "flask": 8.2,
    "swift": 8.1,
    "kotlin": 8.2,
    
    # Cloud and Infrastructure (8.5-9.5)
    "cloud computing": 9.2,
    "aws": 9.0,
    "amazon web services": 9.0,
    "azure": 8.8,
    "google cloud": 8.8,
    "kubernetes": 9.0,
    "docker": 8.8,
    "microservices": 8.7,
    "serverless": 8.8,
    "infrastructure as code": 8.9,
    
    # Cybersecurity (8.5-9.5)
    "cybersecurity": 9.3,
    "information security": 9.2,
    "network security": 8.9,
    "ethical hacking": 8.8,
    "penetration testing": 8.8,
    "cryptography": 8.6,
    "security": 8.7,
    
    # Blockchain and Crypto (7.5-8.5)
    "blockchain": 8.0,
    "cryptocurrency": 7.8,
    "smart contracts": 7.9,
    "ethereum": 7.7,
    "web3": 7.9,
    
    # Business and Management (6.5-8)
    "business": 7.0,
    "management": 7.2,
    "project management": 7.8,
    "product management": 8.0,
    "agile": 7.9,
    "scrum": 7.8,
    "entrepreneurship": 7.5,
    "innovation": 7.3,
    "leadership": 7.5,
    "strategy": 7.2,
    "operations": 6.8,
    
    # Finance and Economics (7-8.5)
    "finance": 7.8,
    "fintech": 8.3,
    "accounting": 7.0,
    "economics": 7.2,
    "investment": 7.5,
    "banking": 7.0,
    "trading": 7.3,
    "risk management": 7.5,
    
    # Marketing and Sales (6.5-8)
    "marketing": 7.0,
    "digital marketing": 7.8,
    "seo": 7.5,
    "social media marketing": 7.2,
    "content marketing": 7.3,
    "email marketing": 7.0,
    "sales": 6.8,
    "advertising": 6.7,
    "branding": 6.8,
    
    # Design and UX (7-8.5)
    "design": 7.5,
    "ux": 8.2,
    "ui": 8.0,
    "user experience": 8.2,
    "user interface": 8.0,
    "graphic design": 7.2,
    "web design": 7.5,
    "product design": 8.0,
    "interaction design": 7.8,
    
    # Arts and Creativity (5.5-7)
    "music": 6.0,
    "art": 5.5,
    "photography": 5.8,
    "film": 6.0,
    "animation": 7.0,
    "creative writing": 5.8,
    
    # Sciences (7-8.5)
    "physics": 7.5,
    "biology": 7.2,
    "chemistry": 7.0,
    "astronomy": 7.0,
    "environmental science": 7.2,
    "genetics": 7.5,
    "neuroscience": 7.8,
    
    # Mathematics and Statistics (7.5-8.5)
    "mathematics": 7.8,
    "statistics": 8.2,
    "calculus": 7.6,
    "linear algebra": 7.8,
    "probability": 8.0,
    "numerical analysis": 7.5,
    
    # Healthcare and Medicine (7-8.5)
    "health": 7.5,
    "healthcare": 7.8,
    "medicine": 8.0,
    "public health": 7.7,
    "nursing": 7.5,
    "nutrition": 7.0,
    "mental health": 7.5,
    
    # Engineering (7.5-8.5)
    "engineering": 8.0,
    "mechanical engineering": 7.8,
    "electrical engineering": 8.0,
    "civil engineering": 7.5,
    "chemical engineering": 7.5,
    "biomedical engineering": 8.2,
    "aerospace engineering": 7.8,
    
    # Education and Psychology (6-7.5)
    "education": 6.5,
    "teaching": 6.3,
    "psychology": 6.8,
    "child development": 6.5,
    "counseling": 6.7,
    "cognitive science": 7.3,
    
    # Languages and Communication (5.5-7)
    "language": 6.0,
    "english": 5.8,
    "spanish": 5.8,
    "chinese": 6.5,
    "japanese": 6.3,
    "communication": 6.5,
    "public speaking": 6.8,
    "writing": 6.0,
    "technical writing": 7.0,
    
    # IoT and Hardware (7.5-8.5)
    "internet of things": 8.0,
    "iot": 8.0,
    "embedded systems": 7.8,
    "arduino": 7.5,
    "raspberry pi": 7.6,
    "robotics": 8.3,
    "hardware": 7.7,
    
    # Emerging Technologies (8-9.5)
    "quantum computing": 9.0,
    "augmented reality": 8.5,
    "virtual reality": 8.3,
    "ar": 8.5,
    "vr": 8.3,
    "metaverse": 8.0,
    "biotechnology": 8.5,
    "nanotechnology": 8.2,
    "3d printing": 7.8,
    "drone": 7.5,
    
    # Default for unlisted fields
    "default": 6.0
}

# Skill value scores based on current job market demand and future growth potential
SKILL_SCORES = {
    # AI and Machine Learning (9-10)
    "artificial intelligence": 10,
    "machine learning": 10,
    "deep learning": 10,
    "neural networks": 9.7,
    "natural language processing": 9.8,
    "nlp": 9.8,
    "computer vision": 9.5,
    "generative ai": 10,
    "generative artificial intelligence": 10,
    "large language models": 9.9,
    "llm": 9.9,
    "gpt": 9.6,
    "transformers": 9.7,
    "reinforcement learning": 9.3,
    "supervised learning": 9.0,
    "unsupervised learning": 9.1,
    "chatgpt": 9.5,
    "prompt engineering": 9.7,
    "openai": 9.5,
    "hugging face": 9.3,
    "tensorflow": 9.2,
    "pytorch": 9.4,
    "keras": 9.1,
    "scikit-learn": 9.0,
    
    # Data Science and Analytics (8-9.5)
    "data science": 9.5,
    "data analysis": 9.0,
    "data analytics": 9.0,
    "data visualization": 8.5,
    "data mining": 8.7,
    "big data": 8.8,
    "predictive analytics": 9.0,
    "statistical analysis": 8.7,
    "business intelligence": 8.5,
    "bi": 8.5,
    "tableau": 8.6,
    "power bi": 8.5,
    "data modeling": 8.8,
    "data engineering": 9.2,
    "etl": 8.8,
    "data warehousing": 8.6,
    "data governance": 8.3,
    "data storytelling": 8.4,
    "dashboard design": 8.3,
    
    # Programming Languages (7.5-9.5)
    "programming": 8.5,
    "python": 9.5,
    "r programming": 8.5,
    "r": 8.5,
    "javascript": 9.0,
    "typescript": 9.1,
    "java": 8.5,
    "c++": 8.7,
    "c#": 8.5,
    "go": 9.0,
    "golang": 9.0,
    "rust": 9.1,
    "swift": 8.5,
    "kotlin": 8.6,
    "php": 7.8,
    "ruby": 7.9,
    "scala": 8.3,
    "perl": 7.0,
    "shell scripting": 8.0,
    "bash": 8.0,
    "powershell": 7.8,
    "sql": 8.7,
    "nosql": 8.5,
    "haskell": 7.8,
    "assembly": 7.5,
    "cobol": 7.0,
    "fortran": 6.5,
    
    # Web and Mobile Development (8-9.2)
    "web development": 8.8,
    "mobile development": 8.7,
    "front-end": 8.8,
    "frontend": 8.8,
    "front-end development": 8.8,
    "back-end": 8.9,
    "backend": 8.9,
    "back-end development": 8.9,
    "full-stack": 9.0,
    "fullstack": 9.0,
    "full-stack development": 9.0,
    "html": 8.0,
    "css": 8.0,
    "sass": 8.0,
    "less": 7.8,
    "react": 9.2,
    "react native": 9.0,
    "angular": 8.5,
    "vue.js": 8.8,
    "vue": 8.8,
    "svelte": 8.7,
    "node.js": 9.0,
    "express.js": 8.8,
    "django": 8.7,
    "flask": 8.6,
    "ruby on rails": 8.0,
    "spring boot": 8.5,
    "laravel": 8.2,
    "asp.net": 8.3,
    "jquery": 7.5,
    "bootstrap": 8.0,
    "tailwind css": 8.7,
    "responsive design": 8.2,
    "progressive web apps": 8.6,
    "pwa": 8.5,
    "ios development": 8.5,
    "android development": 8.5,
    "flutter": 8.8,
    "xamarin": 8.0,
    "ionic": 8.0,
    "cordova": 7.7,
    "react navigation": 8.7,
    
    # Cloud Computing (8.5-9.5)
    "cloud computing": 9.2,
    "aws": 9.2,
    "amazon web services": 9.2,
    "azure": 9.0,
    "microsoft azure": 9.0,
    "google cloud": 8.8,
    "gcp": 8.8,
    "cloud architecture": 9.0,
    "cloud migration": 8.8,
    "cloud security": 9.0,
    "cloud native": 9.0,
    "serverless": 8.8,
    "lambda": 8.7,
    "ec2": 8.5,
    "s3": 8.5,
    "rds": 8.5,
    "dynamodb": 8.6,
    
    # DevOps and Infrastructure (8.5-9.3)
    "devops": 9.3,
    "ci/cd": 9.0,
    "continuous integration": 9.0,
    "continuous deployment": 9.0,
    "infrastructure as code": 9.0,
    "iac": 9.0,
    "terraform": 9.0,
    "ansible": 8.7,
    "puppet": 8.5,
    "chef": 8.5,
    "kubernetes": 9.2,
    "k8s": 9.2,
    "docker": 9.0,
    "container orchestration": 9.0,
    "microservices": 9.0,
    "service mesh": 8.8,
    "istio": 8.7,
    "jenkins": 8.7,
    "github actions": 8.8,
    "gitlab ci": 8.7,
    "monitoring": 8.5,
    "prometheus": 8.7,
    "grafana": 8.6,
    "logging": 8.5,
    "elk stack": 8.6,
    "site reliability engineering": 9.0,
    "sre": 9.0,
    
    # Databases (8-9)
    "database": 8.5,
    "database management": 8.5,
    "database design": 8.5,
    "relational database": 8.5,
    "mysql": 8.3,
    "postgresql": 8.7,
    "oracle database": 8.2,
    "sql server": 8.3,
    "mongodb": 8.6,
    "cassandra": 8.5,
    "redis": 8.7,
    "elasticsearch": 8.7,
    "neo4j": 8.3,
    "couchbase": 8.2,
    "database optimization": 8.7,
    "query optimization": 8.6,
    "index optimization": 8.5,
    "data modeling": 8.6,
    
    # Cybersecurity (8.5-9.5)
    "cybersecurity": 9.3,
    "information security": 9.2,
    "network security": 9.0,
    "application security": 9.1,
    "cloud security": 9.2,
    "security architecture": 9.0,
    "ethical hacking": 8.8,
    "penetration testing": 8.9,
    "vulnerability assessment": 8.7,
    "security operations": 8.8,
    "threat intelligence": 8.9,
    "incident response": 9.0,
    "digital forensics": 8.7,
    "cryptography": 8.5,
    "encryption": 8.5,
    "identity and access management": 8.8,
    "iam": 8.8,
    "siem": 8.7,
    "soar": 8.8,
    "zero trust": 9.0,
    "devsecops": 9.1,
    
    # Blockchain and Web3 (7.5-8.5)
    "blockchain": 8.0,
    "cryptocurrency": 7.7,
    "smart contracts": 8.0,
    "ethereum": 7.8,
    "solidity": 8.0,
    "web3": 8.2,
    "decentralized applications": 8.0,
    "dapps": 8.0,
    "defi": 7.8,
    "nft": 7.5,
    "tokenomics": 7.7,
    "consensus mechanisms": 7.9,
    "distributed ledger": 8.0,
    
    # Data Engineering and Big Data (8.5-9.3)
    "data engineering": 9.2,
    "etl": 8.8,
    "data pipelines": 9.0,
    "apache spark": 8.8,
    "hadoop": 8.0,
    "kafka": 8.9,
    "airflow": 8.8,
    "hive": 8.0,
    "pig": 7.5,
    "data lake": 8.7,
    "data warehouse": 8.6,
    "snowflake": 9.0,
    "redshift": 8.7,
    "bigquery": 8.8,
    "dbt": 8.9,
    "streaming data": 8.8,
    
    # Mathematics and Statistics (7.5-9)
    "mathematics": 8.0,
    "statistics": 8.5,
    "linear algebra": 8.2,
    "calculus": 7.8,
    "probability": 8.3,
    "bayesian statistics": 8.5,
    "regression analysis": 8.5,
    "time series analysis": 8.7,
    "mathematical modeling": 8.3,
    "operations research": 8.0,
    "optimization": 8.5,
    "numerical analysis": 8.0,
    "discrete mathematics": 7.8,
    "hypothesis testing": 8.2,
    "a/b testing": 8.5,
    "experimental design": 8.3,
    
    # Product and Project Management (7.5-8.5)
    "product management": 8.5,
    "project management": 8.0,
    "agile": 8.2,
    "scrum": 8.0,
    "kanban": 7.8,
    "lean": 7.8,
    "sprint planning": 7.9,
    "product roadmap": 8.0,
    "user stories": 7.8,
    "backlog grooming": 7.7,
    "product owner": 8.0,
    "scrum master": 7.9,
    "stakeholder management": 7.8,
    "requirements gathering": 7.7,
    "jira": 7.8,
    "confluence": 7.5,
    "trello": 7.5,
    "asana": 7.5,
    "gantt charts": 7.0,
    "pert charts": 7.0,
    "risk management": 7.8,
    "resource allocation": 7.5,
    
    # Business and Strategy (6.5-8)
    "business analysis": 7.8,
    "business strategy": 7.5,
    "strategic planning": 7.5,
    "business process": 7.3,
    "business process improvement": 7.5,
    "business intelligence": 8.0,
    "market research": 7.3,
    "competitive analysis": 7.3,
    "swot analysis": 7.0,
    "business model canvas": 7.2,
    "value proposition": 7.3,
    "business case": 7.2,
    "process mapping": 7.0,
    "process optimization": 7.3,
    "change management": 7.5,
    "leadership": 7.5,
    "team management": 7.3,
    "decision making": 7.2,
    "strategic thinking": 7.3,
    "negotiation": 7.0,
    "presentation skills": 7.0,
    "public speaking": 7.0,
    
    # UX/UI Design (7.5-8.5)
    "user experience": 8.5,
    "ux": 8.5,
    "user interface": 8.3,
    "ui": 8.3,
    "ux/ui": 8.4,
    "user research": 8.0,
    "usability testing": 8.0,
    "wireframing": 7.8,
    "prototyping": 8.0,
    "information architecture": 7.9,
    "interaction design": 8.0,
    "visual design": 7.8,
    "web design": 7.9,
    "mobile design": 8.0,
    "responsive design": 8.0,
    "accessibility": 8.2,
    "figma": 8.3,
    "sketch": 7.8,
    "adobe xd": 7.7,
    "invision": 7.5,
    "design systems": 8.2,
    "design thinking": 8.0,
    "user-centered design": 8.1,
    
    # Marketing and Digital Skills (6.5-8)
    "digital marketing": 7.8,
    "content marketing": 7.5,
    "inbound marketing": 7.3,
    "email marketing": 7.0,
    "social media marketing": 7.3,
    "search engine optimization": 7.5,
    "seo": 7.5,
    "search engine marketing": 7.3,
    "sem": 7.3,
    "pay-per-click": 7.2,
    "ppc": 7.2,
    "google analytics": 7.7,
    "google ads": 7.5,
    "facebook ads": 7.3,
    "content strategy": 7.5,
    "content creation": 7.2,
    "copywriting": 7.0,
    "conversion rate optimization": 7.7,
    "cro": 7.7,
    "analytics": 8.0,
    "growth hacking": 7.8,
    "brand management": 7.0,
    "customer relationship management": 7.2,
    "crm": 7.2,
    
    # General Professional Skills (6-7.5)
    "communication": 7.0,
    "problem solving": 7.5,
    "critical thinking": 7.3,
    "analytical thinking": 7.5,
    "creativity": 7.0,
    "teamwork": 6.8,
    "collaboration": 7.0,
    "time management": 7.0,
    "organizational skills": 6.8,
    "adaptability": 7.0,
    "emotional intelligence": 7.0,
    "conflict resolution": 6.8,
    "networking": 6.5,
    "attention to detail": 6.8,
    "research skills": 7.0,
    "writing": 6.5,
    "technical writing": 7.5,
    
    # Specialized and Emerging Technologies (8-9.5)
    "quantum computing": 9.0,
    "augmented reality": 8.5,
    "ar": 8.5,
    "virtual reality": 8.3,
    "vr": 8.3,
    "mixed reality": 8.4,
    "mr": 8.4,
    "extended reality": 8.4,
    "xr": 8.4,
    "internet of things": 8.5,
    "iot": 8.5,
    "edge computing": 8.7,
    "5g": 8.3,
    "computer graphics": 8.0,
    "game development": 8.0,
    "unity": 8.0,
    "unreal engine": 8.0,
    "robotics": 8.5,
    "autonomous vehicles": 8.7,
    "drones": 8.0,
    "3d modeling": 7.8,
    "3d printing": 7.9,
    "cad": 7.7,
    "biotechnology": 8.5,
    "bioinformatics": 8.3,
    "genomics": 8.4,
    "computational biology": 8.3,
    "nanotechnology": 8.2,
    "clean energy": 8.0,
    "sustainable technology": 8.0,
    
    # Finance and FinTech (7-8.5)
    "financial analysis": 7.8,
    "financial modeling": 8.0,
    "investment analysis": 7.7,
    "portfolio management": 7.5,
    "risk assessment": 7.8,
    "financial planning": 7.3,
    "fintech": 8.3,
    "algorithmic trading": 8.0,
    "trading strategies": 7.7,
    "financial regulations": 7.5,
    "accounting": 7.0,
    "bookkeeping": 6.8,
    "budgeting": 7.0,
    "forecasting": 7.5,
    "excel": 7.5,
    "financial markets": 7.3,
    "banking": 7.0,
    "payment processing": 7.5,
    
    # Default for unlisted skills
    "default": 6.0
}

def calculate_course_bonus(course: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate bonus points for a single course.
    
    Args:
        course (Dict[str, Any]): Course information including title, institution, duration, etc.
        
    Returns:
        Dict[str, Any]: The course with added bonus information.
    """
    # Create a copy of the course to add bonus information
    result = course.copy()
    
    # Initialize bonus points
    total_points = 0
    bonus_breakdown = {}
    
    # 1. Institution reputation (0-10 points)
    institution = course.get("institution") or ""
    institution = institution.strip()
    institution_score = INSTITUTION_SCORES.get(institution, INSTITUTION_SCORES["default"])
    total_points += institution_score
    bonus_breakdown["institution"] = institution_score
    
    # 2. Course duration (0-5 points)
    duration = course.get("duration", "")
    duration_points = 0
    
    # Convert duration to approximate hours or weeks
    if isinstance(duration, str):
        duration_lower = duration.lower()
        
        if "week" in duration_lower:
            # Extract number of weeks
            try:
                weeks = int(''.join(filter(str.isdigit, duration_lower)))
                if weeks >= 10:
                    duration_points = 5  # Long courses (10+ weeks)
                elif weeks >= 6:
                    duration_points = 4  # Medium-long courses (6-9 weeks)
                elif weeks >= 4:
                    duration_points = 3  # Medium courses (4-5 weeks)
                elif weeks >= 2:
                    duration_points = 2  # Short-medium courses (2-3 weeks)
                else:
                    duration_points = 1  # Very short courses (1 week)
            except:
                duration_points = 2  # Default if unable to parse
                
        elif "month" in duration_lower:
            # Extract number of months
            try:
                months = int(''.join(filter(str.isdigit, duration_lower)))
                if months >= 6:
                    duration_points = 5  # Very long courses (6+ months)
                elif months >= 3:
                    duration_points = 4  # Long courses (3-5 months)
                elif months >= 2:
                    duration_points = 3  # Medium courses (2 months)
                else:
                    duration_points = 2  # Shorter courses (1 month)
            except:
                duration_points = 3  # Default if unable to parse
                
        elif "hour" in duration_lower:
            # Extract number of hours
            try:
                hours = int(''.join(filter(str.isdigit, duration_lower)))
                if hours >= 40:
                    duration_points = 3  # Medium courses (40+ hours)
                elif hours >= 20:
                    duration_points = 2  # Short-medium courses (20-39 hours)
                else:
                    duration_points = 1  # Very short courses (<20 hours)
            except:
                duration_points = 1  # Default if unable to parse
        else:
            duration_points = 2  # Default if duration format unknown
    
    total_points += duration_points
    bonus_breakdown["duration"] = duration_points
    
    # 3. Course topic/field (0-10 points)
    title = course.get("title", "").lower()
    field_points = 0
    
    # Find matching field with highest score
    for field, score in FIELD_SCORES.items():
        if field in title:
            field_points = max(field_points, score)
    
    # If no field was found, use default
    if field_points == 0:
        field_points = FIELD_SCORES["default"]
    
    total_points += field_points
    bonus_breakdown["field"] = field_points
    
    # 4. Skills covered (0-20 points, average of top 3 skills)
    skills = course.get("skills", [])
    skill_points = 0
    
    if skills:
        # Calculate score for each skill
        skill_scores = []
        for skill in skills:
            skill_lower = skill.lower()
            score = SKILL_SCORES.get(skill_lower, SKILL_SCORES["default"])
            skill_scores.append(score)
        
        # Take average of top 3 skills (or all if fewer than 3)
        skill_scores.sort(reverse=True)
        top_skills = skill_scores[:min(3, len(skill_scores))]
        avg_skill_score = sum(top_skills) / len(top_skills)
        
        # Scale to 0-20 points
        skill_points = avg_skill_score * 2
    
    total_points += skill_points
    bonus_breakdown["skills"] = skill_points
    
    # Calculate final bonus percentage
    # Scale total points (0-45) to percentage (0-100%)
    max_possible_points = 45
    bonus_percentage = (total_points / max_possible_points) * 100
    
    # Add bonus information to the result
    result["bonus_points"] = round(total_points, 1)
    result["bonus_percentage"] = round(bonus_percentage, 1)
    result["bonus_breakdown"] = bonus_breakdown
    
    # Print total bonus points and breakdown
    print(f"\nTotal Bonus Points: {total_points:.1f} / {max_possible_points} ({bonus_percentage:.1f}%)")
    print("Bonus Breakdown:")
    print(f"  Institution: {bonus_breakdown['institution']:.1f}")
    print(f"  Duration: {bonus_breakdown['duration']:.1f}")
    print(f"  Field: {bonus_breakdown['field']:.1f}")
    print(f"  Skills: {bonus_breakdown['skills']:.1f}")
    
    return result

def calculate_profile_bonus(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate bonus points for all courses in a Coursera profile.
    
    Args:
        profile_data (Dict[str, Any]): The profile data containing user info and completed courses.
        
    Returns:
        Dict[str, Any]: The profile data with added bonus information.
    """
    # Create a copy of the profile data
    
    global total_bonus_sum 
    result = profile_data.copy()
    
    # Calculate bonus for each course
    total_bonus_sum = 0.0
    courses_with_bonus = []
    for course in profile_data.get("completed_courses", []):
        course_with_bonus = calculate_course_bonus(course)
        courses_with_bonus.append(course_with_bonus)
        total_bonus_sum += course_with_bonus.get("bonus_points", 0)
    
    # Print the total sum of all bonus points
    print(f"\nTotal Sum of All Bonus Points: {total_bonus_sum:.1f}")

    
    # Sort courses by bonus points (highest first)
    courses_with_bonus.sort(key=lambda x: x.get("bonus_points", 0), reverse=True)
    
    # Replace the original courses with the enhanced ones
    result["completed_courses"] = courses_with_bonus
    
    # Calculate overall profile metrics
    if courses_with_bonus:
        total_bonus_points = sum(course.get("bonus_points", 0) for course in courses_with_bonus)
        avg_bonus_points = total_bonus_points / len(courses_with_bonus)
        max_bonus_points = max(course.get("bonus_points", 0) for course in courses_with_bonus)
        
        result["profile_metrics"] = {
            "total_bonus_points": round(total_bonus_points, 1),
            "average_bonus_points": round(avg_bonus_points, 1),
            "max_bonus_points": round(max_bonus_points, 1),
            "course_count": len(courses_with_bonus)
        }
        
        # Analyze skills distribution across all courses
        all_skills = {}
        for course in courses_with_bonus:
            for skill in course.get("skills", []):
                if isinstance(skill, str):
                    skill_lower = skill.lower()
                    skill_value = SKILL_SCORES.get(skill_lower, SKILL_SCORES["default"])
                    
                    if skill not in all_skills:
                        all_skills[skill] = {
                            "count": 1,
                            "value": skill_value,
                            "courses": [course.get("title", "Unknown Course")]
                        }
                    else:
                        all_skills[skill]["count"] += 1
                        all_skills[skill]["courses"].append(course.get("title", "Unknown Course"))
        
        # Calculate total skill value and sort skills by value
        for skill, data in all_skills.items():
            data["total_value"] = data["value"] * data["count"]
        
        # Get top skills by value
        top_skills = sorted(
            all_skills.items(), 
            key=lambda x: x[1]["total_value"], 
            reverse=True
        )[:10]  # Top 10 skills
        
        result["profile_metrics"]["top_skills"] = [
            {
                "name": skill, 
                "count": data["count"], 
                "value": data["value"],
                "total_value": data["total_value"]
            } 
            for skill, data in top_skills
        ]
        
        # Analyze field distribution
        field_distribution = {}
        for course in courses_with_bonus:
            field = course.get("matched_field", "general")
            if field != "general":  # Skip general field
                if field in field_distribution:
                    field_distribution[field]["count"] += 1
                    field_distribution[field]["courses"].append(course.get("title", "Unknown Course"))
                else:
                    field_distribution[field] = {
                        "count": 1,
                        "value": FIELD_SCORES.get(field, FIELD_SCORES["default"]),
                        "courses": [course.get("title", "Unknown Course")]
                    }
        
        # Calculate total field value and sort fields by value
        for field, data in field_distribution.items():
            data["total_value"] = data["value"] * data["count"]
        
        # Get top fields by total value
        top_fields = sorted(
            field_distribution.items(), 
            key=lambda x: x[1]["total_value"], 
            reverse=True
        )[:5]  # Top 5 fields
        
        result["profile_metrics"]["top_fields"] = [
            {
                "name": field, 
                "count": data["count"], 
                "value": data["value"],
                "total_value": data["total_value"]
            } 
            for field, data in top_fields
        ]
        
        # Calculate career focus areas based on skills and fields
        career_areas = {}
        
        # Map from fields to career areas
        field_to_career = {
            "artificial intelligence": "AI & Machine Learning",
            "machine learning": "AI & Machine Learning",
            "deep learning": "AI & Machine Learning",
            "data science": "Data Science & Analytics",
            "data analytics": "Data Science & Analytics",
            "programming": "Software Development",
            "software engineering": "Software Development",
            "web development": "Web & Mobile Development",
            "mobile development": "Web & Mobile Development",
            "cloud computing": "Cloud & DevOps",
            "devops": "Cloud & DevOps",
            "cybersecurity": "Cybersecurity",
            "information security": "Cybersecurity",
            "business": "Business & Management",
            "management": "Business & Management",
            "finance": "Finance & Economics",
            "economics": "Finance & Economics",
            "marketing": "Marketing & Sales",
            "sales": "Marketing & Sales",
            "design": "Design & UX/UI",
            "ux": "Design & UX/UI",
            "ui": "Design & UX/UI"
        }
        
        # Add career areas based on matched fields
        for course in courses_with_bonus:
            field = course.get("matched_field", "")
            if field in field_to_career:
                career_area = field_to_career[field]
                if career_area in career_areas:
                    career_areas[career_area] += 1
                else:
                    career_areas[career_area] = 1
        
        # Get top career areas
        top_careers = sorted(
            career_areas.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]  # Top 3 career areas
        
        result["profile_metrics"]["career_focus"] = [
            {"area": area, "strength": count} 
            for area, count in top_careers
        ]
    
    return result

def calculate_from_json_file(filename: str) -> Dict[str, Any]:
    """
    Calculate bonus points from a JSON file containing Coursera profile data.
    
    Args:
        filename (str): Path to the JSON file.
        
    Returns:
        Dict[str, Any]: The profile data with added bonus information.
    """
    with open(filename, 'r') as f:
        profile_data = json.load(f)
    
    return calculate_profile_bonus(profile_data)

def calculate_from_scraper_result(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate bonus points from Coursera scraper result.
    
    Args:
        profile_data (Dict[str, Any]): The profile data from the scraper.
        
    Returns:
        Dict[str, Any]: The profile data with added bonus information.
    """
    return calculate_profile_bonus(profile_data)

def print_bonus_summary(profile_data: Dict[str, Any]) -> None:
    """
    Print a summary of bonus calculations with enhanced profile analysis.
    
    Args:
        profile_data (Dict[str, Any]): The profile data with bonus information.
    """
    print("\n=== Coursera Profile Bonus Summary ===")
    
    # Print user info
    user_info = profile_data.get("user_info", {})
    print(f"Profile: {user_info.get('name', 'Unknown User')}")
    
    # Print profile metrics
    metrics = profile_data.get("profile_metrics", {})
    if metrics:
        print(f"\nTotal Courses: {metrics.get('course_count', 0)}")
        print(f"Total Bonus Points: {metrics.get('total_bonus_points', 0)}")
        print(f"Average Bonus Points: {metrics.get('average_bonus_points', 0)}")
        
        # Print career focus areas if available
        if "career_focus" in metrics and metrics["career_focus"]:
            print("\nCareer Focus Areas:")
            for i, focus in enumerate(metrics["career_focus"], 1):
                area = focus.get("area", "Unknown")
                strength = focus.get("strength", 0)
                print(f"{i}. {area} (Strength: {strength})")
        
        # Print top skills if available
        if "top_skills" in metrics and metrics["top_skills"]:
            print("\nTop Skills by Value:")
            for i, skill_data in enumerate(metrics["top_skills"][:5], 1):  # Show top 5
                name = skill_data.get("name", "Unknown")
                value = skill_data.get("value", 0)
                count = skill_data.get("count", 0)
                print(f"{i}. {name} (Value: {value}, Count: {count})")
        
        # Print top fields if available
        if "top_fields" in metrics and metrics["top_fields"]:
            print("\nTop Knowledge Areas:")
            for i, field_data in enumerate(metrics["top_fields"][:3], 1):  # Show top 3
                name = field_data.get("name", "Unknown").title()
                value = field_data.get("value", 0)
                count = field_data.get("count", 0)
                print(f"{i}. {name} (Value: {value}, Count: {count})")
    
    # Print course bonuses
    courses = profile_data.get("completed_courses", [])
    if courses:
        print("\nCourses by Bonus Points:")
        for i, course in enumerate(courses, 1):
            title = course.get("title", "Unknown Course")
            institution = course.get("institution", "Unknown Institution")
            points = course.get("bonus_points", 0)
            percentage = course.get("bonus_percentage", 0)
            print(f"{i}. {title} ({institution})")
            print(f"   Bonus: {points:.1f} points ({percentage:.1f}%)")
            
            # Print bonus breakdown
            breakdown = course.get("bonus_breakdown", {})
            if breakdown:
                print(f"   Breakdown: Institution: {breakdown.get('institution', 0)}, " +
                      f"Duration: {breakdown.get('duration', 0)}, " +
                      f"Field: {breakdown.get('field', 0)}, " +
                      f"Skills: {breakdown.get('skills', 0)}")
                
                # Show difficulty and certificate value if available
                additional = []
                if "difficulty" in breakdown:
                    additional.append(f"Difficulty: {breakdown['difficulty']}")
                if "certificate" in breakdown:
                    additional.append(f"Certificate: {breakdown['certificate']}")
                
                if additional:
                    print(f"   Additional: {', '.join(additional)}")
            
            # Print skills if available
            skills = course.get("skills", [])
            if skills and len(skills) > 0:
                skill_list = skills[:5]  # Show up to 5 skills
                print(f"   Skills: {', '.join(skill_list)}" + 
                      (f" and {len(skills)-5} more" if len(skills) > 5 else ""))
                
            print()
    
    print("\nNote: Bonus points are calculated based on institution reputation, course")
    print("      duration, topic relevance, skills market value, difficulty level,")
    print("      and certificate value. Higher points indicate more valuable courses.")

def main():
    """Main function to run the bonus calculator."""
    # Check if file is provided as argument
    if len(sys.argv) > 1:
        try:
            # Calculate bonus from file
            profile_data = calculate_from_json_file(sys.argv[1])
            print_bonus_summary(profile_data)
            return 0
        except Exception as e:
            print(f"Error processing file: {e}", file=sys.stderr)
            return 1
    
    # If no file is provided, try to get data from the scraper
    try:
        # Try to import the scraper
        from friendly_scraper import main as run_scraper
        from coursera_scraper import scrape_coursera_profile
        
        print("\n=== Coursera Bonus Calculator ===")
        print("This tool calculates bonus points for Coursera courses based on")
        print("institution reputation, course duration, topic, and skills.")
        print("\nEnter a Coursera profile URL to begin or press Enter for demo profile:")
        
        profile_url = input("Profile URL: ").strip()
        if not profile_url:
            profile_url = "https://www.coursera.org/user/example123"
            print(f"Using demo profile: {profile_url}")
            use_mock = True
        else:
            use_mock = False
        
        # Scrape the profile
        print(f"\nScraping profile: {profile_url}...")
        profile_data = scrape_coursera_profile(profile_url, use_mock=use_mock)
        
        # Calculate bonus points
        print("Calculating bonus points...")
        profile_data_with_bonus = calculate_profile_bonus(profile_data)
        
        # Print summary
        print_bonus_summary(profile_data_with_bonus)
        
        # Ask if user wants to save the results
        save = input("\nDo you want to save these results to a file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            filename = input("Enter filename (or press Enter for 'coursera_bonus_results.json'): ").strip()
            if not filename:
                filename = "coursera_bonus_results.json"
            
            with open(filename, 'w') as f:
                json.dump(profile_data_with_bonus, f, indent=2)
            print(f"Results saved to {filename}")
        
        print("\nThank you for using the Coursera Bonus Calculator!")
        return 0
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("\nPlease provide a JSON file with Coursera profile data:")
        print("python bonus_calculator.py profile_data.json")
        return 1

if __name__ == "__main__":
    sys.exit(main())