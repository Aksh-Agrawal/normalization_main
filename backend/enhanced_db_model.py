#!/usr/bin/env python3
"""
Enhanced Database Schema and Migration System
"""
import sqlite3
import bcrypt
import os
import shutil
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple

class EnhancedUserModel:
    """Enhanced User Model with systematic database design"""
    
    def __init__(self, db_path: str = "users.db"):
        """Initialize the enhanced user model"""
        self.db_path = db_path
        self.db_version = "2.0"
        self._backup_and_migrate()
        self._init_enhanced_database()
    
    def _backup_and_migrate(self):
        """Backup existing database and prepare for migration"""
        if os.path.exists(self.db_path):
            backup_path = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(self.db_path, backup_path)
            print(f"📁 Database backed up to: {backup_path}")
    
    def _init_enhanced_database(self):
        """Initialize the enhanced database with proper schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Create database metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS db_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Store database version
        cursor.execute('''
            INSERT OR REPLACE INTO db_metadata (key, value, updated_at)
            VALUES ('version', ?, CURRENT_TIMESTAMP)
        ''', (self.db_version,))
        
        # Enhanced users table with better validation and tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL CHECK (email LIKE '%_@_%._%'),
                password_hash TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                full_name TEXT,
                profile_picture_url TEXT,
                timezone TEXT DEFAULT 'UTC',
                preferred_language TEXT DEFAULT 'en',
                email_verified BOOLEAN DEFAULT 0,
                total_platform_score REAL DEFAULT 0.0,
                total_course_bonus REAL DEFAULT 0.0,
                total_unified_score REAL DEFAULT 0.0,
                rank_position INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                last_active TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                login_count INTEGER DEFAULT 0
            )
        ''')
        
        # Enhanced platforms table with comprehensive tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platforms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                max_rating INTEGER NOT NULL,
                base_url TEXT,
                api_endpoint TEXT,
                difficulty_weight REAL DEFAULT 1.0,
                is_active BOOLEAN DEFAULT 1,
                supports_auto_fetch BOOLEAN DEFAULT 0,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced user_platforms with rating history and statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_platforms_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                platform_id INTEGER NOT NULL,
                handle TEXT NOT NULL,
                current_rating INTEGER,
                max_rating_achieved INTEGER,
                rating_percentile REAL,
                normalized_score REAL,
                contests_participated INTEGER DEFAULT 0,
                problems_solved INTEGER DEFAULT 0,
                last_contest_date DATE,
                verification_status TEXT DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'failed')),
                auto_fetch_enabled BOOLEAN DEFAULT 1,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users_new (id) ON DELETE CASCADE,
                FOREIGN KEY (platform_id) REFERENCES platforms (id),
                UNIQUE(user_id, platform_id)
            )
        ''')
        
        # Rating history for tracking progress over time
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_platform_id INTEGER NOT NULL,
                old_rating INTEGER,
                new_rating INTEGER,
                rating_change INTEGER,
                contest_name TEXT,
                performance_rank INTEGER,
                date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'manual' CHECK (source IN ('manual', 'auto_fetch', 'contest')),
                FOREIGN KEY (user_platform_id) REFERENCES user_platforms_new (id) ON DELETE CASCADE
            )
        ''')
        
        # Enhanced institutions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS institutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                short_name TEXT,
                country TEXT,
                prestige_score REAL DEFAULT 5.0 CHECK (prestige_score >= 1.0 AND prestige_score <= 10.0),
                institution_type TEXT DEFAULT 'university' CHECK (institution_type IN ('university', 'company', 'organization', 'online_platform')),
                website_url TEXT,
                logo_url TEXT,
                is_verified BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced course categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS course_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                parent_category_id INTEGER,
                field_relevance_score REAL DEFAULT 5.0 CHECK (field_relevance_score >= 1.0 AND field_relevance_score <= 10.0),
                market_demand_multiplier REAL DEFAULT 1.0,
                description TEXT,
                FOREIGN KEY (parent_category_id) REFERENCES course_categories (id)
            )
        ''')
        
        # Enhanced user_courses with comprehensive tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_courses_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_name TEXT NOT NULL,
                course_url TEXT,
                institution_id INTEGER,
                category_id INTEGER,
                certificate_url TEXT,
                completion_date DATE,
                start_date DATE,
                duration_weeks INTEGER,
                difficulty_level TEXT DEFAULT 'intermediate' CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
                course_type TEXT DEFAULT 'course' CHECK (course_type IN ('course', 'specialization', 'certificate', 'degree', 'nanodegree')),
                grade_achieved TEXT,
                skills_learned TEXT, -- JSON array of skills
                institution_bonus REAL DEFAULT 0.0,
                duration_bonus REAL DEFAULT 0.0,
                field_bonus REAL DEFAULT 0.0,
                skills_bonus REAL DEFAULT 0.0,
                total_bonus REAL GENERATED ALWAYS AS (institution_bonus + duration_bonus + field_bonus + skills_bonus) STORED,
                verification_status TEXT DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'failed')),
                source_platform TEXT DEFAULT 'coursera',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users_new (id) ON DELETE CASCADE,
                FOREIGN KEY (institution_id) REFERENCES institutions (id),
                FOREIGN KEY (category_id) REFERENCES course_categories (id)
            )
        ''')
        
        # User achievements and milestones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_type TEXT NOT NULL CHECK (achievement_type IN ('rating_milestone', 'course_completion', 'streak', 'rank_achievement', 'platform_mastery')),
                title TEXT NOT NULL,
                description TEXT,
                points_awarded REAL DEFAULT 0.0,
                badge_icon TEXT,
                achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users_new (id) ON DELETE CASCADE
            )
        ''')
        
        # User sessions for analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_end TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                actions_performed INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users_new (id) ON DELETE CASCADE
            )
        ''')
        
        # System analytics and insights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_type TEXT DEFAULT 'counter' CHECK (metric_type IN ('counter', 'gauge', 'histogram')),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT -- JSON data
            )
        ''')
        
        # Create indexes for better performance
        self._create_indexes(cursor)
        
        # Insert default data
        self._insert_default_data(cursor)
        
        # Migrate existing data if needed
        self._migrate_existing_data(cursor)
        
        conn.commit()
        conn.close()
        print("✅ Enhanced database schema created successfully")
    
    def _create_indexes(self, cursor):
        """Create database indexes for better performance"""
        indexes = [
            # Users table indexes
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users_new(email)",
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users_new(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_active ON users_new(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_users_score ON users_new(total_unified_score DESC)",
            
            # User platforms indexes
            "CREATE INDEX IF NOT EXISTS idx_user_platforms_user ON user_platforms_new(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_platforms_platform ON user_platforms_new(platform_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_platforms_handle ON user_platforms_new(handle)",
            "CREATE INDEX IF NOT EXISTS idx_user_platforms_rating ON user_platforms_new(current_rating DESC)",
            
            # User courses indexes
            "CREATE INDEX IF NOT EXISTS idx_user_courses_user ON user_courses_new(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_courses_institution ON user_courses_new(institution_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_courses_category ON user_courses_new(category_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_courses_bonus ON user_courses_new(total_bonus DESC)",
            "CREATE INDEX IF NOT EXISTS idx_user_courses_date ON user_courses_new(completion_date)",
            
            # Rating history indexes
            "CREATE INDEX IF NOT EXISTS idx_rating_history_user_platform ON rating_history(user_platform_id)",
            "CREATE INDEX IF NOT EXISTS idx_rating_history_date ON rating_history(date_recorded)",
            
            # Analytics indexes
            "CREATE INDEX IF NOT EXISTS idx_analytics_metric ON system_analytics(metric_name)",
            "CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON system_analytics(timestamp)",
            
            # Sessions indexes
            "CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_start ON user_sessions(session_start)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        print("📊 Database indexes created")
    
    def _insert_default_data(self, cursor):
        """Insert default platforms, institutions, and categories"""
        # Default platforms
        platforms = [
            ('codeforces', 'CodeForces', 3000, 'https://codeforces.com', 'https://codeforces.com/api', 1.2, 1, 1, 'Competitive programming platform'),
            ('leetcode', 'LeetCode', 2500, 'https://leetcode.com', 'https://leetcode.com/graphql', 1.1, 1, 1, 'Interview preparation platform'),
            ('codechef', 'CodeChef', 1800, 'https://codechef.com', 'https://www.codechef.com/api', 1.0, 1, 1, 'Programming contests platform'),
            ('atcoder', 'AtCoder', 2800, 'https://atcoder.jp', '', 1.15, 1, 0, 'Japanese competitive programming'),
            ('hackerrank', 'HackerRank', 2000, 'https://hackerrank.com', '', 0.9, 1, 0, 'Coding challenges and hiring'),
            ('topcoder', 'TopCoder', 3000, 'https://topcoder.com', '', 1.1, 1, 0, 'Competitive programming and crowdsourcing')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM platforms")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO platforms (name, display_name, max_rating, base_url, api_endpoint, difficulty_weight, is_active, supports_auto_fetch, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', platforms)
        
        # Default institutions
        institutions = [
            ('Stanford University', 'Stanford', 'USA', 10.0, 'university', 'https://stanford.edu', '', 1),
            ('Harvard University', 'Harvard', 'USA', 10.0, 'university', 'https://harvard.edu', '', 1),
            ('Massachusetts Institute of Technology', 'MIT', 'USA', 10.0, 'university', 'https://mit.edu', '', 1),
            ('University of California Berkeley', 'UC Berkeley', 'USA', 9.5, 'university', 'https://berkeley.edu', '', 1),
            ('Carnegie Mellon University', 'CMU', 'USA', 9.5, 'university', 'https://cmu.edu', '', 1),
            ('Google', 'Google', 'USA', 9.0, 'company', 'https://google.com', '', 1),
            ('IBM', 'IBM', 'USA', 8.5, 'company', 'https://ibm.com', '', 1),
            ('Microsoft', 'Microsoft', 'USA', 9.0, 'company', 'https://microsoft.com', '', 1),
            ('Coursera', 'Coursera', 'USA', 7.0, 'online_platform', 'https://coursera.org', '', 1),
            ('edX', 'edX', 'USA', 7.5, 'online_platform', 'https://edx.org', '', 1),
            ('Udacity', 'Udacity', 'USA', 7.0, 'online_platform', 'https://udacity.com', '', 1),
            ('DeepLearning.AI', 'DeepLearning.AI', 'USA', 8.5, 'organization', 'https://deeplearning.ai', '', 1)
        ]
        
        cursor.execute("SELECT COUNT(*) FROM institutions")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO institutions (name, short_name, country, prestige_score, institution_type, website_url, logo_url, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', institutions)
        
        # Default course categories
        categories = [
            ('Computer Science', None, 10.0, 1.5, 'Core computer science subjects'),
            ('Programming', 1, 9.5, 1.4, 'Programming languages and development'),
            ('Data Science', 1, 9.8, 1.6, 'Data analysis, machine learning, and AI'),
            ('Web Development', 2, 8.5, 1.3, 'Frontend and backend web development'),
            ('Mobile Development', 2, 8.0, 1.2, 'iOS and Android development'),
            ('Machine Learning', 3, 10.0, 1.8, 'ML algorithms and applications'),
            ('Artificial Intelligence', 3, 10.0, 1.9, 'AI and deep learning'),
            ('Cloud Computing', 1, 9.0, 1.5, 'AWS, Azure, GCP platforms'),
            ('Cybersecurity', 1, 9.2, 1.4, 'Information security and ethical hacking'),
            ('DevOps', 1, 8.8, 1.3, 'Development operations and automation'),
            ('Business', None, 6.0, 0.8, 'Business and management courses'),
            ('Design', None, 7.0, 0.9, 'UI/UX and graphic design'),
            ('Mathematics', None, 8.0, 1.1, 'Mathematics and statistics'),
            ('Science', None, 7.5, 1.0, 'General science subjects')
        ]
        
        cursor.execute("SELECT COUNT(*) FROM course_categories")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO course_categories (name, parent_category_id, field_relevance_score, market_demand_multiplier, description)
                VALUES (?, ?, ?, ?, ?)
            ''', categories)
        
        print("📋 Default data inserted")
    
    def _migrate_existing_data(self, cursor):
        """Migrate data from old schema to new schema"""
        try:
            # Check if old tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone():
                print("🔄 Migrating existing user data...")
                
                # Migrate users
                cursor.execute('''
                    INSERT OR IGNORE INTO users_new (id, email, password_hash, username, created_at, last_login, is_active)
                    SELECT id, email, password_hash, 
                           COALESCE(username, SUBSTR(email, 1, INSTR(email, '@') - 1)) as username,
                           created_at, last_login, is_active
                    FROM users
                ''')
                
                # Migrate platform data
                cursor.execute('''
                    INSERT OR IGNORE INTO user_platforms_new (user_id, platform_id, handle, current_rating, last_updated)
                    SELECT up.user_id, p.id, up.handle, up.rating, up.last_updated
                    FROM user_platforms up
                    JOIN platforms p ON LOWER(p.name) = LOWER(up.platform_name)
                ''')
                
                # Migrate course data
                cursor.execute('''
                    INSERT OR IGNORE INTO user_courses_new (user_id, course_name, institution_id, completion_date, institution_bonus, total_bonus)
                    SELECT uc.user_id, uc.course_name, 
                           COALESCE(i.id, (SELECT id FROM institutions WHERE name = 'Coursera')), 
                           uc.completion_date, uc.bonus_points, uc.bonus_points
                    FROM user_courses uc
                    LEFT JOIN institutions i ON i.name = uc.institution OR i.short_name = uc.institution
                ''')
                
                print("✅ Data migration completed")
        except Exception as e:
            print(f"⚠️  Migration warning: {e}")
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """Get comprehensive user statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Basic user info
        cursor.execute('''
            SELECT username, email, total_platform_score, total_course_bonus, 
                   total_unified_score, rank_position, created_at, login_count
            FROM users_new WHERE id = ?
        ''', (user_id,))
        
        user_info = cursor.fetchone()
        if not user_info:
            return {}
        
        # Platform statistics
        cursor.execute('''
            SELECT p.display_name, up.handle, up.current_rating, up.max_rating_achieved,
                   up.contests_participated, up.problems_solved, up.rating_percentile
            FROM user_platforms_new up
            JOIN platforms p ON up.platform_id = p.id
            WHERE up.user_id = ?
        ''', (user_id,))
        platforms = cursor.fetchall()
        
        # Course statistics
        cursor.execute('''
            SELECT COUNT(*) as total_courses, SUM(total_bonus) as total_bonus,
                   AVG(total_bonus) as avg_bonus, COUNT(DISTINCT institution_id) as institutions_count
            FROM user_courses_new WHERE user_id = ?
        ''', (user_id,))
        course_stats = cursor.fetchone()
        
        # Recent achievements
        cursor.execute('''
            SELECT achievement_type, title, points_awarded, achieved_at
            FROM user_achievements
            WHERE user_id = ? ORDER BY achieved_at DESC LIMIT 5
        ''', (user_id,))
        achievements = cursor.fetchall()
        
        conn.close()
        
        return {
            'user_info': {
                'username': user_info[0],
                'email': user_info[1],
                'platform_score': user_info[2],
                'course_bonus': user_info[3],
                'unified_score': user_info[4],
                'rank': user_info[5],
                'member_since': user_info[6],
                'login_count': user_info[7]
            },
            'platforms': [{
                'name': p[0], 'handle': p[1], 'rating': p[2], 'max_rating': p[3],
                'contests': p[4], 'problems': p[5], 'percentile': p[6]
            } for p in platforms],
            'courses': {
                'total': course_stats[0] or 0,
                'total_bonus': course_stats[1] or 0,
                'average_bonus': course_stats[2] or 0,
                'institutions': course_stats[3] or 0
            },
            'achievements': [{
                'type': a[0], 'title': a[1], 'points': a[2], 'date': a[3]
            } for a in achievements]
        }
    
    def get_leaderboard(self, limit: int = 50) -> List[Dict]:
        """Get global leaderboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, total_unified_score, total_platform_score, total_course_bonus,
                   rank_position, last_active
            FROM users_new 
            WHERE is_active = 1 AND total_unified_score > 0
            ORDER BY total_unified_score DESC, total_platform_score DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'rank': i + 1,
            'username': row[0],
            'total_score': row[1],
            'platform_score': row[2],
            'course_bonus': row[3],
            'official_rank': row[4],
            'last_active': row[5]
        } for i, row in enumerate(results)]

if __name__ == "__main__":
    print("🚀 Initializing Enhanced Database System...")
    enhanced_db = EnhancedUserModel()
    print("✅ Enhanced database system ready!")
