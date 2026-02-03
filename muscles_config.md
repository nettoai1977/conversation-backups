# Muscles Configuration Guide

This guide outlines how to configure your AI "Muscles" for maximum efficiency using your free resources.

## 1. Primary Coding Muscle (NVIDIA API)

### Configuration:
- Model: `nvidia/llama-3.1-405b-instruct` or similar coding-heavy model
- API Endpoint: `https://integrate.api.nvidia.com/v1`
- API Key: [YOUR_NVIDIA_KEY]

### Setup Instructions:
1. Set your NVIDIA API key as an environment variable:
```bash
export NVIDIA_API_KEY="your_actual_nvidia_api_key_here"
```

2. Configure OpenCode to use the NVIDIA backend:
```yaml
models:
  coding:
    provider: nvidia
    model: nvidia/llama-3.1-405b-instruct
    api_key_env: NVIDIA_API_KEY
```

## 2. Web Search Muscle (Brave Search)

### Configuration:
- API Endpoint: `https://api.search.brave.com/res/v1`
- API Key: [YOUR_BRAVE_KEY]
- Purpose: Fact-finding and general web searches

### Setup Instructions:
1. Set your Brave Search API key as an environment variable:
```bash
export BRAVE_API_KEY="your_actual_brave_api_key_here"
```

2. Install/configure the Brave Search skill for OpenClaw

## 3. Deep Research Muscle (Tavily)

### Configuration:
- API Endpoint: `https://api.tavily.com/search`
- API Key: [YOUR_TAVILY_KEY]
- Purpose: Deep dives and comprehensive summaries

### Setup Instructions:
1. Set your Tavily API key as an environment variable:
```bash
export TAVILY_API_KEY="your_actual_tavily_api_key_here"
```

2. Install/configure the Tavily MCP skill for OpenClaw

## 4. Fallback Muscle (DuckDuckGo)

### Configuration:
- Zero-cost fallback for when primary search engines fail
- Available through built-in skill or OneSearch MCP

## 5. Integration with OpenClaw

The `agents.md` file has been updated to reflect the routing priorities:
- Technical tasks → NVIDIA API
- Web research → Brave Search
- Deep research → Tavily
- Fallback → DuckDuckGo

## 6. Environment Variables

Add these to your `.env` file or system environment:
```
NVIDIA_API_KEY=your_nvidia_api_key
BRAVE_API_KEY=your_brave_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## 7. Verification

After setting up the API keys, verify that:
1. Coding tasks route correctly to OpenCode/NVIDIA
2. Web research uses Brave Search first
3. Deep research uses Tavily
4. Fallback to DuckDuckGo works when needed