# Marketplace Installer

Install skills from the Claude Code Plugin Marketplace.

## Triggers

This skill activates when users say:
- "Install the [skill-name] skill"
- "Set up [skill-name] from the marketplace"
- "Add [skill-name] plugin"

## Installation Process

When a user requests to install a skill, Claude should:

### 1. Locate the Skill

Find the skill's `manifest.json` in the marketplace repository:
```
skills/<skill-name>/manifest.json
```

### 2. Read Current Settings

Read the user's Claude Code settings:
```
~/.claude/settings.json
```

### 3. Merge MCP Configuration

Extract the `mcpServer` object from the manifest and merge it into the user's `mcpServers` in settings.json.

**Important:** Preserve all existing MCP servers - only add or update the new one.

### 4. Write Updated Settings

Write the merged configuration back to `~/.claude/settings.json`.

### 5. Confirm Installation

Tell the user:
- The skill has been installed
- They need to restart Claude Code to activate it
- Any authentication steps required (e.g., OAuth browser flow)

## Example Installation Flow

User: "Install the dreamsolve skill"

Claude:
1. Reads `skills/dreamsolve/manifest.json`
2. Reads `~/.claude/settings.json`
3. Adds dreamsolve MCP server config to settings
4. Writes updated settings
5. Responds: "Installed dreamsolve. Restart Claude Code to activate. You'll authenticate via browser on first use."

## Uninstallation

To uninstall a skill:
1. Read `~/.claude/settings.json`
2. Remove the skill's entry from `mcpServers`
3. Write the updated settings
4. Restart Claude Code

## Error Handling

- If skill not found: List available skills
- If settings.json doesn't exist: Create it with the new MCP server
- If MCP server already exists: Ask user if they want to update it
