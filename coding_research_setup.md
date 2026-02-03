# OpenCode & Research Tools Setup Guide

This guide outlines the configuration for setting up OpenCode as your primary coding engine with associated research tools.

## 1. OpenCode Configuration

### Installation Steps:
1. Install OpenCode CLI:
```bash
curl -fsSL https://opencode.ai/install.sh | bash
```

2. Configure OpenCode with NVIDIA API:
Create/edit `~/.config/opencode/config.yaml`:
```yaml
models:
  coding:
    provider: nvidia
    model: nvidia/llama-3.1-405b-instruct  # or latest available coding model
    api_key: [INSERT_YOUR_NVIDIA_API_KEY_HERE]

# Additional model configuration
providers:
  nvidia:
    base_url: "https://integrate.api.nvidia.com/v1"
    api_key_env: NVIDIA_API_KEY
```

3. Set your NVIDIA API key as an environment variable:
```bash
export NVIDIA_API_KEY="your_actual_nvidia_api_key_here"
```

## 2. Web Search Configuration (Free Options)

### Option A: Firecrawl (Free Tier)
The Firecrawl skill can be installed with its free tier (500 requests/month):

1. Install Firecrawl CLI:
```bash
npm install -g @michaelfallis/firecrawl-cl
```

2. Get a free API key from https://firecrawl.dev and set it:
```bash
export FIRECRAWL_API_KEY="your_firecrawl_api_key"
```

### Option B: DuckDuckGo via OneSearch MCP
There appears to be a OneSearch MCP skill that supports DuckDuckGo:

1. Install the OneSearch skill from the OpenClaw skills repository
2. Configure it to use DuckDuckGo as the backend

## 3. Social/X Research Configuration (Free Options)

### Option A: Brave Search (Free Tier)
1. Sign up for a free Brave Search API key at https://brave.com/search/api/
2. Set up the Brave Search skill:
```bash
export BRAVE_API_KEY="your_brave_api_key"
```

### Option B: OpenRouter (Free Models)
1. Create an account at https://openrouter.ai/
2. Some models like `openrouter/auto` may be available without payment
3. Configure OpenRouter in your OpenClaw setup

## 4. Agent Configuration (agents.md)

Update your `agents.md` file with routing instructions:

```markdown
# Agent Routing Configuration

## Coding Tasks
- Route all coding tasks to OpenCode with NVIDIA backend
- Priority: High
- Models: nvidia/llama-3.1-405b-instruct or latest

## Research Tasks  
- Route general web searches to Firecrawl (free tier) or DuckDuckGo via OneSearch
- Route social/X trends to Brave Search or OpenRouter (free models)
- Priority: Medium
- Fallback: Built-in web search tools

## Memory Tasks
- Use persistent memory for context retention
- Follow memory protocols for compaction and search
```

## 5. MCP Server Configuration

To set up the tools as MCP servers that OpenCode can use:

### Firecrawl MCP Server
```bash
# Install firecrawl-cl as MCP server
firecrawl-mcp --api-key $FIRECRAWL_API_KEY
```

### Web Search MCP Server (for DuckDuckGo/Brave)
Create a custom MCP server that interfaces with free search APIs

## 6. Environment Variables Setup

Add to your `.env` file:
```
NVIDIA_API_KEY=your_nvidia_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
BRAVE_API_KEY=your_brave_api_key
OPENROUTER_API_KEY=your_openrouter_api_key_if_needed
```

## 7. Verification Steps

1. Test coding capabilities with a simple code generation task
2. Test web search with a factual query
3. Test social/X trend search with a current events query
4. Verify that all tools are properly routed according to agents.md

Note: Some of these integrations may require custom skill development or MCP server implementations depending on the current availability of pre-built skills in the OpenClaw ecosystem.