#!/usr/bin/env python3
"""
Microsoft Graph API MCP Server

This MCP server provides tools to manage Microsoft 365 users, licenses, and groups
through the Microsoft Graph API.
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
    
    async def list_available_licenses(self) -> dict:
        """List all available licenses in the tenant"""
        return await self._make_request("GET", "subscribedSkus")
    
    async def list_groups(self) -> dict:
        """List all groups in the tenant"""
        return await self._make_request("GET", "groups")
    
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


# Initialize the MCP server
app = Server("microsoft-graph-mcp")
graph_client = GraphAPIClient()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
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
            description="Add a user to a group",
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
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    try:
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
