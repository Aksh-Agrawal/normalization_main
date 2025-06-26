#!/usr/bin/env python3
"""
Database Management Utility
Provides tools for database maintenance, migration, and analytics
"""
import sqlite3
import json
import os
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import argparse

class DatabaseManager:
    """Comprehensive database management utility"""
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
    
    def backup_database(self, backup_dir: str = "backups") -> str:
        """Create a backup of the database"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database {self.db_path} does not exist")
        
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"users_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database
        shutil.copy2(self.db_path, backup_path)
        
        # Verify backup
        if os.path.exists(backup_path):
            size = os.path.getsize(backup_path)
            print(f"✅ Database backed up successfully")
            print(f"   📁 Location: {backup_path}")
            print(f"   📏 Size: {size:,} bytes")
            return backup_path
        else:
            raise Exception("Failed to create backup")
    
    def migrate_to_enhanced_schema(self) -> bool:
        """Migrate existing database to enhanced schema"""
        print("🔄 Starting database migration to enhanced schema...")
        
        # Create backup first
        backup_path = self.backup_database()
        print(f"📁 Backup created: {backup_path}")
        
        try:
            # Initialize enhanced database
            from enhanced_db_model import EnhancedUserModel
            enhanced_db = EnhancedUserModel(self.db_path)
            print("✅ Migration completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            # Restore from backup
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_path)
                print("🔄 Database restored from backup")
            return False
    
    def analyze_database(self) -> Dict:
        """Comprehensive database analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        analysis = {
            'metadata': {},
            'tables': {},
            'statistics': {},
            'health': {}
        }
        
        # Database metadata
        cursor.execute("PRAGMA database_list")
        db_info = cursor.fetchall()
        analysis['metadata']['database_info'] = db_info
        
        cursor.execute("PRAGMA user_version")
        analysis['metadata']['user_version'] = cursor.fetchone()[0]
        
        # Get file size
        if os.path.exists(self.db_path):
            analysis['metadata']['file_size'] = os.path.getsize(self.db_path)
        
        # Table analysis
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            if table.startswith('sqlite_'):
                continue
                
            table_info = {}
            
            # Row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            table_info['row_count'] = cursor.fetchone()[0]
            
            # Schema info
            cursor.execute(f"PRAGMA table_info({table})")
            table_info['columns'] = cursor.fetchall()
            
            # Index info
            cursor.execute(f"PRAGMA index_list({table})")
            table_info['indexes'] = cursor.fetchall()
            
            analysis['tables'][table] = table_info
        
        # User statistics
        try:
            # Check which schema is being used
            if 'users_new' in tables:
                cursor.execute("SELECT COUNT(*) FROM users_new WHERE is_active = 1")
                analysis['statistics']['active_users'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM user_platforms_new")
                analysis['statistics']['platform_connections'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM user_courses_new")
                analysis['statistics']['courses_tracked'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT AVG(total_unified_score) FROM users_new WHERE total_unified_score > 0")
                avg_score = cursor.fetchone()[0]
                analysis['statistics']['average_score'] = avg_score or 0
                
            elif 'users' in tables:
                cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
                analysis['statistics']['active_users'] = cursor.fetchone()[0]
                
                if 'user_platforms' in tables:
                    cursor.execute("SELECT COUNT(*) FROM user_platforms")
                    analysis['statistics']['platform_connections'] = cursor.fetchone()[0]
                
                if 'user_courses' in tables:
                    cursor.execute("SELECT COUNT(*) FROM user_courses")
                    analysis['statistics']['courses_tracked'] = cursor.fetchone()[0]
        
        except Exception as e:
            analysis['statistics']['error'] = str(e)
        
        # Database health checks
        try:
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()[0]
            analysis['health']['integrity'] = integrity_result == 'ok'
            
            cursor.execute("PRAGMA foreign_key_check")
            fk_violations = cursor.fetchall()
            analysis['health']['foreign_key_violations'] = len(fk_violations)
            
            # Check for orphaned records
            orphaned_checks = []
            if 'user_platforms_new' in tables and 'users_new' in tables:
                cursor.execute('''
                    SELECT COUNT(*) FROM user_platforms_new up 
                    LEFT JOIN users_new u ON up.user_id = u.id 
                    WHERE u.id IS NULL
                ''')
                orphaned_platforms = cursor.fetchone()[0]
                if orphaned_platforms > 0:
                    orphaned_checks.append(f"Orphaned platform records: {orphaned_platforms}")
            
            analysis['health']['orphaned_records'] = orphaned_checks
            
        except Exception as e:
            analysis['health']['error'] = str(e)
        
        conn.close()
        return analysis
    
    def cleanup_database(self, dry_run: bool = True) -> Dict:
        """Clean up database by removing orphaned records and optimizing"""
        print(f"🧹 Database cleanup {'(DRY RUN)' if dry_run else '(LIVE)'}")
        
        results = {
            'orphaned_removed': 0,
            'duplicate_removed': 0,
            'optimizations': []
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Remove orphaned platform records
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_platforms_new'")
            if cursor.fetchone():
                cursor.execute('''
                    SELECT COUNT(*) FROM user_platforms_new up 
                    LEFT JOIN users_new u ON up.user_id = u.id 
                    WHERE u.id IS NULL
                ''')
                orphaned_platforms = cursor.fetchone()[0]
                
                if orphaned_platforms > 0:
                    if not dry_run:
                        cursor.execute('''
                            DELETE FROM user_platforms_new 
                            WHERE user_id NOT IN (SELECT id FROM users_new)
                        ''')
                    results['orphaned_removed'] += orphaned_platforms
                    print(f"  🗑️  {'Would remove' if dry_run else 'Removed'} {orphaned_platforms} orphaned platform records")
            
            # Remove orphaned course records
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_courses_new'")
            if cursor.fetchone():
                cursor.execute('''
                    SELECT COUNT(*) FROM user_courses_new uc 
                    LEFT JOIN users_new u ON uc.user_id = u.id 
                    WHERE u.id IS NULL
                ''')
                orphaned_courses = cursor.fetchone()[0]
                
                if orphaned_courses > 0:
                    if not dry_run:
                        cursor.execute('''
                            DELETE FROM user_courses_new 
                            WHERE user_id NOT IN (SELECT id FROM users_new)
                        ''')
                    results['orphaned_removed'] += orphaned_courses
                    print(f"  🗑️  {'Would remove' if dry_run else 'Removed'} {orphaned_courses} orphaned course records")
            
            # Remove duplicate courses (same user, course name, institution)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_courses_new'")
            if cursor.fetchone():
                cursor.execute('''
                    SELECT COUNT(*) - COUNT(DISTINCT user_id, course_name, institution_id)
                    FROM user_courses_new
                ''')
                duplicate_courses = cursor.fetchone()[0]
                
                if duplicate_courses > 0:
                    if not dry_run:
                        cursor.execute('''
                            DELETE FROM user_courses_new 
                            WHERE id NOT IN (
                                SELECT MIN(id) 
                                FROM user_courses_new 
                                GROUP BY user_id, course_name, institution_id
                            )
                        ''')
                    results['duplicate_removed'] += duplicate_courses
                    print(f"  🗑️  {'Would remove' if dry_run else 'Removed'} {duplicate_courses} duplicate course records")
            
            # Vacuum database to reclaim space
            if not dry_run:
                print("  🔧 Optimizing database...")
                cursor.execute("VACUUM")
                results['optimizations'].append("Database vacuumed")
                
                cursor.execute("ANALYZE")
                results['optimizations'].append("Statistics updated")
            
            if not dry_run:
                conn.commit()
                print("✅ Database cleanup completed")
            else:
                print("ℹ️  Dry run completed - no changes made")
        
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
            conn.rollback()
        
        finally:
            conn.close()
        
        return results
    
    def export_user_data(self, user_id: int, output_file: str = None) -> str:
        """Export all data for a specific user"""
        if not output_file:
            output_file = f"user_{user_id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        export_data = {
            'export_info': {
                'user_id': user_id,
                'export_date': datetime.now().isoformat(),
                'database_version': None
            },
            'user_profile': {},
            'platforms': [],
            'courses': [],
            'achievements': [],
            'rating_history': []
        }
        
        try:
            # Check database version
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_new'")
            use_new_schema = cursor.fetchone() is not None
            
            if use_new_schema:
                # Export from new schema
                cursor.execute('''
                    SELECT email, username, full_name, total_platform_score, 
                           total_course_bonus, total_unified_score, created_at, last_login
                    FROM users_new WHERE id = ?
                ''', (user_id,))
                
                user_data = cursor.fetchone()
                if user_data:
                    export_data['user_profile'] = {
                        'email': user_data[0],
                        'username': user_data[1],
                        'full_name': user_data[2],
                        'platform_score': user_data[3],
                        'course_bonus': user_data[4],
                        'unified_score': user_data[5],
                        'created_at': user_data[6],
                        'last_login': user_data[7]
                    }
                
                # Export platforms
                cursor.execute('''
                    SELECT p.name, up.handle, up.current_rating, up.max_rating_achieved,
                           up.contests_participated, up.problems_solved, up.last_updated
                    FROM user_platforms_new up
                    JOIN platforms p ON up.platform_id = p.id
                    WHERE up.user_id = ?
                ''', (user_id,))
                
                for row in cursor.fetchall():
                    export_data['platforms'].append({
                        'platform': row[0],
                        'handle': row[1],
                        'current_rating': row[2],
                        'max_rating': row[3],
                        'contests': row[4],
                        'problems': row[5],
                        'last_updated': row[6]
                    })
                
                # Export courses
                cursor.execute('''
                    SELECT uc.course_name, i.name, uc.completion_date, uc.total_bonus,
                           uc.course_url, uc.skills_learned, uc.difficulty_level
                    FROM user_courses_new uc
                    LEFT JOIN institutions i ON uc.institution_id = i.id
                    WHERE uc.user_id = ?
                ''', (user_id,))
                
                for row in cursor.fetchall():
                    skills = json.loads(row[5]) if row[5] else []
                    export_data['courses'].append({
                        'course_name': row[0],
                        'institution': row[1],
                        'completion_date': row[2],
                        'bonus_points': row[3],
                        'course_url': row[4],
                        'skills': skills,
                        'difficulty': row[6]
                    })
                
                # Export achievements
                cursor.execute('''
                    SELECT achievement_type, title, description, points_awarded, achieved_at
                    FROM user_achievements WHERE user_id = ?
                ''', (user_id,))
                
                for row in cursor.fetchall():
                    export_data['achievements'].append({
                        'type': row[0],
                        'title': row[1],
                        'description': row[2],
                        'points': row[3],
                        'date': row[4]
                    })
                
                export_data['export_info']['database_version'] = '2.0 (Enhanced)'
            
            else:
                # Export from old schema
                cursor.execute('''
                    SELECT email, username, created_at, last_login
                    FROM users WHERE id = ?
                ''', (user_id,))
                
                user_data = cursor.fetchone()
                if user_data:
                    export_data['user_profile'] = {
                        'email': user_data[0],
                        'username': user_data[1],
                        'created_at': user_data[2],
                        'last_login': user_data[3]
                    }
                
                # Export platforms (old schema)
                cursor.execute('''
                    SELECT platform_name, handle, rating, max_rating, last_updated
                    FROM user_platforms WHERE user_id = ?
                ''', (user_id,))
                
                for row in cursor.fetchall():
                    export_data['platforms'].append({
                        'platform': row[0],
                        'handle': row[1],
                        'current_rating': row[2],
                        'max_rating': row[3],
                        'last_updated': row[4]
                    })
                
                # Export courses (old schema)
                cursor.execute('''
                    SELECT course_name, institution, completion_date, bonus_points
                    FROM user_courses WHERE user_id = ?
                ''', (user_id,))
                
                for row in cursor.fetchall():
                    export_data['courses'].append({
                        'course_name': row[0],
                        'institution': row[1],
                        'completion_date': row[2],
                        'bonus_points': row[3]
                    })
                
                export_data['export_info']['database_version'] = '1.0 (Legacy)'
        
        except Exception as e:
            export_data['export_error'] = str(e)
        
        finally:
            conn.close()
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ User data exported to: {output_file}")
        return output_file
    
    def generate_analytics_report(self) -> Dict:
        """Generate comprehensive analytics report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'user_metrics': {},
            'platform_metrics': {},
            'course_metrics': {},
            'growth_metrics': {}
        }
        
        try:
            # Check schema
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_new'")
            use_new_schema = cursor.fetchone() is not None
            
            if use_new_schema:
                # User metrics
                cursor.execute("SELECT COUNT(*) FROM users_new WHERE is_active = 1")
                report['user_metrics']['total_active_users'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM users_new WHERE last_login > date('now', '-7 days')")
                report['user_metrics']['weekly_active_users'] = cursor.fetchone()[0]
                
                cursor.execute("SELECT AVG(total_unified_score) FROM users_new WHERE total_unified_score > 0")
                avg_score = cursor.fetchone()[0]
                report['user_metrics']['average_unified_score'] = round(avg_score or 0, 2)
                
                # Platform metrics
                cursor.execute('''
                    SELECT p.display_name, COUNT(*), AVG(up.current_rating), MAX(up.current_rating)
                    FROM user_platforms_new up
                    JOIN platforms p ON up.platform_id = p.id
                    GROUP BY p.id, p.display_name
                    ORDER BY COUNT(*) DESC
                ''')
                
                platform_stats = []
                for row in cursor.fetchall():
                    platform_stats.append({
                        'platform': row[0],
                        'user_count': row[1],
                        'avg_rating': round(row[2] or 0, 1),
                        'max_rating': row[3] or 0
                    })
                report['platform_metrics']['platform_usage'] = platform_stats
                
                # Course metrics
                cursor.execute('''
                    SELECT i.name, COUNT(*), AVG(uc.total_bonus), SUM(uc.total_bonus)
                    FROM user_courses_new uc
                    JOIN institutions i ON uc.institution_id = i.id
                    GROUP BY i.id, i.name
                    ORDER BY COUNT(*) DESC
                    LIMIT 10
                ''')
                
                institution_stats = []
                for row in cursor.fetchall():
                    institution_stats.append({
                        'institution': row[0],
                        'course_count': row[1],
                        'avg_bonus': round(row[2] or 0, 2),
                        'total_bonus': round(row[3] or 0, 2)
                    })
                report['course_metrics']['top_institutions'] = institution_stats
                
                cursor.execute("SELECT AVG(total_bonus) FROM user_courses_new WHERE total_bonus > 0")
                avg_bonus = cursor.fetchone()[0]
                report['course_metrics']['average_course_bonus'] = round(avg_bonus or 0, 2)
                
                # Growth metrics (registrations by month)
                cursor.execute('''
                    SELECT strftime('%Y-%m', created_at) as month, COUNT(*)
                    FROM users_new
                    WHERE created_at > date('now', '-12 months')
                    GROUP BY month
                    ORDER BY month
                ''')
                
                growth_data = []
                for row in cursor.fetchall():
                    growth_data.append({
                        'month': row[0],
                        'new_users': row[1]
                    })
                report['growth_metrics']['monthly_registrations'] = growth_data
        
        except Exception as e:
            report['error'] = str(e)
        
        finally:
            conn.close()
        
        return report

def main():
    """Command line interface for database management"""
    parser = argparse.ArgumentParser(description='Database Management Utility')
    parser.add_argument('--db', default='users.db', help='Database file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--dir', default='backups', help='Backup directory')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Migrate to enhanced schema')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze database')
    analyze_parser.add_argument('--output', help='Output file for analysis report')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up database')
    cleanup_parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export user data')
    export_parser.add_argument('--user-id', type=int, required=True, help='User ID to export')
    export_parser.add_argument('--output', help='Output file')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate analytics report')
    report_parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db_manager = DatabaseManager(args.db)
    
    try:
        if args.command == 'backup':
            backup_path = db_manager.backup_database(args.dir)
            print(f"Backup created: {backup_path}")
        
        elif args.command == 'migrate':
            success = db_manager.migrate_to_enhanced_schema()
            if success:
                print("Migration completed successfully")
            else:
                print("Migration failed")
        
        elif args.command == 'analyze':
            analysis = db_manager.analyze_database()
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(analysis, f, indent=2)
                print(f"Analysis saved to: {args.output}")
            else:
                print(json.dumps(analysis, indent=2))
        
        elif args.command == 'cleanup':
            results = db_manager.cleanup_database(dry_run=args.dry_run)
            print(f"Cleanup results: {results}")
        
        elif args.command == 'export':
            output_file = db_manager.export_user_data(args.user_id, args.output)
            print(f"User data exported to: {output_file}")
        
        elif args.command == 'report':
            report = db_manager.generate_analytics_report()
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"Report saved to: {args.output}")
            else:
                print(json.dumps(report, indent=2))
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
