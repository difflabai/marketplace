#!/usr/bin/env python3
"""
Format contribution JSON (from collect_contributions.py) into a markdown report.

Usage:
    python3 collect_contributions.py --org difflabai --days 7 | python3 format_report.py
    python3 format_report.py < contributions.json
    python3 format_report.py --input contributions.json
"""

import argparse
import json
import sys

MAX_COMMITS_PER_PR = 10
MAX_DIRECT_COMMITS = 15


def _format_commit_list(commits: list[dict], max_commits: int, prefix: str) -> list[str]:
    """Format a list of commits with deduplication and truncation."""
    commit_lines: list[str] = []
    seen_messages: set[str] = set()
    shown = 0
    for commit in commits:
        msg = commit["message"].strip()
        if msg and msg not in seen_messages:
            seen_messages.add(msg)
            commit_lines.append(f"{prefix}{msg}")
            shown += 1
            if shown >= max_commits:
                remaining = len(commits) - shown
                if remaining > 0:
                    commit_lines.append(f"{prefix}*… and {remaining} more commits*")
                break
    return commit_lines


def format_report(data: dict) -> str:
    """Convert contribution JSON into a markdown report."""
    lines: list[str] = []
    period = data["period"]
    org = data["organization"]

    start_date = period["start"][:10]
    end_date = period["end"][:10]

    lines.append(f"# Team Contributions Report")
    lines.append(f"**Organization:** {org}")
    lines.append(f"**Period:** {start_date} → {end_date} ({period['days']} days)")
    lines.append(f"**Active Repositories:** {data['active_repos']} / {data['total_repos']}")
    lines.append("")

    # Repository PR overview
    repo_summaries = data.get("repo_summaries", [])
    if any(r.get("prs") for r in repo_summaries):
        lines.append("## Repository Activity")
        lines.append("")
        for repo in repo_summaries:
            repo_prs = repo.get("prs", [])
            if not repo_prs:
                continue
            lines.append(f"### {repo['name']}")
            for pr in repo_prs:
                attr = ""
                if pr.get("attributed_to"):
                    attr = f" *(attributed to @{pr['attributed_to']})*"
                lines.append(f"- [PR #{pr['number']}]({pr['url']}): {pr['title']} — @{pr['author']}{attr}")
            lines.append("")

    contributors = data.get("contributors", {})

    if not contributors:
        lines.append("*No contributions found in this period.*")
        return "\n".join(lines)

    # Sort contributors by total commits descending
    sorted_contributors = sorted(
        contributors.items(),
        key=lambda x: x[1]["total_commits"],
        reverse=True,
    )

    # Per-contributor sections
    for login, info in sorted_contributors:
        name = info["name"]
        lines.append("---")
        lines.append("")
        lines.append(f"## {name} (@{login})")
        lines.append("")
        lines.append(
            f"**Summary:** {info['total_commits']} commits across "
            f"{info['repo_count']} {'repository' if info['repo_count'] == 1 else 'repositories'} "
            f"| +{info['total_additions']} / -{info['total_deletions']}"
        )
        lines.append("")

        # Sort repos by commit count descending
        sorted_repos = sorted(
            info["repos"].items(),
            key=lambda x: x[1]["commit_count"],
            reverse=True,
        )

        for repo_name, repo_data in sorted_repos:
            lines.append(f"### {repo_name}")
            lines.append(f"- **Commits:** {repo_data['commit_count']}")
            lines.append(f"- **Files changed:** {repo_data['files_changed_count']}")
            lines.append(
                f"- **Lines:** +{repo_data['total_additions']} / -{repo_data['total_deletions']}"
            )

            # List PRs with their commits
            prs = repo_data.get("prs", [])
            if prs:
                for pr in prs:
                    lines.append("")
                    lines.append(
                        f"#### [PR #{pr['number']}]({pr['url']}): {pr['title']}"
                    )
                    lines.append(
                        f"- **Lines:** +{pr['total_additions']} / -{pr['total_deletions']}"
                    )
                    lines.append("- **Commits:**")
                    lines.extend(_format_commit_list(pr["commits"], MAX_COMMITS_PER_PR, "  - "))

            # List direct commits (not associated with a PR)
            direct_commits = repo_data.get("direct_commits", [])
            if direct_commits:
                lines.append("")
                lines.append("#### Direct commits (no PR)")
                lines.extend(_format_commit_list(direct_commits, MAX_DIRECT_COMMITS, "- "))

            lines.append("")

    # Summary table
    lines.append("---")
    lines.append("")
    lines.append("## Organization Totals")
    lines.append("")
    lines.append("| Contributor | Commits | Repos | Lines Added | Lines Removed |")
    lines.append("|-------------|---------|-------|-------------|---------------|")

    total_commits = 0
    total_additions = 0
    total_deletions = 0
    total_repos_set: set[str] = set()

    for login, info in sorted_contributors:
        name = info["name"]
        lines.append(
            f"| @{login} ({name}) | {info['total_commits']} | {info['repo_count']} "
            f"| +{info['total_additions']} | -{info['total_deletions']} |"
        )
        total_commits += info["total_commits"]
        total_additions += info["total_additions"]
        total_deletions += info["total_deletions"]
        total_repos_set.update(info["repos"].keys())

    lines.append(
        f"| **Total** | **{total_commits}** | **{len(total_repos_set)}** "
        f"| **+{total_additions}** | **-{total_deletions}** |"
    )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format contribution JSON as markdown")
    parser.add_argument("--input", "-i", help="Input JSON file (default: stdin)")
    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    print(format_report(data))


if __name__ == "__main__":
    main()
