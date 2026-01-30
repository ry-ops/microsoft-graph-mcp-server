#!/usr/bin/env python3
"""
Microsoft Graph API MCP Server

This MCP server provides tools to manage Microsoft 365 users, licenses, groups,
and SharePoint sites through the Microsoft Graph API.
"""

import os
import json
import asyncio
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import msal
import httpx


class GraphAPIClient:
    """Client for Microsoft Graph API operations"""
    
    def __init__(self):
        self.tenant_id = os.getenv("MICROSOFT_TENANT_ID")
        self.client_id = os.getenv("MICROSOFT_CLIENT_ID")
        self.client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError(
                "Missing required environment variables: "
                "MICROSOFT_TENANT_ID, MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET"
            )
        
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.graph_endpoint = "https://graph.microsoft.com/v1.0"
        
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        self._token = None
    
    async def get_token(self) -> str:
        """Get or refresh access token"""
        result = self.app.acquire_token_silent(self.scope, account=None)
        if not result:
            result = self.app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            self._token = result["access_token"]
            return self._token
        else:
            raise Exception(f"Failed to acquire token: {result.get('error_description')}")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: dict = None
    ) -> dict:
        """Make authenticated request to Graph API"""
        token = await self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.graph_endpoint}/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method == "PATCH":
                response = await client.patch(url, headers=headers, json=data)
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            
            # Some endpoints return 204 No Content
            if response.status_code == 204:
                return {"success": True}
            
            return response.json()
    
    # ==================== USER OPERATIONS ====================
    
    async def create_user(
        self,
        display_name: str,
        user_principal_name: str,
        mail_nickname: str,
        password: str,
        account_enabled: bool = True,
        force_change_password: bool = True
    ) -> dict:
        """Create a new user in Microsoft 365"""
        user_data = {
            "accountEnabled": account_enabled,
            "displayName": display_name,
            "mailNickname": mail_nickname,
            "userPrincipalName": user_principal_name,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": force_change_password,
                "password": password
            }
        }
        
        return await self._make_request("POST", "users", user_data)
    
    async def assign_license(
        self,
        user_id: str,
        sku_id: str,
        disabled_plans: list = None
    ) -> dict:
        """Assign a license to a user"""
        license_data = {
            "addLicenses": [
                {
                    "skuId": sku_id,
                    "disabledPlans": disabled_plans or []
                }
            ],
            "removeLicenses": []
        }
        
        return await self._make_request(
            "POST",
            f"users/{user_id}/assignLicense",
            license_data
        )
    
    async def add_user_to_group(
        self,
        user_id: str,
        group_id: str
    ) -> dict:
        """Add a user to a group"""
        member_data = {
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
        }
        
        return await self._make_request(
            "POST",
            f"groups/{group_id}/members/$ref",
            member_data
        )
    
    async def remove_user_from_group(
        self,
        user_id: str,
        group_id: str
    ) -> dict:
        """Remove a user from a group"""
        return await self._make_request(
            "DELETE",
            f"groups/{group_id}/members/{user_id}/$ref"
        )
    
    async def list_available_licenses(self) -> dict:
        """List all available licenses in the tenant"""
        return await self._make_request("GET", "subscribedSkus")
    
    async def list_groups(self) -> dict:
        """List all groups in the tenant"""
        return await self._make_request("GET", "groups?$select=id,displayName,description,groupTypes,mail")
    
    async def get_group_members(self, group_id: str) -> dict:
        """Get members of a group"""
        return await self._make_request("GET", f"groups/{group_id}/members?$select=id,displayName,userPrincipalName")
    
    async def get_user(self, user_id: str) -> dict:
        """Get user details"""
        return await self._make_request("GET", f"users/{user_id}")
    
    async def search_user(self, search_term: str) -> dict:
        """Search for users by display name or email"""
        filter_query = f"startswith(displayName,'{search_term}') or startswith(userPrincipalName,'{search_term}')"
        return await self._make_request(
            "GET",
            f"users?$filter={filter_query}"
        )
    
    async def list_users(self, top: int = 100) -> dict:
        """List all users in the tenant"""
        return await self._make_request(
            "GET",
            f"users?$select=id,displayName,userPrincipalName,mail,jobTitle&$top={top}"
        )
    
    # ==================== SHAREPOINT OPERATIONS ====================
    
    async def list_sites(self, search: str = None) -> dict:
        """List SharePoint sites. Optionally search by name."""
        if search:
            return await self._make_request(
                "GET",
                f"sites?search={search}&$select=id,name,displayName,webUrl"
            )
        return await self._make_request(
            "GET",
            "sites?$select=id,name,displayName,webUrl"
        )
    
    async def get_site(self, site_id: str) -> dict:
        """Get a SharePoint site by ID or path (e.g., 'contoso.sharepoint.com:/sites/marketing')"""
        # Handle site path format
        if ".sharepoint.com:" in site_id or "/" in site_id:
            return await self._make_request("GET", f"sites/{site_id}")
        return await self._make_request("GET", f"sites/{site_id}")
    
    async def get_site_by_url(self, hostname: str, site_path: str) -> dict:
        """Get a SharePoint site by hostname and path"""
        return await self._make_request(
            "GET",
            f"sites/{hostname}:/{site_path}"
        )
    
    async def list_site_permissions(self, site_id: str) -> dict:
        """List permissions on a SharePoint site"""
        return await self._make_request("GET", f"sites/{site_id}/permissions")
    
    async def add_site_permission(
        self,
        site_id: str,
        user_id: str,
        role: str = "write"
    ) -> dict:
        """
        Add a user permission to a SharePoint site.
        
        Roles: read, write, owner
        """
        roles_map = {
            "read": ["read"],
            "write": ["write"],
            "owner": ["owner"]
        }
        
        permission_data = {
            "roles": roles_map.get(role, ["write"]),
            "grantedToIdentities": [
                {
                    "application": None,
                    "user": {
                        "id": user_id
                    }
                }
            ]
        }
        
        return await self._make_request(
            "POST",
            f"sites/{site_id}/permissions",
            permission_data
        )
    
    async def remove_site_permission(self, site_id: str, permission_id: str) -> dict:
        """Remove a permission from a SharePoint site"""
        return await self._make_request(
            "DELETE",
            f"sites/{site_id}/permissions/{permission_id}"
        )
    
    async def list_site_drives(self, site_id: str) -> dict:
        """List document libraries (drives) in a SharePoint site"""
        return await self._make_request(
            "GET",
            f"sites/{site_id}/drives?$select=id,name,webUrl"
        )
    
    async def list_site_lists(self, site_id: str) -> dict:
        """List all lists in a SharePoint site"""
        return await self._make_request(
            "GET",
            f"sites/{site_id}/lists?$select=id,name,displayName,webUrl"
        )
    
    async def get_root_site(self) -> dict:
        """Get the root SharePoint site for the tenant"""
        return await self._make_request("GET", "sites/root")


