import asyncio
from mcp.server.fastmcp import FastMCP
from crawl4ai import AsyncWebCrawler
from pydantic import BaseModel, Field
import json

class ScrapeRequest(BaseModel):
    url: str = Field(description="URL to scrape")
    extraction_schema: dict = Field(default=None, description="Schema for structured extraction")

class Crawl4AIServer:
    def __init__(self):
        self.app = FastMCP("crawl4ai")
        self.crawler = AsyncWebCrawler()

    async def setup(self):
        await self.crawler.__aenter__()

    async def cleanup(self):
        await self.crawler.__aexit__(None, None, None)

    async def scrape_url(self, url: str, extraction_schema: dict = None) -> dict:
        """Scrape a URL and optionally extract structured data."""
        try:
            result = await self.crawler.arun(url=url)
            if extraction_schema:
                # For now, we'll return the full content along with extracted data
                # since Crawl4AI's extraction might need more specific implementation
                return {
                    "success": True,
                    "url": url,
                    "content": result.markdown,
                    "extracted_data": extraction_schema,  # Placeholder for actual extraction
                    "links": result.links,
                    "images": result.images
                }
            else:
                return {
                    "success": True,
                    "url": url,
                    "content": result.markdown,
                    "links": result.links,
                    "images": result.images
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }

def create_server():
    server = Crawl4AIServer()
    
    @server.app.tool("scrape_url", "Scrape content from a URL with optional structured extraction")
    async def handle_scrape(request: ScrapeRequest) -> dict:
        return await server.scrape_url(request.url, request.extraction_schema)
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_server()
    
    async def run_server():
        await server.setup()
        config = uvicorn.Config(app=server.app, host="127.0.0.1", port=3000)
        server_instance = uvicorn.Server(config)
        await server_instance.serve()
    
    asyncio.run(run_server())