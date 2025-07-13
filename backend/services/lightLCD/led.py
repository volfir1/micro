#!/usr/bin/env python3
"""
WS2812B LED Strip Test for Raspberry Pi
Converted from Arduino code for testing WS2812B LEDs

Hardware Requirements:
- Connect WS2812B data pin to GPIO 18 (PWM0) on Raspberry Pi
- Add 1000µF capacitor between LED strip + and - connections
- Use 300-500 ohm resistor on data line
- Consider logic level converter for 5V strips with 3.3V Pi

Installation:
sudo pip3 install rpi_ws281x
"""

import time
import colorsys
from datetime import datetime

# Try to import Raspberry Pi LED library, fallback to mock for development
try:
    from rpi_ws281x import PixelStrip, Color
    HAS_RPI_WS281X = True
except ImportError:
    HAS_RPI_WS281X = False
    # Mock classes for development
    class PixelStrip:
        def __init__(self, *args, **kwargs):
            pass
        def begin(self):
            pass
        def setPixelColor(self, *args):
            pass
        def show(self):
            pass
        def getPixels(self):
            return 30
    
    def Color(r, g, b):
        return (r << 16) | (g << 8) | b
from datetime import datetime

# LED strip configuration
LED_COUNT = 12          # Number of LED pixels
LED_PIN = 18           # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0        # Set to '1' for GPIOs 13, 19, 41, 45 or 53

class WS2812BTest:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Initialize the library (must be called once before other functions)
        self.strip.begin()
        
    def color_wipe(self, color, wait_ms=50):
        """Wipe color across display one pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
    
    def theater_chase(self, color, wait_ms=50):
        """Movie theater light style chasing lights."""
        for j in range(10):  # Repeat 10 times
            for q in range(3):  # 'q' counts from 0 to 2
                # Clear all pixels
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, 0)
                
                # Set every third pixel starting from q
                for i in range(q, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i, color)
                
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
    
    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
    
    def rainbow(self, wait_ms=10):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * 5):  # 5 cycles of all colors on wheel
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
    
    def rainbow_cycle(self, wait_ms=10):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256 * 5):  # 5 cycles of all colors on wheel
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(((i * 256 // self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
    
    def theater_chase_rainbow(self, wait_ms=50):
        """Rainbow movie theater light style chasing lights."""
        for j in range(256):  # Cycle through all 256 colors
            for q in range(3):  # 'q' counts from 0 to 2
                # Clear all pixels
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, 0)
                
                # Set every third pixel with rainbow color
                for i in range(q, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i, self.wheel((i + j) % 255))
                
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color values."""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color(int(r * 255), int(g * 255), int(b * 255))
    
    def clear_strip(self):
        """Turn off all pixels."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
    
    def run_test_sequence(self):
        """Run the complete test sequence similar to Arduino version."""
        print("Starting WS2812B LED test sequence...")
        
        try:
            while True:
                print("Color wipe animations...")
                self.color_wipe(Color(255, 0, 0), 50)    # Red
                self.color_wipe(Color(0, 255, 0), 50)    # Green  
                self.color_wipe(Color(0, 0, 255), 50)    # Blue
                
                print("Theater chase animations...")
                self.theater_chase(Color(127, 127, 127), 50)  # White
                self.theater_chase(Color(127, 0, 0), 50)      # Red
                self.theater_chase(Color(0, 0, 127), 50)      # Blue
                
                print("Rainbow cycle...")
                self.rainbow(10)
                
                print("Theater chase rainbow...")
                self.theater_chase_rainbow(50)
                
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
        finally:
            print("Clearing strip and exiting...")
            self.clear_strip()

class SimpleWS2812BController:
    """Simple LED controller for compatibility"""
    def __init__(self):
        self.current_color = (0, 0, 0)
        self.brightness = 0.5
        
    def set_color(self, r, g, b):
        """Set LED color"""
        self.current_color = (r, g, b)
        
    def set_brightness(self, brightness):
        """Set LED brightness"""
        self.brightness = max(0, min(1, brightness))
        
    def turn_off(self):
        """Turn off LEDs"""
        self.current_color = (0, 0, 0)

class LEDService:
    """LED Service for sleep monitoring"""
    def __init__(self):
        self.controller = SimpleWS2812BController()
        self.current_data = {
            'isOn': False,
            'color': {'r': 0, 'g': 0, 'b': 0},
            'brightness': 50,
            'pattern': 'solid',
            'timestamp': None
        }
        
    def update_data(self, data):
        """Update LED data"""
        try:
            self.current_data.update({
                'isOn': data.get('isOn', False),
                'color': data.get('color', {'r': 0, 'g': 0, 'b': 0}),
                'brightness': data.get('brightness', 50),
                'pattern': data.get('pattern', 'solid'),
                'timestamp': datetime.now().isoformat()
            })
            
            # Apply changes to controller
            if self.current_data['isOn']:
                color = self.current_data['color']
                self.controller.set_color(color['r'], color['g'], color['b'])
                self.controller.set_brightness(self.current_data['brightness'] / 100)
            else:
                self.controller.turn_off()
                
            return True
        except Exception as e:
            print(f"LED update error: {e}")
            return False
            
    def get_current_data(self):
        """Get current LED status"""
        return self.current_data.copy()
        
    def set_color(self, r, g, b):
        """Set LED color directly"""
        self.update_data({
            'isOn': True,
            'color': {'r': r, 'g': g, 'b': b},
            'brightness': self.current_data['brightness'],
            'pattern': 'solid'
        })
        
    def turn_off(self):
        """Turn off LEDs"""
        self.update_data({
            'isOn': False,
            'color': {'r': 0, 'g': 0, 'b': 0},
            'brightness': 0,
            'pattern': 'off'
        })

def main():
    """Main function to run the LED test."""
    print("WS2812B LED Strip Test for Raspberry Pi")
    print("Press Ctrl+C to exit")
    
    try:
        led_test = WS2812BTest()
        led_test.run_test_sequence()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you're running as root (sudo python3 script.py)")
        print("and that the rpi_ws281x library is installed")

if __name__ == "__main__":
    main()