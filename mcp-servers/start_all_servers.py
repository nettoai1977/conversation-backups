#!/usr/bin/env python3
"""
Startup script to launch all MCP servers for OpenClaw integration enhancement.
This script starts all the MCP servers in separate processes.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def start_server(script_name, port, description):
    """Start an MCP server in a subprocess."""
    print(f"Starting {description} on port {port}...")
    
    # Get the absolute path to the script
    script_path = Path(__file__).parent / script_name
    
    # Start the server as a subprocess
    process = subprocess.Popen([
        sys.executable, str(script_path)
    ])
    
    return process

def main():
    print("🚀 Starting OpenClaw MCP Server Suite...")
    print("=" * 50)
    
    # Define all servers to start
    servers = [
        ("crawl4ai_mcp_server.py", 3000, "Crawl4AI Web Scraping Server"),
        ("notion_mcp_server.py", 3001, "Notion Integration Server"),
        ("email_mcp_server.py", 3002, "Email Management Server"),
        ("business_ops_mcp_server.py", 3003, "Business Operations Server"),
        ("research_analysis_mcp_server.py", 3004, "Research & Analysis Server")
    ]
    
    processes = []
    
    try:
        # Start all servers
        for script, port, description in servers:
            process = start_server(script, port, description)
            processes.append((process, description, port))
            time.sleep(2)  # Brief pause between starting servers
        
        print("\n✅ All MCP servers started successfully!")
        print("\n📋 Server Status:")
        for i, (_, desc, port) in enumerate(processes, 1):
            print(f"  {i}. {desc} - http://localhost:{port}")
        
        print(f"\n📖 Configuration available in: {Path(__file__).parent}/config.json")
        print("\n💡 To use these servers with OpenClaw, add the configuration to your OpenClaw config file.")
        print("\n🔄 Press Ctrl+C to stop all servers")
        
        # Wait for all processes to finish (they run indefinitely)
        for process, desc, port in processes:
            try:
                process.wait()
            except KeyboardInterrupt:
                print(f"\n🛑 Shutting down {desc}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal. Shutting down all servers...")
        
        # Terminate all processes
        for process, desc, port in processes:
            print(f"Stopping {desc}...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print("All servers stopped.")
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        
        # Clean up any started processes
        for process, desc, port in processes:
            try:
                process.terminate()
                process.wait(timeout=2)
            except:
                process.kill()

if __name__ == "__main__":
    main()