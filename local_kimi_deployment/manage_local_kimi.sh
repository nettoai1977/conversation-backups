#!/bin/bash

# Management script for local Kimi K2.5 deployment

show_help() {
    echo "Local Kimi K2.5 Management Script"
    echo "==================================="
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup          - Install dependencies and prepare environment"
    echo "  download       - Download Kimi K2.5 model (large download ~230GB)"
    echo "  start          - Start local Kimi K2.5 server"
    echo "  stop           - Stop local Kimi K2.5 server"
    echo "  status         - Check status of local Kimi K2.5 server"
    echo "  test           - Test local Kimi K2.5 server"
    echo "  logs           - View server logs"
    echo "  cleanup        - Clean up temporary files"
    echo "  help           - Show this help message"
    echo ""
}

case "$1" in
    setup)
        echo "🔧 Setting up local Kimi K2.5 environment..."
        bash setup_local_kimi.sh
        ;;
    download)
        echo "📥 Downloading Kimi K2.5 model..."
        echo "⚠️  WARNING: This will download ~230GB of data"
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            python3 download_model.py
        else
            echo "Download cancelled."
        fi
        ;;
    start)
        echo "🚀 Starting local Kimi K2.5 server..."
        echo "This will start the server on port 3007"
        echo "Check http://localhost:3007/health to verify it's running"
        python3 local_kimi_server.py
        ;;
    stop)
        echo "🛑 Stopping local Kimi K2.5 server..."
        pkill -f local_kimi_server.py
        pkill -f llama-server
        echo "Local Kimi K2.5 server stopped."
        ;;
    status)
        echo "📊 Checking local Kimi K2.5 server status..."
        if pgrep -f local_kimi_server.py > /dev/null; then
            echo "✓ Local Kimi K2.5 server is running"
            echo "  Check: http://localhost:3007/health"
        else
            echo "✗ Local Kimi K2.5 server is not running"
        fi
        
        if pgrep -f llama-server > /dev/null; then
            echo "✓ Underlying llama.cpp server is running"
            echo "  Check: http://localhost:8000/models"
        else
            echo "✗ Underlying llama.cpp server is not running"
        fi
        ;;
    test)
        echo "🧪 Testing local Kimi K2.5 server..."
        python3 test_local_kimi.py
        ;;
    logs)
        echo "📄 Showing recent logs..."
        if [ -f "../logs/kimi_k25.log" ]; then
            echo "Recent logs from main Kimi server:"
            tail -20 ../logs/kimi_k25.log
        fi
        if [ -d "logs" ]; then
            echo "Recent logs from local deployment:"
            ls -la logs/
        fi
        ;;
    cleanup)
        echo "🧹 Cleaning up temporary files..."
        rm -rf __pycache__/
        rm -rf */__pycache__/
        rm -rf *.log
        rm -rf logs/
        mkdir -p logs
        echo "Cleanup complete."
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        if [ -z "$1" ]; then
            show_help
        else
            echo "Unknown command: $1"
            echo ""
            show_help
        fi
        ;;
esac