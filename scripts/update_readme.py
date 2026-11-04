#!/usr/bin/env python3
"""Render README.md and the stats cards from live GitHub data.

Placeholders in README.template.md:
  {{ MERGED_COUNT }}    "N merged upstream PRs", counted on repos owned by someone else
  {{ UPSTREAM_TABLE }}  one row per project: merged/open counts, focus, latest PR
  {{ OPEN_PRS }}        bullet list of open upstream PRs
  {{ UPDATED }}         today's date (UTC)

It also writes assets/stats.svg and assets/languages.svg.
Only the standard library is used, so the workflow needs no setup step.
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html import escape
from pathlib import Path, PurePosixPath

USER = os.environ.get("PROFILE_USER", "vaidikgarg-bit")
API = "https://api.github.com"
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "README.template.md"
OUTPUT = ROOT / "README.md"
ASSETS = ROOT / "assets"

# Repos grouped into the projects shown in the "Upstream work" table, in display order.
# A repo not listed here still shows up, as its own row with no focus text.
PROJECTS = [
    {
        "name": "Apache HugeGraph",
        "repos": ["apache/hugegraph", "apache/hugegraph-doc"],
        "focus": "Store module fixes: row hashing and dedup in scan iterators, "
                 "id-only projections, MultiListIterator cleanup, and the tests around them.",
    },
    {
        "name": "Apache Fineract back-office UI",
        "repos": ["apache/fineract-backoffice-ui"],
        "focus": "Angular screens: client dates, scheduler job editing, "
                 "SMS gateway setup, share dividend approval.",
    },
]

# Extension -> (language, colour), colours from GitHub's linguist palette.
LANGUAGES = {
    ".java": ("Java", "#b07219"),
    ".py": ("Python", "#3572A5"),
    ".ts": ("TypeScript", "#3178c6"),
    ".js": ("JavaScript", "#f1e05a"),
    ".mjs": ("JavaScript", "#f1e05a"),
    ".html": ("HTML", "#e34c26"),
    ".css": ("CSS", "#663399"),
    ".scss": ("SCSS", "#c6538c"),
    ".sh": ("Shell", "#89e051"),
    ".md": ("Markdown", "#083fa1"),
    ".yaml": ("YAML", "#cb171e"),
    ".yml": ("YAML", "#cb171e"),
}
OTHER = ("Other", "#8b949e")
# Lockfiles, data and translation files would swamp the real code.
SKIP_SUFFIXES = {".json", ".lock", ".xml", ".txt", ".csv", ".svg", ".png", ".jpg"}
MAX_LANGUAGES = 6

CARD_STYLE = """<style>
  .title { font: 600 18px 'Segoe UI', -apple-system, Ubuntu, sans-serif; fill: #58a6ff; }
  .label { font: 400 14px 'Segoe UI', -apple-system, Ubuntu, sans-serif; fill: #c9d1d9; }
  .value { font: 600 14px 'Segoe UI', -apple-system, Ubuntu, sans-serif; fill: #f0f6fc; }
</style>"""


def request(url, body=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": f"{USER}-profile-readme",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")[:300]
        sys.exit(f"{url} failed: {err.code} {detail}")


def get(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return request(url)


def search_all(query):
    # is:public keeps private work out even if the token can see it.
    q = f"{query} author:{USER} -user:{USER} is:public"
    items, page = [], 1
    while True:
        data = get("/search/issues", {"q": q, "sort": "created", "order": "desc",
                                      "per_page": 100, "page": page})
        items += data["items"]
        if len(items) >= data["total_count"] or not data["items"]:
            return items
        page += 1


def repo_of(item):
    # repository_url looks like https://api.github.com/repos/apache/hugegraph
    return item["repository_url"].split("/repos/", 1)[1]


def is_merged(pr):
    return bool(pr["pull_request"].get("merged_at"))


def cell(text):
    return text.replace("|", "\\|").replace("\n", " ").strip()


def pr_ref(pr):
    return f"{repo_of(pr)}#{pr['number']}"


def group_prs(prs):
    groups = [dict(p, prs=[]) for p in PROJECTS]
    by_repo = {repo: g for g in groups for repo in g["repos"]}
    for pr in prs:
        repo = repo_of(pr)
        if repo not in by_repo:
            group = {"name": repo, "repos": [repo], "focus": "", "prs": []}
            groups.append(group)
            by_repo[repo] = group
        by_repo[repo]["prs"].append(pr)
    return [g for g in groups if g["prs"]]


def render_table(groups):
    rows = ["| Project | PRs | Focus |", "| --- | --- | --- |"]
    for g in groups:
        merged = sum(is_merged(pr) for pr in g["prs"])
        open_ = sum(pr["state"] == "open" for pr in g["prs"])
        q = " ".join(["is:pr", f"author:{USER}"] + [f"repo:{r}" for r in g["repos"]])
        link = "https://github.com/pulls?" + urllib.parse.urlencode({"q": q})
        latest = g["prs"][0]  # search results are newest first
        focus = cell(g["focus"])
        note = (f'<sub>Latest: <a href="{latest["html_url"]}">#{latest["number"]}</a>'
                f' — {escape(cell(latest["title"]), quote=False)}</sub>')
        focus = f"{focus}<br>{note}" if focus else note
        rows.append(f"| [{g['name']}]({link}) | {merged} merged · {open_} open | {focus} |")
    return "\n".join(rows)


def render_open(prs):
    open_prs = [pr for pr in prs if pr["state"] == "open"]
    if not open_prs:
        return "_None right now._"
    return "\n".join(f"- [{pr_ref(pr)}]({pr['html_url']}) — {cell(pr['title'])}" for pr in open_prs)


def contributions_last_year():
    # The contribution calendar is only in GraphQL. Leave the row out if it can't be read.
    query = f'{{ user(login: "{USER}") {{ contributionsCollection {{ contributionCalendar {{ totalContributions }} }} }} }}'
    try:
        data = request(f"{API}/graphql", {"query": query})
        return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except (SystemExit, KeyError, TypeError):
        return None


def language_of(filename):
    path = PurePosixPath(filename)
    suffix = path.suffix.lower()
    if suffix in SKIP_SUFFIXES:
        return None
    return LANGUAGES.get(suffix, OTHER)


def language_totals(prs):
    """Changed lines per language across merged and open PRs."""
    totals, colours = Counter(), {}
    for pr in prs:
        if pr["state"] == "closed" and not is_merged(pr):
            continue
        page = 1
        while True:
            files = get(f"/repos/{repo_of(pr)}/pulls/{pr['number']}/files",
                        {"per_page": 100, "page": page})
            for f in files:
                lang = language_of(f["filename"])
                if lang and f["changes"]:
                    totals[lang[0]] += f["changes"]
                    colours[lang[0]] = lang[1]
            if len(files) < 100:
                break
            page += 1
    return totals, colours


def card(width, height, title, body):
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        CARD_STYLE,
        # A solid background keeps the card readable in both GitHub themes.
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="6" fill="#0d1117" stroke="#30363d"/>',
        f'<text x="25" y="35" class="title">{escape(title)}</text>',
        *body,
        "</svg>",
    ]) + "\n"


def stats_svg(rows):
    body = []
    for i, (label, value) in enumerate(rows):
        y = 70 + 28 * i
        body.append(f'<text x="25" y="{y}" class="label">{escape(label)}</text>')
        body.append(f'<text x="375" y="{y}" class="value" text-anchor="end">{value:,}</text>')
    return card(400, 64 + 28 * len(rows), "Upstream contributions", body)


def languages_svg(totals, colours):
    width, bar_x, bar_w = 445, 25, 395
    top = totals.most_common(MAX_LANGUAGES)
    rest = sum(totals.values()) - sum(n for _, n in top)
    if rest:
        top.append((OTHER[0], rest))
        colours[OTHER[0]] = OTHER[1]
    total = sum(n for _, n in top) or 1
    body = [f'<clipPath id="bar"><rect x="{bar_x}" y="52" width="{bar_w}" height="8" rx="4"/></clipPath>',
            '<g clip-path="url(#bar)">']
    x = bar_x
    for name, n in top:
        w = bar_w * n / total
        body.append(f'<rect x="{x:.2f}" y="52" width="{w:.2f}" height="8" fill="{colours[name]}"/>')
        x += w
    body.append("</g>")
    for i, (name, n) in enumerate(top):
        col, row = i % 2, i // 2
        cx, cy = 30 + 200 * col, 83 + 26 * row
        body.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{colours[name]}"/>')
        body.append(f'<text x="{cx + 12}" y="{cy + 5}" class="label">{escape(name)} '
                    f'<tspan class="value">{100 * n / total:.1f}%</tspan></text>')
    rows = (len(top) + 1) // 2
    return card(width, max(110, 70 + 26 * rows), "Languages in my PRs", body)


def main():
    prs = search_all("type:pr")
    issues = search_all("type:issue")
    merged = sum(is_merged(pr) for pr in prs)
    open_count = sum(pr["state"] == "open" for pr in prs)
    groups = group_prs(prs)

    rows = [
        ("PRs merged", merged),
        ("PRs open", open_count),
        ("Projects contributed to", len(groups)),
        ("Issues reported", len(issues)),
    ]
    contributions = contributions_last_year()
    if contributions is not None:
        rows.append(("Contributions in the last year", contributions))

    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "stats.svg").write_text(stats_svg(rows), encoding="utf-8")
    (ASSETS / "languages.svg").write_text(languages_svg(*language_totals(prs)), encoding="utf-8")

    values = {
        "{{ MERGED_COUNT }}": f"{merged} merged upstream PR{'' if merged == 1 else 's'}",
        "{{ UPSTREAM_TABLE }}": render_table(groups) if groups else "_Nothing yet._",
        "{{ OPEN_PRS }}": render_open(prs),
        "{{ UPDATED }}": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    }
    text = TEMPLATE.read_text(encoding="utf-8")
    for marker, value in values.items():
        text = text.replace(marker, value)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} and assets/*.svg")


if __name__ == "__main__":
    main()
