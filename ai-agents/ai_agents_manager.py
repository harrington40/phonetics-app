#!/usr/bin/env python3
"""
AI Agents Manager for Phonetics App Development Workflow
Advanced Python wrapper for ChatGPT and DeepSeek integration
"""

import os
import sys
import json
import yaml
import logging
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import argparse
from datetime import datetime

@dataclass
class AIAgentConfig:
    """Configuration for AI agents"""
    enabled: bool
    model: str
    api_endpoint: str
    temperature: float
    max_tokens: int
    system_prompt: str

@dataclass
class WorkflowConfig:
    """Configuration for workflows"""
    enabled: bool
    trigger_on: List[str]
    primary_agent: str
    secondary_agent: str

class AIAgentsManager:
    """Main AI Agents Manager"""

    def __init__(self, config_path: str = "config.yaml", api_keys_path: str = "api-keys.yaml"):
        self.config_path = Path(__file__).parent / config_path
        self.api_keys_path = Path(__file__).parent / api_keys_path
        self.logger = self._setup_logging()

        # Load configurations
        self.config = self._load_config()
        self.api_keys = self._load_api_keys()

        # Initialize agents
        self.chatgpt_config = self._get_agent_config("chatgpt")
        self.deepseek_config = self._get_agent_config("deepseek")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Path(__file__).parent / "logs" / "ai_agents.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger("AIAgentsManager")

    def _load_config(self) -> Dict[str, Any]:
        """Load main configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {self.config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing configuration: {e}")
            sys.exit(1)

    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys"""
        try:
            with open(self.api_keys_path, 'r') as f:
                keys_config = yaml.safe_load(f)

            # Check environment variables first, then config file
            openai_key = os.getenv('OPENAI_API_KEY') or keys_config.get('openai', {}).get('api_key', '')
            deepseek_key = os.getenv('DEEPSEEK_API_KEY') or keys_config.get('deepseek', {}).get('api_key', '')

            if not openai_key or openai_key.startswith('${'):
                self.logger.error("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
                sys.exit(1)

            if not deepseek_key or deepseek_key.startswith('${'):
                self.logger.error("DeepSeek API key not found. Set DEEPSEEK_API_KEY environment variable.")
                sys.exit(1)

            return {
                'openai': openai_key,
                'deepseek': deepseek_key
            }

        except FileNotFoundError:
            self.logger.error(f"API keys file not found: {self.api_keys_path}")
            sys.exit(1)

    def _get_agent_config(self, agent_name: str) -> AIAgentConfig:
        """Get agent configuration"""
        agent_config = self.config.get('ai_agents', {}).get(agent_name, {})
        return AIAgentConfig(
            enabled=agent_config.get('enabled', True),
            model=agent_config.get('model', ''),
            api_endpoint=agent_config.get('api_endpoint', ''),
            temperature=agent_config.get('temperature', 0.7),
            max_tokens=agent_config.get('max_tokens', 4000),
            system_prompt=agent_config.get('system_prompt', '')
        )

    async def _call_ai_api(self, agent_config: AIAgentConfig, prompt: str, context: str = "") -> str:
        """Call AI API asynchronously"""
        headers = {
            'Content-Type': 'application/json',
        }

        if 'openai.com' in agent_config.api_endpoint:
            headers['Authorization'] = f'Bearer {self.api_keys["openai"]}'
        elif 'deepseek.com' in agent_config.api_endpoint:
            headers['Authorization'] = f'Bearer {self.api_keys["deepseek"]}'

        data = {
            'model': agent_config.model,
            'messages': [
                {'role': 'system', 'content': agent_config.system_prompt},
                {'role': 'user', 'content': f'Context: {context}\n\nRequest: {prompt}'}
            ],
            'temperature': agent_config.temperature,
            'max_tokens': agent_config.max_tokens
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(agent_config.api_endpoint, headers=headers, json=data) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"API call failed: {response.status} - {error_text}")
                        return f"API Error: {response.status}"

                    result = await response.json()
                    return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')

            except Exception as e:
                self.logger.error(f"Exception during API call: {e}")
                return f"Exception: {e}"

    async def analyze_build_failure(self, error_log: str, project_type: str = "flutter") -> Dict[str, str]:
        """Analyze build failure using both agents"""
        self.logger.info("Starting build failure analysis workflow")

        # ChatGPT analysis
        chatgpt_prompt = "Analyze this build failure and explain what might be causing it. Provide high-level insights about the issue."
        chatgpt_context = f"Build Error Log: {error_log}"
        chatgpt_analysis = await self._call_ai_api(self.chatgpt_config, chatgpt_prompt, chatgpt_context)

        # DeepSeek debugging
        deepseek_prompt = "Based on the analysis above, provide specific code changes and debugging steps to fix this build failure. Include exact file paths and code snippets."
        deepseek_context = f"ChatGPT Analysis: {chatgpt_analysis}\nBuild Error: {error_log}\nProject Type: {project_type}"
        deepseek_fix = await self._call_ai_api(self.deepseek_config, deepseek_prompt, deepseek_context)

        return {
            'chatgpt_analysis': chatgpt_analysis,
            'deepseek_fix': deepseek_fix
        }

    async def analyze_code_review(self, code_changes: str, file_path: str) -> Dict[str, str]:
        """Analyze code changes for review"""
        self.logger.info("Starting code review workflow")

        # DeepSeek code review
        deepseek_prompt = "Review this code for bugs, performance issues, and best practices. Provide specific recommendations."
        deepseek_context = f"Code Changes: {code_changes}\nFile: {file_path}"
        deepseek_review = await self._call_ai_api(self.deepseek_config, deepseek_prompt, deepseek_context)

        # ChatGPT architectural insights
        chatgpt_prompt = "Based on the code review, provide architectural recommendations and long-term maintainability insights."
        chatgpt_context = f"DeepSeek Code Review: {deepseek_review}\nFile: {file_path}"
        chatgpt_insights = await self._call_ai_api(self.chatgpt_config, chatgpt_prompt, chatgpt_context)

        return {
            'deepseek_review': deepseek_review,
            'chatgpt_insights': chatgpt_insights
        }

    async def analyze_dependency_update(self, dependency_changes: str) -> Dict[str, str]:
        """Analyze dependency updates"""
        self.logger.info("Starting dependency update analysis")

        # DeepSeek compatibility check
        deepseek_prompt = "Analyze these dependency changes for compatibility issues and breaking changes."
        deepseek_context = f"Dependency Changes: {dependency_changes}"
        deepseek_compat = await self._call_ai_api(self.deepseek_config, deepseek_prompt, deepseek_context)

        # ChatGPT impact assessment
        chatgpt_prompt = "Assess the broader impact of these dependency changes on the project architecture and roadmap."
        chatgpt_context = f"DeepSeek Compatibility Analysis: {deepseek_compat}"
        chatgpt_impact = await self._call_ai_api(self.chatgpt_config, chatgpt_prompt, chatgpt_context)

        return {
            'deepseek_compat': deepseek_compat,
            'chatgpt_impact': chatgpt_impact
        }

    def format_results(self, workflow_type: str, results: Dict[str, str]) -> str:
        """Format results for display"""
        output = f"=== {workflow_type.upper().replace('_', ' ')} ANALYSIS ===\n\n"

        for agent, result in results.items():
            agent_name = agent.replace('_', ' ').title()
            emoji = "🔍" if "chatgpt" in agent else "🔧" if "deepseek" in agent else "📊"
            output += f"{emoji} {agent_name}:\n{result}\n\n"

        output += "=== WORKFLOW COMPLETED ==="
        return output

async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Agents Manager for Phonetics App")
    parser.add_argument("workflow", choices=["build_failure", "code_review", "dependency_update"],
                       help="Workflow type to execute")
    parser.add_argument("--error-log", help="Build error log for build_failure workflow")
    parser.add_argument("--code-changes", help="Code changes for code_review workflow")
    parser.add_argument("--file-path", help="File path for code_review workflow")
    parser.add_argument("--dependency-changes", help="Dependency changes for dependency_update workflow")
    parser.add_argument("--project-type", default="flutter", help="Project type (default: flutter)")

    args = parser.parse_args()

    # Initialize manager
    manager = AIAgentsManager()

    # Execute workflow
    if args.workflow == "build_failure":
        if not args.error_log:
            print("Error: --error-log is required for build_failure workflow")
            sys.exit(1)
        results = await manager.analyze_build_failure(args.error_log, args.project_type)
        workflow_name = "build_failure"

    elif args.workflow == "code_review":
        if not args.code_changes or not args.file_path:
            print("Error: --code-changes and --file-path are required for code_review workflow")
            sys.exit(1)
        results = await manager.analyze_code_review(args.code_changes, args.file_path)
        workflow_name = "code_review"

    elif args.workflow == "dependency_update":
        if not args.dependency_changes:
            print("Error: --dependency-changes is required for dependency_update workflow")
            sys.exit(1)
        results = await manager.analyze_dependency_update(args.dependency_changes)
        workflow_name = "dependency_update"

    # Display results
    print(manager.format_results(workflow_name, results))

if __name__ == "__main__":
    asyncio.run(main())