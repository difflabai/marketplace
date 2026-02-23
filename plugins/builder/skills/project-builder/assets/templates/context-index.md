---
name: index
description: "Catalog of files and documents available for AI analysis. Includes local files, remote documents, and auto-included repository files."
---

# Context Index

## Local Files

| File | Description | Format |
|---|---|---|
| [filename] | [What it contains and when to load it] | [format] |

## Remote Documents

| Document | URL | Refresh |
|---|---|---|
| [name] | [url] | [session/daily/weekly/manual] |

## Auto-Include Patterns

[Glob patterns for repository files that should be automatically included as context]

```yaml
auto_include:
  - "src/**/*.schema.ts"
  - "docs/api/**/*.md"
```
