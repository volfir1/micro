#!/usr/bin/env python3
"""
WS2812B LED Strip Test - Cross-Platform Version
Works on Windows (simulation) and Raspberry Pi (real hardware)

For Windows: Shows LED effects in console for testing
For Raspberry Pi: Controls actual WS2812B LEDs

The code automatically detects the platform and uses appropriate method.

Windows Installation:
pip install colorama

Raspberry Pi Installation:
sudo pip3 install rpi_ws281x colorama

Run on Windows: python ws2812b_test.py
Run on Raspberry Pi: sudo python3 ws2812b_test.py
"""

import time
import colorsys
import platform
import os
import sys

# Detect platform and import appropriate libraries
IS_RASPBERRY_PI = False
try:
    # Try to detect Raspberry Pi
    with open('/proc/cpuinfo', 'r') as f:
        if 'raspberry pi' in f.read().lower():
            IS_RASPBERRY_PI = True
except:
    pass

# Import libraries based on platform
if IS_RASPBERRY_PI:
    try:
        from rpi_ws281x import PixelStrip, Color as RPiColor
        RPI_AVAILABLE = True
        print("Raspberry Pi detected - using real hardware control")
    except ImportError:
        RPI_AVAILABLE = False
        print("Raspberry Pi detected but rpi_ws281x not installed")
        print("Install with: sudo pip3 install rpi_ws281x")
else:
    RPI_AVAILABLE = False
    print("Windows/Other OS detected - using simulation mode")

# Try to import colorama for colored console output
try:
    from colorama import init, Fore, Back, Style
    init()
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    if not IS_RASPBERRY_PI:
        print("Tip: Install colorama for colored output: pip install colorama")

# LED strip configuration
LED_COUNT = 12          # Number of LED pixels
LED_PIN = 18           # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50    # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0        # Set to '1' for GPIOs 13, 19, 41, 45 or 53

class Color:
    """Universal Color class that works on both platforms"""
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green  
        self.blue = blue
        
    def __repr__(self):
        return f"Color({self.red}, {self.green}, {self.blue})"
    
    def to_rpi_color(self):
        """Convert to rpi_ws281x Color format"""
        if IS_RASPBERRY_PI and RPI_AVAILABLE:
            return RPiColor(self.red, self.green, self.blue)
        return self

class LEDStripBase:
    """Base class for LED strip control"""
    def __init__(self, led_count):
        self.led_count = led_count
        self.pixels = [Color(0, 0, 0)] * led_count
    
    def numPixels(self):
        return self.led_count
    
    def setPixelColor(self, pixel, color):
        if 0 <= pixel < self.led_count:
            self.pixels[pixel] = color
    
    def show(self):
        pass  # Override in subclasses
    
    def clear(self):
        for i in range(self.led_count):
            self.setPixelColor(i, Color(0, 0, 0))

