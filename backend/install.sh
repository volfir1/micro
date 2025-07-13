#!/bin/bash

# Installation script for Sleep Monitoring Backend on Raspberry Pi
# Run this script to set up the complete backend system

echo "🚀 Setting up Sleep Monitoring Backend on Raspberry Pi..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip if not already installed
echo "🐍 Installing Python dependencies..."
sudo apt install -y python3 python3-pip python3-venv git

# Install system dependencies for sensors
echo "🔧 Installing system dependencies..."
sudo apt install -y sqlite3 libsqlite3-dev
sudo apt install -y libasound2-dev portaudio19-dev  # For audio processing
sudo apt install -y python3-rpi.gpio  # For GPIO control

# Create virtual environment
echo "🏠 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Install additional packages for Raspberry Pi
pip install RPi.GPIO
pip install adafruit-circuitpython-mpu6050
pip install pygame  # For audio alerts

# Set up database
echo "🗄️ Setting up database..."
python3 -c "from app import init_database; init_database()"

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/sleep-monitor.service > /dev/null <<EOF
[Unit]
Description=Sleep Monitoring Backend Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/sleep-monitor-backend
Environment=PATH=/home/pi/sleep-monitor-backend/venv/bin
ExecStart=/home/pi/sleep-monitor-backend/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "🔄 Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable sleep-monitor.service

# Set up log rotation
echo "📝 Setting up log rotation..."
sudo tee /etc/logrotate.d/sleep-monitor > /dev/null <<EOF
/var/log/sleep-monitor.log {
    daily
    missingok
    rotate 7
    compress
    create 644 pi pi
    postrotate
        systemctl reload sleep-monitor
    endscript
}
EOF

# Create .env file from example
if [ ! -f .env ]; then
    echo "📄 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual configuration!"
fi

# Set up GPIO permissions
echo "🔌 Setting up GPIO permissions..."
sudo usermod -a -G gpio pi
sudo usermod -a -G dialout pi

# Install additional tools
echo "🛠️ Installing development tools..."
sudo apt install -y screen htop

echo "✅ Installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file with your configuration"
echo "2. Connect your ESP32 to the Raspberry Pi"
echo "3. Update WiFi credentials in ESP32 code"
echo "4. Start the service: sudo systemctl start sleep-monitor"
echo "5. Check status: sudo systemctl status sleep-monitor"
echo "6. View logs: journalctl -u sleep-monitor -f"
echo ""
echo "🌐 The server will be available at:"
echo "   http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "🔧 To start development mode:"
echo "   source venv/bin/activate"
echo "   python app.py"
