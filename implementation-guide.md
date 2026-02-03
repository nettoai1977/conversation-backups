# Practical Implementation Guide: OpenClaw Integrations

## Getting Started with Enhanced Integrations

### Prerequisites
- OpenClaw installation with admin access
- Basic understanding of MCP (Model Context Protocol)
- Access to external services (API keys, credentials)
- Development environment for custom MCP servers

## 1. Web Scraping Enhancement Implementation

### A. Setting up Crawl4AI Integration

#### Installation
```bash
pip install crawl4ai
```

#### Create MCP Server for Crawl4AI
Create a file `crawl4ai_mcp_server.py`:

```python
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
                extracted = await self.crawler.extract_straight_text(
                    url=url,
                    extraction_schema=json.dumps(extraction_schema)
                )
                return {
                    "success": True,
                    "url": url,
                    "content": result.markdown,
                    "extracted_data": extracted.extracted_content if extracted else None
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
```

#### Configuration for OpenClaw
Add to your OpenClaw configuration:

```json
{
  "mcpServers": {
    "crawl4ai": {
      "url": "http://localhost:3000",
      "enabled": true
    }
  }
}
```

### B. Enhanced Browser Automation Scripts

Create a scraping workflow script `browser_scraper.py`:

```python
import asyncio
from playwright.async_api import async_playwright
import json
from urllib.parse import urljoin, urlparse

class BrowserScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        
    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_with_login(self, base_url, login_data, target_url, selectors):
        """Scrape content from a site that requires login."""
        page = await self.browser.new_page()
        
        try:
            # Navigate to login page
            await page.goto(base_url)
            
            # Perform login
            for field, value in login_data.items():
                await page.fill(f'[name="{field}"]', value)
            
            await page.click('button[type="submit"]')
            await page.wait_for_load_state('networkidle')
            
            # Navigate to target page
            await page.goto(target_url)
            await page.wait_for_load_state('networkidle')
            
            # Extract data using selectors
            results = {}
            for name, selector in selectors.items():
                try:
                    element = await page.query_selector(selector)
                    if element:
                        results[name] = await element.text_content()
                    else:
                        results[name] = None
                except:
                    results[name] = None
            
            return {
                "success": True,
                "url": target_url,
                "data": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": target_url
            }
        finally:
            await page.close()

# Usage example
async def main():
    scraper = BrowserScraper()
    await scraper.start()
    
    login_info = {
        "username": "your_username",
        "password": "your_password"
    }
    
    selectors = {
        "title": "h1",
        "price": ".price",
        "description": ".description"
    }
    
    result = await scraper.scrape_with_login(
        base_url="https://example.com/login",
        login_data=login_info,
        target_url="https://example.com/product/123",
        selectors=selectors
    )
    
    print(json.dumps(result, indent=2))
    await scraper.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## 2. MCP Server Implementation Examples

### A. Notion MCP Server

Create `notion_mcp_server.py`:

```python
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
```

### B. Email MCP Server

Create `email_mcp_server.py`:

```python
import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import email
import json
from typing import List, Optional

class EmailConfig(BaseModel):
    smtp_server: str = Field(description="SMTP server address")
    smtp_port: int = Field(default=587, description="SMTP server port")
    email_address: EmailStr = Field(description="Email address for sending/receiving")
    password: str = Field(description="Email password or app password")
    imap_server: str = Field(description="IMAP server address")

class SendEmailRequest(BaseModel):
    to: List[EmailStr] = Field(description="Recipients' email addresses")
    subject: str = Field(description="Email subject")
    body: str = Field(description="Email body content")
    cc: List[EmailStr] = Field(default=[], description="CC recipients")
    bcc: List[EmailStr] = Field(default=[], description="BCC recipients")
    attachments: List[str] = Field(default=[], description="File paths to attach")

class ReadEmailsRequest(BaseModel):
    folder: str = Field(default="INBOX", description="Mail folder to read from")
    limit: int = Field(default=10, description="Maximum number of emails to return")
    unread_only: bool = Field(default=False, description="Only return unread emails")

