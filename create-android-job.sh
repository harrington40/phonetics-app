#!/bin/bash

# Create Android Jenkins Job using Jenkins CLI
# Usage: ./create-android-job.sh [jenkins_token]

set -e

JENKINS_URL="https://jenkins.transtechologies.com"
JENKINS_USER="admin"
JOB_NAME="Phonetics-App-Android"
CONFIG_FILE="android-job-config.xml"

# Get token from argument or prompt
if [ -n "$1" ]; then
    JENKINS_TOKEN="$1"
else
    echo "Get your Jenkins API token from: $JENKINS_URL/user/admin/configure"
    echo "Enter your Jenkins API token:"
    read -s JENKINS_TOKEN
fi

echo "=== Creating Android Jenkins Job ==="
echo "Jenkins URL: $JENKINS_URL"
echo "Job Name: $JOB_NAME"
echo ""

# Check if jenkins-cli.jar exists
if [ ! -f "jenkins-cli.jar" ]; then
    echo "Downloading jenkins-cli.jar..."
    wget "${JENKINS_URL}/jnlpJars/jenkins-cli.jar" -O jenkins-cli.jar
fi

# Create the job
echo "Creating job from configuration..."
java -jar jenkins-cli.jar \
    -s "$JENKINS_URL" \
    -auth "$JENKINS_USER:$JENKINS_TOKEN" \
    create-job "$JOB_NAME" < "$CONFIG_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Job created: $JENKINS_URL/job/$JOB_NAME"
    echo ""
    echo "Next steps:"
    echo "1. Go to Jenkins and configure GitHub credentials if needed"
    echo "2. Click 'Build Now' to test the pipeline"
else
    echo ""
    echo "❌ Failed to create job. Check your credentials and try again."
fi
