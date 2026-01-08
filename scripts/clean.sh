#!/bin/bash
set -e

echo "Cleaning up..."

# Stop docker services
if command -v docker-compose &> /dev/null; then
    docker-compose down --volumes 2>/dev/null || true
    echo "✓ Stopped Docker services"
fi

# Clean backend
cd backend
rm -rf venv __pycache__ .pytest_cache *.pyc uploads
echo "✓ Cleaned backend"
cd ..

# Clean frontend
cd frontend
rm -rf build .dart_tool .flutter-plugins
echo "✓ Cleaned frontend"
cd ..

# Clean other
rm -rf coverage .coverage htmlcov

echo ""
echo "✓ Cleanup complete"
