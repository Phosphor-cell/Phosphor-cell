#!/usr/bin/env python3
"""
Generate custom GitHub stats SVG for the profile README.

Queries the GitHub API for the authenticated user's stats and emits
.github/assets/stats.svg in the same warm-amber-on-dark aesthetic as
the rest of the profile.

Run locally:    python tools/generate_stats.py
Run from CI:    .github/workflows/stats.yml invokes this daily.

Requires environment variable:
    GITHUB_TOKEN — a GitHub token with public_repo read access.
                    In CI this is provided automatically as secrets.GITHUB_TOKEN.

Output: .github/assets/stats.svg
"""

import os
import sys
import json
import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER = "Phosphor-cell"   # update if username changes
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, ".github", "assets", "stats.svg")


def gh_request(query: str) -> dict:
    """Run a GraphQL query against the GitHub API."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("error: GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    req = Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{USER}-profile-stats",
        },
    )

    try:
        with urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except HTTPError as e:
        print(f"http error: {e.code} {e.reason}", file=sys.stderr)
        print(e.read().decode(), file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"url error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def fetch_stats() -> dict:
    """Collect total commits, PRs, issues, stars, and language usage."""
    query = """
    query {
      user(login: "%s") {
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalPullRequestReviewContributions
          contributionCalendar {
            totalContributions
          }
        }
        repositories(first: 100, ownerAffiliations: OWNER, isFork: false, orderBy: {field: STARGAZERS, direction: DESC}) {
          totalCount
          nodes {
            stargazerCount
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node { name color }
              }
            }
          }
        }
      }
    }
    """ % USER

    data = gh_request(query)
    if "errors" in data:
        print("graphql errors:", data["errors"], file=sys.stderr)
        sys.exit(1)

    user = data["data"]["user"]
    contrib = user["contributionsCollection"]
    repos = user["repositories"]["nodes"]

    # Aggregate per-language byte sizes across all owned repos.
    # Excludes a few that skew the picture (CSS, HTML in particular —
    # these dominate when you commit generated docs but don't reflect
    # what you "do").
    EXCLUDE = {"HTML", "CSS", "SCSS", "TeX", "Roff"}
    lang_bytes: dict[str, int] = {}
    lang_colors: dict[str, str] = {}
    total_stars = 0

    for repo in repos:
        total_stars += repo["stargazerCount"]
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            if name in EXCLUDE:
                continue
            lang_bytes[name] = lang_bytes.get(name, 0) + edge["size"]
            lang_colors[name] = edge["node"]["color"] or "#888888"

    # Sort languages by byte size, keep top 5.
    sorted_langs = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:5]
    total = sum(b for _, b in sorted_langs) or 1
    languages = [
        {
            "name": name,
            "pct": 100.0 * b / total,
            "color": lang_colors[name],
        }
        for name, b in sorted_langs
    ]

    return {
        "commits": contrib["totalCommitContributions"],
        "prs": contrib["totalPullRequestContributions"],
        "issues": contrib["totalIssueContributions"],
        "reviews": contrib["totalPullRequestReviewContributions"],
        "total_contribs": contrib["contributionCalendar"]["totalContributions"],
        "stars": total_stars,
        "repos": user["repositories"]["totalCount"],
        "languages": languages,
    }


def render(stats: dict) -> str:
    """Emit the SVG. Matches the visual language of the profile."""

    # Build the language bar (horizontal stacked segments).
    # Total width of the bar: 770px, starts at x=80.
    bar_x = 80
    bar_y = 175
    bar_w = 740
    bar_h = 8

    segments = []
    legend = []
    cursor = bar_x
    for i, lang in enumerate(stats["languages"]):
        seg_w = bar_w * (lang["pct"] / 100.0)
        rx = "3" if i == 0 else "0"
        segments.append(
            f'<rect x="{cursor:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="{bar_h}" '
            f'fill="{lang["color"]}" opacity="0.85"/>'
        )
        cursor += seg_w

    # Legend below the bar — wraps if needed; we keep it on one line for 5 items
    legend_x = bar_x
    for lang in stats["languages"]:
        # Small color dot + name + percentage
        legend.append(
            f'<circle cx="{legend_x + 5}" cy="200" r="3.5" fill="{lang["color"]}" opacity="0.85"/>'
            f'<text x="{legend_x + 15}" y="204" font-family="JetBrains Mono, monospace" '
            f'font-size="10" fill="#a8a098">'
            f'{lang["name"]} '
            f'<tspan fill="#5a5249">{lang["pct"]:.0f}%</tspan>'
            f'</text>'
        )
        legend_x += len(lang["name"]) * 7 + 50    # rough estimate of width

    segments_svg = "\n  ".join(segments)
    legend_svg = "\n  ".join(legend)

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 240" width="900" height="240" role="img" aria-label="GitHub stats for {USER}">
  <defs>
    <linearGradient id="bg-stats" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d0e10"/>
      <stop offset="100%" stop-color="#13151a"/>
    </linearGradient>
    <linearGradient id="acc-stats" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c89858"/>
      <stop offset="100%" stop-color="#b88848"/>
    </linearGradient>
    <pattern id="grid-stats" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1f2126" stroke-width="0.5"/>
    </pattern>
  </defs>

  <rect width="900" height="240" fill="url(#bg-stats)" rx="6"/>
  <rect width="900" height="240" fill="url(#grid-stats)" opacity="0.4"/>

  <text x="30" y="32" font-family="JetBrains Mono, monospace" font-size="10" fill="#5a5249" letter-spacing="2">
    GITHUB ACTIVITY · LAST 12 MONTHS · UPDATED {today.upper()}
  </text>
  <line x1="30" y1="42" x2="870" y2="42" stroke="#2a2d34" stroke-width="1"/>

  <!-- Four stat cells across the top -->
  <g font-family="JetBrains Mono, monospace">
    <g transform="translate(30, 60)">
      <text x="0" y="14" font-size="9" fill="#5a5249" letter-spacing="1.5">COMMITS</text>
      <text x="0" y="48" font-size="32" fill="url(#acc-stats)" font-weight="500">{stats['commits']:,}</text>
    </g>
    <g transform="translate(240, 60)">
      <text x="0" y="14" font-size="9" fill="#5a5249" letter-spacing="1.5">PULL REQUESTS</text>
      <text x="0" y="48" font-size="32" fill="url(#acc-stats)" font-weight="500">{stats['prs']:,}</text>
    </g>
    <g transform="translate(450, 60)">
      <text x="0" y="14" font-size="9" fill="#5a5249" letter-spacing="1.5">STARS EARNED</text>
      <text x="0" y="48" font-size="32" fill="url(#acc-stats)" font-weight="500">{stats['stars']:,}</text>
    </g>
    <g transform="translate(660, 60)">
      <text x="0" y="14" font-size="9" fill="#5a5249" letter-spacing="1.5">REPOSITORIES</text>
      <text x="0" y="48" font-size="32" fill="url(#acc-stats)" font-weight="500">{stats['repos']:,}</text>
    </g>
  </g>

  <!-- Secondary row: issues, reviews, total contribs -->
  <g font-family="JetBrains Mono, monospace" font-size="11" fill="#8b8275">
    <text x="30"  y="135"><tspan fill="#5a5249">issues opened</tspan><tspan dx="8" fill="#e8dcc8">{stats['issues']:,}</tspan></text>
    <text x="240" y="135"><tspan fill="#5a5249">PRs reviewed</tspan><tspan dx="8" fill="#e8dcc8">{stats['reviews']:,}</tspan></text>
    <text x="450" y="135"><tspan fill="#5a5249">total contributions</tspan><tspan dx="8" fill="#e8dcc8">{stats['total_contribs']:,}</tspan></text>
  </g>

  <!-- Language breakdown -->
  <text x="30" y="165" font-family="JetBrains Mono, monospace" font-size="10" fill="#5a5249" letter-spacing="1.5">
    LANGUAGES
  </text>

  <!-- Background of the language bar -->
  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="#1a1c20" stroke="#2a2d34" stroke-width="0.5"/>
  {segments_svg}

  <!-- Language legend -->
  {legend_svg}

  <!-- Right edge accent -->
  <rect x="897" y="20" width="3" height="200" fill="url(#acc-stats)" opacity="0.3"/>
</svg>
"""


def main():
    stats = fetch_stats()
    svg = render(stats)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(svg)

    print(f"wrote {OUTPUT}")
    print(f"  commits: {stats['commits']:,}")
    print(f"  prs: {stats['prs']:,}")
    print(f"  stars: {stats['stars']:,}")
    print(f"  repos: {stats['repos']:,}")
    print(f"  top languages: {', '.join(l['name'] for l in stats['languages'])}")


if __name__ == "__main__":
    main()
