#!/usr/bin/env python3
"""
routes/device_control.py - Device Control API Routes
Handles all device control endpoints (fan, pillow, speaker, etc.)
"""

from flask import Blueprint, jsonify, request
import logging
from services import FanService

logger = logging.getLogger(__name__)
device_bp = Blueprint('device', __name__, url_prefix='/api/control')

# Initialize services
fan_service = FanService()

@device_bp.route('/fan', methods=['POST'])
def control_fan():
    """Control fan based on temperature/heart rate"""
    try:
        data = request.get_json()
        result = fan_service.control_fan(data)
        logger.info(f"🌀 {result['message']}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"❌ Fan control error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@device_bp.route('/pillow', methods=['POST'])
def control_pillow():
    """Control pillow adjustment"""
    try:
        data = request.get_json()
        angle = data.get('angle', 0)
        height = data.get('height', 50)
        message = f"Pillow adjustment: {angle}° (Height: {height}%)"
        logger.info(f"🛏️ {message}")
        return jsonify({'status': 'success', 'angle': angle, 'height': height, 'message': message})
    except Exception as e:
        logger.error(f"❌ Pillow control error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@device_bp.route('/speaker', methods=['POST'])
def control_speaker():
    """Play audio alert"""
    try:
        data = request.get_json()
        message = data.get('message', 'Alert!')
        action = data.get('action', 'play')
        duration = data.get('duration', 3000)
        log_message = f"Speaker alert: {message} (Action: {action}, Duration: {duration}ms)"
        logger.info(f"🔊 {log_message}")
        return jsonify({'status': 'success', 'message': message, 'action': action, 'duration': duration})
    except Exception as e:
        logger.error(f"❌ Speaker control error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@device_bp.route('/vibration', methods=['POST'])
def control_vibration():
    """Control bed vibration"""
    try:
        data = request.get_json()
        state = data.get('state', False)
        intensity = data.get('intensity', 50)
        message = f"Bed vibration: {'ON' if state else 'OFF'} (Intensity: {intensity}%)"
        logger.info(f"🛌 {message}")
        return jsonify({'status': 'success', 'state': state, 'intensity': intensity, 'message': message})
    except Exception as e:
        logger.error(f"❌ Vibration control error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@device_bp.route('/legs', methods=['POST'])
def control_legs():
    """Control leg elevation"""
    try:
        data = request.get_json()
        height = data.get('height', 50)
        angle = data.get('angle', 0)
        message = f"Leg elevation: {height}% (Angle: {angle}°)"
        logger.info(f"🦵 {message}")
        return jsonify({'status': 'success', 'height': height, 'angle': angle, 'message': message})
    except Exception as e:
        logger.error(f"❌ Leg control error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@device_bp.route('/status')
def get_device_status():
    """Get status of all devices"""
    try:
        status = {
            'fan': fan_service.get_fan_status(),
            'devices_connected': 5,
            'last_update': 'Just now'
        }
        return jsonify(status)
    except Exception as e:
        logger.error(f"❌ Device status error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500