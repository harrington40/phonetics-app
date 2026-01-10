#!/bin/bash

# Start all services for development

set -e

echo "🚀 Starting Phonetics App Services"
echo "==================================="

# Function to cleanup background processes on exit
cleanup() {
    echo "Shutting down services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo "✓ Backend started on http://localhost:8000"

# Wait a bit for backend to start
sleep 3

# Start web app
echo "Starting web app..."
cd react-web
npm run dev &
WEB_PID=$!
cd ..

echo "✓ Web app starting on http://localhost:3000"

echo ""
echo "==================================="
echo "✅ All services started!"
echo "==================================="
echo "Backend: http://localhost:8000"
echo "Web App: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for all background processes
wait
