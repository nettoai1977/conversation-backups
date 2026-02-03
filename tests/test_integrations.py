import asyncio
import aiohttp
import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_mcp_server(server_name, server_url, tool_name, params, expected_fields=None):
    """Test an MCP server tool."""
    print(f"\n--- Testing {server_name} ({server_url}) ---")
    print(f"Tool: {tool_name}")
    print(f"Params: {params}")
    
    try:
        async with aiohttp.ClientSession() as session:
            # MCP typically uses JSON-RPC protocol
            payload = {
                "jsonrpc": "2.0",
                "method": f"tools/{tool_name}",
                "params": params,
                "id": 1
            }
            
            try:
                async with session.post(f"{server_url}", json=payload, timeout=10) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✓ Response received: {json.dumps(result, indent=2)[:200]}...")
                        
                        # Check if response has expected structure
                        if "result" in result or "error" in result:
                            print("✓ Valid MCP response structure")
                        else:
                            print("⚠ Unexpected response structure")
                            
                        # Check for expected fields if provided
                        if expected_fields and "result" in result:
                            result_data = result["result"]
                            for field in expected_fields:
                                if field in str(result_data):
                                    print(f"✓ Found expected field: {field}")
                                else:
                                    print(f"⚠ Missing expected field: {field}")
                        
                        return True
                    else:
                        print(f"✗ HTTP Error: {response.status}")
                        error_text = await response.text()
                        print(f"Error details: {error_text}")
                        return False
                        
            except asyncio.TimeoutError:
                print("✗ Request timed out - server may not be running")
                return False
            except aiohttp.ClientConnectorError:
                print("✗ Cannot connect to server - server may not be running")
                print("   To start servers: ./scripts/start_mcp_servers.sh")
                return False
                
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

async def run_tests():
    """Run tests for all MCP servers."""
    print("Running Integration Tests for OpenClaw MCP Servers")
    print("=" * 60)
    
    # Test crawl4ai server
    success_crawl4ai = await test_mcp_server(
        "Crawl4AI", 
        "http://localhost:3000", 
        "scrape_url",
        {"url": "https://httpbin.org/html", "extraction_schema": None},
        ["success", "url", "content"]
    )
    
    # Test notion server
    success_notion = await test_mcp_server(
        "Notion",
        "http://localhost:3001",
        "query_database", 
        {"database_id": "test_db_id", "filter_conditions": None},
        ["success", "error"]
    )
    
    # Test email server
    success_email = await test_mcp_server(
        "Email",
        "http://localhost:3002", 
        "read_emails",
        {"folder": "INBOX", "limit": 1, "unread_only": False},
        ["success", "emails", "count"]
    )
    
    # Test business operations server
    success_business = await test_mcp_server(
        "Business Operations",
        "http://localhost:3003",
        "create_contact",
        {"name": "Test User", "email": "test@example.com", "company": "Test Co"},
        ["success", "contact_id", "name", "email"]
    )
    
    # Test research & analysis server
    success_research = await test_mcp_server(
        "Research & Analysis",
        "http://localhost:3004",
        "analyze_content",
        {"text": "This is a positive test sentence.", "analysis_types": ["sentiment", "entities"]},
        ["success", "results", "analysis_types"]
    )
    
    # Test system & devops server
    success_devops = await test_mcp_server(
        "System & DevOps",
        "http://localhost:3005",
        "get_system_stats",
        {"cpu": True, "memory": True, "disk": True},
        ["success", "stats"]
    )
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print(f"Crawl4AI Server: {'✓ PASS' if success_crawl4ai else '✗ FAIL (Expected if not running)'}")
    print(f"Notion Server: {'✓ PASS' if success_notion else '✗ FAIL (Expected if not running)'}")
    print(f"Email Server: {'✓ PASS' if success_email else '✗ FAIL (Expected if not running)'}")
    print(f"Business Ops Server: {'✓ PASS' if success_business else '✗ FAIL (Expected if not running)'}")
    print(f"Research & Analysis Server: {'✓ PASS' if success_research else '✗ FAIL (Expected if not running)'}")
    print(f"System & DevOps Server: {'✓ PASS' if success_devops else '✗ FAIL (Expected if not running)'}")
    
    all_running = all([success_crawl4ai, success_notion, success_email, success_business, success_research, success_devops])
    
    if all_running:
        print("\n🎉 All servers are responding correctly!")
        print("You can now integrate these with your OpenClaw instance.")
    else:
        print("\n⚠ Some servers are not responding.")
        print("Make sure to start them with: ./scripts/start_mcp_servers.sh")
    
    return all_running

if __name__ == "__main__":
    asyncio.run(run_tests())