#!/usr/bin/env python3
"""
Sensor Routes - API endpoints for sensor data
"""

from flask import Blueprint, jsonify, request
from services import HeartRateService, BreathingService, GyroscopeService, WeightService, SnoreService
import logging

logger = logging.getLogger(__name__)

# Create blueprint
sensor_bp = Blueprint('sensor', __name__, url_prefix='/api')

# Initialize services
heart_rate_service = HeartRateService()
breathing_service = BreathingService()
gyroscope_service = GyroscopeService()
weight_service = WeightService()
snore_service = SnoreService()

@sensor_bp.route('/heart-rate')
def get_heart_rate():
    """Get latest heart rate data"""
    return jsonify(heart_rate_service.get_data())

@sensor_bp.route('/breathing-data')
def get_breathing_data():
    """Get latest breathing data"""
    return jsonify(breathing_service.get_data())

@sensor_bp.route('/gyroscope-data')
def get_gyroscope_data():
    """Get latest gyroscope/posture data"""
    return jsonify(gyroscope_service.get_data())

@sensor_bp.route('/weight-data')
def get_weight_data():
    """Get latest weight data"""
    return jsonify(weight_service.get_data())

@sensor_bp.route('/snore-data')
def get_snore_data():
    """Get latest snore detection data"""
    return jsonify(snore_service.get_data())

@sensor_bp.route('/sleep-history')
def get_sleep_history():
    """Get historical sleep session data"""
    # This could be handled by a separate SleepHistoryService
    # For now, return from any service that has this method
    return jsonify(heart_rate_service.get_sleep_history())

@sensor_bp.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    """Receive sensor data from ESP32"""
    try:
        data = request.get_json()
        logger.info(f"📡 Received sensor data: {data}")
        
        results = []
        
        # Update each sensor service
        if 'heart_rate' in data:
            result = heart_rate_service.update_data(data['heart_rate'])
            results.append(result)
        
        if 'breathing' in data:
            result = breathing_service.update_data(data['breathing'])
            results.append(result)
            
        if 'gyroscope' in data:
            result = gyroscope_service.update_data(data['gyroscope'])
            results.append(result)
            
        if 'weight' in data:
            result = weight_service.update_data(data['weight'])
            results.append(result)
            
        if 'snore' in data:
            result = snore_service.update_data(data['snore'])
            results.append(result)
        
        return jsonify({'status': 'success', 'message': 'Data received successfully', 'results': results})
    
    except Exception as e:
        logger.error(f"Error processing sensor data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
