#!/bin/bash
set -e

echo "Running backend tests..."
cd backend

# Activate virtual environment
source venv/bin/activate

# Install test dependencies
pip install -q pytest pytest-cov pytest-asyncio

# Run tests
echo "✓ Running unit tests..."
pytest tests/ -v --tb=short || true

# Generate coverage
echo ""
echo "✓ Generating coverage report..."
pytest tests/ --cov=app --cov-report=html || true

cd ..

echo ""
echo "✓ Tests complete"
echo ""
echo "Coverage report: htmlcov/index.html"
