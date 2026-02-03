# OpenClaw Multi-Agent Systems & Integration Tools Implementation

This repository contains the implementation of the research findings on multi-agent systems and integration tools for OpenClaw, based on the comprehensive research conducted in the following areas:

- Multi-Agent Systems & Skills Development
- Integration Tools Research (Scraper tools, MCP tools, CLI tools)
- Modular Skills Architecture
- MCP Server Implementations

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [MCP Servers](#mcp-servers)
3. [Skills Registry](#skills-registry)
4. [Multi-Agent System](#multi-agent-system)
5. [Installation & Setup](#installation--setup)
6. [Usage Examples](#usage-examples)
7. [Configuration](#configuration)
8. [Testing](#testing)

## Architecture Overview

The implementation follows the architectural patterns identified in the research:

- **Orchestrator-Worker Pattern**: Central coordinator assigns tasks to specialized worker agents
- **Modular Skills Architecture**: Atomic, composite, and adaptive skills
- **MCP Integration**: Model Context Protocol servers for external service integration
- **Hierarchical Organization**: Organized into categories for scalability

## MCP Servers

We've implemented seven MCP servers based on the research findings:

### 1. Crawl4AI Server (`mcp-servers/crawl4ai_mcp_server.py`)
- Advanced web scraping with LLM-friendly crawling
- Automated schema generation for structured data extraction
- Domain-specific scrapers for common platforms

### 2. Notion Server (`mcp-servers/notion_mcp_server.py`)
- Notion API integration for pages and databases
- Query and create operations for Notion content
- Secure authentication and authorization

### 3. Email Server (`mcp-servers/email_mcp_server.py`)
- Email sending and receiving capabilities
- Attachment handling and email categorization
- IMAP and SMTP integration

### 4. Business Operations Server (`mcp-servers/business_ops_mcp_server.py`)
- Email, calendar, contact, and task management
- Integrated business workflow operations
- Scheduling and coordination tools

### 5. Research & Analysis Server (`mcp-servers/research_analysis_mcp_server.py`)
- Web scraping, content analysis, and data processing
- Report generation and insight extraction
- Entity recognition and sentiment analysis

### 6. System & DevOps Server (`mcp-servers/system_devops_mcp_server.py`)
- System monitoring and resource tracking
- File operations and process management
- Network operations and connectivity checks

### 7. Kimi K2.5 Server (`mcp-servers/kimi_k25_mcp_server.py`)
- Access to Kimi K2.5 1T multimodal MoE model through NVIDIA's NIM platform
- Supports both thinking mode and instant mode for different use cases
- Multimodal capabilities for image and text processing
- OpenAI-compatible API interface

### 8. Local Kimi K2.5 Deployment Option (`local_kimi_deployment/`)
- Local deployment capability using GGUF format from Unsloth
- 1-bit quantized model reduces 1.09TB to ~230GB with quality preservation
- Privacy-focused: run Kimi K2.5 on your own hardware
- Includes setup scripts, model downloader, and local server wrapper
- Detailed deployment guide for different hardware configurations

## Skills Registry

The skills registry implements the enhanced skills architecture:

- **Atomic Skills**: Single responsibility, stateless operations
- **Composite Skills**: Combinations of atomic skills
- **Adaptive Skills**: Learning and improvement capabilities

Located in: `skills/skills_registry.py`

## Multi-Agent System

Implementation of the orchestrator-worker pattern with:

- Task assignment and load balancing
- Agent coordination and communication
- Priority-based task processing
- Status tracking and monitoring

Located in: `multi_agent_system/orchestrator_worker.py`

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip package manager
- OpenClaw installation
- NVIDIA API key for Kimi K2.5 access

### Setup Steps

1. Install required dependencies:
```bash
pip install mcp crawl4ai pydantic requests psutil uvicorn openai
```

2. Start all MCP servers:
```bash
bash scripts/start_mcp_servers.sh
```

3. Verify servers are running:
```bash
python scripts/test_all_servers.py
```

## Usage Examples

### Starting MCP Servers
```bash
# Start all servers in the background
bash scripts/start_mcp_servers.sh

# Check server status
ps aux | grep mcp_server
```

### Using the Kimi K2.5 Server
```bash
# Test the Kimi K2.5 server specifically
python scripts/test_kimi_k25.py

# Or test all servers including Kimi K2.5
python scripts/test_all_servers.py
```

### Using the Skills Registry
```python
from skills.skills_registry import skills_registry

# Execute a skill
result = skills_registry.execute_skill("send_email", recipient="user@example.com", subject="Test", body="Hello")
print(result)
```

### Using the Multi-Agent System
```python
import asyncio
from multi_agent_system.orchestrator_worker import MultiAgentSystem, example_worker_executor

async def example():
    mas = MultiAgentSystem()
    orchestrator = mas.setup_orchestrator()
    worker = mas.add_worker_agent("my_worker", ["general"], example_worker_executor)
    
    result = await mas.submit_task("Process this data", priority=2)
    print(result)

asyncio.run(example)
```

## Configuration

### MCP Server Configuration
Located in `config/mcp_servers_config.json`, this file defines all MCP server endpoints and settings:

```json
{
  "crawl4ai": {
    "url": "http://localhost:3000",
    "enabled": true,
    "name": "Web Scraping Server",
    "description": "Advanced web scraping with Crawl4AI",
    "health_check_interval": 30
  },
  "kimi_k25": {
    "url": "http://localhost:3006",
    "enabled": true,
    "name": "Kimi K2.5 AI Server",
    "description": "Kimi K2.5 1T multimodal MoE model access",
    "health_check_interval": 30
  }
  ...
}
```

### OpenClaw Integration
To integrate with OpenClaw, add the MCP server configurations to your OpenClaw configuration:

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
    "kimi_k25": {
      "url": "http://localhost:3006",
      "enabled": true
    }
    // ... other servers
  }
}
```

## Testing

### Server Tests
Run the test script to verify all MCP servers are responding:

```bash
python scripts/test_all_servers.py
```

### Kimi K2.5 Specific Tests
Test the Kimi K2.5 server specifically:

```bash
python scripts/test_kimi_k25.py
```

### Skills Tests
Test the skills registry:

```python
from skills.skills_registry import skills_registry

# List all available skills
all_skills = skills_registry.get_all_skills()
print(f"Available skills: {list(all_skills.keys())}")

# Execute a sample skill
result = skills_registry.execute_skill("search_web", query="OpenClaw")
print(result)
```

### Multi-Agent System Tests
Test the multi-agent system:

```bash
python multi_agent_system/orchestrator_worker.py
```

## Security Considerations

- All MCP servers run in isolated environments
- Input validation and sanitization implemented
- Authentication mechanisms for protected APIs
- Rate limiting to prevent abuse
- Comprehensive audit logging
- API key management for external services like Kimi K2.5

## Extending the System

### Adding New MCP Servers
1. Create a new server file in `mcp-servers/`
2. Implement the server using the MCP framework
3. Add the server to the configuration file
4. Update the startup script to launch the new server

### Adding New Skills
1. Create a new skill function
2. Register it with the skills registry
3. Define input/output schemas if needed
4. Test the skill integration

## Performance Optimization

- Caching for frequently requested data
- Asynchronous processing where possible
- Connection pooling for external services
- Load balancing across agents
- Resource monitoring and alerts

## Troubleshooting

### Common Issues

1. **Servers not starting**: Check logs in the `logs/` directory
2. **Connection timeouts**: Verify server URLs in the configuration
3. **Permission errors**: Ensure proper authentication setup
4. **High resource usage**: Monitor system stats with the DevOps server
5. **Kimi K2.5 API errors**: Verify your NVIDIA API key is correctly configured in the server

### Checking Server Status
```bash
# Check if servers are running
ps aux | grep mcp_server

# Check logs
tail -f logs/crawl4ai.log
tail -f logs/notion.log
tail -f logs/kimi_k25.log
# ... etc
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Add your implementation
4. Include tests for new functionality
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the terms of the license specified in the main OpenClaw repository.

## Acknowledgments

This implementation is based on the comprehensive research documented in the following files:
- `multi-agent-research.md`
- `integration-tools-research.md`
- `implementation-guide.md`
- `enhancement-plan.md`
- `skills-enhancement-plan.md`
- `executive-summary-integrations.md`