#!/usr/bin/env python3
"""
services/weight_service.py - Weight Monitoring Service
Handles ONLY weight sensor data and bed occupancy detection
"""

import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class WeightService:
    def __init__(self):
        self.current_data = {
            'weight': 0,
            'is_in_bed': False,
            'pressure_points': [],
            'stability': 'Stable',
            'timestamp': None,
            'isConnected': False
        }
        self.baseline_weight = 0
        self.weight_threshold = 20  # kg threshold for bed occupancy
    
    def update_weight(self, data):
        """Update weight data from sensor"""
        try:
            weight = data.get('weight', 0)
            is_in_bed = weight > self.weight_threshold
            
            self.current_data = {
                'weight': weight,
                'is_in_bed': is_in_bed,
                'pressure_points': data.get('pressure_points', []),
                'stability': self._determine_stability(data.get('movement', 0)),
                'timestamp': datetime.now().isoformat(),
                'isConnected': True
            }
            
            # Store in database
            self._store_in_database(data)
            
            status = "In Bed" if is_in_bed else "Out of Bed"
            logger.info(f"⚖️ Weight: {weight:.1f}kg ({status}, {self.current_data['stability']})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Weight update failed: {e}")
            self.current_data['isConnected'] = False
            return False
    
    def get_weight_data(self):
        """Get current weight data"""
        data = self.current_data.copy()
        data['lastMeasured'] = data.pop('timestamp', 'Never')
        return data
    
    def _determine_stability(self, movement):
        """Determine bed stability based on movement"""
        if movement == 0:
            return 'Stable'
        elif movement < 5:
            return 'Minor Movement'
        elif movement < 15:
            return 'Restless'
        else:
            return 'Very Restless'
    
    def _store_in_database(self, data):
        """Store weight data in database"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO weight (weight, is_in_bed)
                VALUES (?, ?)
            ''', (
                data.get('weight', 0),
                self.current_data['is_in_bed']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Weight database error: {e}")
    
    def get_weight_history(self, hours=24):
        """Get weight history for specified hours"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT weight, is_in_bed, timestamp 
                FROM weight 
                WHERE timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp DESC
                LIMIT 100
            '''.format(hours))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'weight': row[0],
                    'is_in_bed': row[1],
                    'timestamp': row[2]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"❌ Weight history error: {e}")
            return []
    
    def check_weight_alerts(self):
        """Check if weight needs alerts"""
        weight = self.current_data['weight']
        stability = self.current_data['stability']
        alerts = []
        
        if weight == 0:
            alerts.append({
                'type': 'no_signal',
                'message': 'Weight sensor not connected',
                'severity': 'error'
            })
        elif stability == 'Very Restless':
            alerts.append({
                'type': 'restless_sleep',
                'message': 'Very restless sleep detected',
                'severity': 'warning'
            })
        elif not self.current_data['is_in_bed'] and weight > 0:
            alerts.append({
                'type': 'out_of_bed',
                'message': 'User has left the bed',
                'severity': 'info'
            })
        
        return alerts
    
    def get_weight_stats(self):
        """Get weight statistics"""
        return {
            'current': self.current_data,
            'connected': self.current_data['isConnected'],
            'last_update': self.current_data['timestamp'],
            'alerts': self.check_weight_alerts()
        }
    
    def set_weight_threshold(self, threshold):
        """Set weight threshold for bed occupancy detection"""
        self.weight_threshold = threshold
        logger.info(f"Weight threshold set to {threshold}kg")
    
    # Consistent interface methods
    def update_data(self, data):
        """Update weight data - consistent interface"""
        return self.update_weight(data)
    
    def get_data(self):
        """Get weight data - consistent interface"""
        return self.get_weight_data()
    
    def init_database(self):
        """Initialize database - consistent interface"""
        # Database initialization is handled in _store_in_database
        pass

__all__ = [
    'WeightService',
]
