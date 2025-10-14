#!/bin/bash

# Microsoft Graph MCP Server - Installation Script
# This script automates the setup process

set -e  # Exit on error

echo "🚀 Microsoft Graph MCP Server - Installation"
echo "============================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. You have $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Check if uv is installed
echo "📋 Checking for uv package manager..."
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv is not installed. Installing uv..."
    
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
    else
        echo "❌ Automatic uv installation is not supported on this platform."
        echo "   Please install uv manually from: https://github.com/astral-sh/uv"
        exit 1
    fi
else
    echo "✅ uv is already installed"
fi
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
uv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
uv pip install -e .
echo "✅ Dependencies installed"
echo ""

# Setup .env file
echo "⚙️  Setting up environment configuration..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created from template"
        echo ""
        echo "⚠️  IMPORTANT: Edit the .env file with your Azure credentials:"
        echo "   - MICROSOFT_TENANT_ID"
        echo "   - MICROSOFT_CLIENT_ID"
        echo "   - MICROSOFT_CLIENT_SECRET"
        echo ""
        echo "   You can edit it now or later using:"
        echo "   nano .env  (or your preferred editor)"
        echo ""
    else
        echo "⚠️  .env.example not found. Please create .env manually."
    fi
else
    echo "ℹ️  .env file already exists"
fi
echo ""

# Print next steps
echo "✅ Installation complete!"
echo ""
echo "📝 Next Steps:"
echo "============="
echo ""
echo "1. Configure your Azure credentials in .env:"
echo "   nano .env"
echo ""
echo "2. Set up Claude Desktop configuration:"
echo "   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   - Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo ""
echo "   Add this configuration (update the path):"
echo '   {'
echo '     "mcpServers": {'
echo '       "microsoft-graph": {'
echo '         "command": "uv",'
echo '         "args": ['
echo '           "--directory",'
echo "           \"$(pwd)\","
echo '           "run",'
echo '           "mcp_graph_server.py"'
echo '         ],'
echo '         "env": {'
echo '           "MICROSOFT_TENANT_ID": "your-tenant-id",'
echo '           "MICROSOFT_CLIENT_ID": "your-client-id",'
echo '           "MICROSOFT_CLIENT_SECRET": "your-client-secret"'
echo '         }'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "4. Test by asking Claude: 'List all available Microsoft 365 licenses'"
echo ""
echo "📚 Documentation:"
echo "   - QUICKSTART.md - Fast 10-minute setup guide"
echo "   - README.md - Complete documentation"
echo "   - AZURE_SETUP.md - Azure configuration help"
echo "   - EXAMPLES.md - Usage examples"
echo ""
echo "🎉 Happy automating!"