class RaspberryPiLEDStrip(LEDStripBase):
    """Real hardware control for Raspberry Pi"""
    def __init__(self, led_count=LED_COUNT):
        super().__init__(led_count)
        self.strip = PixelStrip(led_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        print(f"Raspberry Pi LED strip initialized - {led_count} LEDs on GPIO {LED_PIN}")
    
    def setPixelColor(self, pixel, color):
        super().setPixelColor(pixel, color)
        if isinstance(color, Color):
            self.strip.setPixelColor(pixel, color.to_rpi_color())
        else:
            self.strip.setPixelColor(pixel, color)
    
    def show(self):
        self.strip.show()

class SimulatedLEDStrip(LEDStripBase):
    """Simulated LED strip for Windows/testing"""
    def __init__(self, led_count=LED_COUNT):
        super().__init__(led_count)
        self.clear_console()
        print(f"LED Strip Simulator - {led_count} LEDs")
    
    def clear_console(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show(self):
        """Display the current state of LEDs in console"""
        # Move cursor to top of console
        print("\033[H", end="")
        
        print(f"WS2812B LED Strip Simulator - {self.led_count} LEDs")
        print("=" * 60)
        
        # Display LEDs as colored blocks
        for i, pixel in enumerate(self.pixels):
            intensity = self.get_intensity(pixel)
            if COLORAMA_AVAILABLE:
                color_code = self.get_ansi_color(pixel)
                print(f"LED {i:2d}: {color_code}██{Style.RESET_ALL} RGB({pixel.red:3d},{pixel.green:3d},{pixel.blue:3d}) {intensity}")
            else:
                print(f"LED {i:2d}: ██ RGB({pixel.red:3d},{pixel.green:3d},{pixel.blue:3d}) {intensity}")
        
        print(f"\nPlatform: {platform.system()}")
        print("Press Ctrl+C to exit")
        print("=" * 60)
    
    def get_intensity(self, color):
        """Get visual intensity indicator"""
        total = color.red + color.green + color.blue
        if total == 0:
            return "○○○○○"
        elif total < 100:
            return "●○○○○"
        elif total < 200:
            return "●●○○○"
        elif total < 400:
            return "●●●○○"
        elif total < 600:
            return "●●●●○"
        else:
            return "●●●●●"
    
    def get_ansi_color(self, color):
        """Convert RGB to ANSI color code"""
        r, g, b = color.red, color.green, color.blue
        
        if r > 200 and g < 50 and b < 50:
            return Fore.RED + Back.RED
        elif g > 200 and r < 50 and b < 50:
            return Fore.GREEN + Back.GREEN
        elif b > 200 and r < 50 and g < 50:
            return Fore.BLUE + Back.BLUE
        elif r > 150 and g > 150 and b < 50:
            return Fore.YELLOW + Back.YELLOW
        elif r > 150 and b > 150 and g < 50:
            return Fore.MAGENTA + Back.MAGENTA
        elif g > 150 and b > 150 and r < 50:
            return Fore.CYAN + Back.CYAN
        elif r > 100 and g > 100 and b > 100:
            return Fore.WHITE + Back.WHITE
        else:
            return Fore.BLACK + Back.BLACK

class WS2812BController:
    def __init__(self):
        # Choose appropriate LED strip based on platform
        if IS_RASPBERRY_PI and RPI_AVAILABLE:
            self.strip = RaspberryPiLEDStrip(LED_COUNT)
        else:
            self.strip = SimulatedLEDStrip(LED_COUNT)
        
        self.strip.show()
        
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
                self.strip.clear()
                
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
        cycles = 2 if not IS_RASPBERRY_PI else 5  # Faster for simulation
        for j in range(256 * cycles):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
    
    def theater_chase_rainbow(self, wait_ms=50):
        """Rainbow movie theater light style chasing lights."""
        step = 8 if not IS_RASPBERRY_PI else 1  # Faster for simulation
        for j in range(0, 256, step):
            for q in range(3):  # 'q' counts from 0 to 2
                # Clear all pixels
                self.strip.clear()
                
                # Set every third pixel with rainbow color
                for i in range(q, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i, self.wheel((i + j) % 255))
                
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
    
    def clear_strip(self):
        """Turn off all pixels."""
        self.strip.clear()
        self.strip.show()
    
    def test_individual_leds(self):
        """Test each LED individually."""
        for i in range(self.strip.numPixels()):
            self.clear_strip()
            self.strip.setPixelColor(i, Color(255, 255, 255))  # White
            self.strip.show()
            time.sleep(0.3)
        self.clear_strip()
    
    def run_test_sequence(self):
        """Run the complete test sequence."""
        platform_name = "Raspberry Pi (Hardware)" if IS_RASPBERRY_PI and RPI_AVAILABLE else "Windows (Simulation)"
        print(f"Starting WS2812B test sequence on {platform_name}")
        
        try:
            # Test individual LEDs first
            self.test_individual_leds()
            
            while True:
                # Color wipe animations
                self.color_wipe(Color(255, 0, 0), 100)    # Red
                self.color_wipe(Color(0, 255, 0), 100)    # Green  
                self.color_wipe(Color(0, 0, 255), 100)    # Blue
                
                # Theater chase animations
                self.theater_chase(Color(127, 127, 127), 100)  # White
                self.theater_chase(Color(127, 0, 0), 100)      # Red
                self.theater_chase(Color(0, 0, 127), 100)      # Blue
                
                # Rainbow cycle
                self.rainbow(20)
                
                # Theater chase rainbow
                self.theater_chase_rainbow(100)
                
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
        finally:
            print("Clearing strip and exiting...")
            self.clear_strip()
            time.sleep(1)

def main():
    """Main function to run the LED test."""
    print("WS2812B LED Strip Test - Cross-Platform")
    print("=" * 50)
    
    if IS_RASPBERRY_PI:
        if RPI_AVAILABLE:
            print("Running on Raspberry Pi with real hardware control")
        else:
            print("Running on Raspberry Pi but rpi_ws281x not available")
            print("Install with: sudo pip3 install rpi_ws281x")
    else:
        print("Running on Windows/Other OS - using simulation mode")
    
    print("Press Ctrl+C to exit")
    print("=" * 50)
    
    try:
        controller = WS2812BController()
        controller.run_test_sequence()
    except Exception as e:
        print(f"Error: {e}")
        if IS_RASPBERRY_PI:
            print("Make sure you're running with sudo on Raspberry Pi")

if __name__ == "__main__":
    main()