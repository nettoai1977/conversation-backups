#!/usr/bin/env python3
"""
Test script for Kimi K2.5 MCP Server
Tests the Kimi K2.5 server functionality with various request types
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any


async def test_health_check():
    """Test the health check endpoint"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:3006/health') as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Health check passed: {data}")
                    return True
                else:
                    print(f"✗ Health check failed with status: {response.status}")
                    return False
        except Exception as e:
            print(f"✗ Health check error: {e}")
            return False


async def test_chat_completion():
    """Test basic chat completion"""
    async with aiohttp.ClientSession() as session:
        try:
            payload = {
                "messages": [
                    {
                        "role": "user", 
                        "content": "Hello, this is a test message to Kimi K2.5. Please respond briefly."
                    }
                ],
                "model": "moonshotai/kimi-k2.5",
                "max_tokens": 200,
                "temperature": 0.7,
                "thinking": True  # Use thinking mode for this test
            }
            
            async with session.post('http://localhost:3006/chat/completions', json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Chat completion test passed")
                    print(f"  Response: {data['choices'][0]['message']['content'][:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"✗ Chat completion failed with status {response.status}: {error_text}")
                    return False
        except Exception as e:
            print(f"✗ Chat completion error: {e}")
            return False


async def test_multimodal_request():
    """Test multimodal request (without actual image for now)"""
    async with aiohttp.ClientSession() as session:
        try:
            # Test with text content
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this request for multimodal capability testing."}
                        ]
                    }
                ],
                "model": "moonshotai/kimi-k2.5",
                "max_tokens": 200,
                "temperature": 0.7,
                "thinking": False  # Use instant mode for this test
            }
            
            async with session.post('http://localhost:3006/chat/completions', json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Multimodal request test passed")
                    print(f"  Response: {data['choices'][0]['message']['content'][:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"✗ Multimodal request failed with status {response.status}: {error_text}")
                    return False
        except Exception as e:
            print(f"✗ Multimodal request error: {e}")
            return False


async def test_model_list():
    """Test listing available models"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://localhost:3006/models') as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✓ Model list test passed")
                    print(f"  Available models: {[model['id'] for model in data['data']]}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"✗ Model list failed with status {response.status}: {error_text}")
                    return False
        except Exception as e:
            print(f"✗ Model list error: {e}")
            return False


async def main():
    """Run all tests"""
    print("Running Kimi K2.5 MCP Server Tests...\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Model List", test_model_list),
        ("Chat Completion", test_chat_completion),
        ("Multimodal Request", test_multimodal_request),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = await test_func()
        results.append((test_name, result))
        print()
    
    print("Test Results:")
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Kimi K2.5 MCP Server is working correctly.")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the server.")


if __name__ == "__main__":
    asyncio.run(main())