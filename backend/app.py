#!/usr/bin/env python3
"""
Sleep Monitoring Backend Server - Clean Version
Organized structure with minimal, useful logging
"""

from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import logging
import random
from datetime import datetime

# Import routes
from routes.sensor_routes import sensor_bp
from routes.device_control import device_bp
from routes.led_routes import led_bp

# Import services
from services import (
    HeartRateService, BreathingService, GyroscopeService, 
    WeightService, SnoreService, FanService, LEDService
)

# Import database initialization
from database_init import init_all_databases

# Configure clean logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Reduce service logging to WARNING level (less spam)
logging.getLogger('services.heart_rate').setLevel(logging.WARNING)
logging.getLogger('services.breathing').setLevel(logging.WARNING)
logging.getLogger('services.gyroscope').setLevel(logging.WARNING)
logging.getLogger('services.weight').setLevel(logging.WARNING)
logging.getLogger('services.snore').setLevel(logging.WARNING)
logging.getLogger('services.fan').setLevel(logging.WARNING)
logging.getLogger('services.led').setLevel(logging.INFO)  # Keep LED logs

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# Initialize services
services = {
    'heart_rate': HeartRateService(),
    'breathing': BreathingService(),
    'gyroscope': GyroscopeService(),
    'weight': WeightService(),
    'snore': SnoreService(),
    'fan': FanService(),
    'led': LEDService()
}

# Register blueprints
app.register_blueprint(sensor_bp)
app.register_blueprint(device_bp)
app.register_blueprint(led_bp)

def init_database():
    """Initialize database for all services"""
    try:
        init_all_databases()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database init failed: {e}")

def simulate_sensor_data():
    """Generate fake sensor data - QUIET mode"""
    simulation_count = 0
    
    while True:
        try:
            simulation_count += 1
            
            # Only log every 12th simulation (every minute instead of every 5 seconds)
            quiet_mode = simulation_count % 12 != 0
            
            # Generate data
            heart_rate_data = {
                'rate': random.randint(60, 90),
                'status': random.choice(['Normal', 'High', 'Low']),
                'min': random.randint(55, 65),
                'max': random.randint(85, 95),
                'average': random.randint(65, 80),
                'variability': random.randint(5, 15)
            }
            
            breathing_data = {
                'rate': random.randint(12, 20),
                'rhythm': random.choice(['Normal', 'Irregular', 'Shallow']),
                'apneaEvents': random.randint(0, 3)
            }
            
            gyro_data = {
                'pitch': random.uniform(-30, 30),
                'roll': random.uniform(-45, 45)
            }
            
            weight_data = {
                'weight': random.randint(150, 180) if random.random() > 0.3 else 0
            }
            
            snore_data = {
                'isDetected': random.random() > 0.8,
                'frequency': random.randint(0, 10),
                'duration': f"{random.randint(0, 2)}h {random.randint(0, 59)}m"
            }
            
            # Update services
            services['heart_rate'].update_data(heart_rate_data)
            services['breathing'].update_data(breathing_data)
            services['gyroscope'].update_data(gyro_data)
            services['weight'].update_data(weight_data)
            services['snore'].update_data(snore_data)
            
            # Only show summary every minute
            if not quiet_mode:
                in_bed = "In Bed" if weight_data['weight'] > 0 else "Out of Bed"
                snoring = "SNORING" if snore_data['isDetected'] else "Quiet"
                
                logger.info(f"📊 Simulation Update: HR={heart_rate_data['rate']}bpm | {in_bed} | {snoring}")
            
            time.sleep(5)  # Update every 5 seconds
            
        except Exception as e:
            logger.error(f"❌ Simulation error: {e}")
            time.sleep(5)

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services_count': len(services),
        'all_services_ok': True
    })

# Status summary endpoint
@app.route('/api/status-summary')
def status_summary():
    """Get a clean summary of all systems"""
    try:
        # Get current data from services
        heart_rate = services['heart_rate'].get_current_data()
        weight = services['weight'].get_current_data()
        snore = services['snore'].get_current_data()
        
        return jsonify({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'heart_rate': f"{heart_rate.get('rate', 0)} BPM",
            'in_bed': weight.get('weight', 0) > 0,
            'snoring': snore.get('isDetected', False),
            'services_online': len(services),
            'simulation_active': True
        })
    except:
        return jsonify({'error': 'Status unavailable'}), 500

# Root endpoint
@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Sleep Monitoring Backend Server',
        'status': 'running',
        'version': '2.0 Clean',
        'services': list(services.keys()),
        'quiet_logging': True
    })

if __name__ == '__main__':
    print("🚀 Sleep Monitoring Backend Server")
    print("📦 Modular Architecture with Clean Logging")
    print("🔇 Reduced log spam - only important events shown")
    print()
    
    # Initialize database
    init_database()
    
    # Start quiet simulation
    simulation_thread = threading.Thread(target=simulate_sensor_data, daemon=True)
    simulation_thread.start()
    
    # Start the server
    logger.info("🚀 Server starting on http://localhost:5000")
    logger.info("💡 LED logs: ENABLED | Sensor logs: QUIET")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)  # Debug=False for cleaner logs
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")