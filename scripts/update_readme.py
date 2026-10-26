#!/usr/bin/env python3
"""Render README.md from README.template.md using live GitHub data.

Placeholders in the template:
  {{ MERGED_COUNT }}        "N merged upstream PRs", counted on repos owned by someone else
  {{ OPEN_SOURCE_PRS }}     pull requests to repos owned by someone else, with status
  {{ OPEN_SOURCE_ISSUES }}  issues opened on repos owned by someone else
  {{ PROJECTS }}            my own public, non-fork repositories

Only the standard library is used, so the workflow needs no setup step.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "vaidikgarg-bit")
API = "https://api.github.com"
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.md"
MAX_PRS = 10
MAX_ISSUES = 5
MAX_PROJECTS = 6

BADGES = {
    "merged": "![merged](https://img.shields.io/badge/merged-8250df?style=flat-square)",
    "approved": "![approved](https://img.shields.io/badge/approved-1a7f37?style=flat-square)",
    "changes requested": "![changes requested](https://img.shields.io/badge/changes_requested-cf222e?style=flat-square)",
    "open": "![open](https://img.shields.io/badge/open-2da44e?style=flat-square)",
    "draft": "![draft](https://img.shields.io/badge/draft-6e7781?style=flat-square)",
    "closed": "![closed](https://img.shields.io/badge/closed-6e7781?style=flat-square)",
}


def get(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"{USER}-profile-readme",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        body = err.read().decode(errors="replace")[:300]
        sys.exit(f"GET {url} failed: {err.code} {body}")


def search(query, limit):
    # is:public keeps private work out even if the token can see it.
    q = f"{query} author:{USER} -user:{USER} is:public"
    data = get("/search/issues", {"q": q, "sort": "created", "order": "desc", "per_page": limit})
    return data["items"]


def repo_name(item):
    # repository_url looks like https://api.github.com/repos/apache/hugegraph
    return item["repository_url"].split("/repos/", 1)[1]


def pr_status(item):
    if item["pull_request"].get("merged_at"):
        return "merged"
    if item["state"] == "closed":
        return "closed"
    if item.get("draft"):
        return "draft"
    reviews = get(f"/repos/{repo_name(item)}/pulls/{item['number']}/reviews", {"per_page": 100})
    # A reviewer's latest approve/request-changes review is the one that counts.
    latest = {}
    for review in reviews:
        if review["state"] in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[review["user"]["login"]] = review["state"]
    states = set(latest.values())
    if "CHANGES_REQUESTED" in states:
        return "changes requested"
    if "APPROVED" in states:
        return "approved"
    return "open"


def cell(text):
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render_prs():
    items = search("type:pr", MAX_PRS)
    if not items:
        return "_Nothing yet._"
    rows = ["| Pull request | Repository | Status |", "| --- | --- | --- |"]
    for item in items:
        repo = repo_name(item)
        rows.append(
            f"| [{cell(item['title'])}]({item['html_url']}) "
            f"| [{repo}](https://github.com/{repo}) "
            f"| {BADGES[pr_status(item)]} |"
        )
    return "\n".join(rows)


def render_merged_count():
    q = f"type:pr is:merged author:{USER} -user:{USER} is:public"
    count = get("/search/issues", {"q": q, "per_page": 1})["total_count"]
    return f"{count} merged upstream PR{'' if count == 1 else 's'}"


def render_issues():
    items = search("type:issue", MAX_ISSUES)
    if not items:
        return "_Nothing yet._"
    lines = []
    for item in items:
        repo = repo_name(item)
        lines.append(f"- [{cell(item['title'])}]({item['html_url']}) in `{repo}` ({item['state']})")
    return "\n".join(lines)


def render_projects():
    repos = get(f"/users/{USER}/repos", {"type": "owner", "sort": "pushed", "per_page": 100})
    repos = [r for r in repos if not r["fork"] and not r["private"] and r["name"] != USER]
    if not repos:
        return "_Nothing public yet._"
    lines = []
    for repo in repos[:MAX_PROJECTS]:
        line = f"- [{repo['name']}]({repo['html_url']})"
        if repo.get("description"):
            line += f": {cell(repo['description'])}"
        if repo.get("language"):
            line += f" `{repo['language']}`"
        lines.append(line)
    return "\n".join(lines)


def main():
    text = TEMPLATE.read_text(encoding="utf-8")
    sections = {
        "{{ MERGED_COUNT }}": render_merged_count,
        "{{ OPEN_SOURCE_PRS }}": render_prs,
        "{{ OPEN_SOURCE_ISSUES }}": render_issues,
        "{{ PROJECTS }}": render_projects,
    }
    for marker, render in sections.items():
        if marker in text:
            text = text.replace(marker, render())
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
