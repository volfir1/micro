# routes/__init__.py
"""
Routes module for Sleep Monitoring Backend
Contains all API route definitions
"""

from .sensor_routes import sensor_bp
from .device_control import device_bp
from .led_routes import led_bp

__all__ = ['sensor_bp', 'device_bp', 'led_bp']