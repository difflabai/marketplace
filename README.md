# Claude Code Plugin Marketplace

A collection of skills and plugins for Claude Code.

## Installing

Add the marketplace, then install a plugin:

```
/plugin marketplace add difflabai/marketplace
/plugin install dreamsolve@difflabai
```

MCP servers are configured automatically on install.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [dreamsolve](./plugins/dreamsolve) | Project management, file handling, and AI agents via DreamSolve MCP |

## Testing Locally

```
/plugin marketplace add ./path/to/this/repo
/plugin install dreamsolve@difflabai
```

## Structure

```
.claude-plugin/
  marketplace.json              # Marketplace catalog
plugins/
  dreamsolve/
    .claude-plugin/
      plugin.json               # Plugin metadata
    .mcp.json                   # MCP server configuration (auto-installed)
    skills/
      dreamsolve/
        SKILL.md                # Skill definition
```

## Contributing

1. Create a directory under `plugins/` with your plugin name
2. Add `.claude-plugin/plugin.json` with name, description, and author
3. Add `.mcp.json` if your plugin needs an MCP server
4. Add skills under `skills/<name>/SKILL.md`
5. Register the plugin in `.claude-plugin/marketplace.json`
6. Submit a pull request

## License

MIT License - see [LICENSE](./LICENSE) for details.
