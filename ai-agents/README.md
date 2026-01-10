# AI Agents for Phonetics App Development Workflow

This directory contains AI-powered automation tools for the Phonetics App development workflow. The system integrates ChatGPT for reasoning and planning with DeepSeek for debugging and implementation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r ai-agents/requirements.txt

# Make scripts executable
chmod +x ai-agents/run-ai-agents.sh
chmod +x ai-agents/ai_agents_manager.py
```

### 2. Configure API Keys

Edit `ai-agents/api-keys.yaml` and add your API keys:

```yaml
openai:
  api_key: "your-openai-api-key-here"

deepseek:
  api_key: "your-deepseek-api-key-here"
```

Or set environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export DEEPSEEK_API_KEY="your-deepseek-api-key-here"
```

### 3. Test the Setup

```bash
# Test with a simple build failure analysis
./ai-agents/run-ai-agents.sh build_failure "Error: package not found" flutter
```

## 🤖 AI Agents Overview

### ChatGPT Agent
- **Role**: Reasoning and high-level planning
- **Model**: GPT-4 Turbo
- **Focus**: Architecture decisions, problem analysis, strategic planning
- **Use Cases**: Build failure analysis, code review insights, dependency impact assessment

### DeepSeek Agent
- **Role**: Debugging and implementation
- **Model**: DeepSeek Coder
- **Focus**: Code fixes, debugging, detailed implementation
- **Use Cases**: Specific code changes, bug fixes, compatibility checks

## 🔄 Available Workflows

### 1. Build Failure Analysis
Analyzes build errors and provides both high-level reasoning and specific fixes.

```bash
# Using Bash script
./ai-agents/run-ai-agents.sh build_failure "error log content" flutter

# Using Python script
python ai-agents/ai_agents_manager.py build_failure --error-log "error log content" --project-type flutter
```

### 2. Code Review
Reviews code changes for bugs, performance issues, and best practices.

```bash
# Using Bash script
./ai-agents/run-ai-agents.sh code_review "code changes here" "lib/main.dart"

# Using Python script
python ai-agents/ai_agents_manager.py code_review --code-changes "code changes" --file-path "lib/main.dart"
```

### 3. Dependency Update Analysis
Analyzes dependency changes for compatibility and impact.

```bash
# Using Bash script
./ai-agents/run-ai-agents.sh dependency_update "dependency changes here"

# Using Python script
python ai-agents/ai_agents_manager.py dependency_update --dependency-changes "dependency changes"
```

## ⚙️ Configuration

### Main Configuration (`config.yaml`)
- **AI Agents Settings**: Enable/disable agents, model configurations
- **Workflow Triggers**: Define when workflows should run
- **Integration Points**: Jenkins, GitHub, local development hooks
- **Security Settings**: API key encryption, rate limiting
- **Performance Tuning**: Concurrent requests, timeouts, retries

### API Keys Configuration (`api-keys.yaml`)
- **OpenAI Settings**: API key, organization ID, project ID
- **DeepSeek Settings**: API key, base URL
- **Environment Variables**: Support for secure key management

## 🔗 Integration Points

### Jenkins CI/CD Integration
The AI agents can be integrated with Jenkins pipelines for automated issue resolution:

```groovy
// Add to Jenkinsfile.android
stage('AI Analysis') {
    when {
        expression { currentBuild.result == 'FAILURE' }
    }
    steps {
        script {
            sh './ai-agents/run-ai-agents.sh build_failure "${BUILD_LOG}" flutter'
        }
    }
}
```

### GitHub Integration
Set up webhooks for pull request and issue analysis:

```yaml
# .github/workflows/ai-analysis.yml
name: AI Code Analysis
on: [pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run AI Code Review
        run: |
          python ai-agents/ai_agents_manager.py code_review \
            --code-changes "${{ github.event.pull_request.body }}" \
            --file-path "flutter_app/"
```

### Local Development Integration
Monitor file changes and provide real-time assistance:

```bash
# Watch for changes and run analysis
find flutter_app/ -name "*.dart" -type f -exec \
  python ai-agents/ai_agents_manager.py code_review \
    --code-changes "$(cat {})" --file-path {} \;
```

## 📊 Logging and Monitoring

### Log Files
- **Agent Activity**: `ai-agents/logs/agent_activity.log`
- **API Calls**: `ai-agents/logs/ai_agents.log`
- **Performance Metrics**: Response times, success rates, error patterns

### Monitoring Dashboard
```bash
# View recent activity
tail -f ai-agents/logs/agent_activity.log

# Check API usage
grep "API call" ai-agents/logs/ai_agents.log | wc -l
```

## 🔒 Security Best Practices

### API Key Management
- Use environment variables instead of hardcoding keys
- Rotate keys regularly (recommended: every 90 days)
- Use a key management service for production deployments
- Never commit API keys to version control

### Rate Limiting
- Configurable requests per minute limits
- Burst protection to prevent API quota exhaustion
- Automatic backoff and retry logic

### Data Privacy
- No sensitive code or data sent to external APIs
- Local logging of all AI interactions
- Configurable data retention policies

## 🛠️ Advanced Usage

### Custom Workflows
Create custom workflow scripts by extending the base classes:

```python
from ai_agents_manager import AIAgentsManager

class CustomWorkflow(AIAgentsManager):
    async def custom_analysis(self, custom_data):
        # Implement custom logic
        pass
```

### Batch Processing
Process multiple files or issues in batch:

```bash
# Analyze all Dart files
find flutter_app/lib/ -name "*.dart" -exec \
  ./ai-agents/run-ai-agents.sh code_review "$(cat {})" {} \;
```

### Integration with IDEs
Set up IDE integrations for real-time assistance:

```json
// .vscode/settings.json
{
    "ai-agents.enable": true,
    "ai-agents.triggerOnSave": true,
    "ai-agents.workflows": ["code_review", "build_failure"]
}
```

## 📈 Performance Optimization

### Concurrent Processing
- Multiple workflows can run simultaneously
- Configurable max concurrent requests
- Async/await patterns for efficient API calls

### Caching
- Response caching to reduce API calls
- Intelligent cache invalidation
- Configurable cache sizes and TTL

### Error Handling
- Automatic retry with exponential backoff
- Circuit breaker pattern for API failures
- Graceful degradation when services are unavailable

## 🤝 Contributing

### Adding New Workflows
1. Define the workflow in `config.yaml`
2. Implement the workflow method in `AIAgentsManager`
3. Add CLI support in both Bash and Python scripts
4. Update documentation and examples

### Testing
```bash
# Run unit tests
python -m pytest ai-agents/tests/

# Test API integrations
python ai-agents/test_api_integration.py
```

## 📚 Troubleshooting

### Common Issues

**API Key Errors**
```
Error: OpenAI API key not found
```
- Check environment variables: `echo $OPENAI_API_KEY`
- Verify `api-keys.yaml` configuration
- Ensure keys are not expired

**Network Errors**
```
Exception: Connection timeout
```
- Check internet connectivity
- Verify API endpoints in config
- Adjust timeout settings in config.yaml

**Rate Limiting**
```
API Error: 429 Too Many Requests
```
- Reduce request frequency
- Implement caching
- Check API usage quotas

### Debug Mode
Enable verbose logging for troubleshooting:

```bash
export AI_AGENTS_DEBUG=true
./ai-agents/run-ai-agents.sh build_failure "error" flutter
```

## 📄 License

This AI agents system is part of the Phonetics App project and follows the same license terms.

## 🆘 Support

For issues with the AI agents system:
1. Check the logs in `ai-agents/logs/`
2. Review the configuration files
3. Test API connectivity manually
4. Create an issue in the project repository

---

**Note**: This AI agents system enhances development productivity but should be used as a complement to, not a replacement for, human code review and testing processes.