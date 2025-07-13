#!/usr/bin/env python3
"""
Database initialization for all services
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_all_databases():
    """Initialize all database tables for the services"""
    try:
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        
        # Heart rate table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heart_rate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate INTEGER,
                status TEXT,
                min_rate INTEGER,
                max_rate INTEGER,
                average_rate REAL,
                variability REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Breathing table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS breathing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate INTEGER,
                rhythm TEXT,
                apnea_events INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Gyroscope table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gyroscope (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pitch REAL,
                roll REAL,
                neck_angle REAL,
                position TEXT,
                posture_severity TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Weight table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weight (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight REAL,
                is_in_bed BOOLEAN DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Snore detection table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snore_detection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                is_detected BOOLEAN,
                frequency REAL,
                duration_minutes INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sleep sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sleep_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time DATETIME,
                end_time DATETIME,
                duration_minutes INTEGER,
                sleep_score INTEGER,
                total_snore_events INTEGER,
                avg_heart_rate REAL,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ All database tables initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise e
