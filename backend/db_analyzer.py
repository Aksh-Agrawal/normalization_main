#!/usr/bin/env python3
"""
Database Analysis and Migration Script
"""
import sqlite3
import os
from datetime import datetime

def analyze_current_database():
    """Analyze the current database structure"""
    db_path = "users.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file does not exist")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("📊 Current Database Structure:")
    print("="*40)
    
    for table in tables:
        table_name = table[0]
        print(f"\n🗂️  Table: {table_name}")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print("   Columns:")
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            is_null = "NULL" if col[3] == 0 else "NOT NULL"
            default_val = f" DEFAULT {col[4]}" if col[4] else ""
            primary_key = " PRIMARY KEY" if col[5] == 1 else ""
            print(f"     - {col_name}: {col_type} {is_null}{default_val}{primary_key}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   Records: {count}")
    
    conn.close()

if __name__ == "__main__":
    analyze_current_database()
