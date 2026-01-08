#!/bin/bash

# PhonicsLearn Backend Setup Script
echo "🚀 Setting up PhonicsLearn backend..."

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn pydantic sqlalchemy psycopg2-binary alembic
pip install stripe sendgrid python-dotenv aiofiles numpy gtts python-multipart
pip install email-validator

echo "✅ Backend setup complete!"
echo ""
echo "To start the server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
