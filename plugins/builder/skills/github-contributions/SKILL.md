---
name: github-contributions
description: "Summarize GitHub contributions across an organization's repositories. Collects commit messages, files changed, and lines changed (no diffs) grouped by contributor for a configurable time period. Use when: generating team activity reports, weekly standups, contribution summaries, or developer productivity reviews. Triggers on: 'contribution report', 'github summary', 'team contributions', 'weekly contributions', 'who did what', 'activity report'."
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3"]
    install:
      - id: pip
        kind: pip
        packages: ["requests"]
        label: "Install Python requests library"
---

# GitHub Contributions Skill

Generate contribution summaries across all active repositories in a GitHub organization, grouped by contributor.

## What This Does

1. Queries a GitHub organization for repositories with activity within a configurable time period
2. For each active repository, collects commit history grouped by author
3. Gathers: commit messages, files changed, lines added/removed (no diffs)
4. Produces a structured per-contributor summary across all repositories

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ORG` | *(required)* | GitHub organization name |
| `TIME_PERIOD` | `7` | Number of days to look back |
| `GITHUB_TOKEN` | *(from env)* | GitHub personal access token (uses `gh` auth if not set) |

## Usage

### Quick Run (Agent)

When the user asks for a contribution report:

1. Determine the organization name (ask if not provided)
2. Determine time period (default: 7 days)
3. Run the collection script:
   ```bash
   python3 <skill_dir>/scripts/collect_contributions.py --org <ORG> --days <TIME_PERIOD>
   ```
4. The script outputs JSON to stdout. Parse it and format the report.
5. Format the output using the template below.

### Manual Run

```bash
# Using gh CLI token
export GITHUB_TOKEN=$(gh auth token)
python3 scripts/collect_contributions.py --org difflabai --days 7
```

## Output Format

Structure the report as follows:

```markdown
# Team Contributions Report
**Organization:** {org}
**Period:** {start_date} → {end_date}

---

## {Contributor Name} (@{username})

**Summary:** {total_commits} commits across {repo_count} repositories | +{lines_added} / -{lines_removed}

### {repo_name}
- **Commits:** {count}
- **Files changed:** {count}
- **Lines:** +{added} / -{removed}
- **Key changes:**
  - {commit_message_1}
  - {commit_message_2}
  ...

---
## Organization Totals

| Contributor | Commits | Repos | Lines Added | Lines Removed |
|-------------|---------|-------|-------------|---------------|
| @{user1}    | {n}     | {n}   | +{n}        | -{n}          |
| ...         |         |       |             |               |
| **Total**   | **{n}** |**{n}**| **+{n}**    | **-{n}**      |
```

## Scripts

### `scripts/collect_contributions.py`

Main collection script. Queries the GitHub API for:
1. All repositories in the organization
2. Filters to repos with commits in the time period
3. Collects commit details per author per repo

Outputs structured JSON to stdout for agent consumption.

### `scripts/format_report.py`

Optional formatting script. Takes the JSON output from `collect_contributions.py` and produces a markdown report.

```bash
python3 scripts/collect_contributions.py --org difflabai --days 7 | python3 scripts/format_report.py
```

## Notes

- Uses GitHub REST API (not GraphQL) for broad compatibility
- Respects rate limits with automatic retry on 429
- Merge commits are excluded by default (use `--include-merges` to include)
- Bot accounts (those ending in `[bot]`) are excluded by default
- If `GITHUB_TOKEN` is not set, attempts to use `gh auth token`
