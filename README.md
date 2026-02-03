<img src="https://github.com/ry-ops/microsoft-graph-mcp-server/blob/main/microsoft_graph_mcp_server.png" width="100%">

[\![Version](https://img.shields.io/github/v/release/ry-ops/microsoft-graph-mcp-server?style=flat-square)](https://github.com/ry-ops/microsoft-graph-mcp-server/releases)
[\![License](https://img.shields.io/github/license/ry-ops/microsoft-graph-mcp-server?style=flat-square)](LICENSE)
[\![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[\![MCP](https://img.shields.io/badge/MCP-Server-00A67E?style=flat-square)](https://modelcontextprotocol.io)


# Microsoft Graph API MCP Server

A Model Context Protocol (MCP) server that integrates Microsoft Graph API with Claude, enabling management of Microsoft 365 users, licenses, and groups.

## Features

- **User Management**: Create new Microsoft 365 users
- **License Management**: Assign licenses to users with optional service plan customization
- **Group Management**: Add users to groups
- **Query Operations**: List available licenses, groups, and search for users
- **A2A Protocol Support**: Agent-to-Agent communication for automated M365 administration

## Prerequisites

1. **Microsoft Azure App Registration**:
   - An Azure AD application with the following API permissions:
     - `User.ReadWrite.All`
     - `Directory.ReadWrite.All`
     - `Group.ReadWrite.All`
     - `Organization.Read.All`
   - Admin consent granted for these permissions
   - A client secret generated

2. **Python 3.10+** and **uv** package manager

## Setup

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup Project

```bash
# Create project directory
mkdir microsoft-graph-mcp
cd microsoft-graph-mcp

# Copy the server files
# (copy mcp_graph_server.py and pyproject.toml to this directory)

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scriptsctivate
uv pip install -e .
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
MICROSOFT_TENANT_ID=your-tenant-id
MICROSOFT_CLIENT_ID=your-client-id
MICROSOFT_CLIENT_SECRET=your-client-secret
```

**To find these values:**

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to Azure Active Directory → App registrations
3. Select your app registration
4. **Tenant ID**: Found in the Overview page
5. **Client ID**: Application (client) ID in the Overview page
6. **Client Secret**: Create one in Certificates & secrets

### 4. Configure Claude Desktop

Add the server configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude
