# 🔌 Raspberry Pi Pin Configuration Guide

## 📍 **Current Pin Assignments (Already Configured in Code)**

Your backend services already have pin assignments built-in. Here's what each device uses:

### **🎛️ Output Devices (Actuators)**
```
GPIO Pin 18 - LED Strip (WS2812B)
GPIO Pin 19 - Fan Control (PWM)
GPIO Pin 20 - Bed Vibration Motor
GPIO Pin 21 - Pillow Servo Motor
GPIO Pin 22 - Leg Elevation Servo
GPIO Pin 23 - Speaker/Buzzer
```

### **📡 Input Devices (Sensors)**
```
I2C Bus (SDA=GPIO 2, SCL=GPIO 3):
  - Heart Rate Sensor (MAX30102)
  - Gyroscope/Accelerometer (MPU6050)

Analog Pins (via MCP3008 ADC):
  - Weight/Pressure Sensor (Load Cell + HX711)
  - Breathing Sensor (Strain Gauge)

Digital Pins:
  - GPIO 24 - Microphone for Snore Detection
  - GPIO 25 - Backup sensor input
```

## 🔧 **Physical Wiring Guide**

### **Power Connections:**
- **3.3V** → Sensor VCC (Heart Rate, Gyroscope)
- **5V** → Actuator VCC (Servos, Fan, LED Strip)
- **GND** → All GND connections

### **Data Connections:**
```
Raspberry Pi Pin → Device
=====================================
GPIO 2 (SDA)     → Heart Rate SDA, Gyro SDA
GPIO 3 (SCL)     → Heart Rate SCL, Gyro SCL
GPIO 18          → LED Strip Data In
GPIO 19          → Fan Control Input
GPIO 20          → Vibration Motor +
GPIO 21          → Pillow Servo Signal
GPIO 22          → Leg Servo Signal
GPIO 23          → Speaker/Buzzer +
GPIO 24          → Microphone Data
```

## ⚠️ **Important Notes:**

1. **You DON'T need to change any code** - pins are already configured!
2. **Multiple devices can share I2C** (pins 2 & 3) with different addresses
3. **Use appropriate resistors** for voltage level conversion if needed
4. **Test one device at a time** when connecting
5. **Power management**: Use external power for high-current devices (LED strip, servos)

## 🚀 **Quick Start Steps:**

1. **Start Simple**: Connect just the LED strip first (GPIO 18)
2. **Test**: Run your existing code - it should work immediately!
3. **Add Gradually**: Connect one sensor/actuator at a time
4. **Monitor**: Watch the backend logs to see real sensor data

## 🔧 **Code Changes Needed (Minimal)**

To switch from simulation to real hardware, just uncomment these lines in each service:

```python
# Current (simulation):
# import RPi.GPIO as GPIO  # ← Uncomment this

# Change from:
if USE_SIMULATION:
    return self._generate_mock_data()

# To:
# Real sensor reading code (already written!)
```

The pin assignments are already perfect - no changes needed! 🎯
