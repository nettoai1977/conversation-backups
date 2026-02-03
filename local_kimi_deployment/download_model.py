#!/usr/bin/env python3
"""
Download Kimi K2.5 GGUF model from Hugging Face
"""

import os
from huggingface_hub import snapshot_download

def download_kimi_model():
    """Download Kimi K2.5 model in GGUF format"""
    
    # Enable faster downloads
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
    
    print("Downloading Kimi K2.5 model...")
    print("Model: unsloth/Kimi-K2-Thinking-GGUF")
    print("Quantization: UD-TQ1_0 (Dynamic 1-bit, ~230GB)")
    print("This may take a while depending on your internet connection...")
    
    try:
        # Download the 1-bit quantized model (~230GB)
        snapshot_download(
            repo_id="unsloth/Kimi-K2-Thinking-GGUF",
            local_dir="./models/kimi-k25-quantized",
            allow_patterns=["*UD-TQ1_0*"],  # Use 1-bit quant (230GB)
            # Alternative: Use "*UD-Q2_K_XL*" for 2-bit quant (360GB) with better quality
        )
        
        print("\n✅ Model download completed successfully!")
        print("Model saved to: ./models/kimi-k25-quantized/")
        print("\n💡 To run the model with llama.cpp:")
        print("   ./llama.cpp/llama-cli \\")
        print("    --model ./models/kimi-k25-quantized/Kimi-K2-Thinking-UD-TQ1_0-00001-of-00006.gguf \\")
        print("    --n-gpu-layers 99 \\")
        print("    --temp 1.0 \\")
        print("    --min-p 0.01 \\")
        print("    --ctx-size 16384 \\")
        print("    --seed 3407 \\")
        print("    -ot \".ffn_.*_exps.=CPU\"")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("\n💡 Alternative quantizations available:")
        print("   - UD-Q2_K_XL (Dynamic 2-bit, ~360GB) - Better quality")
        print("   - Other quantizations at: https://huggingface.co/unsloth/Kimi-K2-Thinking-GGUF")
        
        # Offer to download a smaller quantization
        try:
            choice = input("\nWould you like to try a different quantization? (y/n): ")
            if choice.lower() == 'y':
                print("\nAvailable quantizations:")
                print("1. UD-Q2_K_XL (Dynamic 2-bit, ~360GB) - Better quality")
                print("2. Other quantizations at the Hugging Face link above")
                
                quant_choice = input("Enter choice (1 or 2): ")
                if quant_choice == "1":
                    snapshot_download(
                        repo_id="unsloth/Kimi-K2-Thinking-GGUF",
                        local_dir="./models/kimi-k25-quantized-q2",
                        allow_patterns=["*UD-Q2_K_XL*"],  # Use 2-bit quant (360GB)
                    )
                    print("\n✅ Model download completed successfully!")
                    print("Model saved to: ./models/kimi-k25-quantized-q2/")
        
        except KeyboardInterrupt:
            print("\nDownload cancelled by user.")

if __name__ == "__main__":
    download_kimi_model()