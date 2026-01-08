#!/bin/bash
set -e

echo "Starting services with docker-compose..."

# Check if docker-compose file exists
if [ ! -f "docker-compose.yml" ]; then
    echo "✗ docker-compose.yml not found"
    exit 1
fi

# Start services
docker-compose up -d

echo "✓ Services started"
echo ""
echo "Waiting for services to initialize..."
sleep 5

# Check status
echo ""
echo "Service Status:"
docker-compose ps

echo ""
echo "✓ Services are running!"
echo ""
echo "Access:"
echo "  RethinkDB Admin: http://localhost:8080"
echo "  API Docs: http://localhost:8000/docs"
echo "  API Health: http://localhost:8000/api/health"
echo ""
echo "View logs:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f rethinkdb"
echo ""
echo "Stop services:"
echo "  docker-compose down"
echo ""
