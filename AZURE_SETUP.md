# Azure App Registration Setup Guide

This guide walks you through setting up an Azure App Registration for the Microsoft Graph MCP Server.

## Step-by-Step Setup

### 1. Access Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your Microsoft 365 administrator account

### 2. Create App Registration

1. Navigate to **Azure Active Directory** (or **Microsoft Entra ID**)
2. Click **App registrations** in the left menu
3. Click **+ New registration**
4. Fill in the details:
   - **Name**: `Microsoft Graph MCP Server` (or your preferred name)
   - **Supported account types**: Select "Accounts in this organizational directory only"
   - **Redirect URI**: Leave blank (not needed for this application)
5. Click **Register**

### 3. Note Your Credentials

After registration, you'll see the Overview page. **Save these values**:

- **Application (client) ID**: This is your `MICROSOFT_CLIENT_ID`
- **Directory (tenant) ID**: This is your `MICROSOFT_TENANT_ID`

### 4. Create Client Secret

1. In the left menu, click **Certificates & secrets**
2. Click **+ New client secret**
3. Add a description: `MCP Server Secret`
4. Choose an expiration period (recommended: 12-24 months)
5. Click **Add**
6. **IMPORTANT**: Copy the **Value** immediately - this is your `MICROSOFT_CLIENT_SECRET`
   - You won't be able to see it again!
   - Store it securely

### 5. Configure API Permissions

1. In the left menu, click **API permissions**
2. Click **+ Add a permission**
3. Select **Microsoft Graph**
4. Choose **Application permissions** (not Delegated)
5. Add the following permissions:

   **User Management:**
   - `User.ReadWrite.All` - Create, read, update, and delete user accounts

   **Group Management:**
   - `Group.ReadWrite.All` - Read and write all groups

   **Directory Management:**
   - `Directory.ReadWrite.All` - Read and write directory data

   **Organization Info:**
   - `Organization.Read.All` - Read organization information (for license listing)

6. Click **Add permissions**

### 6. Grant Admin Consent

**CRITICAL STEP**: These permissions require administrator consent.

1. After adding all permissions, click **Grant admin consent for [Your Organization]**
2. Click **Yes** to confirm
3. Verify that all permissions show a green checkmark under the **Status** column

### 7. Verify Setup

Your permissions should look like this:

| API / Permission Name          | Type        | Status  |
|-------------------------------|-------------|---------|
| User.ReadWrite.All            | Application | ✓ Granted |
| Group.ReadWrite.All           | Application | ✓ Granted |
| Directory.ReadWrite.All       | Application | ✓ Granted |
| Organization.Read.All         | Application | ✓ Granted |

## Security Best Practices

### Client Secret Management

1. **Never commit secrets to version control**
   - Add `.env` to your `.gitignore`
   - Use environment variables or secret management tools

2. **Rotate secrets regularly**
   - Set calendar reminders before expiration
   - Create a new secret before the old one expires
   - Test the new secret before deleting the old one

3. **Limit secret lifetime**
   - Don't use secrets that never expire
   - Recommended: 12-24 months maximum

### Principle of Least Privilege

Only grant the permissions your application actually needs. The permissions listed above are for full user, group, and license management. If you only need to read data, use read-only permissions instead:

- `User.Read.All` instead of `User.ReadWrite.All`
- `Group.Read.All` instead of `Group.ReadWrite.All`
- `Directory.Read.All` instead of `Directory.ReadWrite.All`

### Monitoring and Auditing

1. **Enable audit logs**:
   - Go to Azure AD → Audit logs
   - Monitor for unexpected API calls

2. **Review sign-in logs**:
   - Go to Azure AD → Sign-in logs
   - Filter by your application

3. **Set up alerts**:
   - Configure alerts for suspicious activity
   - Monitor for failed authentication attempts

## Troubleshooting

### "Insufficient privileges to complete the operation"

**Cause**: Admin consent was not granted or permissions are incorrect.

**Solution**:
1. Verify all permissions are granted with admin consent
2. Ensure you're using **Application permissions**, not Delegated
3. Wait a few minutes after granting consent for changes to propagate

### "Invalid client secret"

**Cause**: The client secret is incorrect or expired.

**Solution**:
1. Generate a new client secret
2. Update your `.env` file with the new secret
3. Delete the old secret after verifying the new one works

### "Application not found"

**Cause**: Client ID or Tenant ID is incorrect.

**Solution**:
1. Double-check the Client ID in App Registration Overview
2. Verify the Tenant ID in Azure AD Overview
3. Ensure there are no extra spaces in your `.env` file

## Required Administrator Roles

To complete this setup, you need one of these Azure AD roles:

- **Global Administrator** (can do everything)
- **Application Administrator** (can manage app registrations and grant consent)
- **Cloud Application Administrator** (similar to Application Administrator)

If you don't have these roles, contact your Microsoft 365 administrator.

## Alternative: Using Existing App Registration

If your organization already has an app registration with the required permissions:

1. Ask your administrator for:
   - The Application (client) ID
   - The Tenant ID
   - A client secret (they'll need to generate one for you)

2. Verify the app has the required permissions with admin consent

## Additional Resources

- [Microsoft Graph Permissions Reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [App Registration Quickstart](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Application vs Delegated Permissions](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent)
- [Microsoft Graph API Best Practices](https://learn.microsoft.com/en-us/graph/best-practices-concept)

## Next Steps

After completing this setup:

1. Copy your credentials to the `.env` file
2. Follow the main README to configure the MCP server
3. Test the connection by listing available licenses
