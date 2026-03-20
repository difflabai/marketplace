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

MAX_COMMITS_PER_REPO = 15


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
            lines.append("- **Key changes:**")

            # List commit messages (deduplicated, max 15 per repo)
            seen_messages = set()
            shown = 0
            for commit in repo_data["commits"]:
                msg = commit["message"].strip()
                if msg and msg not in seen_messages:
                    seen_messages.add(msg)
                    lines.append(f"  - {msg}")
                    shown += 1
                    if shown >= MAX_COMMITS_PER_REPO:
                        remaining = len(repo_data["commits"]) - shown
                        if remaining > 0:
                            lines.append(f"  - *… and {remaining} more commits*")
                        break

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
