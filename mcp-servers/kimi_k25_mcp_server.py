#!/usr/bin/env python3
"""
Kimi K2.5 MCP Server
Provides access to the Kimi K2.5 1T multimodal MoE model through NVIDIA's NIM platform
Supports both thinking mode and instant mode with multimodal capabilities
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import openai
import base64
import requests
from datetime import datetime


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions"""
    messages: List[Dict[str, Any]]
    model: str = "moonshotai/kimi-k2.5"
    max_tokens: int = 4096
    temperature: float = 0.6
    top_p: float = 0.95
    stream: bool = False
    thinking: bool = True  # Whether to use thinking mode or instant mode
    images: Optional[List[str]] = None  # Base64 encoded images


class Tool(BaseModel):
    """Tool definition for function calling"""
    type: str = "function"
    function: Dict[str, Any]


class ToolCallRequest(BaseModel):
    """Request model for tool-enabled completions"""
    messages: List[Dict[str, Any]]
    tools: Optional[List[Tool]] = None
    model: str = "moonshotai/kimi-k2.5"
    max_tokens: int = 4096
    temperature: float = 0.6
    thinking: bool = True


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    model: str = "moonshotai/kimi-k2.5"
    timestamp: datetime = Field(default_factory=datetime.now)


# Initialize FastAPI app
app = FastAPI(
    title="Kimi K2.5 MCP Server",
    description="MCP Server for Kimi K2.5 1T multimodal MoE model",
    version="1.0.0"
)


# Global variables
API_KEY = "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"  # Your API key
BASE_URL = "https://integrate.api.nvidia.com/v1"


@app.on_event("startup")
async def startup_event():
    """Initialize the OpenAI client with NVIDIA API configuration"""
    global client
    client = openai.AsyncOpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    print("Kimi K2.5 MCP Server started successfully")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse()


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    Create a chat completion using Kimi K2.5
    
    Supports both thinking mode (with reasoning traces) and instant mode (direct responses)
    Also supports multimodal inputs with images
    """
    try:
        # Prepare messages with potential image content
        processed_messages = []
        
        for msg in request.messages:
            if isinstance(msg.get('content'), str):
                # Simple text message
                processed_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            elif isinstance(msg.get('content'), list):
                # Multimodal message with text and images
                content_parts = []
                for item in msg['content']:
                    if item['type'] == 'text':
                        content_parts.append({
                            'type': 'text',
                            'text': item['text']
                        })
                    elif item['type'] == 'image_url':
                        content_parts.append({
                            'type': 'image_url',
                            'image_url': item['image_url']
                        })
                
                processed_messages.append({
                    "role": msg["role"],
                    "content": content_parts
                })
            else:
                processed_messages.append(msg)
        
        # Prepare API call parameters
        api_params = {
            "model": request.model,
            "messages": processed_messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "top_p": request.top_p,
            "stream": request.stream,
        }
        
        # Set thinking mode based on request
        if request.thinking:
            # Use thinking mode (includes reasoning traces)
            api_params["extra_body"] = {"thinking": {"type": "default"}}
        else:
            # Use instant mode (direct responses without reasoning traces)
            api_params["extra_body"] = {"thinking": {"type": "disabled"}}
        
        # Make the API call
        response = await client.chat.completions.create(**api_params)
        
        # Format the response
        result = {
            "id": response.id,
            "object": response.object,
            "created": response.created,
            "model": response.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content,
                    },
                    "finish_reason": choice.finish_reason,
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0),
                "completion_tokens": getattr(response.usage, 'completion_tokens', 0),
                "total_tokens": getattr(response.usage, 'total_tokens', 0),
            }
        }
        
        # Add reasoning content if available (in thinking mode)
        if hasattr(response.choices[0].message, 'reasoning_content') and response.choices[0].message.reasoning_content:
            result["choices"][0]["message"]["reasoning_content"] = response.choices[0].message.reasoning_content
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Kimi K2.5 API: {str(e)}")


@app.post("/chat/completions/tools")
async def chat_completions_with_tools(request: ToolCallRequest):
    """
    Create a chat completion with tool calling capabilities
    """
    try:
        # Prepare API call parameters
        api_params = {
            "model": request.model,
            "messages": request.messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
        
        # Add tools if provided
        if request.tools:
            api_params["tools"] = [tool.dict() for tool in request.tools]
            api_params["tool_choice"] = "auto"
        
        # Set thinking mode
        if request.thinking:
            api_params["extra_body"] = {"thinking": {"type": "default"}}
        else:
            api_params["extra_body"] = {"thinking": {"type": "disabled"}}
        
        # Make the API call
        response = await client.chat.completions.create(**api_params)
        
        # Format the response
        result = {
            "id": response.id,
            "object": response.object,
            "created": response.created,
            "model": response.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content,
                    },
                    "finish_reason": choice.finish_reason,
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0),
                "completion_tokens": getattr(response.usage, 'completion_tokens', 0),
                "total_tokens": getattr(response.usage, 'total_tokens', 0),
            }
        }
        
        # Add reasoning content if available
        if hasattr(response.choices[0].message, 'reasoning_content') and response.choices[0].message.reasoning_content:
            result["choices"][0]["message"]["reasoning_content"] = response.choices[0].message.reasoning_content
        
        # Add tool calls if present
        if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
            tool_calls = []
            for tool_call in response.choices[0].message.tool_calls:
                tool_calls.append({
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    }
                })
            result["choices"][0]["message"]["tool_calls"] = tool_calls
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Kimi K2.5 API with tools: {str(e)}")


@app.get("/models")
async def list_models():
    """List available models (currently just Kimi K2.5)"""
    return {
        "object": "list",
        "data": [
            {
                "id": "moonshotai/kimi-k2.5",
                "object": "model",
                "created": 1706745600,  # Creation timestamp for Kimi K2.5 on NVIDIA platform
                "owned_by": "moonshotai"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3006)