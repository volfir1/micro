#!/usr/bin/env python3
"""
services/breathingVibration/breathing.py - Breathing Pattern Monitoring Service
Handles ONLY breathing sensor data and respiratory analysis
"""

import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BreathingService:
    def __init__(self):
        self.current_data = {
            'rate': 0,
            'rhythm': 'Normal',
            'apneaEvents': 0,
            'timestamp': None,
            'isConnected': False
        }
    
    def update_data(self, data):
        """Update breathing data from sensor"""
        try:
            self.current_data = {
                'rate': data.get('rate', 0),
                'rhythm': data.get('rhythm', 'Normal'),
                'apneaEvents': data.get('apneaEvents', 0),
                'timestamp': datetime.now().isoformat(),
                'isConnected': True
            }
            
            # Store in database
            self._store_in_database(data)
            
            logger.debug(f"🫁 Breathing: {self.current_data['rate']}/min ({self.current_data['rhythm']})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Breathing update failed: {e}")
            self.current_data['isConnected'] = False
            return False
    
    def get_current_data(self):
        """Get current breathing data"""
        data = self.current_data.copy()
        data['lastMeasured'] = data.pop('timestamp', None)
        return data
    
    def _store_in_database(self, data):
        """Store breathing data in database"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO breathing_data (rate, rhythm, apnea_events, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (
                data.get('rate', 0),
                data.get('rhythm', 'Normal'),
                data.get('apneaEvents', 0),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database error: {e}")
    
    def get_recent_data(self, limit=10):
        """Get recent breathing measurements"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT rate, rhythm, apnea_events, timestamp 
                FROM breathing_data 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [{
                'rate': row[0],
                'rhythm': row[1],
                'apneaEvents': row[2],
                'timestamp': row[3]
            } for row in rows]
            
        except Exception as e:
            logger.error(f"Database query error: {e}")
            return []
