"""
Configuration settings for the Sleep Monitoring Backend
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'sensor_data.db')
    
    # ESP32 Communication
    SERIAL_PORT = os.getenv('SERIAL_PORT', '/dev/ttyUSB0')
    BAUD_RATE = int(os.getenv('BAUD_RATE', 115200))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    
    # Simulation mode (for development)
    SIMULATION_MODE = os.getenv('SIMULATION_MODE', 'True').lower() == 'true'
    
    # Data validation thresholds
    HEART_RATE_MIN = int(os.getenv('HEART_RATE_MIN', 30))
    HEART_RATE_MAX = int(os.getenv('HEART_RATE_MAX', 200))
    
    BREATHING_RATE_MIN = int(os.getenv('BREATHING_RATE_MIN', 5))
    BREATHING_RATE_MAX = int(os.getenv('BREATHING_RATE_MAX', 60))
    
    WEIGHT_MAX = float(os.getenv('WEIGHT_MAX', 500))  # kg
    
    # Sensor update intervals (seconds)
    HEART_RATE_INTERVAL = int(os.getenv('HEART_RATE_INTERVAL', 2))
    BREATHING_INTERVAL = int(os.getenv('BREATHING_INTERVAL', 2))
    GYROSCOPE_INTERVAL = int(os.getenv('GYROSCOPE_INTERVAL', 1))
    WEIGHT_INTERVAL = int(os.getenv('WEIGHT_INTERVAL', 5))
    SNORE_INTERVAL = int(os.getenv('SNORE_INTERVAL', 3))
    
    # GPIO Pin assignments (for Raspberry Pi)
    FAN_PIN = int(os.getenv('FAN_PIN', 18))
    SPEAKER_PIN = int(os.getenv('SPEAKER_PIN', 19))
    LED_STRIP_PIN = int(os.getenv('LED_STRIP_PIN', 21))
    
    # Servo pins for pillow adjustment
    PILLOW_SERVO_PIN = int(os.getenv('PILLOW_SERVO_PIN', 12))
    
    # Alert thresholds
    HIGH_HEART_RATE_THRESHOLD = int(os.getenv('HIGH_HEART_RATE_THRESHOLD', 100))
    LOW_HEART_RATE_THRESHOLD = int(os.getenv('LOW_HEART_RATE_THRESHOLD', 50))
    
    BAD_POSTURE_ANGLE = float(os.getenv('BAD_POSTURE_ANGLE', 30))
    POOR_POSTURE_ANGLE = float(os.getenv('POOR_POSTURE_ANGLE', 15))
    
    # Sleep session settings
    SLEEP_DETECTION_WEIGHT_THRESHOLD = float(os.getenv('SLEEP_DETECTION_WEIGHT_THRESHOLD', 30))
    INACTIVITY_SLEEP_THRESHOLD = int(os.getenv('INACTIVITY_SLEEP_THRESHOLD', 900))  # 15 minutes
    
    # Data retention (days)
    DATA_RETENTION_DAYS = int(os.getenv('DATA_RETENTION_DAYS', 90))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SIMULATION_MODE = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SIMULATION_MODE = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production environment")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Use in-memory database for tests
    SIMULATION_MODE = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
