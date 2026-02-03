#!/usr/bin/env python3
"""
Local Kimi K2.5 Server
Provides a local API interface to run Kimi K2.5 model using llama.cpp server
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
import subprocess
import threading
import time
import requests
from contextlib import asynccontextmanager


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions"""
    messages: List[Dict[str, Any]]
    model: str = "kimi-k25-local"
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False
    thinking: bool = True  # Whether to use thinking mode or instant mode


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    model: str = "kimi-k25-local"
    timestamp: datetime = Field(default_factory=datetime.now)
    local_deployed: bool = True


# Global variables
LLAMA_SERVER_URL = "http://127.0.0.1:8000/v1"  # Default llama.cpp server
SERVER_PROCESS = None
SERVER_READY = False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown of the llama.cpp server"""
    global SERVER_PROCESS, SERVER_READY
    
    # Startup
    print("Starting local llama.cpp server for Kimi K2.5...")
    
    # Start the llama.cpp server in a subprocess
    # NOTE: This assumes you've already set up llama.cpp and have the model
    try:
        # Command to start llama.cpp server with Kimi K2.5 model
        cmd = [
            "./llama.cpp/llama-server",
            "--model", "./models/kimi-k25-quantized/",  # Path to your downloaded model
            "--host", "127.0.0.1",
            "--port", "8000",
            "--n-gpu-layers", "999",
            "-ot", ".ffn_.*_exps.=CPU",  # Offload MoE layers to CPU
            "--min-p", "0.01",
            "--ctx-size", "16384",  # 16K context
            "--parallel", "1",
            "--batch-size", "512",
            "--threads", "8"
        ]
        
        SERVER_PROCESS = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        time.sleep(5)
        
        # Check if server is responding
        max_wait = 60  # Wait up to 60 seconds
        waited = 0
        while waited < max_wait and not SERVER_READY:
            try:
                response = requests.get(f"{LLAMA_SERVER_URL}/models", timeout=5)
                if response.status_code == 200:
                    SERVER_READY = True
                    print("✅ Local Kimi K2.5 server is ready!")
                    break
            except requests.exceptions.RequestException:
                time.sleep(2)
                waited += 2
        
        if not SERVER_READY:
            print("⚠️  Could not confirm server is ready, but continuing...")
        
    except FileNotFoundError:
        print("⚠️  llama.cpp server not found. Make sure you've run setup_local_kimi.sh and downloaded the model.")
        print("⚠️  You can still use this API if you manually start llama.cpp server separately.")
    except Exception as e:
        print(f"⚠️  Error starting llama.cpp server: {e}")
        print("⚠️  You can still use this API if you manually start llama.cpp server separately.")
    
    yield  # Run the application
    
    # Shutdown
    if SERVER_PROCESS:
        print("Shutting down local Kimi K2.5 server...")
        SERVER_PROCESS.terminate()
        SERVER_PROCESS.wait()


app = FastAPI(
    title="Local Kimi K2.5 Server",
    description="Local API interface for Kimi K2.5 1T multimodal MoE model",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(local_deployed=True)


@app.get("/models")
async def list_models():
    """List available models (proxies to underlying llama.cpp server)"""
    try:
        response = requests.get(f"{LLAMA_SERVER_URL}/models")
        return response.json()
    except requests.exceptions.RequestException:
        # Return a default response if the underlying server isn't available
        return {
            "object": "list",
            "data": [
                {
                    "id": "kimi-k25-local",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "local"
                }
            ]
        }


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    Create a chat completion using local Kimi K2.5 model
    
    This proxies the request to the underlying llama.cpp server
    """
    try:
        # Prepare the payload for llama.cpp server
        payload = {
            "model": request.model,
            "messages": request.messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": request.stream,
        }
        
        # Add any Kimi-specific parameters
        # For Kimi K2-Thinking, we might want to handle special tokens
        if request.thinking:
            # Thinking mode specific parameters
            payload["temperature"] = 1.0  # Recommended for Kimi K2-Thinking
        else:
            # Instant mode parameters
            payload["temperature"] = 0.6  # Recommended for Kimi K2-Instruct
        
        # Make request to llama.cpp server
        response = requests.post(
            f"{LLAMA_SERVER_URL}/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minute timeout for long completions
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        return response.json()
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Local llama.cpp server is not running")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request to local server timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/embeddings")
async def embeddings(request: Dict[str, Any]):
    """Generate embeddings using the local model (if supported)"""
    try:
        response = requests.post(
            f"{LLAMA_SERVER_URL}/embeddings",
            json=request,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code != 200:
            # Embeddings might not be supported by the model, return a mock response
            return {
                "object": "list",
                "data": [],
                "model": request.get("model", "kimi-k25-local"),
                "usage": {"prompt_tokens": 0, "total_tokens": 0}
            }
        
        return response.json()
    except:
        # If embeddings aren't supported, return a mock response
        return {
            "object": "list",
            "data": [],
            "model": request.get("model", "kimi-k25-local"),
            "usage": {"prompt_tokens": 0, "total_tokens": 0}
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3007)  # Using port 3007 to avoid conflicts