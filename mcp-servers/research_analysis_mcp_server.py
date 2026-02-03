import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
import requests
from urllib.parse import urlparse
import re

class ScrapeRequest(BaseModel):
    url: str = Field(description="URL to scrape")
    extraction_schema: Optional[Dict] = Field(default=None, description="Schema for structured extraction")

class ContentAnalysisRequest(BaseModel):
    text: str = Field(description="Text to analyze")
    analysis_types: List[str] = Field(default=["summarize"], description="Types of analysis to perform")

class DataProcessingRequest(BaseModel):
    data: List[Dict] = Field(description="Data to process")
    operations: List[str] = Field(default=["clean"], description="Operations to perform")

class ReportGenerationRequest(BaseModel):
    findings: List[Dict] = Field(description="Findings to include in report")
    format_type: str = Field(default="markdown", description="Output format")

class ResearchAnalysisMCP:
    def __init__(self):
        self.app = FastMCP("research-analysis")
        
    async def scrape_url(self, url: str, extraction_schema: Optional[Dict] = None) -> dict:
        """Scrape content from a URL."""
        try:
            # This would normally use a proper scraping tool like the Crawl4AI server
            # For simulation, we'll return a mock response
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            return {
                "success": True,
                "url": url,
                "domain": domain,
                "content_preview": f"Content from {domain} - simulated scraping result",
                "extraction_schema": extraction_schema,
                "timestamp": asyncio.get_event_loop().time()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }

    async def analyze_content(self, text: str, analysis_types: List[str]) -> dict:
        """Analyze content based on specified analysis types."""
        try:
            results = {}
            
            if "summarize" in analysis_types:
                # Simple summarization simulation
                sentences = text.split('.')
                summary_length = min(3, len(sentences))
                results["summary"] = '. '.join(sentences[:summary_length]) + '.'
            
            if "sentiment" in analysis_types:
                # Simple sentiment analysis simulation
                positive_words = ['good', 'great', 'excellent', 'positive', 'wonderful']
                negative_words = ['bad', 'terrible', 'awful', 'negative', 'horrible']
                
                pos_count = sum(1 for word in positive_words if word.lower() in text.lower())
                neg_count = sum(1 for word in negative_words if word.lower() in text.lower())
                
                if pos_count > neg_count:
                    results["sentiment"] = "positive"
                elif neg_count > pos_count:
                    results["sentiment"] = "negative"
                else:
                    results["sentiment"] = "neutral"
                    
            if "entities" in analysis_types:
                # Simple entity extraction simulation
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, text)
                
                phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
                phones = re.findall(phone_pattern, text)
                
                results["entities"] = {
                    "emails": emails,
                    "phones": phones
                }
            
            return {
                "success": True,
                "analysis_types": analysis_types,
                "results": results,
                "input_length": len(text)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def process_data(self, data: List[Dict], operations: List[str]) -> dict:
        """Process data according to specified operations."""
        try:
            processed_data = data.copy()
            
            for operation in operations:
                if operation == "clean":
                    # Remove empty values and normalize
                    cleaned_data = []
                    for item in processed_data:
                        cleaned_item = {}
                        for k, v in item.items():
                            if v is not None and v != "":
                                cleaned_item[k] = v
                        if cleaned_item:
                            cleaned_data.append(cleaned_item)
                    processed_data = cleaned_data
                    
                elif operation == "deduplicate":
                    # Remove duplicates based on all fields
                    seen = set()
                    unique_data = []
                    for item in processed_data:
                        item_tuple = tuple(sorted(item.items()))
                        if item_tuple not in seen:
                            seen.add(item_tuple)
                            unique_data.append(item)
                    processed_data = unique_data
                    
                elif operation == "standardize":
                    # Convert field names to lowercase and trim whitespace
                    standardized_data = []
                    for item in processed_data:
                        standardized_item = {}
                        for k, v in item.items():
                            standardized_key = k.lower().strip().replace(" ", "_")
                            if isinstance(v, str):
                                standardized_value = v.strip()
                            else:
                                standardized_value = v
                            standardized_item[standardized_key] = standardized_value
                        standardized_data.append(standardized_item)
                    processed_data = standardized_data
            
            return {
                "success": True,
                "original_count": len(data),
                "processed_count": len(processed_data),
                "operations": operations,
                "data": processed_data
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_report(self, findings: List[Dict], format_type: str = "markdown") -> dict:
        """Generate a report from findings."""
        try:
            if format_type == "markdown":
                report_content = "# Research Report\n\n"
                for i, finding in enumerate(findings, 1):
                    report_content += f"## Finding {i}\n"
                    for key, value in finding.items():
                        report_content += f"- **{key.capitalize()}**: {value}\n"
                    report_content += "\n"
            elif format_type == "json":
                report_content = json.dumps({
                    "report_type": "research_findings",
                    "findings": findings,
                    "generated_at": asyncio.get_event_loop().time()
                }, indent=2)
            else:
                report_content = str(findings)
            
            return {
                "success": True,
                "format": format_type,
                "content": report_content,
                "finding_count": len(findings)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def create_research_analysis_server():
    server = ResearchAnalysisMCP()
    
    @server.app.tool("scrape_url", "Scrape content from a URL with optional structured extraction")
    async def handle_scrape(request: ScrapeRequest) -> dict:
        return await server.scrape_url(request.url, request.extraction_schema)
    
    @server.app.tool("analyze_content", "Analyze content with various analysis techniques")
    async def handle_analyze(request: ContentAnalysisRequest) -> dict:
        return await server.analyze_content(request.text, request.analysis_types)
    
    @server.app.tool("process_data", "Process data with various operations")
    async def handle_process(request: DataProcessingRequest) -> dict:
        return await server.process_data(request.data, request.operations)
    
    @server.app.tool("generate_report", "Generate a report from findings")
    async def handle_generate_report(request: ReportGenerationRequest) -> dict:
        return await server.generate_report(request.findings, request.format_type)
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_research_analysis_server()
    
    async def run_server():
        config_obj = uvicorn.Config(app=server.app, host="127.0.0.1", port=3004)
        server_instance = uvicorn.Server(config_obj)
        await server_instance.serve()
    
    asyncio.run(run_server())