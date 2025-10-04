#!/bin/bash

# HomeGenie MCP Server Startup Script

echo "🏠 HomeGenie MCP Server Setup"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "genie_mcp_server.py" ]; then
    echo "❌ Please run this script from the mcp-server directory"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    if [ -f "../.venv/bin/activate" ]; then
        source ../.venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found. Please run from HomeGenie root:"
        echo "   cd /path/to/HomeGenie && source .venv/bin/activate && cd mcp-server"
        exit 1
    fi
fi

echo ""
echo "🛠️  Available Options:"
echo "1. Test functionality (recommended first)"
echo "2. Start MCP Server (for MCP client integration)"
echo ""

read -p "Choose option (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🧪 Running functionality tests..."
        python test_server.py
        ;;
    2)
        echo ""
        echo "🚀 Starting MCP Server..."
        echo "ℹ️  This server communicates via stdin/stdout for MCP protocol"
        echo "ℹ️  Use Ctrl+C to stop the server"
        echo ""
        python genie_mcp_server.py
        ;;
    *)
        echo "❌ Invalid option. Please choose 1 or 2."
        exit 1
        ;;
esac