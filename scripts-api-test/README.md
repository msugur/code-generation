# 🧪 API Testing Suite

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenAI Compatible](https://img.shields.io/badge/API-OpenAI%20Compatible-green.svg)](https://platform.openai.com/docs/api-reference)
[![Mistral](https://img.shields.io/badge/LLM-Mistral-purple.svg)](https://mistral.ai/)

> Comprehensive testing utilities for validating Mistral AI API connectivity and functionality with OpenAI-compatible endpoints.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Test Functions](#-test-functions)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)

## 🎯 Overview

The API Testing Suite provides essential tools for:
- Testing Mistral LLM API connectivity
- Validating OpenAI-compatible endpoints
- Debugging API authentication issues
- Performance benchmarking
- Model availability verification

## ✨ Features

- **🔌 OpenAI Compatibility**: Tests standard OpenAI API format
- **🎯 Endpoint Testing**: Validates both `/chat/completions` and `/models` endpoints
- **🔐 Authentication**: Supports Bearer token authentication
- **📊 Detailed Logging**: Comprehensive request/response logging
- **🚨 Error Handling**: Graceful error reporting with detailed diagnostics
- **⚡ No Dependencies**: Uses only Python standard library

## 📦 Installation

No additional dependencies required! The test script uses only Python standard library modules:

```python
import json
import urllib.request
import urllib.error
import sys
```

## 🚀 Usage

### Basic Usage

```bash
# Run with default settings (no authentication)
python mistral_api_test.py

# Run with API key
python mistral_api_test.py YOUR_API_KEY_HERE
```

### Setting API Key

Three methods to provide API key:

1. **Command Line Argument**
   ```bash
   python mistral_api_test.py sk-your-api-key-here
   ```

2. **Edit Script Directly**
   ```python
   API_KEY = "your-api-key-here"
   ```

3. **Environment Variable** (modify script)
   ```python
   import os
   API_KEY = os.getenv("MISTRAL_API_KEY", "")
   ```

## 🌐 API Endpoints

### Default Configuration

```python
BASE_URL = "https://mistral-llm.apps.cluster-gg696.gg696.sandbox3157.opentlc.com/v1"
```

### Tested Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/models` | GET | List available models |
| `/v1/chat/completions` | POST | Generate chat completions |

## 🔧 Test Functions

### `test_models_endpoint()`

Tests the models listing endpoint:

```python
def test_models_endpoint():
    """Test the models endpoint to list available models"""
    url = f"{BASE_URL}/models"
    # Returns available models in OpenAI format
```

**Expected Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "mistral",
      "object": "model",
      "created": 1234567890,
      "owned_by": "mistral"
    }
  ]
}
```

### `test_chat_completion()`

Tests the chat completions endpoint:

```python
def test_chat_completion():
    """Test the chat completions endpoint"""
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you tell me a short joke?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
```

**Expected Response:**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "mistral",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Why don't scientists trust atoms? Because they make up everything!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 15,
    "total_tokens": 40
  }
}
```

## ⚙️ Configuration

### Customizing the Script

#### Change Base URL
```python
BASE_URL = "https://your-mistral-endpoint.com/v1"
```

#### Modify Test Payload
```python
payload = {
    "model": "your-model-name",
    "messages": [...],
    "temperature": 0.9,
    "max_tokens": 500,
    "top_p": 0.95,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}
```

#### Add Custom Headers
```python
req.add_header('X-Custom-Header', 'value')
req.add_header('User-Agent', 'MistralTestClient/1.0')
```

## 💡 Examples

### Example 1: Testing Different Models

```python
def test_specific_model(model_name="mistral-7b"):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "What is 2+2?"}
        ],
        "temperature": 0.1  # Low temperature for deterministic output
    }
    # ... rest of the function
```

### Example 2: Streaming Response Test

```python
def test_streaming():
    payload = {
        "model": "mistral",
        "messages": [...],
        "stream": True  # Enable streaming
    }
    # Note: Requires additional handling for SSE responses
```

### Example 3: Function Calling Test

```python
def test_function_calling():
    payload = {
        "model": "mistral",
        "messages": [...],
        "functions": [
            {
                "name": "get_weather",
                "description": "Get weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    }
                }
            }
        ]
    }
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Authentication Error (401)
```
HTTP Error 401: Unauthorized
```
**Solution**: Verify your API key is correct and properly formatted

#### 2. Connection Error
```
URL Error: [Errno -2] Name or service not known
```
**Solution**: Check the BASE_URL and network connectivity

#### 3. Model Not Found (404)
```
HTTP Error 404: Model not found
```
**Solution**: Verify model name in payload matches available models

#### 4. Rate Limiting (429)
```
HTTP Error 429: Too Many Requests
```
**Solution**: Add delay between requests or implement retry logic

### Debug Mode

Add verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# In the test function
logger = logging.getLogger(__name__)
logger.debug(f"Request: {json.dumps(payload, indent=2)}")
logger.debug(f"Response: {json.dumps(result, indent=2)}")
```

## 📊 Output Format

### Successful Test Run

```
Testing Mistral API (OpenAI Compatible)
==================================================

1. Testing Models Endpoint:
Testing models endpoint: https://mistral-llm.../v1/models
Available models: {
  "object": "list",
  "data": [...]
}

2. Testing Chat Completion:
Sending request to: https://mistral-llm.../v1/chat/completions
Payload: {
  "model": "mistral",
  "messages": [...]
}

Response received successfully!
Full response: {...}
Assistant's response: Why don't scientists trust atoms? Because they make up everything!
```

## 🔄 Integration with Main Project

This testing suite integrates with:

- [🏠 Main Project](../) - For testing agent LLM connectivity
- [🤖 ReAct Agent](../agents/) - Validates LLM client functionality
- [🔧 Flask Backend](../app/) - Tests API integration endpoints

## 🚀 Advanced Usage

### Custom Test Suite

Create a comprehensive test suite:

```python
class MistralAPITestSuite:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.results = []
    
    def run_all_tests(self):
        self.test_authentication()
        self.test_models()
        self.test_chat_completion()
        self.test_error_handling()
        return self.results
    
    def generate_report(self):
        # Generate test report
        pass
```

### Performance Testing

```python
import time

def benchmark_api(num_requests=10):
    times = []
    for i in range(num_requests):
        start = time.time()
        test_chat_completion()
        elapsed = time.time() - start
        times.append(elapsed)
    
    avg_time = sum(times) / len(times)
    print(f"Average response time: {avg_time:.2f}s")
```

## 📄 License

Part of the AI Agent Code Generation Framework. See main project for license details.

---

<p align="center">
Part of the <a href="../">AI Agent Code Generation Framework</a>
</p>