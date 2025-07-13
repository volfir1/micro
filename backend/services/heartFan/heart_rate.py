#!/usr/bin/env python3
"""
services/heart_rate_service.py - Heart Rate Monitoring Service
Handles ONLY heart rate sensor data and processing
"""
import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HeartRateService:
    def __init__(self):
        self.current_data = {
            'rate': 0,
            'status': 'Normal',
            'min': 0,
            'max': 0,
            'average': 0,
            'variability': 0,
            'timestamp': None,
            'isConnected': False
        }
    
    def update_heart_rate(self, data):
        """Update heart rate data from sensor"""
        try:
            self.current_data = {
                'rate': data.get('rate', 0),
                'status': self._determine_status(data.get('rate', 0)),
                'min': data.get('min', 0),
                'max': data.get('max', 0),
                'average': data.get('average', 0),
                'variability': data.get('variability', 0),
                'timestamp': datetime.now().isoformat(),
                'isConnected': True
            }
            
            # Store in database
            self._store_in_database(data)
            
            logger.info(f"💓 Heart Rate: {self.current_data['rate']} BPM ({self.current_data['status']})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Heart rate update failed: {e}")
            self.current_data['isConnected'] = False
            return False
    
    def get_heart_rate_data(self):
        """Get current heart rate data"""
        data = self.current_data.copy()
        data['lastUpdated'] = data.pop('timestamp', 'Never')
        return data
    
    def _determine_status(self, rate):
        """Determine heart rate status based on BPM"""
        if rate == 0:
            return 'No Signal'
        elif rate < 60:
            return 'Low'
        elif rate > 100:
            return 'High'
        else:
            return 'Normal'
    
    def _store_in_database(self, data):
        """Store heart rate data in database"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO heart_rate (rate, status, min_rate, max_rate, average_rate, variability)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data.get('rate', 0),
                self.current_data['status'],
                data.get('min', 0),
                data.get('max', 0),
                data.get('average', 0),
                data.get('variability', 0)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Heart rate database error: {e}")
    
    def get_heart_rate_history(self, hours=24):
        """Get heart rate history for specified hours"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT rate, status, timestamp 
                FROM heart_rate 
                WHERE timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp DESC
                LIMIT 100
            '''.format(hours))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'rate': row[0],
                    'status': row[1],
                    'timestamp': row[2]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"❌ Heart rate history error: {e}")
            return []
    
    def check_heart_rate_alerts(self):
        """Check if heart rate needs alerts"""
        rate = self.current_data['rate']
        alerts = []
        
        if rate > 120:
            alerts.append({
                'type': 'high_heart_rate',
                'message': f'High heart rate detected: {rate} BPM',
                'severity': 'warning'
            })
        elif rate < 50 and rate > 0:
            alerts.append({
                'type': 'low_heart_rate', 
                'message': f'Low heart rate detected: {rate} BPM',
                'severity': 'warning'
            })
        elif rate == 0:
            alerts.append({
                'type': 'no_signal',
                'message': 'Heart rate sensor not connected',
                'severity': 'error'
            })
        
        return alerts
    
    def get_heart_rate_stats(self):
        """Get heart rate statistics"""
        return {
            'current': self.current_data,
            'connected': self.current_data['isConnected'],
            'last_update': self.current_data['timestamp'],
            'alerts': self.check_heart_rate_alerts()
        }
    
    # Consistent interface methods
    def update_data(self, data):
        """Update heart rate data - consistent interface"""
        return self.update_heart_rate(data)
    
    def get_data(self):
        """Get heart rate data - consistent interface"""
        return self.get_heart_rate_data()
    
    def init_database(self):
        """Initialize database - consistent interface"""
        # Database initialization is handled in _store_in_database
        pass
    
    def get_sleep_history(self):
        """Get sleep history - placeholder for consistent interface"""
        return []

__all__ = [
    'HeartRateService',
]
