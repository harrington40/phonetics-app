#!/bin/bash

# Phonetics App - Setup Script for React-based Architecture
# This script sets up both web and mobile React apps

set -e

echo "🚀 Setting up Phonetics App (React + React Native)"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "\n${BLUE}Checking prerequisites...${NC}"

command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Please install Node.js 18+"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed."; exit 1; }

echo -e "${GREEN}✓ Prerequisites check passed${NC}"

# Setup Backend
echo -e "\n${BLUE}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please update backend/.env with your configuration"
fi

cd ..

# Setup React Web App
echo -e "\n${BLUE}Setting up React Web App...${NC}"
cd react-web

echo "Installing web app dependencies..."
npm install

echo "Creating .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

cd ..

# Setup React Native Mobile App
echo -e "\n${BLUE}Setting up React Native Mobile App...${NC}"
cd react-native-mobile

echo "Installing mobile app dependencies..."
npm install

echo -e "${GREEN}✓ Mobile app dependencies installed${NC}"

# iOS-specific setup (only on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "\n${BLUE}Setting up iOS (detected macOS)...${NC}"
    if command -v pod >/dev/null 2>&1; then
        cd ios
        echo "Installing iOS pods..."
        pod install
        cd ..
        echo -e "${GREEN}✓ iOS setup complete${NC}"
    else
        echo "⚠️  CocoaPods not found. Install it for iOS development: sudo gem install cocoapods"
    fi
fi

cd ..

echo -e "\n${GREEN}=================================================="
echo "✅ Setup Complete!"
echo "==================================================${NC}"

echo -e "\n📋 Next Steps:"
echo "1. Start the backend:"
echo "   cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo "2. Start the web app:"
echo "   cd react-web && npm run dev"
echo ""
echo "3. Start the mobile app:"
echo "   cd react-native-mobile && npm run android  # or npm run ios"
echo ""
echo "📖 Read the README files in each directory for more details"
