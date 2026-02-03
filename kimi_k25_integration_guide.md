# Kimi K2.5 Integration Guide for OpenClaw

Based on the research findings, here's a comprehensive guide to properly integrate Kimi K2.5 with OpenClaw for optimal performance.

## Recommended Configuration Approach

### 1. API Key Setup
- Obtain Kimi API key from Moonshot AI
- Store as KIMI_API_KEY environment variable
- Use secure credential management

### 2. OpenClaw Configuration
Based on the documentation found, the recommended configuration is:

```json
{
  "env": {
    "KIMI_API_KEY": "sk-..."
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5"
      },
      "models": {
        "kimi-coding/k2p5": {
          "alias": "Kimi K2.5"
        }
      }
    }
  }
}
```

### 3. Moonshot Model References
- Moonshot models use format: moonshot/<modelId>
- Kimi Coding models use format: kimi-coding/<modelId>
- Recommended primary model: kimi-coding/k2p5

### 4. Best Practices
- Use Kimi K2.5 as the strategic muscle for visual analysis, deep research, and verification
- Integrate with Fireworks AI for enhanced performance if needed
- Implement proper error handling and rate limiting
- Monitor token usage for cost optimization

### 5. Integration Benefits
- Enhanced reasoning capabilities
- Improved visual analysis
- Advanced research and verification
- Better code review and logical verification
- Complements existing OpenCode and search capabilities