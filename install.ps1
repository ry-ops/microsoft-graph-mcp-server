# Microsoft Graph MCP Server - Installation Script (Windows)
# Run this script in PowerShell

$ErrorActionPreference = "Stop"

Write-Host "🚀 Microsoft Graph MCP Server - Installation" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [version]$matches[1]
        $requiredVersion = [version]"3.10"
        
        if ($version -lt $requiredVersion) {
            Write-Host "❌ Python 3.10 or higher is required. You have $($version.ToString())" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "✅ Python $($version.ToString()) detected" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Python 3 is not installed. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if uv is installed
Write-Host "📋 Checking for uv package manager..." -ForegroundColor Yellow
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvInstalled) {
    Write-Host "⚠️  uv is not installed. Installing uv..." -ForegroundColor Yellow
    try {
        irm https://astral.sh/uv/install.ps1 | iex
        Write-Host "✅ uv installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install uv. Please install manually from: https://github.com/astral-sh/uv" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ uv is already installed" -ForegroundColor Green
}
Write-Host ""

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
uv venv
Write-Host "✅ Virtual environment created" -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
uv pip install -e .
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Setup .env file
Write-Host "⚙️  Setting up environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "✅ .env file created from template" -ForegroundColor Green
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: Edit the .env file with your Azure credentials:" -ForegroundColor Yellow
        Write-Host "   - MICROSOFT_TENANT_ID"
        Write-Host "   - MICROSOFT_CLIENT_ID"
        Write-Host "   - MICROSOFT_CLIENT_SECRET"
        Write-Host ""
        Write-Host "   You can edit it now or later using:"
        Write-Host "   notepad .env"
        Write-Host ""
    } else {
        Write-Host "⚠️  .env.example not found. Please create .env manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "ℹ️  .env file already exists" -ForegroundColor Blue
}
Write-Host ""

# Print next steps
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "=============" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure your Azure credentials in .env:"
Write-Host "   notepad .env"
Write-Host ""
Write-Host "2. Set up Claude Desktop configuration:"
Write-Host "   Location: $env:APPDATA\Claude\claude_desktop_config.json"
Write-Host ""
Write-Host "   Add this configuration (update the path):"
$currentPath = (Get-Location).Path
Write-Host '   {' -ForegroundColor Gray
Write-Host '     "mcpServers": {' -ForegroundColor Gray
Write-Host '       "microsoft-graph": {' -ForegroundColor Gray
Write-Host '         "command": "uv",' -ForegroundColor Gray
Write-Host '         "args": [' -ForegroundColor Gray
Write-Host '           "--directory",' -ForegroundColor Gray
Write-Host "           `"$currentPath`"," -ForegroundColor Gray
Write-Host '           "run",' -ForegroundColor Gray
Write-Host '           "mcp_graph_server.py"' -ForegroundColor Gray
Write-Host '         ],' -ForegroundColor Gray
Write-Host '         "env": {' -ForegroundColor Gray
Write-Host '           "MICROSOFT_TENANT_ID": "your-tenant-id",' -ForegroundColor Gray
Write-Host '           "MICROSOFT_CLIENT_ID": "your-client-id",' -ForegroundColor Gray
Write-Host '           "MICROSOFT_CLIENT_SECRET": "your-client-secret"' -ForegroundColor Gray
Write-Host '         }' -ForegroundColor Gray
Write-Host '       }' -ForegroundColor Gray
Write-Host '     }' -ForegroundColor Gray
Write-Host '   }' -ForegroundColor Gray
Write-Host ""
Write-Host "3. Restart Claude Desktop"
Write-Host ""
Write-Host "4. Test by asking Claude: 'List all available Microsoft 365 licenses'"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - QUICKSTART.md - Fast 10-minute setup guide"
Write-Host "   - README.md - Complete documentation"
Write-Host "   - AZURE_SETUP.md - Azure configuration help"
Write-Host "   - EXAMPLES.md - Usage examples"
Write-Host ""
Write-Host "🎉 Happy automating!" -ForegroundColor Green
