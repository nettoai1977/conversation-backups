import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import psutil
import os
import subprocess
import socket
from datetime import datetime
import json

class SystemStatsRequest(BaseModel):
    cpu: bool = Field(default=True, description="Include CPU stats")
    memory: bool = Field(default=True, description="Include memory stats")
    disk: bool = Field(default=True, description="Include disk stats")
    network: bool = Field(default=False, description="Include network stats")

class FileOperationRequest(BaseModel):
    path: str = Field(description="File path")
    encoding: str = Field(default="utf-8", description="File encoding")
    max_size_mb: int = Field(default=10, description="Max file size in MB")

class CommandRequest(BaseModel):
    command: str = Field(description="Command to execute")
    timeout_seconds: int = Field(default=30, description="Timeout in seconds")
    capture_output: bool = Field(default=True, description="Capture command output")

class NetworkCheckRequest(BaseModel):
    host: str = Field(description="Host to check")
    port: int = Field(default=80, description="Port to check")
    timeout_seconds: int = Field(default=5, description="Timeout in seconds")

class SystemDevOpsMCP:
    def __init__(self):
        self.app = FastMCP("system-devops")
        
    async def get_system_stats(self, cpu: bool = True, memory: bool = True, 
                              disk: bool = True, network: bool = False) -> dict:
        """Get system statistics."""
        try:
            stats = {"timestamp": datetime.now().isoformat()}
            
            if cpu:
                stats["cpu"] = {
                    "percent": psutil.cpu_percent(interval=1),
                    "count": psutil.cpu_count(),
                    "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
                }
            
            if memory:
                mem = psutil.virtual_memory()
                stats["memory"] = {
                    "total_gb": round(mem.total / (1024**3), 2),
                    "available_gb": round(mem.available / (1024**3), 2),
                    "percent_used": mem.percent,
                    "used_gb": round(mem.used / (1024**3), 2)
                }
            
            if disk:
                disk_usage = psutil.disk_usage('/')
                stats["disk"] = {
                    "total_gb": round(disk_usage.total / (1024**3), 2),
                    "used_gb": round(disk_usage.used / (1024**3), 2),
                    "free_gb": round(disk_usage.free / (1024**3), 2),
                    "percent_used": round((disk_usage.used / disk_usage.total) * 100, 2)
                }
            
            if network:
                net_io = psutil.net_io_counters()
                stats["network"] = {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv
                }
            
            return {
                "success": True,
                "stats": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def read_file(self, path: str, encoding: str = "utf-8", max_size_mb: int = 10) -> dict:
        """Read a file with size limitations."""
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"File does not exist: {path}"
                }
            
            file_size = os.path.getsize(path)
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if file_size > max_size_bytes:
                return {
                    "success": False,
                    "error": f"File too large: {file_size} bytes (max: {max_size_bytes})"
                }
            
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()
            
            return {
                "success": True,
                "path": path,
                "size_bytes": file_size,
                "content": content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def run_command(self, command: str, timeout_seconds: int = 30, 
                         capture_output: bool = True) -> dict:
        """Run a command safely with timeout."""
        try:
            # Security check: basic validation to prevent command injection
            dangerous_patterns = [';', '&&', '||', '|', '`', '$(']
            for pattern in dangerous_patterns:
                if pattern in command:
                    return {
                        "success": False,
                        "error": f"Dangerous command pattern detected: {pattern}"
                    }
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=timeout_seconds
            )
            
            return {
                "success": True,
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout if capture_output else None,
                "stderr": result.stderr if capture_output else None,
                "execution_time_seconds": timeout_seconds
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout_seconds} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def check_connectivity(self, host: str, port: int = 80, timeout_seconds: int = 5) -> dict:
        """Check connectivity to a host and port."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout_seconds)
                result = sock.connect_ex((host, port))
                
                return {
                    "success": True,
                    "host": host,
                    "port": port,
                    "is_connected": result == 0,
                    "status_code": result
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "host": host,
                "port": port
            }

def create_system_devops_server():
    server = SystemDevOpsMCP()
    
    @server.app.tool("get_system_stats", "Get system statistics (CPU, memory, disk, network)")
    async def handle_system_stats(req: SystemStatsRequest) -> dict:
        return await server.get_system_stats(
            req.cpu, req.memory, req.disk, req.network
        )
    
    @server.app.tool("read_file", "Read a file with size limitations")
    async def handle_read_file(req: FileOperationRequest) -> dict:
        return await server.read_file(
            req.path, req.encoding, req.max_size_mb
        )
    
    @server.app.tool("run_command", "Run a command safely with timeout")
    async def handle_run_command(req: CommandRequest) -> dict:
        return await server.run_command(
            req.command, req.timeout_seconds, req.capture_output
        )
    
    @server.app.tool("check_connectivity", "Check connectivity to a host and port")
    async def handle_check_connectivity(req: NetworkCheckRequest) -> dict:
        return await server.check_connectivity(
            req.host, req.port, req.timeout_seconds
        )
    
    return server

if __name__ == "__main__":
    import uvicorn
    server = create_system_devops_server()
    
    async def run_server():
        config_obj = uvicorn.Config(app=server.app, host="127.0.0.1", port=3005)
        server_instance = uvicorn.Server(config_obj)
        await server_instance.serve()
    
    asyncio.run(run_server())