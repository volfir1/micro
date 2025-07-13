#!/usr/bin/env python3
"""
database/db_manager.py - Database Management Service
Handles SQLite database initialization and management
"""

import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

def init_database(db_name='sensor_data.db'):
    """Initialize SQLite database with all required tables"""
    try:
        # Create database directory if it doesn't exist
        os.makedirs('database', exist_ok=True)
        db_path = os.path.join('database', db_name)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create heart rate data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heart_rate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate INTEGER NOT NULL,
                status TEXT DEFAULT 'Normal',
                min_rate INTEGER DEFAULT 0,
                max_rate INTEGER DEFAULT 0,
                average_rate REAL DEFAULT 0,
                variability REAL DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create breathing data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS breathing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate INTEGER NOT NULL,
                rhythm TEXT DEFAULT 'Normal',
                apnea_events INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create gyroscope/posture data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gyroscope (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pitch REAL NOT NULL,
                roll REAL NOT NULL,
                neck_angle REAL DEFAULT 0,
                position TEXT DEFAULT 'Back',
                posture_severity TEXT DEFAULT 'Good',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create weight data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight REAL NOT NULL,
                is_in_bed BOOLEAN DEFAULT FALSE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create snore detection data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snore_detection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                is_detected BOOLEAN NOT NULL,
                frequency REAL DEFAULT 0,
                duration_minutes INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create sleep sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sleep_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                duration_minutes INTEGER DEFAULT 0,
                sleep_score INTEGER DEFAULT 0,
                total_snore_events INTEGER DEFAULT 0,
                avg_heart_rate REAL DEFAULT 0,
                status TEXT DEFAULT 'Active',
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create device control logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_type TEXT NOT NULL,
                action TEXT NOT NULL,
                parameters JSON,
                status TEXT DEFAULT 'success',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create LED control logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS led_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command_type TEXT NOT NULL,
                color TEXT,
                brightness INTEGER,
                enabled BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create system events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                description TEXT,
                severity TEXT DEFAULT 'info',
                data JSON,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_heart_rate_timestamp ON heart_rate(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_breathing_timestamp ON breathing(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_gyroscope_timestamp ON gyroscope(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_weight_timestamp ON weight(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_snore_timestamp ON snore_detection(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sleep_sessions_start ON sleep_sessions(start_time)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_device_logs_timestamp ON device_logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_led_logs_timestamp ON led_logs(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_system_events_timestamp ON system_events(timestamp)')
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Database initialized successfully: {db_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        return False

def get_database_info(db_name='sensor_data.db'):
    """Get database information and statistics"""
    try:
        db_path = os.path.join('database', db_name)
        
        if not os.path.exists(db_path):
            return {'error': 'Database file not found'}
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get row counts for each table
        table_stats = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_stats[table] = count
        
        # Get database file size
        file_size = os.path.getsize(db_path)
        
        conn.close()
        
        return {
            'database_path': db_path,
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'total_tables': len(tables),
            'tables': tables,
            'table_stats': table_stats,
            'total_records': sum(table_stats.values())
        }
        
    except Exception as e:
        logger.error(f"❌ Database info error: {e}")
        return {'error': str(e)}

def cleanup_old_data(days_to_keep=30, db_name='sensor_data.db'):
    """Clean up old data from database (keep only recent data)"""
    try:
        db_path = os.path.join('database', db_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete old records from each table
        tables_to_clean = [
            'heart_rate', 'breathing', 'gyroscope', 
            'weight', 'snore_detection', 'device_logs', 
            'led_logs', 'system_events'
        ]
        
        deleted_counts = {}
        
        for table in tables_to_clean:
            cursor.execute(f'''
                DELETE FROM {table} 
                WHERE timestamp < datetime('now', '-{days_to_keep} days')
            ''')
            deleted_counts[table] = cursor.rowcount
        
        # Keep sleep sessions for longer (90 days)
        cursor.execute('''
            DELETE FROM sleep_sessions 
            WHERE timestamp < datetime('now', '-90 days')
        ''')
        deleted_counts['sleep_sessions'] = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        total_deleted = sum(deleted_counts.values())
        logger.info(f"🧹 Database cleanup completed: {total_deleted} old records deleted")
        
        return {
            'success': True,
            'days_kept': days_to_keep,
            'deleted_counts': deleted_counts,
            'total_deleted': total_deleted
        }
        
    except Exception as e:
        logger.error(f"❌ Database cleanup failed: {e}")
        return {'success': False, 'error': str(e)}

def backup_database(db_name='sensor_data.db'):
    """Create a backup of the database"""
    try:
        import shutil
        from datetime import datetime
        
        db_path = os.path.join('database', db_name)
        
        if not os.path.exists(db_path):
            return {'success': False, 'error': 'Database file not found'}
        
        # Create backup directory
        backup_dir = os.path.join('database', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"sensor_data_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        backup_size = os.path.getsize(backup_path)
        
        logger.info(f"💾 Database backup created: {backup_path}")
        
        return {
            'success': True,
            'backup_path': backup_path,
            'backup_size_mb': round(backup_size / (1024 * 1024), 2),
            'timestamp': timestamp
        }
        
    except Exception as e:
        logger.error(f"❌ Database backup failed: {e}")
        return {'success': False, 'error': str(e)}