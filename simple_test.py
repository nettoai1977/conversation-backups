import asyncio
import aiohttp
import json

async def simple_test():
    """Simple test to verify the Kimi K2.5 server is working"""
    async with aiohttp.ClientSession() as session:
        # Test the health endpoint
        print("Testing health endpoint...")
        async with session.get('http://localhost:3006/health') as response:
            if response.status == 200:
                health_data = await response.json()
                print(f"✓ Health check: {health_data['status']}")
            else:
                print(f"✗ Health check failed: {response.status}")
        
        # Test the models endpoint
        print("Testing models endpoint...")
        async with session.get('http://localhost:3006/models') as response:
            if response.status == 200:
                models_data = await response.json()
                print(f"✓ Models available: {[model['id'] for model in models_data['data']]}")
            else:
                print(f"✗ Models check failed: {response.status}")
        
        # Test a simple chat completion (without making the actual API call to NVIDIA)
        print("Testing chat completion endpoint...")
        payload = {
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello, just testing the Kimi K2.5 server connection."
                }
            ],
            "model": "moonshotai/kimi-k2.5",
            "max_tokens": 50,
            "temperature": 0.7,
            "thinking": False
        }
        
        try:
            async with session.post('http://localhost:3006/chat/completions', json=payload, timeout=15) as response:
                if response.status == 200:
                    chat_data = await response.json()
                    print(f"✓ Chat completion successful")
                    print(f"  Response preview: {chat_data['choices'][0]['message']['content'][:100]}...")
                else:
                    error_text = await response.text()
                    print(f"✗ Chat completion failed with status {response.status}: {error_text[:200]}...")
        except asyncio.TimeoutError:
            print("⚠️  Chat completion timed out (this is expected if the NVIDIA API is slow)")
        except Exception as e:
            print(f"✗ Chat completion error: {str(e)[:200]}...")

if __name__ == "__main__":
    asyncio.run(simple_test())