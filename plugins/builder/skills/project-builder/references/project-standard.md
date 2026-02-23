# .project Standard Quick Reference

Quick reference for the `.project` standard v1. Full spec: https://github.com/difflabai/protocols/blob/main/project-standard/spec/v1/specification.md

## Minimal Valid Structure

```
.project/
  PROJECT.md    (only required file)
```

## Full Directory Structure

```
.project/
├── PROJECT.md              # Project manifest (REQUIRED)
├── instructions/
│   ├── index.md            # Base instructions (always loaded)
│   ├── <topic>.md          # Domain-specific instructions
│   └── local.md            # Personal overrides (gitignored)
├── memory/
│   ├── index.md            # Knowledge catalog
│   ├── <topic>.md          # Knowledge files
│   └── entities/           # Structured entity data
├── conversations/
│   ├── index.md            # Conversation catalog
│   └── <conversation>.md   # Archived conversations
├── context/
│   ├── index.md            # Context catalog
│   └── <file>.<ext>        # Loadable files for AI analysis
├── resources/
│   ├── index.md            # Resource catalog
│   └── <resource>.md       # External reference descriptions
├── tasks/
│   ├── index.md            # Task board overview
│   ├── active/             # In-progress tasks
│   └── completed/          # Finished tasks
├── agents/
│   ├── index.md            # Agent catalog
│   └── <agent>.md          # Agent definitions
├── skills/
│   ├── index.md            # Skill catalog
│   └── <skill>/index.md    # Skill definitions
├── extensions/
│   ├── index.md            # Extension catalog
│   └── <extension>/        # Extension directories
├── adapters/
│   └── <provider>.md       # Provider-specific mappings
├── users/
│   ├── index.md            # Role definitions
│   └── <user>.local.md     # Per-user overrides (gitignored)
└── hooks/
    ├── on-session-start.sh # Startup hook
    └── on-session-end.sh   # Teardown hook
```

## File Format

All files use markdown with YAML frontmatter:

```markdown
---
name: identifier
description: Brief explanation
[additional fields]
---

# Body Content

Free-form markdown.
```

## PROJECT.md Required Fields

- `spec`: Version string (e.g., "1.0")

## PROJECT.md Recommended Fields

- `name`: Project name
- `description`: 1-3 sentence overview

## Three-Tier Loading

1. **Tier 1 (Catalog)**: Frontmatter only, loaded at startup (~50-100 tokens/item)
2. **Tier 2 (Content)**: Full body, loaded when relevant (<5,000 tokens/item)
3. **Tier 3 (References)**: Linked files, loaded on demand

## Naming Conventions

- Lowercase kebab-case for filenames
- `.project/` preferred, `.aiproject/` for Eclipse compatibility
- `index.md` = directory catalog (always loaded)
- `local.md` = personal overrides (gitignored)

## Required Gitignore Patterns

```
.project/local.md
.project/**/local.md
.project/**/*.local.md
.project/**/*.secret.*
.project/users/*.local.md
```

## Adapter Provider Mappings

| Provider | Native Paths |
|---|---|
| Claude Code | `.claude/rules/`, `.claude/agents/`, `CLAUDE.md` |
| Cursor | `.cursor/rules/`, `.cursorrules` |
| AGENTS.md | Root `AGENTS.md` |

## Task Status Values (A2A Compatible)

`submitted` | `working` | `input_required` | `completed` | `failed` | `canceled`

## Instruction Activation Modes

- `always` — Loaded every session
- `auto` — Loaded when file patterns match
- `manual` — Loaded only on explicit request
