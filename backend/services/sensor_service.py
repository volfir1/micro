
"""
services/sensor_service.py - Sensor Data Management Service
Handles all sensor data processing and storage
"""

import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SensorService:
    def __init__(self):
        # Global sensor data storage
        self.latest_sensor_data = {
            'heart_rate': {'rate': 0, 'status': 'Normal', 'timestamp': None, 'isConnected': False},
            'breathing': {'rate': 0, 'rhythm': 'Normal', 'apneaEvents': 0, 'timestamp': None, 'isConnected': False},
            'gyroscope': {'pitch': 0, 'roll': 0, 'neckAngle': 0, 'position': 'Back', 'timestamp': None, 'isConnected': False},
            'weight': {'weight': 0, 'timestamp': None, 'isConnected': False},
            'snore': {'isDetected': False, 'frequency': 0, 'duration': '0h 0m', 'timestamp': None, 'isConnected': False}
        }
    
    def get_heart_rate_data(self):
        """Get latest heart rate data"""
        data = self.latest_sensor_data['heart_rate'].copy()
        data['lastUpdated'] = data.pop('timestamp', 'Never')
        return data
    
    def get_breathing_data(self):
        """Get latest breathing data"""
        data = self.latest_sensor_data['breathing'].copy()
        data['lastMeasured'] = data.pop('timestamp', 'Never')
        return data
    
    def get_gyroscope_data(self):
        """Get latest gyroscope/posture data"""
        data = self.latest_sensor_data['gyroscope'].copy()
        data['lastUpdated'] = data.pop('timestamp', 'Never')
        
        # Calculate position and posture severity if not set
        if not data.get('position'):
            roll = data.get('roll', 0)
            if roll > 30:
                data['position'] = 'Right Side'
            elif roll < -30:
                data['position'] = 'Left Side'
            else:
                data['position'] = 'Back'
        
        if not data.get('postureSeverity'):
            neck_angle = data.get('neckAngle', 0)
            if neck_angle < 15:
                data['postureSeverity'] = 'Good'
            elif neck_angle < 30:
                data['postureSeverity'] = 'Poor'
            else:
                data['postureSeverity'] = 'Bad'
        
        return data
    
    def get_weight_data(self):
        """Get latest weight data"""
        data = self.latest_sensor_data['weight'].copy()
        data.pop('timestamp', None)
        return data
    
    def get_snore_data(self):
        """Get latest snore detection data"""
        data = self.latest_sensor_data['snore'].copy()
        data['lastDetected'] = data.pop('timestamp', 'Never')
        return data
    
    def get_sleep_history(self):
        """Get historical sleep session data"""
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, start_time, end_time, duration_minutes, sleep_score, 
                   total_snore_events, avg_heart_rate, status
            FROM sleep_sessions 
            ORDER BY start_time DESC 
            LIMIT 30
        ''')
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': str(row[0]),
                'date': row[1][:10] if row[1] else 'Unknown',
                'duration': f"{row[3]//60}h {row[3]%60}m" if row[3] else '0h 0m',
                'sleepScore': row[4] or 0,
                'snoreEvents': row[5] or 0,
                'avgHR': row[6] or 0,
                'status': row[7] or 'Unknown'
            })
        
        conn.close()
        return sessions
    
    def process_sensor_data(self, data):
        """Process incoming sensor data from ESP32"""
        try:
            # Update latest sensor data and store in database
            if 'heart_rate' in data:
                self.update_heart_rate(data['heart_rate'])
            
            if 'breathing' in data:
                self.update_breathing(data['breathing'])
                
            if 'gyroscope' in data:
                self.update_gyroscope(data['gyroscope'])
                
            if 'weight' in data:
                self.update_weight(data['weight'])
                
            if 'snore' in data:
                self.update_snore(data['snore'])
            
            return {'success': True, 'message': 'Sensor data processed successfully'}
        
        except Exception as e:
            logger.error(f"Error processing sensor data: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_heart_rate(self, data):
        """Update heart rate data"""
        self.latest_sensor_data['heart_rate'] = {
            'rate': data.get('rate', 0),
            'status': data.get('status', 'Normal'),
            'min': data.get('min', 0),
            'max': data.get('max', 0),
            'average': data.get('average', 0),
            'variability': data.get('variability', 0),
            'timestamp': datetime.now().isoformat(),
            'isConnected': True
        }
        
        # Store in database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO heart_rate (rate, status, min_rate, max_rate, average_rate, variability)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.get('rate', 0), data.get('status', 'Normal'), data.get('min', 0),
              data.get('max', 0), data.get('average', 0), data.get('variability', 0)))
        conn.commit()
        conn.close()
    
    def update_breathing(self, data):
        """Update breathing data"""
        self.latest_sensor_data['breathing'] = {
            'rate': data.get('rate', 0),
            'rhythm': data.get('rhythm', 'Normal'),
            'apneaEvents': data.get('apneaEvents', 0),
            'timestamp': datetime.now().isoformat(),
            'isConnected': True
        }
        
        # Store in database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO breathing (rate, rhythm, apnea_events)
            VALUES (?, ?, ?)
        ''', (data.get('rate', 0), data.get('rhythm', 'Normal'), data.get('apneaEvents', 0)))
        conn.commit()
        conn.close()
    
    def update_gyroscope(self, data):
        """Update gyroscope/posture data"""
        pitch = data.get('pitch', 0)
        roll = data.get('roll', 0)
        neck_angle = abs(pitch)
        
        # Determine position from roll
        position = 'Back'
        if roll > 30:
            position = 'Right Side'
        elif roll < -30:
            position = 'Left Side'
        
        # Determine posture severity
        posture_severity = 'Good'
        if neck_angle > 30:
            posture_severity = 'Bad'
        elif neck_angle > 15:
            posture_severity = 'Poor'
        
        self.latest_sensor_data['gyroscope'] = {
            'pitch': pitch,
            'roll': roll,
            'neckAngle': neck_angle,
            'position': position,
            'postureSeverity': posture_severity,
            'timestamp': datetime.now().isoformat(),
            'isConnected': True
        }
        
        # Store in database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gyroscope (pitch, roll, neck_angle, position, posture_severity)
            VALUES (?, ?, ?, ?, ?)
        ''', (pitch, roll, neck_angle, position, posture_severity))
        conn.commit()
        conn.close()
    
    def update_weight(self, data):
        """Update weight data"""
        self.latest_sensor_data['weight'] = {
            'weight': data.get('weight', 0),
            'timestamp': datetime.now().isoformat(),
            'isConnected': True
        }
        
        # Store in database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO weight (weight) VALUES (?)', (data.get('weight', 0),))
        conn.commit()
        conn.close()
    
    def update_snore(self, data):
        """Update snore detection data"""
        self.latest_sensor_data['snore'] = {
            'isDetected': data.get('isDetected', False),
            'frequency': data.get('frequency', 0),
            'duration': data.get('duration', '0h 0m'),
            'timestamp': datetime.now().isoformat(),
            'isConnected': True
        }
        
        # Store in database
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO snore_detection (is_detected, frequency, duration_minutes)
            VALUES (?, ?, ?)
        ''', (data.get('isDetected', False), data.get('frequency', 0), 
              data.get('duration_minutes', 0)))
        conn.commit()
        conn.close()
    
    def get_all_sensor_status(self):
        """Get status of all sensors"""
        return {
            'sensors': self.latest_sensor_data,
            'last_update': datetime.now().isoformat(),
            'total_sensors': 5,
            'connected_sensors': sum(1 for sensor in self.latest_sensor_data.values() if sensor.get('isConnected', False))
        }


__all__ = [
    
    'SnoreService',
    
]
