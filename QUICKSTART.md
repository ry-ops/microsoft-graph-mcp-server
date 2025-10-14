# Quick Start Guide

Get up and running with the Microsoft Graph MCP Server in 10 minutes.

## Prerequisites Checklist

- [ ] Python 3.10 or higher installed
- [ ] uv package manager installed
- [ ] Azure AD admin access
- [ ] Claude Desktop installed

## 5-Minute Setup

### 1. Azure Setup (2 minutes)

1. Go to [Azure Portal](https://portal.azure.com) → Azure AD → App registrations
2. Click "New registration" → Name it "Graph MCP Server" → Register
3. Copy the **Application (client) ID** and **Directory (tenant) ID**
4. Go to "Certificates & secrets" → "New client secret" → Copy the **Value**
5. Go to "API permissions" → Add these **Application** permissions:
   - `User.ReadWrite.All`
   - `Group.ReadWrite.All`
   - `Directory.ReadWrite.All`
   - `Organization.Read.All`
6. Click "Grant admin consent" → Yes

**✓ Azure is ready!**

### 2. Install uv (30 seconds)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Project Setup (1 minute)

```bash
# Create directory
mkdir ~/microsoft-graph-mcp
cd ~/microsoft-graph-mcp

# Download files (or copy from the provided files)
# You should have:
# - mcp_graph_server.py
# - pyproject.toml
# - .env.example

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Add your credentials to `.env`:
```
MICROSOFT_TENANT_ID=your-tenant-id-here
MICROSOFT_CLIENT_ID=your-client-id-here
MICROSOFT_CLIENT_SECRET=your-client-secret-here
```

### 4. Install Dependencies (30 seconds)

```bash
# Create virtual environment and install
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

### 5. Configure Claude Desktop (1 minute)

**macOS**: Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: Edit `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration (replace the path with your actual path):

```json
{
  "mcpServers": {
    "microsoft-graph": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yourname/microsoft-graph-mcp",
        "run",
        "mcp_graph_server.py"
      ],
      "env": {
        "MICROSOFT_TENANT_ID": "your-tenant-id",
        "MICROSOFT_CLIENT_ID": "your-client-id",
        "MICROSOFT_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

**Get your absolute path**:
```bash
# In your project directory, run:
pwd  # macOS/Linux
cd   # Windows (in PowerShell)
```

### 6. Test It! (30 seconds)

1. Restart Claude Desktop
2. Open a new chat
3. Try this message:

```
List all available Microsoft 365 licenses in our tenant
```

If you see license information, **you're all set!** 🎉

## First Commands to Try

```
1. List all groups in our tenant
2. Search for users named "John"
3. Show me the available Microsoft 365 licenses
```

## Troubleshooting

**Error: "Missing required environment variables"**
- Check your `.env` file has all three credentials
- Verify no extra spaces or quotes around values

**Error: "Insufficient privileges"**
- Go back to Azure → API permissions
- Click "Grant admin consent" again
- Wait 2-3 minutes for changes to propagate

**Error: "MCP server not found"**
- Verify the absolute path in claude_desktop_config.json
- Check that uv is installed: `uv --version`
- Restart Claude Desktop completely

**Claude doesn't recognize the server**
- Check the config file syntax (valid JSON)
- Look for Claude Desktop logs in:
  - macOS: `~/Library/Logs/Claude/`
  - Windows: `%APPDATA%\Claude\logs\`

## Next Steps

Once working:
1. Read `EXAMPLES.md` for usage ideas
2. Review `AZURE_SETUP.md` for security best practices
3. Check `README.md` for comprehensive documentation

## Quick Reference

### Common SKU IDs
- **Microsoft 365 E3**: `05e9a617-0261-4cee-bb44-138d3ef5d965`
- **Microsoft 365 E5**: `06ebc4ee-1bb5-47dd-8120-11324bc54e06`
- **Business Standard**: `f245ecc8-75af-4f8e-b61f-27d8114de5f3`

### Useful Commands for Claude

```
Create user: [name] with email [email]
Assign [license] to [user]
Add [user] to [group] group
List all groups
Search for user [name]
```

## Support

If you get stuck:
1. Check the troubleshooting section above
2. Review the full README.md
3. Verify Azure permissions in AZURE_SETUP.md
4. Check Claude Desktop logs for specific errors

Happy automating! 🚀
