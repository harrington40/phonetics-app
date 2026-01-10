#!/bin/bash

# AI Agents Runner for Phonetics App Development Workflow
# This script orchestrates ChatGPT and DeepSeek agents for automated issue resolution

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SCRIPT_DIR/config.yaml"
API_KEYS_FILE="$SCRIPT_DIR/api-keys.yaml"
LOG_FILE="$SCRIPT_DIR/logs/agent_activity.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    echo -e "${BLUE}[$timestamp]${NC} [$level] $message"
}

# Error handling
error_exit() {
    log "ERROR" "$1"
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Check dependencies
check_dependencies() {
    log "INFO" "Checking dependencies..."

    if ! command -v python3 &> /dev/null; then
        error_exit "Python3 is required but not installed"
    fi

    if ! command -v curl &> /dev/null; then
        error_exit "curl is required but not installed"
    fi

    if ! command -v jq &> /dev/null; then
        error_exit "jq is required but not installed. Install with: sudo apt-get install jq"
    fi

    log "INFO" "Dependencies check passed"
}

# Load configuration
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error_exit "Configuration file not found: $CONFIG_FILE"
    fi

    if [[ ! -f "$API_KEYS_FILE" ]]; then
        error_exit "API keys file not found: $API_KEYS_FILE"
    fi

    log "INFO" "Configuration loaded successfully"
}

# Validate API keys
validate_api_keys() {
    log "INFO" "Validating API keys..."

    OPENAI_API_KEY=$(grep "api_key:" "$API_KEYS_FILE" | head -1 | cut -d'"' -f2)
    DEEPSEEK_API_KEY=$(grep "api_key:" "$API_KEYS_FILE" | tail -1 | cut -d'"' -f2)

    if [[ -z "$OPENAI_API_KEY" || "$OPENAI_API_KEY" == "\${OPENAI_API_KEY}" ]]; then
        if [[ -z "${OPENAI_API_KEY}" ]]; then
            error_exit "OpenAI API key not found. Set OPENAI_API_KEY environment variable or update $API_KEYS_FILE"
        fi
    fi

    if [[ -z "$DEEPSEEK_API_KEY" || "$DEEPSEEK_API_KEY" == "\${DEEPSEEK_API_KEY}" ]]; then
        if [[ -z "${DEEPSEEK_API_KEY}" ]]; then
            error_exit "DeepSeek API key not found. Set DEEPSEEK_API_KEY environment variable or update $API_KEYS_FILE"
        fi
    fi

    log "INFO" "API keys validation passed"
}

