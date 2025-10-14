<img src="https://github.com/ry-ops/microsoft-graph-mcp-server/blob/main/microsoft_graph_mcp_server.png" width="100%">

# Microsoft Graph API MCP Server

A Model Context Protocol (MCP) server that integrates Microsoft Graph API with Claude, enabling management of Microsoft 365 users, licenses, and groups.

## Features

- **User Management**: Create new Microsoft 365 users
- **License Management**: Assign licenses to users with optional service plan customization
- **Group Management**: Add users to groups
- **Query Operations**: List available licenses, groups, and search for users

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
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "microsoft-graph": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/microsoft-graph-mcp",
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

**Important**: Replace `/absolute/path/to/microsoft-graph-mcp` with the actual absolute path to your project directory.

### 5. Restart Claude Desktop

After saving the configuration, restart Claude Desktop to load the MCP server.

## Usage

Once configured, you can use natural language with Claude to manage your Microsoft 365 environment:

### Creating Users

```
Create a new user:
- Display Name: John Doe
- Email: john.doe@yourdomain.com
- Mail Nickname: johndoe
- Password: TempPassword123!
```

### Assigning Licenses

```
First, list available licenses, then assign the Microsoft 365 E3 license to john.doe@yourdomain.com
```

### Adding Users to Groups

```
Add john.doe@yourdomain.com to the "Marketing Team" group
```

### Searching and Listing

```
- Search for users named "John"
- List all groups in the tenant
- Get details for user john.doe@yourdomain.com
```

## Available Tools

The MCP server exposes the following tools to Claude:

1. **create_user**: Create a new Microsoft 365 user
2. **assign_license**: Assign a license to a user
3. **add_user_to_group**: Add a user to a group
4. **list_available_licenses**: List all available licenses in the tenant
5. **list_groups**: List all groups in the tenant
6. **get_user**: Get details for a specific user
7. **search_user**: Search for users by name or email

## Security Considerations

- **Never commit the `.env` file** to version control
- Store client secrets securely
- Use the principle of least privilege when granting API permissions
- Regularly rotate client secrets
- Monitor API usage through Azure Portal
- Consider using Azure Key Vault for production deployments

## Troubleshooting

### Authentication Errors

If you receive authentication errors:
1. Verify your credentials in the `.env` file
2. Ensure admin consent is granted for all API permissions
3. Check that the client secret hasn't expired

### Permission Errors

If operations fail with permission errors:
1. Verify the app has the required API permissions
2. Ensure admin consent has been granted
3. Check that the permissions are application permissions, not delegated

### MCP Server Not Loading

If Claude Desktop doesn't recognize the server:
1. Check the config file path is correct
2. Verify the absolute path to the project directory
3. Look at Claude Desktop logs for errors
4. Ensure uv is installed and in your PATH

## Development

### Running Tests

```bash
uv pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
black mcp_graph_server.py
ruff check mcp_graph_server.py
```

## Common License SKU IDs

Here are some common Microsoft 365 license SKU IDs:

- **Microsoft 365 E3**: `05e9a617-0261-4cee-bb44-138d3ef5d965`
- **Microsoft 365 E5**: `06ebc4ee-1bb5-47dd-8120-11324bc54e06`
- **Microsoft 365 Business Basic**: `3b555118-da6a-4418-894f-7df1e2096870`
- **Microsoft 365 Business Standard**: `f245ecc8-75af-4f8e-b61f-27d8114de5f3`
- **Microsoft 365 Business Premium**: `cbdc14ab-d96c-4c30-b9f4-6ada7cdc1d46`

**Note**: SKU IDs may vary by tenant. Use the `list_available_licenses` tool to see your specific SKU IDs.

## API Rate Limits

Microsoft Graph API has rate limits. The server handles basic error responses, but for production use, consider implementing:
- Exponential backoff
- Request queuing
- Rate limit monitoring

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Resources

- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Azure App Registration Guide](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
