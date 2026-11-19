import json
import os
from collections import defaultdict
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER = os.environ.get("GITHUB_USER", "mahdidou711")
TOKEN = os.environ.get("PROFILE_STATS_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
API = "https://api.github.com"
GRAPHQL_API = "https://api.github.com/graphql"
OUTPUT = Path("profile")

EXCLUDED_REPOSITORIES = {
    "mahdidou711",
    "mahdidou711.github.io",
    "polynomial-regression-mlp",
    "lloyd-kmeans",
    "svm-margin-kernel-digits-study",
    "iaq-dashboard-v2",
}

LANG_COLORS = {
    "C": "#555555",
    "C++": "#f34b7d",
    "Python": "#3572A5",
    "VHDL": "#adb2cb",
    "Assembly": "#6E4C13",
    "Tcl": "#e4cc98",
    "Makefile": "#427819",
    "CMake": "#DA3434",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Verilog": "#b2b7f8",
    "SystemVerilog": "#DAE1C2",
}

FONT_FAMILY = "Segoe UI, Ubuntu, -apple-system, BlinkMacSystemFont, sans-serif"

OVERVIEW_QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
      }
    }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""


def api_headers(extra=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    if extra:
        headers.update(extra)
    return headers


def api_get(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers=api_headers())
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def api_graphql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = Request(
        GRAPHQL_API,
        data=payload,
        headers=api_headers({"Content-Type": "application/json"}),
        method="POST",
    )
    with urlopen(req, timeout=30) as response:
        data = json.load(response)
    if data.get("errors"):
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def get_public_repos():
    repos = []
    page = 1
    while True:
        batch = api_get(
            f"/users/{USER}/repos",
            {"type": "owner", "sort": "updated", "per_page": 100, "page": page},
        )
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_normalized_languages(repos):
    weights = defaultdict(float)
    core_repo_count = 0

    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        if repo.get("name") in EXCLUDED_REPOSITORIES:
            continue
        try:
            languages = api_get(f"/repos/{USER}/{repo['name']}/languages")
        except (HTTPError, URLError, TimeoutError):
            continue

        repo_total = sum(int(count) for count in languages.values())
        if repo_total <= 0:
            continue

        core_repo_count += 1
        for language, byte_count in languages.items():
            weights[language] += int(byte_count) / repo_total

    return dict(weights), core_repo_count


def get_overview_stats(public_repos, core_repo_count):
    owned_public_non_fork = [
        r for r in public_repos if not r.get("fork") and not r.get("archived")
    ]
    stats = {
        "contributions_12m": None,
        "commits_12m": None,
        "public_repos": len(owned_public_non_fork),
        "core_repos": core_repo_count,
    }

    if not TOKEN:
        return stats

    try:
        data = api_graphql(OVERVIEW_QUERY, {"login": USER})
        user_data = data.get("user") or {}
        contrib = user_data.get("contributionsCollection") or {}
        calendar = contrib.get("contributionCalendar") or {}
        repos_data = user_data.get("repositories") or {}

        if calendar.get("totalContributions") is not None:
            stats["contributions_12m"] = int(calendar["totalContributions"])
        if contrib.get("totalCommitContributions") is not None:
            stats["commits_12m"] = int(contrib["totalCommitContributions"])
        if repos_data.get("totalCount") is not None:
            stats["public_repos"] = int(repos_data["totalCount"])
    except (HTTPError, URLError, TimeoutError, RuntimeError):
        pass

    return stats


def fmt_int(value):
    if value is None:
        return "N/A"
    return f"{value:,}"


def write_overview_svg(stats):
    rows_data = [
        ("#3fb950", "Contributions (last 12 months)", fmt_int(stats["contributions_12m"])),
        ("#58a6ff", "Public Commits (last 12 months)", fmt_int(stats["commits_12m"])),
        ("#d29922", "Public Repositories", fmt_int(stats["public_repos"])),
        ("#a371f7", "Core Embedded / FPGA / Systems Repos", fmt_int(stats["core_repos"])),
    ]

    row_parts = []
    y_start = 74
    y_step = 28
    for idx, (dot_color, label, value) in enumerate(rows_data):
        y = y_start + idx * y_step
        row_parts.append(
            f'<circle cx="30" cy="{y - 4}" r="4.5" fill="{dot_color}"/>\n'
            f'  <text x="44" y="{y}" fill="#c9d1d9" font-family="{FONT_FAMILY}" font-size="13">{escape(label)}</text>\n'
            f'  <text x="446" y="{y}" text-anchor="end" fill="#f0f6fc" font-family="{FONT_FAMILY}" font-size="13" font-weight="600">{escape(value)}</text>'
        )

    rows_svg = "\n  ".join(row_parts)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="470" height="195" viewBox="0 0 470 195" role="img" aria-label="GitHub overview statistics for {escape(USER)}">
  <rect width="469" height="194" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="38" fill="#58a6ff" font-family="{FONT_FAMILY}" font-size="18" font-weight="600">GitHub Overview</text>
  <line x1="24" y1="50" x2="446" y2="50" stroke="#21262d" stroke-width="1"/>
  {rows_svg}
  <text x="24" y="184" fill="#6e7681" font-family="{FONT_FAMILY}" font-size="10">FPGA/RTL · Processor Architecture · Embedded Systems</text>
</svg>
'''
    (OUTPUT / "overview.svg").write_text(svg, encoding="utf-8")


def write_languages_svg(weights):
    ranked = sorted(weights.items(), key=lambda item: (-item[1], item[0]))
    top = ranked[:6]
    total_weight = sum(weights.values())

    if total_weight <= 0 or not top:
        bar = '<rect x="24" y="58" width="422" height="9" rx="4.5" fill="#21262d"/>'
        rows = f'<text x="24" y="98" fill="#8b949e" font-family="{FONT_FAMILY}" font-size="13">No public language data available.</text>'
    else:
        bar_width = 422.0
        bar_parts = []
        x = 24.0
        for language, value in top:
            width = bar_width * value / total_weight
            color = LANG_COLORS.get(language, "#8b949e")
            bar_parts.append(
                f'<rect x="{x:.2f}" y="58" width="{width:.2f}" height="9" fill="{color}"/>'
            )
            x += width

        remaining = (24.0 + bar_width) - x
        if remaining > 0.2:
            bar_parts.append(
                f'<rect x="{x:.2f}" y="58" width="{remaining:.2f}" height="9" fill="#30363d"/>'
            )

        bar_segments = "\n    ".join(bar_parts)
        bar = (
            '<defs>\n'
            '    <clipPath id="lang-bar-clip">\n'
            '      <rect x="24" y="58" width="422" height="9" rx="4.5" ry="4.5"/>\n'
            '    </clipPath>\n'
            '  </defs>\n'
            '  <rect x="24" y="58" width="422" height="9" rx="4.5" fill="#21262d"/>\n'
            '  <g clip-path="url(#lang-bar-clip)">\n'
            f'    {bar_segments}\n'
            '  </g>'
        )

        row_parts = []
        positions = [(24, 99), (245, 99), (24, 130), (245, 130), (24, 161), (245, 161)]
        for (language, value), (x0, y0) in zip(top, positions):
            pct = 100.0 * value / total_weight
            color = LANG_COLORS.get(language, "#8b949e")
            row_parts.append(
                f'<circle cx="{x0 + 6}" cy="{y0 - 4}" r="5" fill="{color}"/>\n'
                f'  <text x="{x0 + 19}" y="{y0}" fill="#c9d1d9" font-family="{FONT_FAMILY}" font-size="12">{escape(language)} {pct:.1f}%</text>'
            )
        rows = "\n  ".join(row_parts)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="470" height="195" viewBox="0 0 470 195" role="img" aria-label="Normalized languages across core engineering repositories">
  <rect width="469" height="194" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="38" fill="#58a6ff" font-family="{FONT_FAMILY}" font-size="18" font-weight="600">Top Languages</text>
  {bar}
  {rows}
  <text x="24" y="184" fill="#6e7681" font-family="{FONT_FAMILY}" font-size="10">Core embedded/FPGA/systems repos · normalized per repo</text>
</svg>
'''
    (OUTPUT / "top-langs.svg").write_text(svg, encoding="utf-8")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    repos = get_public_repos()
    weights, core_repo_count = get_normalized_languages(repos)
    stats = get_overview_stats(repos, core_repo_count)
    write_overview_svg(stats)
    write_languages_svg(weights)


if __name__ == "__main__":
    main()
