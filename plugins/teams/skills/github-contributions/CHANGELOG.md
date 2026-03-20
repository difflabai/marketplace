# Changelog

## 1.1.0 (2026-03-20)

- List PRs with activity per repository in report output
- Associate commits with their pull requests
- Support attribution override: `Requested by @USER in #CHANNEL.` in PR descriptions reassigns commits to the mentioned user
- Add Repository Activity section to report showing PRs per repo
- Group commits under their PRs in per-contributor sections

## 1.0.0 (2026-03-20)

- Initial release
- Python-based GitHub API collection (commit messages, files changed, line counts)
- Per-contributor grouping across all org repositories
- Configurable time period (default: 7 days)
- Markdown report formatting
- Rate limit handling with automatic retry
- Merge commit and bot account filtering
