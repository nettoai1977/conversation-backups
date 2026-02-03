# Local Kimi K2.5 Deployment

This directory contains files to deploy Kimi K2.5 locally using the GGUF format from Unsloth. This allows you to run the 1T parameter multimodal MoE model on your own hardware.

## Hardware Requirements

- **Minimum**: 247GB disk space for the 1-bit quantized model
- **Recommended**: 247GB combined RAM+VRAM for optimal performance (5+ tokens/s)
- **Alternative**: Works with less RAM+VRAM via disk offloading (slower)

## Deployment Options

1. **llama.cpp** (CPU/GPU support)
2. **vLLM** (GPU optimized)
3. **OpenAI-compatible server** (for integration with existing tools)

## Setup Instructions

1. Clone this repository
2. Install dependencies (see setup scripts)
3. Download the model (instructions provided)
4. Run using your preferred method

The quantized model (UD-TQ1_0) reduces the 1.09TB model to just 230GB, achieving ~80% size reduction while maintaining quality.