# Initialize the MCP server
app = Server("microsoft-graph-mcp")
graph_client = GraphAPIClient()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        # ==================== USER TOOLS ====================
        Tool(
            name="create_user",
            description="Create a new user in Microsoft 365",
            inputSchema={
                "type": "object",
                "properties": {
                    "display_name": {
                        "type": "string",
                        "description": "The display name for the user"
                    },
                    "user_principal_name": {
                        "type": "string",
                        "description": "The user principal name (email format, e.g., user@domain.com)"
                    },
                    "mail_nickname": {
                        "type": "string",
                        "description": "The mail alias for the user"
                    },
                    "password": {
                        "type": "string",
                        "description": "The initial password for the user"
                    },
                    "account_enabled": {
                        "type": "boolean",
                        "description": "Whether the account is enabled",
                        "default": True
                    },
                    "force_change_password": {
                        "type": "boolean",
                        "description": "Whether user must change password on first login",
                        "default": True
                    }
                },
                "required": ["display_name", "user_principal_name", "mail_nickname", "password"]
            }
        ),
        Tool(
            name="assign_license",
            description="Assign a license to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user ID or user principal name"
                    },
                    "sku_id": {
                        "type": "string",
                        "description": "The SKU ID of the license to assign"
                    },
                    "disabled_plans": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of service plan IDs to disable (optional)",
                        "default": []
                    }
                },
                "required": ["user_id", "sku_id"]
            }
        ),
        Tool(
            name="add_user_to_group",
            description="Add a user to a group (also grants access to group-connected SharePoint sites)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user ID or user principal name"
                    },
                    "group_id": {
                        "type": "string",
                        "description": "The group ID"
                    }
                },
                "required": ["user_id", "group_id"]
            }
        ),
        Tool(
            name="remove_user_from_group",
            description="Remove a user from a group",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user ID"
                    },
                    "group_id": {
                        "type": "string",
                        "description": "The group ID"
                    }
                },
                "required": ["user_id", "group_id"]
            }
        ),
        Tool(
            name="list_available_licenses",
            description="List all available licenses (SKUs) in the tenant",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_groups",
            description="List all groups in the tenant",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_group_members",
            description="Get all members of a group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {
                        "type": "string",
                        "description": "The group ID"
                    }
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="get_user",
            description="Get details for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The user ID or user principal name"
                    }
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="search_user",
            description="Search for users by display name or email",
            inputSchema={
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "The search term to look for in display names or emails"
                    }
                },
                "required": ["search_term"]
            }
        ),
        Tool(
            name="list_users",
            description="List all users in the tenant",
            inputSchema={
                "type": "object",
                "properties": {
                    "top": {
                        "type": "integer",
                        "description": "Maximum number of users to return",
                        "default": 100
                    }
                }
            }
        ),
        # ==================== SHAREPOINT TOOLS ====================
        Tool(
            name="list_sites",
            description="List SharePoint sites in the tenant. Optionally search by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Optional search term to filter sites by name"
                    }
                }
            }
        ),
        Tool(
            name="get_site",
            description="Get details for a specific SharePoint site by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "The site ID"
                    }
                },
                "required": ["site_id"]
            }
        ),
        Tool(
            name="get_site_by_url",
            description="Get a SharePoint site by hostname and path",
            inputSchema={
                "type": "object",
                "properties": {
                    "hostname": {
                        "type": "string",
                        "description": "The SharePoint hostname (e.g., contoso.sharepoint.com)"
                    },
                    "site_path": {
                        "type": "string",
                        "description": "The site path (e.g., sites/marketing)"
                    }
                },
                "required": ["hostname", "site_path"]
            }
        ),
        Tool(
            name="get_root_site",
            description="Get the root SharePoint site for the tenant",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_site_permissions",
            description="List all permissions on a SharePoint site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "The site ID"
                    }
                },
                "required": ["site_id"]
            }
        ),
        Tool(
            name="add_site_permission",
            description="Add a user permission to a SharePoint site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "The site ID"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The user ID to grant access"
                    },
                    "role": {
                        "type": "string",
                        "enum": ["read", "write", "owner"],
                        "description": "The permission level: read, write, or owner",
                        "default": "write"
                    }
                },
                "required": ["site_id", "user_id"]
            }
        ),
        Tool(
            name="remove_site_permission",
            description="Remove a permission from a SharePoint site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "The site ID"
                    },
                    "permission_id": {
                        "type": "string",
                        "description": "The permission ID to remove"
                    }
                },
                "required": ["site_id", "permission_id"]
            }
        ),
        Tool(
            name="list_site_drives",
            description="List document libraries in a SharePoint site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "The site ID"
                    }
                },
                "required": ["site_id"]
            }
        ),
        Tool(
            name="list_site_lists",
            description="List all lists in a SharePoint site",
            inputSchema={
                "type": "object",
                "properties": {
                    "site_id": {
                        "type": "string",
                        "description": "The site ID"
                    }
                },
                "required": ["site_id"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
        # ==================== USER HANDLERS ====================
        if name == "create_user":
            result = await graph_client.create_user(
                display_name=arguments["display_name"],
                user_principal_name=arguments["user_principal_name"],
                mail_nickname=arguments["mail_nickname"],
                password=arguments["password"],
                account_enabled=arguments.get("account_enabled", True),
                force_change_password=arguments.get("force_change_password", True)
            )
            return [TextContent(
                type="text",
                text=f"User created successfully:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "assign_license":
            result = await graph_client.assign_license(
                user_id=arguments["user_id"],
                sku_id=arguments["sku_id"],
                disabled_plans=arguments.get("disabled_plans", [])
            )
            return [TextContent(
                type="text",
                text=f"License assigned successfully:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "add_user_to_group":
            result = await graph_client.add_user_to_group(
                user_id=arguments["user_id"],
                group_id=arguments["group_id"]
            )
            return [TextContent(
                type="text",
                text="User added to group successfully"
            )]
        
        elif name == "remove_user_from_group":
            result = await graph_client.remove_user_from_group(
                user_id=arguments["user_id"],
                group_id=arguments["group_id"]
            )
            return [TextContent(
                type="text",
                text="User removed from group successfully"
            )]
        
        elif name == "list_available_licenses":
            result = await graph_client.list_available_licenses()
            return [TextContent(
                type="text",
                text=f"Available licenses:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "list_groups":
            result = await graph_client.list_groups()
            return [TextContent(
                type="text",
                text=f"Groups:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "get_group_members":
            result = await graph_client.get_group_members(
                group_id=arguments["group_id"]
            )
            return [TextContent(
                type="text",
                text=f"Group members:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "get_user":
            result = await graph_client.get_user(
                user_id=arguments["user_id"]
            )
            return [TextContent(
                type="text",
                text=f"User details:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "search_user":
            result = await graph_client.search_user(
                search_term=arguments["search_term"]
            )
            return [TextContent(
                type="text",
                text=f"Search results:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "list_users":
            result = await graph_client.list_users(
                top=arguments.get("top", 100)
            )
            return [TextContent(
                type="text",
                text=f"Users:\n{json.dumps(result, indent=2)}"
            )]
        
        # ==================== SHAREPOINT HANDLERS ====================
        elif name == "list_sites":
            result = await graph_client.list_sites(
                search=arguments.get("search")
            )
            return [TextContent(
                type="text",
                text=f"SharePoint sites:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "get_site":
            result = await graph_client.get_site(
                site_id=arguments["site_id"]
            )
            return [TextContent(
                type="text",
                text=f"Site details:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "get_site_by_url":
            result = await graph_client.get_site_by_url(
                hostname=arguments["hostname"],
                site_path=arguments["site_path"]
            )
            return [TextContent(
                type="text",
                text=f"Site details:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "get_root_site":
            result = await graph_client.get_root_site()
            return [TextContent(
                type="text",
                text=f"Root site:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "list_site_permissions":
            result = await graph_client.list_site_permissions(
                site_id=arguments["site_id"]
            )
            return [TextContent(
                type="text",
                text=f"Site permissions:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "add_site_permission":
            result = await graph_client.add_site_permission(
                site_id=arguments["site_id"],
                user_id=arguments["user_id"],
                role=arguments.get("role", "write")
            )
            return [TextContent(
                type="text",
                text=f"Permission added:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "remove_site_permission":
            result = await graph_client.remove_site_permission(
                site_id=arguments["site_id"],
                permission_id=arguments["permission_id"]
            )
            return [TextContent(
                type="text",
                text="Permission removed successfully"
            )]
        
        elif name == "list_site_drives":
            result = await graph_client.list_site_drives(
                site_id=arguments["site_id"]
            )
            return [TextContent(
                type="text",
                text=f"Document libraries:\n{json.dumps(result, indent=2)}"
            )]
        
        elif name == "list_site_lists":
            result = await graph_client.list_site_lists(
                site_id=arguments["site_id"]
            )
            return [TextContent(
                type="text",
                text=f"Site lists:\n{json.dumps(result, indent=2)}"
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
