#!/bin/bash

# AI Agents Setup Test Script
# Tests the AI agents configuration and API connectivity

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.yaml"
API_KEYS_FILE="$SCRIPT_DIR/api-keys.yaml"

echo "🧪 Testing AI Agents Setup..."
echo

# Test 1: Check configuration files
echo "1. Checking configuration files..."
if [[ -f "$CONFIG_FILE" ]]; then
    echo "✅ Main config file exists: $CONFIG_FILE"
else
    echo "❌ Main config file missing: $CONFIG_FILE"
    exit 1
fi

if [[ -f "$API_KEYS_FILE" ]]; then
    echo "✅ API keys file exists: $API_KEYS_FILE"
else
    echo "❌ API keys file missing: $API_KEYS_FILE"
    exit 1
fi

# Test 2: Check API keys
echo
echo "2. Checking API keys..."
OPENAI_KEY=$(grep "api_key:" "$API_KEYS_FILE" | head -1 | cut -d'"' -f2)
DEEPSEEK_KEY=$(grep "api_key:" "$API_KEYS_FILE" | tail -1 | cut -d'"' -f2)

if [[ -n "$OPENAI_KEY" && "$OPENAI_KEY" != "\${OPENAI_API_KEY}" ]] || [[ -n "$OPENAI_API_KEY" ]]; then
    echo "✅ OpenAI API key configured"
else
    echo "❌ OpenAI API key not configured"
    echo "   Set OPENAI_API_KEY environment variable or update $API_KEYS_FILE"
fi

if [[ -n "$DEEPSEEK_KEY" && "$DEEPSEEK_KEY" != "\${DEEPSEEK_API_KEY}" ]] || [[ -n "$DEEPSEEK_API_KEY" ]]; then
    echo "✅ DeepSeek API key configured"
else
    echo "❌ DeepSeek API key not configured"
    echo "   Set DEEPSEEK_API_KEY environment variable or update $API_KEYS_FILE"
fi

# Test 3: Check dependencies
echo
echo "3. Checking dependencies..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 available"
else
    echo "❌ Python3 not found"
fi

if command -v curl &> /dev/null; then
    echo "✅ curl available"
else
    echo "❌ curl not found"
fi

if command -v jq &> /dev/null; then
    echo "✅ jq available"
else
    echo "❌ jq not found (install with: sudo apt-get install jq)"
fi

# Test 4: Test Python imports
echo
echo "4. Testing Python environment..."
if python3 -c "import yaml, aiohttp; print('✅ Python dependencies available')" 2>/dev/null; then
    echo "✅ Python dependencies available"
else
    echo "❌ Python dependencies missing"
    echo "   Install with: pip install -r $SCRIPT_DIR/requirements.txt"
fi

# Test 5: Create logs directory
echo
echo "5. Setting up logging..."
mkdir -p "$SCRIPT_DIR/logs"
if [[ -d "$SCRIPT_DIR/logs" ]]; then
    echo "✅ Logs directory created: $SCRIPT_DIR/logs"
else
    echo "❌ Failed to create logs directory"
fi

echo
echo "🎉 Setup test completed!"
echo
echo "Next steps:"
echo "1. Add your API keys to $API_KEYS_FILE or set environment variables"
echo "2. Run a test workflow: ./run-ai-agents.sh build_failure \"test error\" flutter"
echo "3. Check logs in: $SCRIPT_DIR/logs/"
echo
echo "📚 See README.md for detailed usage instructions"