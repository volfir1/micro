
#!/usr/bin/env python3
"""
services/fan_service.py - Fan Control Service
Handles ONLY fan control and cooling management
"""

import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class FanService:
    def __init__(self, gpio_pin=18):
        self.gpio_pin = gpio_pin
        self.current_state = {
            'enabled': False,
            'speed': 0,
            'auto_mode': False,
            'last_command': None,
            'temperature_threshold': 24,  # Celsius
            'heart_rate_threshold': 90    # BPM
        }
        
        # Initialize GPIO for fan control
        self.init_hardware()
    
    def init_hardware(self):
        """Initialize GPIO pin for fan control"""
        try:
            # TODO: Initialize actual GPIO
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(self.gpio_pin, GPIO.OUT)
            # self.pwm = GPIO.PWM(self.gpio_pin, 1000)  # 1kHz frequency
            # self.pwm.start(0)
            
            logger.info(f"🌀 Fan GPIO initialized on pin {self.gpio_pin}")
        except Exception as e:
            logger.error(f"❌ Fan GPIO init failed: {e}")
    
    def control_fan(self, data):
        """Control fan based on command"""
        try:
            fan_state = data.get('state', False)
            speed = data.get('speed', 100)
            auto_mode = data.get('auto_mode', False)
            
            # Validate speed
            speed = max(0, min(100, speed))
            
            # Update state
            self.current_state['enabled'] = fan_state
            self.current_state['speed'] = speed if fan_state else 0
            self.current_state['auto_mode'] = auto_mode
            self.current_state['last_command'] = datetime.now().isoformat()
            
            # Apply hardware control
            self._apply_hardware_control()
            
            message = f"Fan {'ON' if fan_state else 'OFF'}"
            if fan_state:
                message += f" (Speed: {speed}%)"
            if auto_mode:
                message += " [AUTO MODE]"
            
            logger.info(f"🌀 {message}")
            
            return {
                'status': 'success',
                'message': message,
                'fan_state': fan_state,
                'speed': speed,
                'auto_mode': auto_mode
            }
            
        except Exception as e:
            logger.error(f"❌ Fan control error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _apply_hardware_control(self):
        """Apply current state to hardware"""
        try:
            if self.current_state['enabled']:
                # Convert speed percentage to PWM duty cycle
                duty_cycle = self.current_state['speed']
                # TODO: Apply to actual hardware
                # self.pwm.ChangeDutyCycle(duty_cycle)
                pass
            else:
                # TODO: Turn off fan
                # self.pwm.ChangeDutyCycle(0)
                pass
                
        except Exception as e:
            logger.error(f"❌ Fan hardware control error: {e}")
    
    def auto_control(self, temperature=None, heart_rate=None):
        """Automatic fan control based on sensor data"""
        if not self.current_state['auto_mode']:
            return {'message': 'Auto mode disabled'}
        
        try:
            should_enable = False
            target_speed = 0
            reason = ""
            
            # Check temperature
            if temperature and temperature > self.current_state['temperature_threshold']:
                should_enable = True
                # Calculate speed based on temperature excess
                temp_excess = temperature - self.current_state['temperature_threshold']
                temp_speed = min(100, 30 + (temp_excess * 10))
                target_speed = max(target_speed, temp_speed)
                reason += f"High temp ({temperature}°C) "
            
            # Check heart rate
            if heart_rate and heart_rate > self.current_state['heart_rate_threshold']:
                should_enable = True
                # Calculate speed based on heart rate
                hr_excess = heart_rate - self.current_state['heart_rate_threshold']
                hr_speed = min(100, 40 + (hr_excess * 2))
                target_speed = max(target_speed, hr_speed)
                reason += f"High HR ({heart_rate} BPM) "
            
            # Apply automatic control
            if should_enable != self.current_state['enabled'] or target_speed != self.current_state['speed']:
                auto_command = {
                    'state': should_enable,
                    'speed': target_speed,
                    'auto_mode': True
                }
                
                result = self.control_fan(auto_command)
                result['auto_reason'] = reason.strip()
                result['temperature'] = temperature
                result['heart_rate'] = heart_rate
                
                return result
            
            return {
                'status': 'no_change',
                'message': 'No automatic adjustment needed',
                'temperature': temperature,
                'heart_rate': heart_rate
            }
            
        except Exception as e:
            logger.error(f"❌ Auto fan control error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def set_thresholds(self, temperature_threshold=None, heart_rate_threshold=None):
        """Set automatic control thresholds"""
        try:
            if temperature_threshold is not None:
                self.current_state['temperature_threshold'] = temperature_threshold
            
            if heart_rate_threshold is not None:
                self.current_state['heart_rate_threshold'] = heart_rate_threshold
            
            logger.info(f"🌀 Fan thresholds updated: Temp={self.current_state['temperature_threshold']}°C, HR={self.current_state['heart_rate_threshold']}BPM")
            
            return {
                'status': 'success',
                'temperature_threshold': self.current_state['temperature_threshold'],
                'heart_rate_threshold': self.current_state['heart_rate_threshold']
            }
            
        except Exception as e:
            logger.error(f"❌ Fan threshold error: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_fan_status(self):
        """Get current fan status"""
        return {
            'enabled': self.current_state['enabled'],
            'speed': self.current_state['speed'],
            'auto_mode': self.current_state['auto_mode'],
            'last_command': self.current_state['last_command'],
            'thresholds': {
                'temperature': self.current_state['temperature_threshold'],
                'heart_rate': self.current_state['heart_rate_threshold']
            },
            'gpio_pin': self.gpio_pin
        }
    
    def emergency_stop(self):
        """Emergency stop fan"""
        try:
            emergency_command = {
                'state': False,
                'speed': 0,
                'auto_mode': False
            }
            
            result = self.control_fan(emergency_command)
            result['emergency'] = True
            
            logger.warning("🛑 Fan emergency stop activated")
            return result
            
        except Exception as e:
            logger.error(f"❌ Fan emergency stop failed: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def cleanup(self):
        """Cleanup GPIO resources"""
        try:
            # TODO: Cleanup actual GPIO
            # self.pwm.stop()
            # GPIO.cleanup()
            
            logger.info("🌀 Fan GPIO cleanup completed")
        except Exception as e:
            logger.error(f"❌ Fan cleanup error: {e}")

__all__ = [
    'FanService',
]
