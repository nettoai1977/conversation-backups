"""
n8n Workflow Integration for OpenClaw
Implements n8n workflow management and execution capabilities
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

class N8nIntegration:
    """Integration with n8n workflow automation platform"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to n8n API"""
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                if method.upper() == 'GET':
                    async with session.get(url, headers=self.headers) as response:
                        return await response.json()
                elif method.upper() in ['POST', 'PUT']:
                    async with session.post(url, headers=self.headers, json=data) as response:
                        return await response.json()
                elif method.upper() == 'PATCH':
                    async with session.patch(url, headers=self.headers, json=data) as response:
                        return await response.json()
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "url": url
                }
    
    async def list_workflows(self) -> Dict[str, Any]:
        """List all available workflows"""
        return await self._make_request('GET', '/workflows')
    
    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get details of a specific workflow"""
        return await self._make_request('GET', f'/workflows/{workflow_id}')
    
    async def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow"""
        return await self._make_request('POST', '/workflows', workflow_data)
    
    async def execute_workflow(self, workflow_id: str, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a workflow with optional input data"""
        execution_data = {
            "workflowId": workflow_id
        }
        
        if input_data:
            execution_data["data"] = input_data
        
        return await self._make_request('POST', '/executions', execution_data)
    
    async def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get details of a specific execution"""
        return await self._make_request('GET', f'/executions/{execution_id}')
    
    async def list_executions(self, workflow_id: str = None) -> Dict[str, Any]:
        """List executions, optionally filtered by workflow ID"""
        endpoint = '/executions'
        if workflow_id:
            endpoint += f'?workflowId={workflow_id}'
        
        return await self._make_request('GET', endpoint)
    
    async def stop_execution(self, execution_id: str) -> Dict[str, Any]:
        """Stop a running execution"""
        return await self._make_request('POST', f'/executions/{execution_id}/stop')

class N8nWorkflowManager:
    """Higher-level manager for n8n workflows with OpenClaw integration"""
    
    def __init__(self, n8n_base_url: str, n8n_api_key: str):
        self.n8n = N8nIntegration(n8n_base_url, n8n_api_key)
        self.workflow_templates = self._load_workflow_templates()
    
    def _load_workflow_templates(self) -> Dict[str, Any]:
        """Load predefined workflow templates"""
        return {
            "web_scraping": {
                "name": "Web Scraping Workflow",
                "description": "Automated web scraping with data processing",
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
                                    "fullResponse": False
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
                }
            },
            "email_automation": {
                "name": "Email Automation Workflow",
                "description": "Automated email sending and tracking",
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
                            "operation": "send",
                            "sender": "={{ $json.sender }}",
                            "recipients": "={{ $json.recipients }}",
                            "subject": "={{ $json.subject }}",
                            "text": "={{ $json.body }}"
                        },
                        "id": "send-email-node",
                        "name": "Send Email",
                        "type": "n8n-nodes-base.emailSend",
                        "typeVersion": 1,
                        "position": [500, 300]
                    }
                ],
                "connections": {
                    "Start": {
                        "main": [
                            [
                                {
                                    "node": "Send Email",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    }
                }
            },
            "data_processing": {
                "name": "Data Processing Workflow",
                "description": "Process and transform data",
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
                            "functionCode": "return [{\n    json: {\n        ...$input.all()[0].json,\n        processed: true,\n        timestamp: new Date().toISOString()\n    }\n}];"
                        },
                        "id": "process-data-node",
                        "name": "Process Data",
                        "type": "n8n-nodes-base.function",
                        "typeVersion": 1,
                        "position": [500, 300]
                    }
                ],
                "connections": {
                    "Start": {
                        "main": [
                            [
                                {
                                    "node": "Process Data",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    }
                }
            }
        }
    
    async def create_predefined_workflow(self, template_name: str, name: str = None) -> Dict[str, Any]:
        """Create a workflow from a predefined template"""
        if template_name not in self.workflow_templates:
            return {
                "success": False,
                "error": f"Template '{template_name}' not found"
            }
        
        template = self.workflow_templates[template_name].copy()
        template["name"] = name or f"{template['name']} - {uuid.uuid4().hex[:8]}"
        
        return await self.n8n.create_workflow(template)
    
    async def run_web_scraping_workflow(self, urls: List[str]) -> Dict[str, Any]:
        """Run a web scraping workflow for given URLs"""
        # First, create the workflow if it doesn't exist
        workflow_result = await self.create_predefined_workflow("web_scraping", f"Scraping Workflow - {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not workflow_result.get("success"):
            return workflow_result
        
        workflow_id = workflow_result.get("id")
        
        # Execute the workflow for each URL
        results = []
        for url in urls:
            execution_result = await self.n8n.execute_workflow(workflow_id, {"url": url})
            results.append(execution_result)
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "executions": results,
            "urls_processed": len(urls)
        }
    
    async def run_email_workflow(self, sender: str, recipients: List[str], subject: str, body: str) -> Dict[str, Any]:
        """Run an email automation workflow"""
        workflow_result = await self.create_predefined_workflow("email_automation", f"Email Workflow - {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not workflow_result.get("success"):
            return workflow_result
        
        workflow_id = workflow_result.get("id")
        
        # Execute the workflow
        execution_result = await self.n8n.execute_workflow(workflow_id, {
            "sender": sender,
            "recipients": recipients,
            "subject": subject,
            "body": body
        })
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "execution": execution_result
        }
    
    async def run_data_processing_workflow(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run a data processing workflow"""
        workflow_result = await self.create_predefined_workflow("data_processing", f"Data Processing Workflow - {datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        if not workflow_result.get("success"):
            return workflow_result
        
        workflow_id = workflow_result.get("id")
        
        # Execute the workflow
        execution_result = await self.n8n.execute_workflow(workflow_id, {"data": data})
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "execution": execution_result
        }

# Example usage and testing
async def test_n8n_integration():
    """Test the n8n integration"""
    print("Testing n8n integration...")
    
    # This would require a real n8n instance to test properly
    # For demonstration, we'll show the expected usage
    
    # n8n_manager = N8nWorkflowManager("http://localhost:5678", "your_api_key_here")
    # 
    # # Test web scraping workflow
    # scraping_result = await n8n_manager.run_web_scraping_workflow(["https://example.com"])
    # print("Web scraping result:", scraping_result)
    # 
    # # Test email workflow
    # email_result = await n8n_manager.run_email_workflow(
    #     "sender@example.com",
    #     ["recipient@example.com"],
    #     "Test Subject",
    #     "Test Body"
    # )
    # print("Email result:", email_result)
    
    print("N8n integration classes created successfully")
    print("To use: Initialize N8nWorkflowManager with your n8n instance URL and API key")

if __name__ == "__main__":
    asyncio.run(test_n8n_integration())