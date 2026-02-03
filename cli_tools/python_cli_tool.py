"""
Python CLI Tool for OpenClaw Integration
Implements the CLI tools enhancement strategies with proper integration to skills system
"""

import argparse
import subprocess
import sys
import os
import json
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import asyncio
import aiohttp
from pathlib import Path

class OpenClawCLITool:
    """Enhanced CLI tool for OpenClaw integration with security and validation"""
    
    def __init__(self):
        self.allowlist_file = Path("./config/cli_allowlist.json")
        self.log_file = Path("/tmp/openclaw_python_cli.log")
        self.security_mode = "strict"  # strict, moderate, relaxed
        self.max_execution_time = 300  # 5 minutes
        
        # Initialize allowlist if it doesn't exist
        self._init_allowlist()
    
    def _init_allowlist(self):
        """Initialize the command allowlist"""
        if not self.allowlist_file.exists():
            self.allowlist_file.parent.mkdir(parents=True, exist_ok=True)
            default_allowlist = {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "approved_commands": [
                    "ls", "pwd", "whoami", "date", "echo", "cat", "grep", "find",
                    "ps", "top", "df", "du", "curl", "wget", "ping", "dig", "nslookup",
                    "git", "docker", "npm", "yarn", "python", "python3", "node", "bash", "sh", "zsh"
                ],
                "approved_patterns": [
                    r"^ls(\s+.*)?$",
                    r"^pwd(\s+.*)?$",
                    r"^whoami(\s+.*)?$",
                    r"^date(\s+.*)?$",
                    r"^echo(\s+.*)?$",
                    r"^cat(\s+.*)?$",
                    r"^grep(\s+.*)?$",
                    r"^find(\s+.*)?$",
                    r"^ps(\s+.*)?$",
                    r"^df(\s+.*)?$",
                    r"^du(\s+.*)?$",
                    r"^curl(\s+.*)?$",
                    r"^wget(\s+.*)?$",
                    r"^ping(\s+\w+)?$",
                    r"^git(\s+.*)?$",
                    r"^docker(\s+.*)?$",
                    r"^npm(\s+.*)?$",
                    r"^python(\d+)?(\s+.*)?$"
                ]
            }
            with open(self.allowlist_file, 'w') as f:
                json.dump(default_allowlist, f, indent=2)
    
    def _load_allowlist(self) -> Dict[str, Any]:
        """Load the command allowlist"""
        with open(self.allowlist_file, 'r') as f:
            return json.load(f)
    
    def _log_activity(self, action: str, details: Dict[str, Any]):
        """Log CLI activity for audit purposes"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _validate_command(self, command: str) -> bool:
        """Validate command against security rules and allowlist"""
        # Check for dangerous patterns
        dangerous_patterns = [
            '&&', '||', ';', '`', '$(', '>/dev/', '</dev/', '>/proc/',
            '&>', '>&', '<&', 'eval', 'exec', 'source', 'import os'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command:
                return False
        
        # Check against allowlist
        allowlist = self._load_allowlist()
        command_parts = command.strip().split()
        if not command_parts:
            return False
        
        cmd_name = command_parts[0]
        
        # Check exact command name
        if cmd_name in allowlist.get("approved_commands", []):
            return True
        
        # Check patterns
        import re
        for pattern in allowlist.get("approved_patterns", []):
            if re.match(pattern, command.strip()):
                return True
        
        return False
    
    async def run_command_securely(self, command: str, description: str = "", timeout: int = 30) -> Dict[str, Any]:
        """Run a command with security validation"""
        start_time = datetime.now()
        
        # Log the attempt
        self._log_activity("command_attempt", {
            "command": command,
            "description": description,
            "timestamp": start_time.isoformat()
        })
        
        # Validate command security
        if not self._validate_command(command):
            error_msg = f"Command '{command}' failed security validation"
            self._log_activity("security_violation", {
                "command": command,
                "error": error_msg
            })
            return {
                "success": False,
                "error": error_msg,
                "command": command
            }
        
        try:
            # Execute command with timeout
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                
                result = {
                    "success": process.returncode == 0,
                    "command": command,
                    "description": description,
                    "return_code": process.returncode,
                    "stdout": stdout.decode() if stdout else "",
                    "stderr": stderr.decode() if stderr else "",
                    "execution_time": execution_time,
                    "timestamp": end_time.isoformat()
                }
                
                # Log successful execution
                self._log_activity("command_executed", {
                    "command": command,
                    "success": result["success"],
                    "execution_time": execution_time
                })
                
                return result
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                
                error_msg = f"Command '{command}' timed out after {timeout} seconds"
                self._log_activity("timeout", {
                    "command": command,
                    "timeout": timeout
                })
                return {
                    "success": False,
                    "error": error_msg,
                    "command": command,
                    "timeout": timeout
                }
                
        except Exception as e:
            error_msg = f"Failed to execute command '{command}': {str(e)}"
            self._log_activity("execution_error", {
                "command": command,
                "error": str(e)
            })
            return {
                "success": False,
                "error": error_msg,
                "command": command
            }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        import psutil
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            stats = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent,
                    "used_gb": round(memory.used / (1024**3), 2)
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent_used": round((disk.used / disk.total) * 100, 2)
                },
                "uptime": psutil.boot_time()
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
    
    def search_files(self, directory: str = ".", pattern: str = "*.txt", recursive: bool = True) -> Dict[str, Any]:
        """Search for files matching a pattern"""
        try:
            import glob
            
            if recursive:
                search_pattern = f"{directory}/**/{pattern}"
                files = glob.glob(search_pattern, recursive=True)
            else:
                search_pattern = f"{directory}/{pattern}"
                files = glob.glob(search_pattern)
            
            return {
                "success": True,
                "directory": directory,
                "pattern": pattern,
                "recursive": recursive,
                "files_found": files,
                "count": len(files)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_connectivity(self, host: str = "google.com", port: int = 80, timeout: int = 5) -> Dict[str, Any]:
        """Check network connectivity to a host and port"""
        try:
            import socket
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                
                return {
                    "success": True,
                    "host": host,
                    "port": port,
                    "is_connected": result == 0,
                    "status_code": result,
                    "timeout": timeout
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "host": host,
                "port": port
            }

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Enhanced CLI Tool")
    parser.add_argument("command", help="Command to execute or action to perform")
    parser.add_argument("--args", nargs="*", help="Arguments for the command")
    parser.add_argument("--desc", "--description", default="", help="Description of the command")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--allowlist", help="Custom allowlist file")
    
    args = parser.parse_args()
    
    cli_tool = OpenClawCLITool()
    
    # Handle special commands
    if args.command == "monitor":
        result = cli_tool.get_system_stats()
        print(json.dumps(result, indent=2))
        
    elif args.command == "search":
        directory = args.args[0] if args.args and len(args.args) > 0 else "."
        pattern = args.args[1] if args.args and len(args.args) > 1 else "*.txt"
        recursive = args.args[2].lower() == "true" if args.args and len(args.args) > 2 else True
        
        result = cli_tool.search_files(directory, pattern, recursive)
        print(json.dumps(result, indent=2))
        
    elif args.command == "connectivity":
        host = args.args[0] if args.args and len(args.args) > 0 else "google.com"
        port = int(args.args[1]) if args.args and len(args.args) > 1 else 80
        timeout = int(args.args[2]) if args.args and len(args.args) > 2 else 5
        
        result = cli_tool.check_connectivity(host, port, timeout)
        print(json.dumps(result, indent=2))
        
    elif args.command == "run":
        if not args.args:
            print("Error: Command to run is required")
            sys.exit(1)
        
        command_to_run = " ".join(args.args)
        result = asyncio.run(cli_tool.run_command_securely(command_to_run, args.desc, args.timeout))
        print(json.dumps(result, indent=2))
        
    else:
        # Treat as a direct command
        command_to_run = args.command
        if args.args:
            command_to_run += " " + " ".join(args.args)
        
        result = asyncio.run(cli_tool.run_command_securely(command_to_run, args.desc, args.timeout))
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()