# ChatGPT Agent Function
chatgpt_agent() {
    local prompt="$1"
    local context="$2"

    log "INFO" "ChatGPT Agent: Processing request"

    local system_prompt="You are an expert Flutter developer and technical lead. Focus on reasoning, planning, and high-level architecture decisions. Provide clear, actionable insights."

    # Use jq to properly construct JSON with escaped content
    local request_data=$(jq -n \
        --arg model "gpt-4o" \
        --arg system_prompt "$system_prompt" \
        --arg user_content "Context: $context\n\nRequest: $prompt" \
        --arg temp "0.7" \
        --arg max_tokens "4000" \
        '{
            model: $model,
            messages: [
                {role: "system", content: $system_prompt},
                {role: "user", content: $user_content}
            ],
            temperature: ($temp | tonumber),
            max_tokens: ($max_tokens | tonumber)
        }')

    local response=$(curl -s -X POST "https://api.openai.com/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "$request_data")

    if [[ $? -ne 0 ]]; then
        error_exit "Failed to call ChatGPT API"
    fi

    local result=$(echo "$response" | jq -r '.choices[0].message.content' 2>/dev/null)
    if [[ -z "$result" || "$result" == "null" ]]; then
        error_exit "Invalid response from ChatGPT API: $response"
    fi

    echo "$result"
}

# DeepSeek Agent Function
deepseek_agent() {
    local prompt="$1"
    local context="$2"

    log "INFO" "DeepSeek Agent: Processing request"

    local system_prompt="You are an expert debugger and implementation specialist. Focus on code fixes, debugging, and detailed implementation. Provide specific, actionable code changes."

    # Use jq to properly construct JSON with escaped content
    local request_data=$(jq -n \
        --arg model "deepseek-coder" \
        --arg system_prompt "$system_prompt" \
        --arg user_content "Context: $context\n\nRequest: $prompt" \
        --arg temp "0.3" \
        --arg max_tokens "6000" \
        '{
            model: $model,
            messages: [
                {role: "system", content: $system_prompt},
                {role: "user", content: $user_content}
            ],
            temperature: ($temp | tonumber),
            max_tokens: ($max_tokens | tonumber)
        }')

    local response=$(curl -s -X POST "https://api.deepseek.com/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
        -d "$request_data")

    if [[ $? -ne 0 ]]; then
        error_exit "Failed to call DeepSeek API"
    fi

    local result=$(echo "$response" | jq -r '.choices[0].message.content' 2>/dev/null)
    if [[ -z "$result" || "$result" == "null" ]]; then
        error_exit "Invalid response from DeepSeek API: $response"
    fi

    echo "$result"
}

# Build failure analysis workflow
analyze_build_failure() {
    local error_log="$1"
    local project_type="$2"

    log "INFO" "Starting build failure analysis workflow"

    # Step 1: ChatGPT analyzes the error and provides reasoning
    local chatgpt_analysis=$(chatgpt_agent \
        "Analyze this build failure and explain what might be causing it. Provide high-level insights about the issue." \
        "Build Error Log: $error_log")

    log "INFO" "ChatGPT analysis completed"

    # Step 2: DeepSeek provides specific debugging and fixes
    local deepseek_fix=$(deepseek_agent \
        "Based on the analysis above, provide specific code changes and debugging steps to fix this build failure. Include exact file paths and code snippets." \
        "ChatGPT Analysis: $chatgpt_analysis\nBuild Error: $error_log\nProject Type: $project_type")

    log "INFO" "DeepSeek debugging completed"

    # Output results
    echo "=== BUILD FAILURE ANALYSIS ==="
    echo ""
    echo "🔍 CHATGPT ANALYSIS (Reasoning):"
    echo "$chatgpt_analysis"
    echo ""
    echo "🔧 DEEPSEEK DEBUGGING (Implementation):"
    echo "$deepseek_fix"
    echo ""
    echo "=== WORKFLOW COMPLETED ==="
}

# Code review workflow
analyze_code_review() {
    local code_changes="$1"
    local file_path="$2"

    log "INFO" "Starting code review workflow"

    # Step 1: DeepSeek analyzes code quality and potential issues
    local deepseek_review=$(deepseek_agent \
        "Review this code for bugs, performance issues, and best practices. Provide specific recommendations." \
        "Code Changes: $code_changes\nFile: $file_path")

    # Step 2: ChatGPT provides architectural insights
    local chatgpt_insights=$(chatgpt_agent \
        "Based on the code review, provide architectural recommendations and long-term maintainability insights." \
        "DeepSeek Code Review: $deepseek_review\nFile: $file_path")

    # Output results
    echo "=== CODE REVIEW ANALYSIS ==="
    echo ""
    echo "🔧 DEEPSEEK CODE REVIEW:"
    echo "$deepseek_review"
    echo ""
    echo "🏗️ CHATGPT ARCHITECTURAL INSIGHTS:"
    echo "$chatgpt_insights"
    echo ""
    echo "=== CODE REVIEW COMPLETED ==="
}

# Dependency update analysis
analyze_dependency_update() {
    local dependency_changes="$1"

    log "INFO" "Starting dependency update analysis"

    # Step 1: DeepSeek checks compatibility
    local deepseek_compat=$(deepseek_agent \
        "Analyze these dependency changes for compatibility issues and breaking changes." \
        "Dependency Changes: $dependency_changes")

    # Step 2: ChatGPT assesses impact
    local chatgpt_impact=$(chatgpt_agent \
        "Assess the broader impact of these dependency changes on the project architecture and roadmap." \
        "DeepSeek Compatibility Analysis: $deepseek_compat")

    # Output results
    echo "=== DEPENDENCY UPDATE ANALYSIS ==="
    echo ""
    echo "🔧 DEEPSEEK COMPATIBILITY CHECK:"
    echo "$deepseek_compat"
    echo ""
    echo "📊 CHATGPT IMPACT ASSESSMENT:"
    echo "$chatgpt_impact"
    echo ""
    echo "=== DEPENDENCY ANALYSIS COMPLETED ==="
}

# Main workflow dispatcher
main() {
    local workflow_type="$1"
    shift

    # Initialize
    mkdir -p "$SCRIPT_DIR/logs"
    check_dependencies
    load_config
    validate_api_keys

    log "INFO" "AI Agents workflow started: $workflow_type"

    case "$workflow_type" in
        "build_failure")
            if [[ $# -lt 2 ]]; then
                error_exit "Usage: $0 build_failure <error_log> <project_type>"
            fi
            analyze_build_failure "$1" "$2"
            ;;
        "code_review")
            if [[ $# -lt 2 ]]; then
                error_exit "Usage: $0 code_review <code_changes> <file_path>"
            fi
            analyze_code_review "$1" "$2"
            ;;
        "dependency_update")
            if [[ $# -lt 1 ]]; then
                error_exit "Usage: $0 dependency_update <dependency_changes>"
            fi
            analyze_dependency_update "$1"
            ;;
        *)
            error_exit "Unknown workflow type: $workflow_type. Available: build_failure, code_review, dependency_update"
            ;;
    esac

    log "INFO" "AI Agents workflow completed successfully"
}

# Run main function with all arguments
main "$@"