# Usage Examples

This document provides concrete examples of how to use the Microsoft Graph MCP Server with Claude.

## Example 1: Onboarding a New Employee

**You**: I need to onboard a new employee. Create a user for Sarah Johnson with email sarah.johnson@company.com, assign her a Microsoft 365 E3 license, and add her to the Marketing Team group.

**Claude will**:
1. Create the user with a temporary password
2. List available licenses to find the E3 SKU ID
3. Assign the license to the new user
4. Search for the Marketing Team group
5. Add Sarah to the group

**Result**: Sarah is fully set up and ready to work!

---

## Example 2: Bulk License Assignment

**You**: List all available licenses in our tenant, then assign the Microsoft 365 Business Standard license to john.doe@company.com and jane.smith@company.com

**Claude will**:
1. List all licenses and their SKU IDs
2. Identify the Business Standard SKU
3. Assign the license to both users
4. Confirm success for each assignment

---

## Example 3: Creating Multiple Users

**You**: Create three new users:
1. Mike Brown - mike.brown@company.com - Engineering team
2. Lisa White - lisa.white@company.com - Sales team  
3. Tom Green - tom.green@company.com - HR team

Give them all temporary password "Welcome2024!" and require password change on first login.

**Claude will**:
1. Create each user account
2. Set the specified password with force change flag
3. Confirm creation of all three users

---

## Example 4: Auditing User Access

**You**: Search for all users with "admin" in their name and list what groups they belong to

**Claude will**:
1. Search for users matching "admin"
2. For each user found, get their details including group memberships
3. Present a summary of admin users and their access

---

## Example 5: License Management

**You**: Show me all available licenses, how many are assigned, and how many are remaining

**Claude will**:
1. Call list_available_licenses
2. Parse the response to show:
   - License name
   - Total units purchased
   - Units assigned
   - Units available
3. Present this in an easy-to-read format

---

## Example 6: Group Management

**You**: Create a comprehensive report of all our groups, showing:
- Group name
- Number of members
- Group type (Security, Microsoft 365, etc.)

**Claude will**:
1. List all groups in the tenant
2. For each group, get member counts
3. Format this into a clear report

---

## Example 7: Troubleshooting User Access

**You**: John Doe says he can't access Teams. Can you check his user account and licenses?

**Claude will**:
1. Search for John Doe
2. Get his user details
3. Check assigned licenses
4. Identify if Teams is included in his license
5. Suggest next steps if there's an issue

---

## Example 8: Offboarding Process

**You**: We need to offboard sarah.johnson@company.com. Show me what licenses and groups she has so I can document it.

**Claude will**:
1. Get Sarah's user details
2. List her assigned licenses
3. List her group memberships
4. Provide a summary for documentation

**Note**: The MCP server currently doesn't include user deletion functionality for safety. You can add this feature if needed.

---

## Example 9: License Optimization

**You**: We're paying for Microsoft 365 E5 licenses but some users might only need E3. Show me all users with E5 licenses and suggest who might be downgraded based on their group memberships.

**Claude will**:
1. List users with E5 licenses
2. Check their group memberships
3. Analyze usage patterns (based on groups)
4. Suggest potential cost savings

---

## Example 10: New Department Setup

**You**: We're creating a new Customer Success department. I need to:
1. Create a "Customer Success" group
2. Add 5 new team members
3. Assign them all Business Standard licenses
4. Add them all to the Customer Success group

**Claude will**: Guide you through each step systematically, confirming each action before moving to the next.

---

## Tips for Best Results

### Be Specific
❌ "Create a user"
✅ "Create a user named John Smith with email john.smith@company.com"

### Provide Context
❌ "Assign a license"
✅ "Assign a Microsoft 365 E3 license to john.smith@company.com"

### Ask for Verification
✅ "First, search for the Marketing group to get its ID, then add the user"

### Use Step-by-Step for Complex Tasks
✅ "Let's onboard a new employee step by step. First, create the user account..."

### Request Summaries
✅ "After creating all the users, give me a summary of what was created"

---

## Advanced Scenarios

### Custom License Plans

You can disable specific services within a license:

**You**: Assign a Microsoft 365 E3 license to user@company.com but disable Yammer and Sway

**Claude will** need the service plan IDs for Yammer and Sway, which you can find by first listing the available licenses and their service plans.

### Conditional Operations

**You**: If john.doe@company.com doesn't have a license yet, assign him a Business Standard license

**Claude will**:
1. Check John's current licenses
2. Only assign if no license is present
3. Report the action taken

### Bulk Operations with Error Handling

**You**: Assign Business Standard licenses to all users in the "New Hires" group. If any fail, tell me which ones and why.

**Claude will**:
1. Get all members of the New Hires group
2. Attempt to assign licenses to each
3. Report successes and failures
4. Provide error details for any failures

---

## Security Reminders

When working with user management:
- Never share passwords in chat (use secure password managers)
- Always verify user identity before making changes
- Document all administrative actions
- Review group memberships regularly
- Audit license assignments periodically

---

## Getting Help

If something isn't working:
1. Ask Claude to verify the configuration
2. Request Claude to check error messages
3. Review the AZURE_SETUP.md for permission issues
4. Check the README.md troubleshooting section
