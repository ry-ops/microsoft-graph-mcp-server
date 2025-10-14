# Microsoft Graph MCP Server - Project Overview

## What You've Got

This is a complete, production-ready MCP (Model Context Protocol) server that integrates Microsoft Graph API with Claude Desktop, enabling you to manage Microsoft 365 users, licenses, and groups using natural language.

## Project Structure

```
microsoft-graph-mcp/
├── mcp_graph_server.py              # Main MCP server implementation
├── pyproject.toml                   # Python project configuration (uv)
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── README.md                        # Complete documentation
├── QUICKSTART.md                    # 10-minute setup guide
├── AZURE_SETUP.md                   # Detailed Azure configuration
├── EXAMPLES.md                      # Usage examples and scenarios
└── claude_desktop_config.example.json  # Claude Desktop config template
```

## What It Does

### Core Features
✅ **User Management**
- Create new Microsoft 365 users
- Search for existing users
- Get detailed user information

✅ **License Management**
- List all available licenses in your tenant
- Assign licenses to users
- Customize which services are enabled

✅ **Group Management**
- List all groups
- Add users to groups
- Search for groups

✅ **Natural Language Interface**
- Talk to Claude naturally
- No need to remember API syntax
- Claude handles all the technical details

## How to Get Started

### Option 1: Quick Start (10 minutes)
Follow `QUICKSTART.md` for the fastest setup experience.

### Option 2: Detailed Setup
Follow `README.md` for comprehensive instructions and explanations.

### Option 3: Azure First
If you need help with Azure setup, start with `AZURE_SETUP.md`.

## Key Technologies

- **MCP (Model Context Protocol)**: Connects Claude to external tools
- **Microsoft Graph API**: Microsoft's unified API for Microsoft 365
- **uv**: Fast Python package installer and resolver
- **MSAL (Microsoft Authentication Library)**: Handles OAuth2 authentication
- **httpx**: Modern async HTTP client for Python

## Security Features

✅ Application-level authentication (no user delegation)
✅ Environment variable credential storage
✅ Secure token management via MSAL
✅ Admin consent required for all operations
✅ Audit trail through Azure AD logs

## What You Need

### Required
1. **Microsoft 365 Tenant** with admin access
2. **Azure AD admin rights** to create app registrations
3. **Python 3.10+** installed on your machine
4. **Claude Desktop** application
5. **uv package manager** (installation included in guides)

### Azure Permissions Required
Your Azure app registration needs these **Application** permissions:
- `User.ReadWrite.All` - Manage users
- `Group.ReadWrite.All` - Manage groups
- `Directory.ReadWrite.All` - Access directory
- `Organization.Read.All` - Read organization info

## Example Usage

Once configured, you can use natural language with Claude:

**You**: "Create a new user named John Smith with email john.smith@company.com and assign him a Microsoft 365 E3 license"

**Claude**: Will execute the following:
1. Create the user account
2. List available licenses to find E3
3. Assign the license to John
4. Confirm success

**You**: "Show me all users in the Marketing Team group"

**Claude**: Will:
1. Search for the Marketing Team group
2. Get all members
3. Display their information

## File Descriptions

### Core Files

**mcp_graph_server.py**
- The main server implementation
- Handles authentication with Microsoft Graph
- Defines all available tools (create_user, assign_license, etc.)
- Processes requests from Claude Desktop

**pyproject.toml**
- Python project configuration
- Lists all required dependencies
- Configuration for code quality tools (black, ruff)
- Defines the project metadata

### Configuration Files

**.env.example**
- Template for your credentials
- Copy to `.env` and fill in your values
- Never commit the actual `.env` file!

**claude_desktop_config.example.json**
- Template for Claude Desktop configuration
- Shows how to register the MCP server
- Update the path to your project directory

### Documentation

**README.md** (Main documentation)
- Complete setup instructions
- Detailed usage guide
- Troubleshooting section
- Security considerations

**QUICKSTART.md** (Fast setup)
- 10-minute setup guide
- Minimal explanation, maximum speed
- Perfect for experienced developers

**AZURE_SETUP.md** (Azure configuration)
- Step-by-step Azure portal walkthrough
- Screenshots and detailed explanations
- Security best practices
- Troubleshooting Azure-specific issues

**EXAMPLES.md** (Usage examples)
- Real-world scenarios
- Example conversations with Claude
- Advanced use cases
- Tips for best results

### Development Files

**.gitignore**
- Prevents committing sensitive files
- Excludes virtual environments
- Ignores IDE configuration

**LICENSE**
- MIT License
- Permissive open-source license
- You can modify and distribute freely

## Customization Options

The server is designed to be extensible. You can add:

### Additional Tools
- User deletion
- Password reset
- License removal
- Bulk operations
- Export reports

### Enhanced Features
- Rate limiting
- Retry logic
- Caching
- Webhook support
- Email notifications

### Integration with Other Services
- Combine with other MCP servers
- Add Slack notifications
- Integrate with ticketing systems
- Connect to HR systems

## Common Workflows

### Employee Onboarding
1. Create user account
2. Assign appropriate license
3. Add to departmental groups
4. Set up email alias (future feature)

### License Audit
1. List all available licenses
2. Check usage statistics
3. Identify unused licenses
4. Optimize costs

### Access Management
1. Search for users
2. Review group memberships
3. Add/remove from groups
4. Audit permissions

## Production Considerations

### Before Production Use

1. **Security Review**
   - Use Azure Key Vault for secrets
   - Implement IP restrictions
   - Enable conditional access
   - Set up Azure Monitor

2. **Error Handling**
   - Add retry logic for API calls
   - Implement exponential backoff
   - Log all operations
   - Set up alerting

3. **Rate Limiting**
   - Monitor API quota usage
   - Implement request throttling
   - Cache frequently accessed data

4. **Compliance**
   - Review data retention policies
   - Implement audit logging
   - Document all operations
   - Set up compliance monitoring

## Support and Resources

### Documentation
- [Microsoft Graph API Docs](https://learn.microsoft.com/en-us/graph/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Azure AD Best Practices](https://learn.microsoft.com/en-us/azure/active-directory/)

### Getting Help
1. Check the troubleshooting sections in README.md
2. Review Azure AD audit logs
3. Check Claude Desktop logs
4. Verify API permissions in Azure portal

## Next Steps

1. **Setup** (Choose one path)
   - Quick: Follow QUICKSTART.md
   - Detailed: Follow README.md
   - Azure first: Start with AZURE_SETUP.md

2. **Test**
   - Start with simple commands
   - List licenses and groups
   - Create a test user in a safe environment

3. **Learn**
   - Review EXAMPLES.md for ideas
   - Experiment with different queries
   - Discover natural language patterns that work well

4. **Customize**
   - Add features you need
   - Integrate with your workflows
   - Share improvements with the community

## Contributing

This is open-source software under the MIT License. Feel free to:
- Report issues
- Suggest features
- Submit pull requests
- Share your use cases

## License

MIT License - See LICENSE file for full text.

---

**Ready to get started?** Open `QUICKSTART.md` for the fastest path to a working system!

**Have questions about Azure?** Check out `AZURE_SETUP.md` for detailed guidance.

**Want to see it in action?** Review `EXAMPLES.md` for real usage scenarios.

**Need comprehensive docs?** The `README.md` has everything you need.

Happy automating! 🚀
