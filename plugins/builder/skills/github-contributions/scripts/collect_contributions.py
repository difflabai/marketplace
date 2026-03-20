#!/usr/bin/env python3
"""
Collect GitHub contributions across an organization's repositories.

Queries the GitHub API for all repos with activity in a given time period,
then collects commit history grouped by author. Outputs structured JSON.

Usage:
    python3 collect_contributions.py --org difflabai --days 7
    python3 collect_contributions.py --org difflabai --days 30 --include-merges
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import requests

# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

API_BASE = "https://api.github.com"
PER_PAGE = 100


def get_token() -> str:
    """Resolve a GitHub token from env or gh CLI."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: No GITHUB_TOKEN set and 'gh auth token' failed.", file=sys.stderr)
        sys.exit(1)


def make_session(token: str) -> requests.Session:
    sess = requests.Session()
    sess.headers.update(
        {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )
    return sess


def api_get(sess: requests.Session, url: str, params: Optional[dict] = None) -> Any:
    """GET with pagination and rate-limit handling."""
    results: list[Any] = []
    params = dict(params or {})
    params.setdefault("per_page", PER_PAGE)

    while url:
        resp = sess.get(url, params=params)

        # Rate-limit back-off
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset - int(time.time()), 1) + 1
            print(f"Rate limited — waiting {wait}s …", file=sys.stderr)
            time.sleep(wait)
            continue

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            print(f"429 — retrying in {retry_after}s …", file=sys.stderr)
            time.sleep(retry_after)
            continue

        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list):
            results.extend(data)
        else:
            return data  # single-object endpoint

        # Follow pagination
        url = resp.links.get("next", {}).get("url")
        params = {}  # params already encoded in next URL

    return results


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


def list_org_repos(sess: requests.Session, org: str) -> list[dict]:
    """List all repos in an org."""
    return api_get(sess, f"{API_BASE}/orgs/{org}/repos", {"type": "all", "sort": "pushed", "direction": "desc"})


def get_commits(
    sess: requests.Session,
    owner: str,
    repo: str,
    since: str,
    until: str,
    include_merges: bool = False,
) -> list[dict]:
    """Get commits for a repo within the time window."""
    commits = api_get(
        sess,
        f"{API_BASE}/repos/{owner}/{repo}/commits",
        {"since": since, "until": until, "per_page": PER_PAGE},
    )
    if not include_merges:
        commits = [c for c in commits if len(c.get("parents", [])) <= 1]
    return commits


def get_commit_detail(sess: requests.Session, owner: str, repo: str, sha: str) -> dict:
    """Get detailed commit info including file stats."""
    return api_get(sess, f"{API_BASE}/repos/{owner}/{repo}/commits/{sha}")


