# Setup Guide

## System Requirements

- **OS**: Linux, macOS, or Windows (WSL2 recommended)
- **RAM**: 8GB minimum
- **Disk**: 10GB free space
- **CPU**: 2+ cores

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourrepo/phonetics-app.git
cd phonetics-app
```

### 2. Install Prerequisites

#### macOS
```bash
# Using Homebrew
brew install flutter python@3.11 rethinkdb docker docker-compose

# Or using Homebrew Cask for Docker Desktop
brew install --cask docker
```

#### Ubuntu/Debian
```bash
# Update package lists
sudo apt-get update

# Install Flutter
git clone https://github.com/flutter/flutter.git -b stable ~/flutter
export PATH="$PATH:$HOME/flutter/bin"

# Install Python
sudo apt-get install -y python3.11 python3.11-venv

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Install RethinkDB
wget https://download.rethinkdb.com/dist/ubuntu/xenial/rethinkdb.list
sudo apt-get install -y rethinkdb
```

#### Windows (WSL2)
```bash
# In WSL2 Ubuntu terminal, follow Linux instructions above
# Ensure Docker Desktop is running with WSL2 backend
```

### 3. Setup Environment Variables

```bash
# In project root
cp backend/.env.example backend/.env

# Edit as needed
nano backend/.env
```

### 4. Verify Installation

```bash
flutter --version
python3 --version
docker --version
docker-compose --version

# Test RethinkDB connection
rethinkdb --version
```

## Development Setup

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# Wait for services to initialize (~30 seconds)
sleep 30

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Access services:
# - RethinkDB Admin: http://localhost:8080
# - API Docs: http://localhost:8000/docs
# - API Health: http://localhost:8000/api/health
```

### Manual Setup (Without Docker)

#### Start RethinkDB
```bash
# macOS/Linux
rethinkdb --port 28015 --bind 127.0.0.1

# Or with Docker
docker run -d -p 28015:28015 -p 29015:29015 -p 8080:8080 rethinkdb:2.4.2
```

#### Start Backend
```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
```

#### Start Frontend
```bash
cd frontend

# Get dependencies
flutter pub get

# Run on device/emulator
flutter run

# Or run on web
flutter run -d web
```

## Project Configuration

### Backend Configuration (backend/.env)

```env
# RethinkDB
RDB_HOST=localhost
RDB_PORT=28015
RDB_DB=phonetics

# Server
PORT=8000
WORKERS=4

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration (frontend/lib/config/)

Create `config.dart`:
```dart
const String API_BASE_URL = 'http://127.0.0.1:8000';
const int API_TIMEOUT_MS = 30000;
const String APP_VERSION = '1.0.0';
```

## Running Tests

### Backend Unit Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_lessons.py -v

# Run specific test
pytest tests/test_lessons.py::test_get_lesson -v
```

### Frontend Tests

```bash
cd frontend

# Run all tests
flutter test

# Run specific test file
flutter test test/widgets/cartoon_animal_test.dart

# Run with coverage
flutter test --coverage
```

### Integration Tests

```bash
# Ensure docker-compose is running
docker-compose up -d

# Wait for services
sleep 10

# Run integration tests
bash scripts/test-integration.sh
```

## Debugging

### Backend Debugging

#### Using print/logging
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

#### Using VS Code debugger
1. Install Python extension
2. Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--port",
                "8000"
            ],
            "jinja": true
        }
    ]
}
```
3. Press F5 to start debugging

### Frontend Debugging

#### Using DevTools
```bash
flutter pub global activate devtools
devtools
flutter run --enable-software-switch --enable-dart-profiling
```

#### Using VS Code
1. Set breakpoints in `lib/main.dart`
2. Press F5 or Run > Start Debugging
3. Use Debug Console for expressions

### Docker Debugging

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f rethinkdb

# Execute command in container
docker-compose exec backend bash

# Inspect RethinkDB
docker-compose exec rethinkdb rethinkdb-admin -j
```

## Monitoring

### RethinkDB Admin UI

Access at http://localhost:8080

- Monitor cluster health
- Query performance
- Data browser
- Real-time replication stats

### Backend Metrics

```bash
# Check API health
curl http://localhost:8000/api/health

# View API documentation
open http://localhost:8000/docs

# Check logs
docker-compose logs backend -f --tail=50
```

### System Resources

```bash
# Monitor Docker containers
docker stats

# View memory usage
docker-compose exec backend ps aux

# Check disk usage
df -h
du -sh uploads/
```

## Common Issues & Solutions

### Issue: RethinkDB Connection Refused
```bash
# Solution: Ensure RethinkDB is running
docker-compose ps rethinkdb

# Restart if needed
docker-compose restart rethinkdb
```

### Issue: Backend Port 8000 Already in Use
```bash
# Solution: Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue: Flutter Can't Find Devices
```bash
# Solution: List available devices
flutter devices

# For Android emulator
emulator -list-avds
emulator -avd <emulator_name>

# For iOS simulator (macOS only)
open -a Simulator

# For web
flutter run -d web
```

### Issue: Module Not Found Error (Python)
```bash
# Solution: Ensure virtual environment is activated
source backend/venv/bin/activate

# Re-install dependencies
pip install -r backend/requirements.txt
```

### Issue: Docker Compose Permission Denied
```bash
# Solution: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Then try again
docker-compose up
```

## Code Style & Linting

### Backend

```bash
cd backend
source venv/bin/activate

# Install linting tools
pip install flake8 black isort

# Check code style
flake8 app --max-line-length=120

# Auto-format code
black app/

# Sort imports
isort app/
```

### Frontend

```bash
cd frontend

# Analyze code
flutter analyze

# Format code
flutter format lib/ test/

# Use custom dart rules
analysis_options.yaml
```

## Performance Optimization

### Backend

1. **Enable Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
async def get_lesson(lesson_id: str):
    return await db.get_by_id("lessons", lesson_id)
```

2. **Database Indexing** (already done in schema)
3. **Connection Pooling** (handled by RethinkDB driver)

### Frontend

1. **Code Splitting** - Use lazy loading routes
2. **Image Optimization** - Use appropriate image sizes
3. **Build Optimization**
```bash
flutter build apk --split-per-abi --obfuscate --split-debug-info=./debug_info
```

## Deployment

### Docker Registry Setup

1. Create account on Docker Hub or ECR
2. Login: `docker login`
3. Tag image: `docker tag phonetics-backend:latest yourrepo/phonetics-backend:latest`
4. Push: `docker push yourrepo/phonetics-backend:latest`

### Environment-Specific .env Files

```bash
# Development
cp backend/.env.example backend/.env.dev

# Staging
cp backend/.env.example backend/.env.staging

# Production
cp backend/.env.example backend/.env.prod
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/phoneme-alignment

# Make changes
git add .
git commit -m "feat: add phoneme alignment"

# Push and create PR
git push origin feature/phoneme-alignment

# After PR approval, merge
git checkout main
git merge feature/phoneme-alignment
git push origin main
```

## Support & Resources

- **Flutter Docs**: https://flutter.dev/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **RethinkDB Docs**: https://rethinkdb.com/docs
- **Docker Docs**: https://docs.docker.com/
- **Jenkins Docs**: https://www.jenkins.io/doc/

---

Last Updated: December 2024
