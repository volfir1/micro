# Sleep Monitoring Backend

A Python Flask backend server for collecting sensor data from ESP32 microcontrollers and serving it to the React frontend.

## Features

- **REST API Endpoints** for all sensor data types
- **WebSocket Support** for real-time data streaming
- **SQLite Database** for data persistence
- **ESP32 Integration** via HTTP POST endpoints
- **Device Control** APIs for actuators (fan, pillow, speaker)
- **CORS Enabled** for React frontend communication

## API Endpoints

### Sensor Data Endpoints
- `GET /api/heart-rate` - Latest heart rate data
- `GET /api/breathing-data` - Latest breathing data  
- `GET /api/gyroscope-data` - Latest posture/position data
- `GET /api/weight-data` - Latest weight sensor data
- `GET /api/snore-data` - Latest snore detection data
- `GET /api/sleep-history` - Historical sleep sessions

### ESP32 Data Reception
- `POST /api/sensor-data` - Receive sensor data from ESP32

### Device Control
- `POST /api/control/fan` - Control fan state
- `POST /api/control/pillow` - Adjust pillow position
- `POST /api/control/speaker` - Play audio alerts

## Installation

1. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Run the server**:
```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

## ESP32 Integration

### Data Format
Send POST requests to `/api/sensor-data` with JSON payload:

```json
{
  "heart_rate": {
    "rate": 72,
    "status": "Normal",
    "min": 68,
    "max": 85,
    "average": 75,
    "variability": 12
  },
  "breathing": {
    "rate": 16,
    "rhythm": "Normal",
    "apneaEvents": 0
  },
  "gyroscope": {
    "pitch": 15.5,
    "roll": -10.2
  },
  "weight": {
    "weight": 150.5
  },
  "snore": {
    "isDetected": false,
    "frequency": 0,
    "duration": "0h 0m"
  }
}
```

### ESP32 Example Code
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* serverURL = "http://raspberry-pi-ip:5000/api/sensor-data";

void sendSensorData() {
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  StaticJsonDocument<200> doc;
  doc["heart_rate"]["rate"] = 72;
  doc["heart_rate"]["status"] = "Normal";
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpResponseCode = http.POST(jsonString);
  http.end();
}
```

## Frontend Integration

Update your React hooks to use real data:

```javascript
// In your hooks files, change:
const USE_REAL_DATA = true;
const API_ENDPOINT = 'http://raspberry-pi-ip:5000/api/heart-rate';
```

## Real-time Updates

The server supports WebSocket connections for real-time data streaming. Connect to:
```
ws://raspberry-pi-ip:5000
```

## Database Schema

The server automatically creates SQLite tables for:
- `heart_rate` - Heart rate measurements
- `breathing` - Breathing pattern data
- `gyroscope` - Posture and position data  
- `weight` - Weight sensor readings
- `snore_detection` - Snore detection events
- `sleep_sessions` - Complete sleep session records

## Development Mode

The server includes a simulation mode that generates fake sensor data for testing. This runs automatically in development. Comment out the simulation thread in production.

## Production Deployment

1. **Disable simulation mode** in `app.py`
2. **Set up proper GPIO** controls for actuators
3. **Configure WiFi** on Raspberry Pi
4. **Update ESP32 code** with Raspberry Pi IP address
5. **Set up systemd service** for auto-start

## Troubleshooting

- **Port 5000 already in use**: Change port in `app.py`
- **CORS errors**: Update origins in CORS configuration
- **Database errors**: Check file permissions for SQLite
- **ESP32 connection issues**: Verify network connectivity and IP addresses
