
#!/usr/bin/env python3
"""
services/snore_service.py - Snore Detection Service  
Handles ONLY snore detection sensor data and audio analysis
"""

import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SnoreService:
    def __init__(self):
        self.current_data = {
            'isDetected': False,
            'frequency': 0,
            'duration': '0h 0m',
            'intensity': 0,
            'timestamp': None,
            'isConnected': False
        }
        self.snore_session_start = None
        self.total_snore_events = 0
    
    def update_snore(self, data):
        """Update snore detection data from sensor"""
        try:
            is_detected = data.get('isDetected', False)
            frequency = data.get('frequency', 0)
            duration_minutes = data.get('duration_minutes', 0)
            intensity = data.get('intensity', 0)
            
            # Format duration
            hours = duration_minutes // 60
            minutes = duration_minutes % 60
            duration_str = f"{hours}h {minutes}m"
            
            self.current_data = {
                'isDetected': is_detected,
                'frequency': frequency,
                'duration': duration_str,
                'intensity': intensity,
                'timestamp': datetime.now().isoformat(),
                'isConnected': True
            }
            
            # Track snore events
            if is_detected and self.snore_session_start is None:
                self.snore_session_start = datetime.now()
                self.total_snore_events += 1
            elif not is_detected and self.snore_session_start is not None:
                self.snore_session_start = None
            
            # Store in database
            self._store_in_database(data)
            
            status = "SNORING" if is_detected else "Quiet"
            logger.info(f"😴 Snore: {status} (Freq: {frequency}Hz, Intensity: {intensity}%)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Snore update failed: {e}")
            self.current_data['isConnected'] = False
            return False
    
    def get_snore_data(self):
        """Get current snore detection data"""
        data = self.current_data.copy()
        data['lastDetected'] = data.pop('timestamp', 'Never')
        return data
    
    def _store_in_database(self, data):
        """Store snore detection data in database"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO snore_detection (is_detected, frequency, duration_minutes)
                VALUES (?, ?, ?)
            ''', (
                data.get('isDetected', False),
                data.get('frequency', 0),
                data.get('duration_minutes', 0)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Snore database error: {e}")
    
    def get_snore_history(self, hours=24):
        """Get snore detection history for specified hours"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT is_detected, frequency, duration_minutes, timestamp 
                FROM snore_detection 
                WHERE timestamp > datetime('now', '-{} hours')
                ORDER BY timestamp DESC
                LIMIT 100
            '''.format(hours))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'isDetected': bool(row[0]),
                    'frequency': row[1],
                    'duration_minutes': row[2],
                    'timestamp': row[3]
                })
            
            conn.close()
            return history
            
        except Exception as e:
            logger.error(f"❌ Snore history error: {e}")
            return []
    
    def get_snore_stats(self):
        """Get snoring statistics for today"""
        try:
            conn = sqlite3.connect('sensor_data.db')
            cursor = conn.cursor()
            
            # Get today's snoring data
            cursor.execute('''
                SELECT is_detected, frequency, timestamp 
                FROM snore_detection 
                WHERE date(timestamp) = date('now')
                ORDER BY timestamp ASC
            ''')
            
            data = cursor.fetchall()
            conn.close()
            
            if not data:
                return {
                    'total_snore_time': '0h 0m',
                    'snore_events': 0,
                    'avg_frequency': 0,
                    'snore_percentage': 0
                }
            
            # Calculate snoring statistics
            total_snore_minutes = 0
            snore_events = 0
            frequency_sum = 0
            frequency_count = 0
            last_was_snoring = False
            snore_start = None
            
            for is_detected, frequency, timestamp in data:
                current_time = datetime.fromisoformat(timestamp)
                
                if is_detected and not last_was_snoring:
                    # Start of snore event
                    snore_events += 1
                    snore_start = current_time
                elif not is_detected and last_was_snoring and snore_start:
                    # End of snore event
                    snore_duration = (current_time - snore_start).total_seconds() / 60
                    total_snore_minutes += snore_duration
                
                if is_detected and frequency > 0:
                    frequency_sum += frequency
                    frequency_count += 1
                
                last_was_snoring = is_detected
            
            # Calculate averages
            avg_frequency = frequency_sum / frequency_count if frequency_count > 0 else 0
            total_time_minutes = len(data) * 2  # Assuming 2-minute intervals
            snore_percentage = (total_snore_minutes / total_time_minutes * 100) if total_time_minutes > 0 else 0
            
            hours = int(total_snore_minutes // 60)
            minutes = int(total_snore_minutes % 60)
            
            return {
                'total_snore_time': f"{hours}h {minutes}m",
                'snore_events': snore_events,
                'avg_frequency': round(avg_frequency, 1),
                'snore_percentage': round(snore_percentage, 1),
                'currently_snoring': self.current_data['isDetected']
            }
            
        except Exception as e:
            logger.error(f"❌ Snore stats error: {e}")
            return {}
    
    def check_snore_alerts(self):
        """Check if snoring needs alerts"""
        alerts = []
        
        if self.current_data['isDetected']:
            intensity = self.current_data['intensity']
            frequency = self.current_data['frequency']
            
            if intensity > 80:
                alerts.append({
                    'type': 'loud_snoring',
                    'message': f'Loud snoring detected: {intensity}% intensity',
                    'severity': 'warning'
                })
            elif intensity > 60:
                alerts.append({
                    'type': 'moderate_snoring',
                    'message': f'Moderate snoring: {intensity}% intensity',
                    'severity': 'info'
                })
            
            if frequency > 50:
                alerts.append({
                    'type': 'high_frequency_snoring',
                    'message': f'High frequency snoring: {frequency}Hz',
                    'severity': 'info'
                })
        
        # Check for extended snoring sessions
        if self.snore_session_start:
            session_duration = (datetime.now() - self.snore_session_start).total_seconds() / 60
            if session_duration > 30:  # 30 minutes of continuous snoring
                alerts.append({
                    'type': 'extended_snoring',
                    'message': f'Extended snoring session: {session_duration:.0f} minutes',
                    'severity': 'warning'
                })
        
        if not self.current_data['isConnected']:
            alerts.append({
                'type': 'sensor_disconnected',
                'message': 'Snore detection sensor not connected',
                'severity': 'error'
            })
        
        return alerts
    
    def analyze_snore_pattern(self):
        """Analyze snoring patterns for insights"""
        try:
            history = self.get_snore_history(24)  # Last 24 hours
            
            if not history:
                return {'pattern': 'No data available'}
            
            # Analyze frequency distribution
            frequencies = [h['frequency'] for h in history if h['isDetected'] and h['frequency'] > 0]
            
            if not frequencies:
                return {'pattern': 'No snoring detected'}
            
            avg_freq = sum(frequencies) / len(frequencies)
            max_freq = max(frequencies)
            min_freq = min(frequencies)
            
            # Determine pattern type
            if avg_freq < 20:
                pattern_type = 'Low frequency snoring'
            elif avg_freq < 40:
                pattern_type = 'Moderate frequency snoring'
            else:
                pattern_type = 'High frequency snoring'
            
            return {
                'pattern': pattern_type,
                'avg_frequency': round(avg_freq, 1),
                'max_frequency': max_freq,
                'min_frequency': min_freq,
                'total_events': len([h for h in history if h['isDetected']]),
                'analysis_period': '24 hours'
            }
            
        except Exception as e:
            logger.error(f"❌ Snore pattern analysis error: {e}")
            return {'pattern': 'Analysis failed'}
    
    def get_snore_full_stats(self):
        """Get comprehensive snore detection statistics"""
        return {
            'current': self.current_data,
            'connected': self.current_data['isConnected'],
            'last_update': self.current_data['timestamp'],
            'daily_stats': self.get_snore_stats(),
            'pattern_analysis': self.analyze_snore_pattern(),
            'alerts': self.check_snore_alerts(),
            'total_events_today': self.total_snore_events
        }
    
    # Consistent interface methods
    def update_data(self, data):
        """Update snore data - consistent interface"""
        return self.update_snore(data)
    
    def get_data(self):
        """Get snore data - consistent interface"""
        return self.get_snore_data()
    
    def init_database(self):
        """Initialize database - consistent interface"""
        # Database initialization is handled in _store_in_database
        pass

__all__ = [
    'SnoreService',
]
