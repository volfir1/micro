#!/usr/bin/env python3
"""
routes/led_routes.py - LED Strip Control Routes
Handles WS2812B LED strip control endpoints
"""

from flask import Blueprint, jsonify, request
import logging
from services import LEDService

logger = logging.getLogger(__name__)
led_bp = Blueprint('led', __name__, url_prefix='/api')
led_service = LEDService()

@led_bp.route('/led-control', methods=['POST'])
def led_control():
    """Main LED control endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Process LED command
        led_service.process_command(data)
        
        logger.info(f"💡 LED: {data}")
        return jsonify({
            'success': True,
            'status': led_service.get_status()['status']
        })
        
    except Exception as e:
        logger.error(f"❌ LED control error: {e}")
        return jsonify({'error': str(e)}), 500

@led_bp.route('/led-status', methods=['GET'])
def led_status():
    """Get current LED strip status"""
    try:
        status = led_service.get_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"❌ LED status error: {e}")
        return jsonify({'error': str(e)}), 500
        result = led_service.test_strip()
        logger.info(f"🧪 LED Test: {result['message']}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"❌ LED test error: {e}")
        return jsonify({'error': str(e)}), 500

@led_bp.route('/led-info', methods=['GET'])
def led_info():
    """Get LED strip hardware information"""
    try:
        info = led_service.get_hardware_info()
        return jsonify(info)
    except Exception as e:
        logger.error(f"❌ LED info error: {e}")
        return jsonify({'error': str(e)}), 500