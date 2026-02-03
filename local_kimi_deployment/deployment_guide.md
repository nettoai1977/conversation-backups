# Kimi K2.5 Local Deployment Guide

This guide explains how to deploy Kimi K2.5 locally on your own hardware using the open-source GGUF format.

## Overview

Kimi K2.5 is one of the most advanced open-source models available, featuring:
- 1 Trillion parameters
- Mixture of Experts (MoE) architecture
- Multimodal capabilities
- Advanced reasoning and agentic abilities
- 256K token context length

Thanks to the work by Unsloth, the 1.09TB full model has been quantized to just 230GB (1-bit) while maintaining quality.

## Hardware Requirements

### Minimum Requirements
- **Disk Space**: 230GB+ (for 1-bit quantized model)
- **RAM**: 16GB+ (can run with less using disk offloading, but slowly)
- **VRAM**: Optional (can run on CPU, but slowly)

### Recommended Requirements
- **Combined RAM+VRAM**: 247GB+ for optimal performance (5+ tokens/sec)
- **VRAM**: 24GB+ (for GPU acceleration)
- **CPU**: Multi-core processor with good single-threaded performance
- **Storage**: SSD recommended for faster loading

## Deployment Methods

### Method 1: Using llama.cpp (Recommended)

llama.cpp offers the best compatibility and performance across different hardware.

1. **Install Dependencies**:
   ```bash
   bash setup_local_kimi.sh
   ```

2. **Download the Model**:
   ```bash
   python3 download_model.py
   ```

3. **Run Directly with llama.cpp**:
   ```bash
   ./llama.cpp/llama-cli \
    -hf unsloth/Kimi-K2-Thinking-GGUF:UD-TQ1_0 \
    --n-gpu-layers 99 \
    --temp 1.0 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
   ```

4. **Or Run as OpenAI-Compatible Server**:
   ```bash
   ./llama.cpp/llama-server \
    --model ./models/kimi-k25-quantized/Kimi-K2-Thinking-UD-TQ1_0-00001-of-00006.gguf \
    --alias "kimi-k25-local" \
    --n-gpu-layers 999 \
    -ot ".ffn_.*_exps.=CPU" \
    --min_p 0.01 \
    --ctx-size 16384 \
    --port 8000 \
    --jinja
   ```

### Method 2: Using the Local Server Wrapper

For easier integration with existing tools:

1. **Start the Local Server**:
   ```bash
   python3 local_kimi_server.py
   ```
   
   This starts a server on port 3007 that acts as a wrapper around the llama.cpp server.

2. **Use via API**:
   ```python
   import requests
   
   response = requests.post("http://localhost:3007/chat/completions", json={
       "messages": [
           {"role": "user", "content": "Hello, what are you?"}
       ],
       "model": "kimi-k25-local",
       "max_tokens": 500,
       "temperature": 0.7
   })
   ```

## Kimi-Specific Configuration

### Thinking Mode vs Instant Mode
- **Thinking Mode**: Enables reasoning chains (temperature=1.0)
- **Instant Mode**: Direct responses (temperature=0.6)

### Recommended Settings
- **Temperature**: 1.0 for thinking mode, 0.6 for instant mode
- **Context Size**: Up to 256K tokens (use 16K or 32K for better performance)
- **Min_P**: 0.01 (to suppress unlikely tokens)

## Performance Optimization

### For Limited VRAM
Use MoE layer offloading:
```bash
-ot ".ffn_.*_exps.=CPU"  # Offloads all MoE layers to CPU
```

### For Better Speed
If you have more VRAM:
```bash
-ot ".ffn_(up)_exps.=CPU"  # Offloads only up projection layers
```

### For Maximum Speed (if you have sufficient VRAM)
Remove the offloading flag entirely to keep all layers on GPU.

## Integration with OpenClaw

Once deployed locally, you can integrate Kimi K2.5 with OpenClaw by:

1. Adding the local server endpoint to your OpenClaw configuration
2. Creating skills that interface with the local Kimi K2.5 server
3. Using it alongside your existing MCP servers

Example configuration addition:
```json
{
  "kimi_k25_local": {
    "url": "http://localhost:3007",
    "enabled": true,
    "name": "Local Kimi K2.5 Server",
    "description": "Kimi K2.5 1T model running locally",
    "health_check_interval": 30
  }
}
```

## Troubleshooting

### Model Loading Issues
- Ensure you have sufficient disk space
- Check that the model path is correct
- Verify that llama.cpp is properly compiled

### Performance Issues
- Reduce context size if experiencing slowdowns
- Use MoE layer offloading to optimize VRAM usage
- Consider using a larger quantization if quality is an issue

### Server Connection Issues
- Verify the llama.cpp server is running
- Check port availability
- Ensure firewall isn't blocking connections

## Benefits of Local Deployment

1. **Privacy**: Your data never leaves your machine
2. **Cost**: No API usage fees
3. **Availability**: Always accessible regardless of internet connectivity
4. **Customization**: Full control over model parameters and behavior
5. **Latency**: Potentially lower latency for repeated requests

## Legal and Ethical Considerations

- The Kimi K2.5 model is released under the Modified MIT License
- Use responsibly and in accordance with local laws
- Attribute appropriately when using in commercial applications
- Respect rate limits and computational constraints