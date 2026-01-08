#!/bin/bash
set -e

echo "================================"
echo "Phonetics App - Development Setup"
echo "================================"

# Check prerequisites
echo "✓ Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "✗ Git is not installed"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    exit 1
fi

if ! command -v flutter &> /dev/null; then
    echo "✗ Flutter is not installed"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed"
    exit 1
fi

echo "✓ All prerequisites found"

# Setup backend
echo ""
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

source venv/bin/activate
pip install -q -r requirements.txt
echo "✓ Backend dependencies installed"

cd ..

# Setup frontend
echo ""
echo "Setting up frontend..."
cd frontend

flutter pub get
echo "✓ Frontend dependencies installed"

cd ..

# Setup .env files
echo ""
echo "Setting up environment files..."

if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "✓ Created backend/.env (review and update if needed)"
fi

# Initialize git
if [ ! -d ".git" ]; then
    echo ""
    echo "Initializing git repository..."
    git init
    git config user.email "dev@example.com"
    git config user.name "Developer"
    git add .
    git commit -m "Initial commit: Phonetics app setup"
    echo "✓ Git repository initialized"
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "  1. Review and update backend/.env"
echo "  2. Start services: docker-compose up -d"
echo "  3. Run backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  4. Run frontend: cd frontend && flutter run"
echo ""
echo "Useful commands:"
echo "  - View API docs: http://localhost:8000/docs"
echo "  - View RethinkDB: http://localhost:8080"
echo "  - View backend logs: docker-compose logs -f backend"
echo ""