def collect(org: str, days: int, include_merges: bool = False, quiet: bool = False) -> dict:
    """Main collection routine."""
    token = get_token()
    sess = make_session(token)

    def log(msg: str) -> None:
        if not quiet:
            print(msg, file=sys.stderr)

    now = datetime.now(timezone.utc)
    since_dt = now - timedelta(days=days)
    since_iso = since_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    until_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    log(f"Collecting contributions for {org} ({days} days) …")

    repos = list_org_repos(sess, org)
    log(f"Found {len(repos)} repositories")

    # Filter to repos pushed within the window
    active_repos = []
    for r in repos:
        pushed = r.get("pushed_at", "")
        if pushed >= since_iso:
            active_repos.append(r)

    log(f"{len(active_repos)} repositories with recent activity")

    # Collect per-contributor data
    contributors: dict[str, dict] = {}  # login -> {name, repos: {repo: {commits, files, +, -}}}
    repo_summaries: list[dict] = []

    for repo_info in active_repos:
        repo_name = repo_info["name"]
        owner = repo_info["owner"]["login"]
        log(f"  Scanning {owner}/{repo_name} …")

        try:
            commits = get_commits(sess, owner, repo_name, since_iso, until_iso, include_merges)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 409:
                # Empty repository
                continue
            raise

        if not commits:
            continue

        repo_contributors: dict[str, dict] = {}

        for commit_summary in commits:
            author_login = (commit_summary.get("author") or {}).get("login", "unknown")
            author_name = (
                (commit_summary.get("commit", {}).get("author") or {}).get("name", author_login)
            )

            # Skip bots — check both login and commit author name
            if (
                author_login.endswith("[bot]")
                or author_name.endswith("[bot]")
                or author_login.lower() in ("dependabot", "copilot", "renovate")
            ):
                continue

            # Get detailed stats (N+1 API calls — one per commit. This is a
            # known limitation; for very large orgs this may be slow or hit rate
            # limits. The REST API does not offer a batch endpoint for commit details.)
            try:
                detail = get_commit_detail(sess, owner, repo_name, commit_summary["sha"])
            except requests.HTTPError as e:
                print(f"Warning: Failed to fetch details for commit {commit_summary['sha']}: {e}", file=sys.stderr)
                continue

            stats = detail.get("stats", {})
            files = detail.get("files", [])
            message = detail.get("commit", {}).get("message", "").split("\n")[0]  # first line

            # File info (name + changes only, no patches)
            file_list = [
                {
                    "filename": f["filename"],
                    "status": f.get("status", "modified"),
                    "additions": f.get("additions", 0),
                    "deletions": f.get("deletions", 0),
                    "changes": f.get("changes", 0),
                }
                for f in files
            ]

            # Aggregate per-contributor per-repo
            if author_login not in repo_contributors:
                repo_contributors[author_login] = {
                    "name": author_name,
                    "commits": [],
                    "total_additions": 0,
                    "total_deletions": 0,
                    "files_changed": set(),
                }

            entry = repo_contributors[author_login]
            entry["commits"].append(
                {
                    "sha": commit_summary["sha"][:8],
                    "message": message,
                    "date": (detail.get("commit", {}).get("author") or {}).get("date", ""),
                    "additions": stats.get("additions", 0),
                    "deletions": stats.get("deletions", 0),
                    "files": file_list,
                }
            )
            entry["total_additions"] += stats.get("additions", 0)
            entry["total_deletions"] += stats.get("deletions", 0)
            for f in file_list:
                entry["files_changed"].add(f["filename"])

        # Roll up into contributors dict
        for login, data in repo_contributors.items():
            if login not in contributors:
                contributors[login] = {"name": data["name"], "repos": {}}
            contributors[login]["repos"][repo_name] = {
                "commits": data["commits"],
                "commit_count": len(data["commits"]),
                "total_additions": data["total_additions"],
                "total_deletions": data["total_deletions"],
                "files_changed_count": len(data["files_changed"]),
                "files_changed": sorted(data["files_changed"]),
            }

        repo_summaries.append(
            {
                "name": repo_name,
                "contributor_count": len(repo_contributors),
                "total_commits": sum(len(d["commits"]) for d in repo_contributors.values()),
            }
        )

    # Build final output
    output = {
        "organization": org,
        "period": {"start": since_iso, "end": until_iso, "days": days},
        "active_repos": len(repo_summaries),
        "total_repos": len(repos),
        "repo_summaries": repo_summaries,
        "contributors": {},
    }

    for login, data in contributors.items():
        total_commits = sum(r["commit_count"] for r in data["repos"].values())
        total_additions = sum(r["total_additions"] for r in data["repos"].values())
        total_deletions = sum(r["total_deletions"] for r in data["repos"].values())
        output["contributors"][login] = {
            "name": data["name"],
            "total_commits": total_commits,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "repo_count": len(data["repos"]),
            "repos": data["repos"],
        }

    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Collect GitHub org contributions")
    parser.add_argument("--org", required=True, help="GitHub organization name")
    parser.add_argument("--days", type=int, default=7, help="Look-back period in days (default: 7)")
    parser.add_argument("--include-merges", action="store_true", help="Include merge commits")
    parser.add_argument("--output", "-o", help="Write JSON to file instead of stdout")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages on stderr")
    args = parser.parse_args()

    result = collect(args.org, args.days, args.include_merges, quiet=args.quiet)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, default=str)
            f.write("\n")
        if not args.quiet:
            print(f"Output written to {args.output}", file=sys.stderr)
    else:
        json.dump(result, sys.stdout, indent=2, default=str)
        print()  # trailing newline


if __name__ == "__main__":
    main()
