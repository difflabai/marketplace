# Claude Code Plugin Marketplace

A collection of skills and plugins for Claude Code.

## Installing Skills

### Automatic Installation

Ask Claude to install a skill:

```
Install the dreamsolve skill from the marketplace
```

Claude will:
1. Read the skill's `manifest.json` to get the MCP server configuration
2. Add the MCP server to your `~/.claude/settings.json`
3. Prompt you to restart Claude Code

### Manual Installation

1. Navigate to the skill directory
2. Copy the `mcpServer` configuration from `manifest.json`
3. Add it to your `~/.claude/settings.json` under `mcpServers`
4. Restart Claude Code

## Available Skills

| Skill | Description |
|-------|-------------|
| [dreamsolve](./skills/dreamsolve) | AI-powered project and task management via MCP |
| [marketplace-installer](./skills/marketplace-installer) | Utility to install other marketplace skills |

## Skill Structure

Each skill contains:

```
skills/<skill-name>/
├── SKILL.md        # Human-readable documentation
└── manifest.json   # Machine-readable configuration
```

### manifest.json Schema

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "What the skill does",
  "mcpServer": {
    "server-name": {
      "command": "npx",
      "args": ["..."]
    }
  },
  "tools": [
    { "name": "toolName", "description": "What it does" }
  ]
}
```

## Contributing

To add a new skill:

1. Create a directory under `skills/` with your skill name
2. Add a `manifest.json` with the MCP server configuration
3. Add a `SKILL.md` with documentation and usage examples
4. Submit a pull request

## License

MIT License - see [LICENSE](./LICENSE) for details.
