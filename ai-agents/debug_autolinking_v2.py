#!/usr/bin/env python3
"""
Debug autolinking.json missing issue - deeper analysis
"""
import asyncio
from orchestrator import AIOrchestrator

error_log = '''
Build #67 Error Evolution:
1. First error: autolinking.json file doesn't exist at android/build/generated/autolinking/autolinking.json
2. After creating empty autolinking.json: New error appears!

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':app:generateAutolinkingPackageList'.
> RNGP - Autolinking: Could not find project.android.packageName in react-native config output! 
  Could not autolink packages without this field.

Context:
- React Native 0.76
- Gradle 8.7
- Running: ./gradlew :app:preBuild --no-daemon --stacktrace
- React Native CLI warning: "react-native depends on @react-native-community/cli for cli commands"

Additional findings:
- npx react-native config shows: "To fix update your package.json to include @react-native-community/cli"
- generateCodegenSchemaFromJavaScript task is SKIPPED
- Manual test: Created empty autolinking.json, got different error about missing packageName in config
'''

code_snippet = '''
// package.json dependencies
"dependencies": {
    "react": "18.3.1",
    "react-native": "0.76.6",
    ...other deps
}

// build.gradle
apply plugin: "com.android.application"
apply plugin: "org.jetbrains.kotlin.android"
apply plugin: "com.facebook.react"

react {
    // Default configuration - all commented out
}

android {
    namespace "com.phoneticsapp"
    defaultConfig {
        applicationId "com.phoneticsapp"
        ...
    }
}
'''

async def main():
    orchestrator = AIOrchestrator()
    result = await orchestrator.orchestrate_code_debugging(
        error_message=error_log,
        code_snippet=code_snippet,
        file_path='React Native 0.76 Autolinking Configuration'
    )
    
    print('\n' + '='*80)
    print('DEEPSEEK BUG FIX & ANALYSIS')
    print('='*80)
    print(result['bug_fix'])
    
    print('\n' + '='*80)
    print('CHATGPT ROOT CAUSE & PREVENTION')
    print('='*80)
    print(result['root_cause_analysis'])

if __name__ == '__main__':
    asyncio.run(main())
