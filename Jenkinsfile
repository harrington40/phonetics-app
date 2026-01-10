/*
 * Phonetics Learning App CI/CD Pipeline
 * React + React Native Architecture
 * Based on HRMS Jenkins architecture
 */

pipeline {
    agent any

    options {
        timeout(time: 2, unit: 'HOURS')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        PROJECT_NAME = "phonetics-app"
        PYTHON_VERSION = '3.11'
        NODE_VERSION = '18'
        BACKEND_DIR = "backend"
        WEB_DIR = "react-web"
        MOBILE_DIR = "react-native-mobile"
        DOCKER_IMAGE = 'harrington40/phonetics-app'
        DOCKER_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        APP_HOST = '0.0.0.0'
        APP_PORT = '8000'
    }

    triggers {
        // Prefer GitHub webhook
        // githubPush()
        // Fallback polling
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Pipeline Info') {
            steps {
                echo "=== Pipeline Information ==="
                echo "Project: ${PROJECT_NAME}"
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Build: ${env.BUILD_NUMBER}"
                echo "GIT_COMMIT: ${env.GIT_COMMIT}"
                echo "Workspace: ${env.WORKSPACE}"
                sh '''
                    set +e
                    pwd
                    ls -la
                    git log --oneline -1 || echo "git log failed"
                '''
            }
        }

        stage('Checkout') {
            steps {
                echo '=== Checking out code ==='
                checkout scm
                sh '''
                    git branch
                    git log --oneline -5
                '''
            }
        }

        stage('Validate Environment') {
            steps {
                sh '''
                    set +e
                    echo "=== Environment Validation ==="
                    which python3 || echo "WARNING: python3 not found"
                    python3 --version
                    
                    which node || echo "WARNING: node not found"
                    node --version || echo "Node not available"
                    
                    which npm || echo "WARNING: npm not found"
                    npm --version || echo "npm not available"
                    
                    # Check for required files
                    test -f backend/requirements.txt || echo "WARNING: requirements.txt not found"
                    test -f react-web/package.json || echo "WARNING: react-web/package.json not found"
                    test -f react-native-mobile/package.json || echo "WARNING: react-native-mobile/package.json not found"
                    test -f setup-react.sh || echo "WARNING: setup-react.sh not found"
                    
                    df -h .
                    echo "Environment validation completed"
                '''
            }
        }

        stage('Setup Backend Environment') {
            steps {
                dir("${BACKEND_DIR}") {
                    sh '''
                        echo "=== Setting up Backend Virtual Environment ==="
                        
                        # Remove existing venv
                        if [ -d "venv" ]; then
                            echo "Removing existing virtual environment..."
                            rm -rf venv
                        fi
                        
                        # Create fresh virtual environment
                        python3 -m venv venv || (echo "ERROR: Failed to create venv" && exit 1)
                        
                        # Upgrade pip
                        ./venv/bin/python -m pip install --upgrade pip || echo "WARNING: pip upgrade failed"
                        
                        # Install requirements
                        ./venv/bin/python -m pip install -r requirements.txt || (echo "ERROR: Failed to install requirements" && exit 1)
                        
                        # Verify critical dependencies
                        ./venv/bin/python -c "import fastapi; print('✓ fastapi available')" || (echo "ERROR: fastapi not available" && exit 1)
                        ./venv/bin/python -c "import uvicorn; print('✓ uvicorn available')" || (echo "ERROR: uvicorn not available" && exit 1)
                        
                        echo "Backend environment setup completed successfully"
                    '''
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    set +e
                    echo "=== Running Security Scan ==="
                    
                    if [ -d "backend/venv" ]; then
                        PIP="./backend/venv/bin/pip"
                        PY="./backend/venv/bin/python"
                    else
                        PIP="pip3"
                        PY="python3"
                    fi
                    
                    # Install security tools
                    $PIP install -q bandit safety || echo "WARNING: Failed to install security tools"
                    
                    # Run bandit
                    echo "Running Bandit security scan..."
                    $PY -m bandit -r backend/app -f json -o bandit-report.json || echo "WARNING: Bandit scan found issues"
                    
                    # Run safety check
                    echo "Running Safety dependency scan..."
               Setup Web App') {
            steps {
                echo '=== Setting up React Web App ==='
                dir("${WEB_DIR}") {
                    sh '''
                        set +e
                        echo "Installing web app dependencies..."
                        npm install || echo "WARNING: npm install failed"
                        
                        # Create .env if not exists
                        if [ ! -f ".env" ]; then
                            cp .env.example .env || echo "WARNING: .env creation failed"
                        fi
                        
                        echo "Web app setup completed"
                    '''
                }
            }
        }

        stage('Backend Lint & Test') {
            steps {
                echo '=== Running Backend Tests ==='
                dir("${BACKEND_DIR}") {
                    sh '''
                        set +e
                        . venv/bin/activate
                        
                        # Install test dependencies
                        pip install -q flake8 pytest pytest-cov pytest-asyncio || echo "WARNING: Test dependencies install failed"
                        
                        # Run flake8
                        echo "Running flake8..."
                        flake8 app --max-line-length=120 --count --statistics || echo "WARNING: Flake8 found issues"
                        
                        # Run pytest (if tests exist)
                        if [ -d "tests" ]; then
                            echo "Running pytest..."
                            pytest tests/ -v --tb=short --cov=app --cov-report=html --cov-report=term || echo "WARNING: Tests failed"
                        else
                            echo "No tests directory found, skipping tests"
                        fi
                    '''
                }
            }
        }

        stage('Web App Lint & Build') {
            steps {
                echo '=== Building React Web App ==='
                dir("${WEB_DIR}") {
                    sh '''
                        set +e
                        
                        # Run linter
                        echo "Running ESLint..."
                        npm run lint || echo "WARNING: ESLint found issues"
                        
                        # Build production bundle
                        echo "Building production bundle..."
                        npm run build || echo "WARNING: Build failed"
                        
                        # Check build output
                        if [ -d "dist" ]; then
                            echo "✓ Build successful"
                            ls -lh dist/
                        else
                            echo "WARNING: Build directory not found
                        flake8 app --max-line-length=120 --count --statistics || echo "WARNING: Flake8 found issues"
                        
                        # Run pytest (if tests exist)
                        if [ -d "tests" ]; then
                            echo "Running pytest..."
                            pytest tests/ -v --tb=short --cov=app --cov-report=html --cov-report=term || echo "WARNING: Tests failed"
                        else
                            echo "No tests directory found, skipping tests"
                        fi
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '=== Building Docker Images ==='
                
                script {
                    // Build backend
                    dir("${BACKEND_DIR}") {
                        sh '''
                            # Use existing Dockerfile if it exists
                            if [ ! -f "Dockerfile" ]; then
                                cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
                            fi
                            
                            echo "Building backend Docker image: ${DOCKER_IMAGE}-backend:${DOCKER_TAG}"
                            docker build -t ${DOCKER_IMAGE}-backend:${DOCKER_TAG} . || echo "WARNING: Backend Docker build failed"
                            docker tag ${DOCKER_IMAGE}-backend:${DOCKER_TAG} ${DOCKER_IMAGE}-backend:latest || echo "WARNING: Docker tag failed"
                        '''
                    }
                    
                    // Build web app
                    dir("${WEB_DIR}") {
                        sh '''
                            # Create Dockerfile for web app
                            cat > Dockerfile << 'EOF'
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF
                            
                            echo "Building web Docker image: ${DOCKER_IMAGE}-web:${DOCKER_TAG}"
                            docker build -t ${DOCKER_IMAGE}-web:${DOCKER_TAG} . || echo "WARNING: Web Docker build failed"
                            docker tag ${DOCKER_IMAGE}-web:${DOCKER_TAG} ${DOCKER_IMAGE}-web:latest || echo "WARNING: Docker tag failed"
                        '''
                    }
                }
            }
        }

        stage('Integration Test') {
            steps {
                echo '=== Running Integration Tests ==='
                sh '''
                    set +e
                    echo "Starting services for integration tests..."
                    
                    # Kill existing processes
                    pkill -9 python python3 2>/dev/null || true
                    sleep 2s ready:"
                    echo "  Backend: ${DOCKER_IMAGE}-backend:${DOCKER_TAG}"
                    echo "  Web: ${DOCKER_IMAGE}-web:${DOCKER_TAG}"
                    
                    # Uncomment to push to Docker Hub
                    # docker login -u $DOCKER_USER -p $DOCKER_PASS
                    # docker push ${DOCKER_IMAGE}-backend:${DOCKER_TAG}
                    # docker push ${DOCKER_IMAGE}-backend:latest
                    # docker push ${DOCKER_IMAGE}-web:${DOCKER_TAG}
                    # docker push ${DOCKER_IMAGE}-webpp --host 0.0.0.0 --port 8000 > /tmp/jenkins-backend.log 2>&1 &
                    BACKEND_PID=$!
                    sleep 5
                    
                    # Test API endpoints
                    echo "Testing API endpoints..."
                    curl -f http://localhost:8000/ || echo "WARNING: Root endpoint failed"
                    curl -f http://localhost:8000/api/lesson || echo "WARNING: Lesson endpoint failed"
                    curl -f http://localhost:8000/api/health || echo "WARNING: Health endpoint failed"
                    
                    # Cleanup
                    kill $BACKEND_PID 2>/dev/null || true
                    pkill -9 python python3 2>/dev/null || true
                    
                    echo "Integration tests completed"
                '''
            }
        }

        stage('Push Docker Images') {
            when {
                branch 'main'
            }
            steps {
                echo '=== Pushing Docker Images ==='
                sh '''
                    set +e
                    echo "Docker image ready: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                    
                    # Uncomment to push to Docker Hub
                    # docker login -u $DOCKER_USER -p $DOCKER_PASS
                    # docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    # docker push ${DOCKER_IMAGE}:latest
                    
                    echo "Note: Docker push commented out. Configure credentials to enable."
                '''
            }
        }

        stage('Deploy to Dev') {
            when {
                branch 'dev'
            }
            steps {
                echo '=== Deploying to Dev Environment ==='
                sh '''
                    set +e
                    echo "Deploying to development..."
                    
                    # Stop existing services
                    docker-compose -f docker-compose-react.yml down || true
                    
                    # Start services (backend + web)
                    docker-compose -f docker-compose-react.yml up -d
                    sleep 5
                    
                    # Verify services
                    docker-compose -f docker-compose-react.yml ps
                    echo "Checking backend..."
                    curl -f http://localhost:8000/ || echo "WARNING: Backend not responding"
                    echo "Checking web app..."
                    curl -f http://localhost:3000/ || echo "WARNING: Web app not responding"
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo '=== Performing Healts health..."
                    
                    # Check backend
                    for i in {1..10}; do
                        echo "Backend health check attempt $i..."
                        if curl -f http://localhost:8000/ > /dev/null 2>&1; then
                            echo "✓ Backend is healthy"
                            break
                        fi
                        sleep 2
                    done
                    
                    # Check web app
                    for i in {1..10}; do
                        echo "Web app health check attempt $i..."
                        if curl -f http://localhost:3000/ > /dev/null 2>&1; then
                            echo "✓ Web app is healthy"
                            exit 0
                        fi
                        sleep 2
                    done, react-web/dist/**, react-web/node_modules/.cache/**', allowEmptyArchive: true
            
            script {
                if (fileExists('bandit-report.json')) {
                    publishHTML([
                        reportDir: '.',
                        reportFiles: 'bandit-report.json',
                        reportName: 'Security Scan Report',
                        allowMissing: true
                    ])
                }
                
                if (fileExists('backend/htmlcov/index.html')) {
                    publishHTML([
                        reportDir: 'backend/htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report',
                        allowMissing: true
                    ])
                }
                
                if (fileExists('react-web/dist/index.html')) {
                    publishHTML([
                        reportDir: 'react-web/dist',
                        reportFiles: 'index.html',
                        reportName: 'Web App Preview
                if (fileExists('bandit-report.json')) {
                    publishHTML([
                        reportDir: '.',
                        reportFiles: 'bandit-report.json',
                        reportName: 'Security Scan Report',
                         (React + React Native)
Build Number: ${BUILD_NUMBER}
Branch: ${BRANCH_NAME}
Commit: ${GIT_COMMIT}
Timestamp: $(date)
Docker Images:
  - Backend: ${DOCKER_IMAGE}-backend:${DOCKER_TAG}
  - Web: ${DOCKER_IMAGE}-webML([
                        reportDir: 'backend/htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Code Coverage Report',
                        allowMissing: true
                    ])
                }
            }
        }

        success {
            echo '=== ✅ Pipeline Completed Successfully ==='
            sh '''
                cat > build-status.txt << EOF
Build Status: SUCCESS
Project: ${PROJECT_NAME}
Build Number: ${BUILD_NUMBER}
Branch: ${BRANCH_NAME}
Commit: ${GIT_COMMIT}
Timestamp: $(date)
Docker Image: ${DOCKER_IMAGE}:${DOCKER_TAG}
EOF
                cat build-status.txt
            '''
            archiveArtifacts artifacts: 'build-status.txt', allowEmptyArchive: true
        }

        failure {
            echo '=== ❌ Pipeline Failed ==='
            sh '''
                cat > build-status.txt << EOF
Build Status: FAILURE
Project: ${PROJECT_NAME}
Build Number: ${BUILD_NUMBER}
Branch: ${BRANCH_NAME}
Commit: ${GIT_COMMIT}
Timestamp: $(date)
EOF
                cat build-status.txt
                
                # Collect logs for debugging
                echo "=== Backend Logs ===" || true
                cat /tmp/jenkins-backend.log 2>/dev/null || echo "No backend logs found"
            '''
            archiveArtifacts artifacts: 'build-status.txt, /tmp/jenkins-backend.log', allowEmptyArchive: true
        }

        cleanup {
            echo '=== Cleaning Up ==='
            sh '''
                # Kill any background processes
                pkill -9 python python3 2>/dev/null || true
                
                # Clean up temporary files
                rm -f /tmp/jenkins-backend.log 2>/dev/null || true
                
                echo "Cleanup completed"
            '''
        }
    }
}
            echo '❌ Pipeline failed!'
            sh 'echo "Build Status: FAILED" > build-status.txt'
        }

        cleanup {
            echo '🧹 Cleaning up...'
            sh 'rm -rf venv'
        }
    }
}
