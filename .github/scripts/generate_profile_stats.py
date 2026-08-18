import json
import os
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER = os.environ.get("GITHUB_USER", "mahdidou711")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
OUTPUT = Path("profile")

LANG_COLORS = {
    "C": "#555555",
    "C++": "#f34b7d",
    "Python": "#3572A5",
    "VHDL": "#adb2cb",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "JavaScript": "#f1e05a",
    "Makefile": "#427819",
    "CMake": "#DA3434",
}


def api_get(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.load(response)


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


def get_languages(repos):
    totals = Counter()
    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        try:
            languages = api_get(f"/repos/{USER}/{repo['name']}/languages")
        except (HTTPError, URLError, TimeoutError):
            continue
        for language, byte_count in languages.items():
            if language.lower() == "typescript":
                continue
            totals[language] += int(byte_count)
    return totals


def write_stats_svg(user, repos):
    owned = [r for r in repos if not r.get("fork")]
    public_repos = int(user.get("public_repos", len(repos)))
    stars = sum(int(r.get("stargazers_count", 0)) for r in owned)
    forks = sum(int(r.get("forks_count", 0)) for r in owned)
    followers = int(user.get("followers", 0))
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="470" height="195" viewBox="0 0 470 195" role="img" aria-label="GitHub public profile stats">
  <rect width="469" height="194" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="38" fill="#58a6ff" font-family="Segoe UI, Ubuntu, sans-serif" font-size="18" font-weight="600">{escape(USER)}'s GitHub</text>
  <text x="24" y="66" fill="#8b949e" font-family="Segoe UI, Ubuntu, sans-serif" font-size="12">Public repositories only</text>

  <text x="24" y="105" fill="#c9d1d9" font-family="Segoe UI, Ubuntu, sans-serif" font-size="22" font-weight="600">{public_repos}</text>
  <text x="24" y="124" fill="#8b949e" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11">Public repos</text>

  <text x="137" y="105" fill="#c9d1d9" font-family="Segoe UI, Ubuntu, sans-serif" font-size="22" font-weight="600">{stars}</text>
  <text x="137" y="124" fill="#8b949e" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11">Stars earned</text>

  <text x="250" y="105" fill="#c9d1d9" font-family="Segoe UI, Ubuntu, sans-serif" font-size="22" font-weight="600">{forks}</text>
  <text x="250" y="124" fill="#8b949e" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11">Forks</text>

  <text x="360" y="105" fill="#c9d1d9" font-family="Segoe UI, Ubuntu, sans-serif" font-size="22" font-weight="600">{followers}</text>
  <text x="360" y="124" fill="#8b949e" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11">Followers</text>

  <text x="24" y="158" fill="#c9d1d9" font-family="Segoe UI, Ubuntu, sans-serif" font-size="12">Embedded Systems · FPGA · Autonomous Systems · Signal Processing</text>
  <text x="24" y="180" fill="#6e7681" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10">Updated {escape(updated)}</text>
</svg>
'''
    (OUTPUT / "stats.svg").write_text(svg, encoding="utf-8")


def write_languages_svg(totals):
    top = totals.most_common(6)
    total_bytes = sum(value for _, value in top)

    if total_bytes == 0:
        rows = '<text x="24" y="95" fill="#8b949e" font-family="Segoe UI, Ubuntu, sans-serif" font-size="13">No public language data available.</text>'
        bar = '<rect x="24" y="60" width="422" height="9" rx="4.5" fill="#21262d"/>'
    else:
        bar_parts = []
        x = 24.0
        for index, (language, value) in enumerate(top):
            width = 422.0 * value / total_bytes
            color = LANG_COLORS.get(language, "#8b949e")
            radius = ' rx="4.5"' if index in (0, len(top) - 1) else ""
            bar_parts.append(
                f'<rect x="{x:.2f}" y="60" width="{width:.2f}" height="9"{radius} fill="{color}"/>'
            )
            x += width
        bar = "\n  ".join(bar_parts)

        row_parts = []
        positions = [(24, 99), (245, 99), (24, 130), (245, 130), (24, 161), (245, 161)]
        for (language, value), (x0, y0) in zip(top, positions):
            pct = 100.0 * value / total_bytes
            color = LANG_COLORS.get(language, "#8b949e")
            row_parts.append(
                f'<circle cx="{x0 + 6}" cy="{y0 - 4}" r="5" fill="{color}"/>\n'
                f'  <text x="{x0 + 19}" y="{y0}" fill="#c9d1d9" font-family="Segoe UI, Ubuntu, sans-serif" font-size="12">{escape(language)} {pct:.1f}%</text>'
            )
        rows = "\n  ".join(row_parts)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="470" height="195" viewBox="0 0 470 195" role="img" aria-label="Top public repository languages">
  <rect width="469" height="194" x="0.5" y="0.5" rx="6" fill="#0d1117" stroke="#30363d"/>
  <text x="24" y="38" fill="#58a6ff" font-family="Segoe UI, Ubuntu, sans-serif" font-size="18" font-weight="600">Top Public Languages</text>
  {bar}
  {rows}
  <text x="24" y="184" fill="#6e7681" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10">TypeScript excluded · private repositories excluded</text>
</svg>
'''
    (OUTPUT / "top-langs.svg").write_text(svg, encoding="utf-8")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    user = api_get(f"/users/{USER}")
    repos = get_public_repos()
    languages = get_languages(repos)
    write_stats_svg(user, repos)
    write_languages_svg(languages)


if __name__ == "__main__":
    main()
