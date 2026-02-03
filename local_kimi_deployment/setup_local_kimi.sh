#!/bin/bash

# Setup script for local Kimi K2.5 deployment
echo "Setting up local Kimi K2.5 deployment..."

# Create necessary directories
mkdir -p models logs downloads

echo "Installing dependencies..."

# Install huggingface_hub for model downloads
pip3 install huggingface_hub hf_transfer

# Check if llama.cpp is available, if not, install it
if [ ! -d "llama.cpp" ]; then
    echo "Installing llama.cpp..."
    git clone https://github.com/ggml-org/llama.cpp
    cd llama.cpp
    
    # Build llama.cpp (assuming CUDA support if available)
    if command -v nvidia-smi &> /dev/null; then
        echo "CUDA detected, building with CUDA support..."
        cmake llama.cpp -B llama.cpp/build \
         -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
    else
        echo "No CUDA detected, building for CPU only..."
        cmake llama.cpp -B llama.cpp/build \
         -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=OFF -DLLAMA_CURL=ON
    fi
    
    cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli
    cp llama.cpp/build/bin/llama-* llama.cpp 2>/dev/null || echo "Some llama tools may not be available"
    cd ..
else
    echo "llama.cpp already installed"
fi

echo "Setup complete!"
echo ""
echo "To download the Kimi K2.5 model, run:"
echo "  python3 download_model.py"
echo ""
echo "To run Kimi K2.5 with llama.cpp, use:"
echo "  ./llama.cpp/llama-cli \\"
echo "   -hf unsloth/Kimi-K2-Thinking-GGUF:UD-TQ1_0 \\"
echo "   --n-gpu-layers 99 \\"
echo "   --temp 1.0 \\"
echo "   --min-p 0.01 \\"
echo "   --ctx-size 16384 \\"
echo "   --seed 3407 \\"
echo "   -ot \".ffn_.*_exps.=CPU\""
echo ""
echo "For an OpenAI-compatible server, use:"
echo "  ./llama.cpp/llama-server \\"
echo "   --model path/to/model.gguf \\"
echo "   --alias \"kimi-k25-local\" \\"
echo "   --n-gpu-layers 999 \\"
echo "   -ot \".ffn_.*_exps.=CPU\" \\"
echo "   --min_p 0.01 \\"
echo "   --ctx-size 16384 \\"
echo "   --port 8000 \\"
echo "   --jinja"