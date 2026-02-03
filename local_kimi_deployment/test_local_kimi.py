#!/usr/bin/env python3
"""
Test script for local Kimi K2.5 deployment
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any


async def test_local_kimi_server():
    """Test the local Kimi K2.5 server"""
    print("🧪 Testing Local Kimi K2.5 Server")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Health check
        print("\n1. Testing Health Endpoint...")
        try:
            async with session.get('http://localhost:3007/health', timeout=5) as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"   ✓ Server is healthy: {health_data['status']}")
                    print(f"   ✓ Model: {health_data['model']}")
                    print(f"   ✓ Local deployment: {health_data['local_deployed']}")
                else:
                    print(f"   ⚠️  Health check returned status: {response.status}")
        except Exception as e:
            print(f"   ⚠️  Health check failed (expected if server not running): {e}")
        
        # Test 2: Models endpoint
        print("\n2. Testing Models Endpoint...")
        try:
            async with session.get('http://localhost:3007/models', timeout=10) as response:
                if response.status == 200:
                    models_data = await response.json()
                    print(f"   ✓ Available models: {[model['id'] for model in models_data['data']]}")
                else:
                    print(f"   ⚠️  Models check returned status: {response.status}")
        except Exception as e:
            print(f"   ⚠️  Models check failed (expected if server not running): {e}")
        
        # Test 3: Sample chat completion (won't work unless server is running)
        print("\n3. Testing Chat Completion Endpoint...")
        print("   Note: This requires the local server to be running")
        
        payload = {
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello, this is a test to local Kimi K2.5. Please respond with a brief greeting."
                }
            ],
            "model": "kimi-k25-local",
            "max_tokens": 100,
            "temperature": 0.7,
            "thinking": False
        }
        
        try:
            async with session.post('http://localhost:3007/chat/completions', 
                                  json=payload, timeout=10) as response:
                if response.status == 200:
                    chat_data = await response.json()
                    print(f"   ✓ Chat completion successful!")
                    print(f"   ✓ Model used: {chat_data['model']}")
                    print(f"   ✓ Response preview: {chat_data['choices'][0]['message']['content'][:100]}...")
                else:
                    error_text = await response.text()
                    print(f"   ⚠️  Chat completion returned status {response.status}")
                    print(f"   ⚠️  Error: {error_text[:200]}...")
                    
        except asyncio.TimeoutError:
            print("   ⏳ Request timed out - server may not be running")
        except Exception as e:
            print(f"   ⚠️  Chat completion error (expected if server not running): {e}")


async def check_setup_requirements():
    """Check if the required components are available"""
    print("\n📋 Checking Setup Requirements")
    print("=" * 50)
    
    import os
    import sys
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Check if llama.cpp exists
    if os.path.exists("./llama.cpp"):
        print("✓ llama.cpp directory found")
    else:
        print("⚠️  llama.cpp directory not found - run setup_local_kimi.sh first")
    
    # Check if models directory exists
    if os.path.exists("./models"):
        print("✓ models directory found")
        # Check if Kimi model exists
        import glob
        kimi_models = glob.glob("./models/kimi-k25-quantized/*.gguf")
        if kimi_models:
            print(f"✓ Kimi K2.5 model found ({len(kimi_models)} files)")
        else:
            print("⚠️  Kimi K2.5 model not found - run download_model.py first")
    else:
        print("⚠️  models directory not found - run download_model.py first")
    
    # Check if required Python packages are available
    try:
        import fastapi
        print("✓ FastAPI is available")
    except ImportError:
        print("⚠️  FastAPI not available - install with: pip3 install fastapi")
    
    try:
        import uvicorn
        print("✓ Uvicorn is available")
    except ImportError:
        print("⚠️  Uvicorn not available - install with: pip3 install uvicorn")


async def main():
    """Main test function"""
    await check_setup_requirements()
    await test_local_kimi_server()
    
    print("\n" + "=" * 50)
    print("🎯 Local Kimi K2.5 Test Complete!")
    print("\n📝 Next Steps:")
    print("   1. If not already done, run: bash setup_local_kimi.sh")
    print("   2. Download the model: python3 download_model.py") 
    print("   3. Start the local server: python3 local_kimi_server.py")
    print("   4. Test with this script again")
    print("\n📖 For detailed instructions, see: deployment_guide.md")


if __name__ == "__main__":
    asyncio.run(main())