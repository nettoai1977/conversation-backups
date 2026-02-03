#!/bin/bash

# Script to start all MCP servers
echo "Starting MCP servers..."

# Create a directory for logs
mkdir -p logs

# Start Crawl4AI server
echo "Starting Crawl4AI server on port 3000..."
nohup python3 mcp-servers/crawl4ai_mcp_server.py > logs/crawl4ai.log 2>&1 &
CRAWL4AI_PID=$!
echo "Crawl4AI server started with PID $CRAWL4AI_PID"

# Start Notion server
echo "Starting Notion server on port 3001..."
nohup python3 mcp-servers/notion_mcp_server.py > logs/notion.log 2>&1 &
NOTION_PID=$!
echo "Notion server started with PID $NOTION_PID"

# Start Email server
echo "Starting Email server on port 3002..."
nohup python3 mcp-servers/email_mcp_server.py > logs/email.log 2>&1 &
EMAIL_PID=$!
echo "Email server started with PID $EMAIL_PID"

# Start Business Operations server
echo "Starting Business Operations server on port 3003..."
nohup python3 mcp-servers/business_ops_mcp_server.py > logs/business_ops.log 2>&1 &
BUSINESS_PID=$!
echo "Business Operations server started with PID $BUSINESS_PID"

# Start Research & Analysis server
echo "Starting Research & Analysis server on port 3004..."
nohup python3 mcp-servers/research_analysis_mcp_server.py > logs/research_analysis.log 2>&1 &
RESEARCH_PID=$!
echo "Research & Analysis server started with PID $RESEARCH_PID"

# Start System & DevOps server
echo "Starting System & DevOps server on port 3005..."
nohup python3 mcp-servers/system_devops_mcp_server.py > logs/system_devops.log 2>&1 &
DEVOPS_PID=$!
echo "System & DevOps server started with PID $DEVOPS_PID"

# Start Kimi K2.5 server
echo "Starting Kimi K2.5 server on port 3006..."
nohup python3 mcp-servers/kimi_k25_mcp_server.py > logs/kimi_k25.log 2>&1 &
KIMI_PID=$!
echo "Kimi K2.5 server started with PID $KIMI_PID"

# Wait a moment for servers to start
sleep 3

# Check if all servers are running
echo "Checking server status..."
if kill -0 $CRAWL4AI_PID 2>/dev/null; then
    echo "✓ Crawl4AI server is running (PID: $CRAWL4AI_PID)"
else
    echo "✗ Crawl4AI server failed to start"
fi

if kill -0 $NOTION_PID 2>/dev/null; then
    echo "✓ Notion server is running (PID: $NOTION_PID)"
else
    echo "✗ Notion server failed to start"
fi

if kill -0 $EMAIL_PID 2>/dev/null; then
    echo "✓ Email server is running (PID: $EMAIL_PID)"
else
    echo "✗ Email server failed to start"
fi

if kill -0 $BUSINESS_PID 2>/dev/null; then
    echo "✓ Business Operations server is running (PID: $BUSINESS_PID)"
else
    echo "✗ Business Operations server failed to start"
fi

if kill -0 $RESEARCH_PID 2>/dev/null; then
    echo "✓ Research & Analysis server is running (PID: $RESEARCH_PID)"
else
    echo "✗ Research & Analysis server failed to start"
fi

if kill -0 $DEVOPS_PID 2>/dev/null; then
    echo "✓ System & DevOps server is running (PID: $DEVOPS_PID)"
else
    echo "✗ System & DevOps server failed to start"
fi

if kill -0 $KIMI_PID 2>/dev/null; then
    echo "✓ Kimi K2.5 server is running (PID: $KIMI_PID)"
else
    echo "✗ Kimi K2.5 server failed to start"
fi

echo ""
echo "All MCP servers have been started."
echo "Logs are available in the logs/ directory."
echo ""
echo "Server endpoints:"
echo "- Crawl4AI: http://localhost:3000"
echo "- Notion: http://localhost:3001"
echo "- Email: http://localhost:3002"
echo "- Business Ops: http://localhost:3003"
echo "- Research & Analysis: http://localhost:3004"
echo "- System & DevOps: http://localhost:3005"
echo "- Kimi K2.5: http://localhost:3006"
echo ""
echo "To stop all servers, run: pkill -f '_mcp_server.py'"