import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import requests
import json

class NotionConfig(BaseModel):
    integration_token: str = Field(description="Notion integration token")
    base_url: str = Field(default="https://api.notion.com/v1", description="Notion API base URL")

class PageQuery(BaseModel):
    database_id: str = Field(description="ID of the database to query")
    filter_conditions: dict = Field(default=None, description="Filter conditions for query")

class NotionMCP:
    def __init__(self):
        self.app = FastMCP("notion")
        self.config = None
        
    def set_config(self, config: NotionConfig):
        self.config = config

    async def query_database(self, database_id: str, filter_conditions: dict = None) -> dict:
        """Query a Notion database."""
        if not self.config:
            return {"success": False, "error": "Notion configuration not set"}
            
        headers = {
            "Authorization": f"Bearer {self.config.integration_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        url = f"{self.config.base_url}/databases/{database_id}/query"
        
        payload = {}
        if filter_conditions:
            payload["filter"] = filter_conditions
            
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            return {
                "success": True,
                "pages": response.json().get("results", []),
                "total": response.json().get("total", 0)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def create_notion_server():
    server = NotionMCP()
    
    @server.app.tool("query_database", "Query a Notion database with optional filters")
    async def handle_query(query: PageQuery) -> dict:
        return await server.query_database(query.database_id, query.filter_conditions)
    
    @server.app.tool("create_page", "Create a new page in Notion")
    async def create_page(properties: dict, parent_database_id: str) -> dict:
        if not server.config:
            return {"success": False, "error": "Notion configuration not set"}
            
        headers = {
            "Authorization": f"Bearer {server.config.integration_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        url = "https://api.notion.com/v1/pages"
        
        payload = {
            "parent": {"database_id": parent_database_id},
            "properties": properties
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            return {
                "success": True,
                "page_id": response.json()["id"],
                "url": response.json()["url"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_notion_server()
    
    async def run_server():
        config = NotionConfig(integration_token="your_token_here")
        server.set_config(config)
        
        config_obj = uvicorn.Config(app=server.app, host="127.0.0.1", port=3001)
        server_instance = uvicorn.Server(config_obj)
        await server_instance.serve()
    
    asyncio.run(run_server())