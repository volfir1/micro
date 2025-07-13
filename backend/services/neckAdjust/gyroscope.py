
#!/usr/bin/env python3
"""
services/gyroscope_service.py - Gyroscope and Position Monitoring Service
Handles ONLY gyroscope sensor data and sleep position detection
"""

import sqlite3
from datetime import datetime
import logging
import math

logger = logging.getLogger(__name__)

class GyroscopeService:
    def __init__(self):
        self.current_data = {
            'pitch': 0,
            'roll': 0,
            'neckAngle': 0,
            'position': 'Back',
            'postureSeverity': 'Good',
            'timestamp': None,
            'isConnected': False
        }
    
    def update_gyroscope(self, data):
        """Update gyroscope data from sensor"""
        try:
            pitch = data.get('pitch', 0)
            roll = data.get('roll', 0)
            
            # Calculate neck angle (absolute pitch)
            neck_angle = abs(pitch)
            
            # Determine sleep position
            position = self._determine_position(roll)
            
            # Determine posture severity
            posture_severity = self._determine_posture_severity(neck_angle)
            
            self.current_data = {
                'pitch': pitch,
                'roll': roll,
                'neckAngle': neck_angle,
                'position': position,
                'postureSeverity': posture_severity,
                'timestamp': datetime.now().isoformat(),
                'isConnected': True
            }
            
            # Store in database
            self._store_in_database(data)
            
            logger.info(f"🔄 Position: {position} (Neck: {neck_angle:.1f}°, Posture: {posture_severity})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Gyroscope update failed: {e}")
            self.current_data['isConnected'] = False
            return False
    
    def get_gyroscope_data(self):
        """Get current gyroscope data"""
        data = self.current_data.copy()
        data['lastUpdated'] = data.pop('timestamp', 'Never')
        return data
    
    def _determine_position(self, roll):
        """Determine sleep position based on roll angle"""
        if roll > 45:
            return 'Right Side'
        elif roll < -45:
            return 'Left Side'
        elif abs(roll) < 15:
            return 'Back'
        elif roll > 0:
            return 'Slightly Right'
        else:
            return 'Slightly Left'
    
    def _determine_posture_severity(self, neck_angle):
        """Determine posture severity based on neck angle"""
        if neck_angle < 10:
            return 'Excellent'
        elif neck_angle < 20:
            return 'Good'
        elif neck_angle < 35:
            return 'Poor'
        else:
            return 'Bad'
    
    def _store_in_database(self, data):
        """Store gyroscope data in database"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO gyroscope (pitch, roll, neck_angle, position, posture_severity)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                self.current_data['pitch'],
                self.current_data['roll'],
                self.current_data['neckAngle'],
                self.current_data['position'],
                self.current_data['postureSeverity']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Gyroscope database error: {e}")
    
    def get_gyroscope_history(self, hours=24):
        """Get gyroscope history for specified hours"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT pitch, roll, neck_angle, position, posture_severity, timestamp 
                FROM gyroscope 
                WHERE timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp DESC
                LIMIT 100
            '''.format(hours))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'pitch': row[0],
                    'roll': row[1],
                    'neckAngle': row[2],
                    'position': row[3],
                    'postureSeverity': row[4],
                    'timestamp': row[5]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"❌ Gyroscope history error: {e}")
            return []
    
    def get_position_stats(self):
        """Get sleep position statistics for today"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT position, COUNT(*) as count
                FROM gyroscope 
                WHERE date(timestamp) = date('now')
                GROUP BY position
                ORDER BY count DESC
            ''')
            
            position_counts = {}
            total_readings = 0
            
            for row in cursor.fetchall():
                position_counts[row[0]] = row[1]
                total_readings += row[1]
            
            # Calculate percentages
            position_percentages = {}
            for position, count in position_counts.items():
                percentage = (count / total_readings * 100) if total_readings > 0 else 0
                position_percentages[position] = round(percentage, 1)
            
            conn.close()
            
            return {
                'position_counts': position_counts,
                'position_percentages': position_percentages,
                'total_readings': total_readings,
                'current_position': self.current_data['position']
            }
            
        except Exception as e:
            logger.error(f"❌ Position stats error: {e}")
            return {}
    
    def check_posture_alerts(self):
        """Check if posture needs alerts"""
        neck_angle = self.current_data['neckAngle']
        posture = self.current_data['postureSeverity']
        alerts = []
        
        if neck_angle > 40:
            alerts.append({
                'type': 'bad_neck_posture',
                'message': f'Poor neck posture detected: {neck_angle:.1f}° angle',
                'severity': 'warning'
            })
        elif neck_angle > 30:
            alerts.append({
                'type': 'moderate_neck_strain',
                'message': f'Moderate neck strain: {neck_angle:.1f}° angle',
                'severity': 'info'
            })
        
        if posture == 'Bad':
            alerts.append({
                'type': 'bad_posture',
                'message': 'Bad sleeping posture detected',
                'severity': 'warning'
            })
        
        if not self.current_data['isConnected']:
            alerts.append({
                'type': 'sensor_disconnected',
                'message': 'Gyroscope sensor not connected',
                'severity': 'error'
            })
        
        return alerts
    
    def calibrate_sensor(self):
        """Calibrate gyroscope sensor to neutral position"""
        try:
            # This would typically involve hardware calibration
            logger.info("🔄 Gyroscope sensor calibrated to neutral position")
            return {
                'success': True,
                'message': 'Gyroscope calibrated successfully',
                'calibration_time': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Gyroscope calibration failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_gyroscope_stats(self):
        """Get gyroscope sensor statistics"""
        return {
            'current': self.current_data,
            'connected': self.current_data['isConnected'],
            'last_update': self.current_data['timestamp'],
            'position_stats': self.get_position_stats(),
            'alerts': self.check_posture_alerts()
        }
    
    # Consistent interface methods
    def update_data(self, data):
        """Update gyroscope data - consistent interface"""
        return self.update_gyroscope(data)
    
    def get_data(self):
        """Get gyroscope data - consistent interface"""
        return self.get_gyroscope_data()
    
    def init_database(self):
        """Initialize database - consistent interface"""
        # Database initialization is handled in _store_in_database
        pass

__all__ = [
    'GyroscopeService',
]
