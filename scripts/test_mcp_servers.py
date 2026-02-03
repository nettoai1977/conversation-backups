import asyncio
import aiohttp
import json
from typing import Dict, Any

async def test_mcp_server(server_name: str, server_url: str, tool_name: str, params: Dict[str, Any]):
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
                    result = await response.json()
                    print(f"Response: {json.dumps(result, indent=2)}")
                    return result
            except asyncio.TimeoutError:
                print(f"ERROR: Timeout connecting to {server_url}")
                return {"error": "timeout"}
            except Exception as e:
                print(f"ERROR: Failed to connect to {server_url}: {str(e)}")
                return {"error": str(e)}
                
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

async def run_tests():
    """Run tests for all MCP servers."""
    print("Testing MCP Servers - Note: Servers must be running first!")
    print("Run 'bash scripts/start_mcp_servers.sh' before running this test.")
    
    # Test crawl4ai server
    await test_mcp_server(
        "Crawl4AI", 
        "http://localhost:3000", 
        "scrape_url",
        {"url": "https://httpbin.org/html", "extraction_schema": None}
    )
    
    # Test notion server
    await test_mcp_server(
        "Notion",
        "http://localhost:3001",
        "query_database", 
        {"database_id": "test_db_id", "filter_conditions": None}
    )
    
    # Test email server
    await test_mcp_server(
        "Email",
        "http://localhost:3002", 
        "read_emails",
        {"folder": "INBOX", "limit": 5, "unread_only": False}
    )
    
    # Test business ops server
    await test_mcp_server(
        "Business Operations",
        "http://localhost:3003",
        "create_task",
        {"title": "Test Task", "description": "Test description", "assignee": "test@example.com"}
    )
    
    # Test research & analysis server
    await test_mcp_server(
        "Research & Analysis",
        "http://localhost:3004",
        "analyze_content",
        {"text": "This is a great product with excellent features.", "analysis_types": ["sentiment", "entities"]}
    )
    
    # Test system & devops server
    await test_mcp_server(
        "System & DevOps",
        "http://localhost:3005",
        "get_system_stats",
        {"cpu": True, "memory": True, "disk": True, "network": False}
    )

if __name__ == "__main__":
    asyncio.run(run_tests())