#!/bin/bash
# Flutter App Factory Setup Script

echo "🚀 Flutter App Factory Setup"
echo "============================"

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check Flutter
echo "✓ Checking Flutter..."
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed"
    exit 1
fi

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "✓ Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "✓ Creating directories..."
mkdir -p templates/mission100
mkdir -p generated_apps
mkdir -p logs
mkdir -p data

# Setup environment file
echo "✓ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the app factory:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run: python cli/app_factory_cli.py --help"