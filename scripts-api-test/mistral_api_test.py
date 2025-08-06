#!/usr/bin/env python3
"""
Mistral API Test - OpenAI Compatible Endpoint
"""

import json
import urllib.request
import urllib.error
import sys

# API endpoint
BASE_URL = "https://mistral-llm.apps.cluster-gg696.gg696.sandbox3157.opentlc.com/v1"

# API Key - Set this to your actual API key
API_KEY = "api-key"  # Replace with your API key or pass as command line argument

def test_chat_completion():
    """Test the chat completions endpoint"""
    
    # Endpoint for chat completions (OpenAI compatible)
    url = f"{BASE_URL}/chat/completions"
    
    # Request payload
    payload = {
        "model": "mistral",  # Adjust model name as needed
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello! Can you tell me a short joke?"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    # Convert payload to JSON bytes
    data = json.dumps(payload).encode('utf-8')
    
    # Create request
    req = urllib.request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    
    # Add API key if provided
    if API_KEY:
        req.add_header('Authorization', f'Bearer {API_KEY}')
    
    try:
        print(f"Sending request to: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}\n")
        
        # Make the API request
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            print("Response received successfully!")
            print(f"Full response: {json.dumps(result, indent=2)}\n")
            
            # Extract the assistant's message
            if "choices" in result and len(result["choices"]) > 0:
                assistant_message = result["choices"][0]["message"]["content"]
                print(f"Assistant's response: {assistant_message}")
            
            return result
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response body: {e.read().decode('utf-8')}")
        return None
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"Error making request: {e}")
        return None

def test_models_endpoint():
    """Test the models endpoint to list available models"""
    
    url = f"{BASE_URL}/models"
    
    # Create request with authorization if API key is provided
    req = urllib.request.Request(url)
    if API_KEY:
        req.add_header('Authorization', f'Bearer {API_KEY}')
    
    try:
        print(f"\nTesting models endpoint: {url}")
        
        with urllib.request.urlopen(req) as response:
            models = json.loads(response.read().decode('utf-8'))
            print(f"Available models: {json.dumps(models, indent=2)}")
            return models
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching models: {e}")
        return None

if __name__ == "__main__":
    # Check if API key is provided as command line argument
    if len(sys.argv) > 1:
        API_KEY = sys.argv[1]
        print(f"Using provided API key: {API_KEY[:8]}..." if API_KEY else "No API key provided")
    
    if not API_KEY:
        print("\nWARNING: No API key provided. The API might require authentication.")
        print("Usage: python3 mistral_api_test.py YOUR_API_KEY")
        print("Continuing without authentication...\n")
    
    print("Testing Mistral API (OpenAI Compatible)\n")
    print("="*50)
    
    # Test models endpoint first
    print("\n1. Testing Models Endpoint:")
    test_models_endpoint()
    
    # Test chat completion
    print("\n2. Testing Chat Completion:")
    test_chat_completion()