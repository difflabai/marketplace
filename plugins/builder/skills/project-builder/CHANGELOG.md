# Changelog

## 1.0.0 (2026-02-23)

### Forked
- Forked from [leegonzales/AISkills ProjectBuilder](https://github.com/leegonzales/AISkills/tree/main/ProjectBuilder/project-builder) (v1.0.0)

### Changed
- Adapted to build `.project/` directory structures per the [.project standard specification v1](https://github.com/difflabai/protocols/blob/main/project-standard/spec/v1/specification.md)
- Removed Claude-specific project assumptions; now vendor-neutral across all AI coding tools
- Interview framework updated to gather `.project/` standard fields (spec version, providers, adapters, instructions, memory, context, resources, tasks, agents)
- Templates rewritten for `.project/` markdown-with-YAML-frontmatter format
- Added agent-aware adapter generation (Claude, Codex, Gemini)
- Added `.project` vs `.aiproject` conflict detection for Eclipse IDE compatibility
- Added file overwrite confirmation before writing any existing files
- Added configurable output directory selection
