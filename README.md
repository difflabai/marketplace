# Plugin Marketplace

A collection of skills, packaged as a Claude Code compatible marketplace.

## Installing

Add the marketplace, then install each plugin you want to use:

```
/plugin marketplace add difflabai/marketplace
/plugin install builder@difflabai
```

MCP servers are configured automatically on install.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [builder](./plugins/builder) | Project scaffolding — build .project/ structures for any AI coding tool |
| [business-world-models](./plugins/business-world-models) | Browse, search, and edit DiffLab Business World Models via the BWM MCP server |
| [dreamsolve](./plugins/dreamsolve) | Use DreamSolve Project management, file handling, and AI agents from Claude, ChatGPT, etc via DreamSolve MCP |
| [pde](./plugins/pde) | Product Delivery Engine — run an idea through DiffLab's 6-stage product pipeline |
| [teams](./plugins/teams) | Team productivity skills — contribution summaries, impact reports, and more |


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
6. Update this README
7. Submit a pull request

## Testing Locally

```
/plugin marketplace add ./path/to/this/repo
/plugin install builder@difflabai
```


## License

MIT License - see [LICENSE](./LICENSE) for details.