class EmailMCP:
    def __init__(self):
        self.app = FastMCP("email")
        self.config = None
        
    def set_config(self, config: EmailConfig):
        self.config = config

    async def send_email(self, to: List[str], subject: str, body: str, 
                         cc: List[str] = [], bcc: List[str] = [], 
                         attachments: List[str] = []) -> dict:
        """Send an email with optional attachments."""
        if not self.config:
            return {"success": False, "error": "Email configuration not set"}
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.email_address
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            for file_path in attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.split("/")[-1]}'
                    )
                    msg.attach(part)
            
            # Connect to server and send email
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.email_address, self.config.password)
            
            all_recipients = to + cc + bcc
            text = msg.as_string()
            server.sendmail(self.config.email_address, all_recipients, text)
            server.quit()
            
            return {
                "success": True,
                "message": f"Email sent to {len(to)} recipients"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def read_emails(self, folder: str = "INBOX", limit: int = 10, 
                          unread_only: bool = False) -> dict:
        """Read emails from specified folder."""
        if not self.config:
            return {"success": False, "error": "Email configuration not set"}
        
        try:
            mail = imaplib.IMAP4_SSL(self.config.imap_server)
            mail.login(self.config.email_address, self.config.password)
            mail.select(folder)
            
            # Search criteria
            search_criteria = "(UNSEEN)" if unread_only else "ALL"
            status, messages = mail.search(None, search_criteria)
            
            email_ids = messages[0].split()
            email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            emails = []
            for e_id in reversed(email_ids):  # Reverse to get newest first
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                email_info = {
                    "id": e_id.decode(),
                    "subject": msg.get("Subject", ""),
                    "from": msg.get("From", ""),
                    "date": msg.get("Date", ""),
                    "body": ""
                }
                
                # Extract body
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            email_info["body"] = part.get_payload(decode=True).decode()
                            break
                else:
                    email_info["body"] = msg.get_payload(decode=True).decode()
                
                emails.append(email_info)
            
            mail.close()
            mail.logout()
            
            return {
                "success": True,
                "emails": emails,
                "count": len(emails)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

def create_email_server():
    server = EmailMCP()
    
    @server.app.tool("send_email", "Send an email with optional attachments")
    async def handle_send_email(req: SendEmailRequest) -> dict:
        return await server.send_email(
            req.to, req.subject, req.body, 
            req.cc, req.bcc, req.attachments
        )
    
    @server.app.tool("read_emails", "Read emails from specified folder")
    async def handle_read_emails(req: ReadEmailsRequest) -> dict:
        return await server.read_emails(req.folder, req.limit, req.unread_only)
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_email_server()
    
    # Example configuration (replace with real credentials)
    config = EmailConfig(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        email_address="your_email@gmail.com",
        password="your_app_password",
        imap_server="imap.gmail.com"
    )
    server.set_config(config)
    
    async def run_server():
        config_obj = uvicorn.Config(app=server.app, host="127.0.0.1", port=3002)
        server_instance = uvicorn.Server(config_obj)
        await server_instance.serve()
    
    asyncio.run(run_server())
```

## 3. CLI Tools Integration

### A. Enhanced exec Tool Usage

Create a script to demonstrate enhanced CLI integration:

```bash
#!/bin/bash
# enhanced_cli_integration.sh

# Function to create a structured CLI tool
run_enhanced_command() {
    local command="$1"
    local description="$2"
    local timeout="${3:-30}"
    
    echo "Executing: $command"
    echo "Description: $description"
    
    # Execute with timeout and capture output
    timeout $timeout bash -c "$command" 2>&1
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "Status: SUCCESS"
    else
        echo "Status: FAILED (exit code: $exit_code)"
    fi
}

# Example usage of enhanced CLI integration
echo "=== Enhanced CLI Integration Examples ==="

# System monitoring
run_enhanced_command "df -h" "Check disk space usage" 10

# Process management
run_enhanced_command "ps aux | grep python" "Find Python processes" 10

# Network connectivity
run_enhanced_command "ping -c 3 google.com" "Test internet connectivity" 15

# File operations
run_enhanced_command "find /tmp -name '*.tmp' -mtime +1 -delete" "Clean old temp files" 30
```

### B. n8n Workflow Integration

Create an example n8n workflow JSON that can be controlled via OpenClaw:

```json
{
  "name": "Web Scraping Workflow",
  "nodes": [
    {
      "parameters": {},
      "id": "start-node",
      "name": "Start",
      "type": "n8n-nodes-base.start",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "url",
              "value": "={{ $json.url }}"
            }
          ]
        }
      },
      "id": "set-url-node",
      "name": "Set URL",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [500, 300]
    },
    {
      "parameters": {
        "url": "={{ $json.url }}",
        "response": {
          "response": {
            "fullResponse": false
          }
        }
      },
      "id": "http-request-node",
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [700, 300]
    },
    {
      "parameters": {
        "values": {
          "string": [
            {
              "name": "content",
              "value": "={{ $response.body }}"
            }
          ]
        }
      },
      "id": "extract-content-node",
      "name": "Extract Content",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [900, 300]
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [
          {
            "node": "Set URL",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Set URL": {
      "main": [
        [
          {
            "node": "HTTP Request",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "HTTP Request": {
      "main": [
        [
          {
            "node": "Extract Content",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "pinData": {},
  "settings": {
    "callerPolicy": "own",
    "errorWorkflow": "",
    "saveManualExecutions": false,
    "executionOrder": "v1"
  },
  "staticData": null,
  "tags": [],
  "triggerCount": 0,
  "updatedAt": "2024-01-01T00:00:00.000Z",
  "versionId": "12345"
}
```

## 4. Configuration and Deployment

### A. MCP Server Configuration

Create `mcp_servers_config.json`:

```json
{
  "crawl4ai": {
    "url": "http://localhost:3000",
    "enabled": true,
    "name": "Web Scraping Server",
    "description": "Advanced web scraping with Crawl4AI",
    "health_check_interval": 30
  },
  "notion": {
    "url": "http://localhost:3001", 
    "enabled": true,
    "name": "Notion Integration Server",
    "description": "Notion API integration for pages and databases",
    "health_check_interval": 30
  },
  "email": {
    "url": "http://localhost:3002",
    "enabled": true,
    "name": "Email Management Server", 
    "description": "Email sending and reading capabilities",
    "health_check_interval": 30
  }
}
```

### B. OpenClaw Integration Configuration

Add to your OpenClaw configuration file:

```json
{
  "mcpServers": {
    "crawl4ai": {
      "url": "http://localhost:3000",
      "enabled": true
    },
    "notion": {
      "url": "http://localhost:3001", 
      "enabled": true
    },
    "email": {
      "url": "http://localhost:3002",
      "enabled": true
    }
  },
  "tools": {
    "allow": [
      "crawl4ai:*",
      "notion:*", 
      "email:*",
      "browser",
      "web_search",
      "web_fetch",
      "exec"
    ]
  }
}
```

## 5. Testing and Validation

### A. Test Script for MCP Servers

Create `test_integrations.py`:

```python
import asyncio
import aiohttp
import json

async def test_mcp_server(server_name, server_url, tool_name, params):
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
            
            async with session.post(f"{server_url}", json=payload) as response:
                result = await response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

async def run_tests():
    """Run tests for all MCP servers."""
    
    # Test crawl4ai server
    await test_mcp_server(
        "Crawl4AI", 
        "http://localhost:3000", 
        "scrape_url",
        {"url": "https://example.com", "extraction_schema": None}
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

if __name__ == "__main__":
    asyncio.run(run_tests())
```

### B. Integration Verification

Run the following to verify your setup:

```bash
# Start each MCP server in separate terminals
python crawl4ai_mcp_server.py  # Port 3000
python notion_mcp_server.py    # Port 3001  
python email_mcp_server.py     # Port 3002

# Test the integrations
python test_integrations.py

# Verify in OpenClaw
openclaw tools list  # Should show the new MCP tools
```

This implementation guide provides practical examples for integrating advanced scraping tools, MCP servers, and CLI tools with OpenClaw. Each section includes runnable code examples that can be adapted to your specific needs.