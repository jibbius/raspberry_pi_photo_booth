#!/bin/bash
# Setup script for Raspberry Pi Photo Booth
# This script creates a virtual environment and installs dependencies

set -e  # Exit on any error

echo "🎪 Raspberry Pi Photo Booth Setup"
echo "=================================="

# Check if we're on a Raspberry Pi or similar system
if command -v raspi-config &> /dev/null; then
    echo "✓ Detected Raspberry Pi system"
    ON_RPI=true
else
    echo "ℹ️  Not on Raspberry Pi - some features will be simulated"
    ON_RPI=false
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install system packages (Raspberry Pi only)
if [ "$ON_RPI" = true ]; then
    echo "📋 Installing system packages..."
    sudo apt update
    sudo apt install -y libcamera-apps python3-libcamera python3-kms++
fi

# Install Python dependencies
echo "📥 Installing Python dependencies..."
if [ "$ON_RPI" = true ]; then
    echo "Installing Raspberry Pi specific requirements..."
    pip install -r requirements-pi.txt
else
    echo "Installing development requirements..."
    pip install -r requirements.txt
fi

# Test the installation
echo "🧪 Testing installation..."
python test_photobooth.py

# Create initial config if it doesn't exist
if [ ! -f "camera-config.yaml" ]; then
    echo "⚙️  Creating initial configuration..."
    cp camera-config.example.yaml camera-config.yaml
    echo "✓ Configuration file created: camera-config.yaml"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Edit camera-config.yaml if needed"
echo ""
if [ "$ON_RPI" = true ]; then
    echo "3. Connect your hardware (camera + buttons)"
    echo ""
    echo "4. Run the photo booth:"
    echo "   python camera.py"
else
    echo "3. Run in test mode:"
    echo "   python camera.py"
    echo "   (Set TESTMODE_AUTOPRESS_BUTTON: True in config for simulation)"
fi
echo ""