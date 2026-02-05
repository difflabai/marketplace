# DreamSolve

Connect Claude to DreamSolve for AI-powered project and task management.

## Description

This skill enables Claude to interact with DreamSolve's project management platform through the Model Context Protocol (MCP). With this skill, Claude can create projects, generate task lists from plans, and assign work to team members.

## Prerequisites

- Active DreamSolve account at https://dreamsolve.ai
- Organization membership in DreamSolve
- Node.js installed (for npx command)

## Installation

When the user asks to install or set up the DreamSolve skill, Claude should:

1. Read the user's `~/.claude/settings.json` file
2. Add the dreamsolve MCP server configuration to the `mcpServers` object:

```json
{
  "mcpServers": {
    "dreamsolve": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://dreamsolve.ai/api/mcp/server"]
    }
  }
}
```

3. Write the updated settings back to `~/.claude/settings.json`
4. Inform the user to restart Claude Code to activate the connection
5. On first use, the user will authenticate via browser using OAuth 2.0

### Manual Installation

Alternatively, users can manually add the configuration above to their `~/.claude/settings.json` file.

## Available Tools

Once connected, Claude has access to these DreamSolve tools:

| Tool | Description |
|------|-------------|
| `createProject` | Create a new project with a goal description |
| `createTask` | Add a task to an existing project |
| `createTasksFromPlan` | Parse a plan and create multiple tasks automatically |
| `assignTask` | Assign a task to a team member |

## Usage Examples

### Create a project
"Create a new DreamSolve project for building a mobile app MVP"

### Generate tasks from a plan
"I have this project plan - create tasks in DreamSolve for each step"

### Assign work
"Assign the database setup task to Sarah"

## Security

- Connections use OAuth 2.0 authentication
- Tokens are scoped to your account and organization
- Access can be revoked anytime from DreamSolve settings

## Links

- [DreamSolve Documentation](https://dreamsolve.ai/docs)
- [MCP Connection Guide](https://dreamsolve.ai/docs/guides/connecting-mcp)
