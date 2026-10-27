"""Draw a Power BI style report of GitHub activity.

Usage: python dashboard.py <github-login> <out-dir> [sample.json]
Needs GITHUB_TOKEN in the environment unless a sample file is given.
The sample file holds {"days": [[date, count], ...], "repos": n}.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

os.environ.setdefault("THEME", "pitwall")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_svgs import BG, BAR, LINE, INK, SOFT, ACCENT, SANS, window, escape  # noqa: E402
from sprites import BATMAN, pixels, size, GLOW_CSS  # noqa: E402

QUERY = """query($login:String!){user(login:$login){
repositories(ownerAffiliations:OWNER, privacy:PUBLIC){totalCount}
contributionsCollection{contributionCalendar{weeks{contributionDays{contributionCount date}}}}}}"""
PBI_YELLOW = "#F2C811"


def fetch(login):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        user = json.load(r)["data"]["user"]
    days = [(d["date"], d["contributionCount"])
            for w in user["contributionsCollection"]["contributionCalendar"]["weeks"]
            for d in w["contributionDays"]]
    return days, user["repositories"]["totalCount"]


def streaks(days):
    counts = [c for _, c in sorted(days)]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    current = 0
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today not done yet still keeps the streak
        i -= 1
    while i >= 0 and counts[i] > 0:
        current += 1
        i -= 1
    return current, longest


def monthly(days):
    last = dt.date.fromisoformat(max(d for d, _ in days))
    months = []
    y, m = last.year, last.month
    for _ in range(12):
        months.append((y, m))
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    months.reverse()
    totals = {k: 0 for k in months}
    for d, c in days:
        key = (int(d[:4]), int(d[5:7]))
        if key in totals:
            totals[key] += c
    names = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return [(names[m - 1], totals[(y, m)]) for y, m in months]


def build(days, repos):
    W, H0, T = 1000, 430, 66  # T = room above the window for Batman to perch
    H = H0 + T
    total = sum(c for _, c in days)
    active = sum(1 for _, c in days if c > 0)
    cur, best = streaks(days)
    months = monthly(days)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-label="Power BI style report: {total} contributions, {active} active days, current streak {cur} days, longest streak {best} days, {repos} public repositories">',
           '<style>.bar{transform-box:fill-box;transform-origin:bottom;animation:grow 1.2s ease-out both}'
           '@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}'
           '.tile{animation:fade .6s ease-out both}@keyframes fade{from{opacity:0}to{opacity:1}}'
           '.cape{animation:cape 1.4s steps(2) infinite}@keyframes cape{0%{transform:translateX(0)}50%{transform:translateX(-2px)}}'
           f'{GLOW_CSS}</style>',
           f'<g transform="translate(0,{T})">',
           window(W, H0, "github_activity.pbix  ·  Power BI")]
    # report header with Power BI mark
    out.append(f'<g transform="translate(24,52)"><rect x="0" y="12" width="7" height="14" rx="1.5" fill="#E8B10A"/>'
               f'<rect x="9" y="6" width="7" height="20" rx="1.5" fill="{PBI_YELLOW}"/><rect x="18" y="0" width="7" height="26" rx="1.5" fill="#F7D84A"/></g>'
               f'<text x="62" y="72" font-family="{SANS}" font-size="17" font-weight="700" fill="{INK}">GitHub Activity Report</text>'
               f'<text x="{W - 24}" y="72" text-anchor="end" font-family="{SANS}" font-size="12" fill="{SOFT}">Last refreshed {stamp}</text>'
               f'<line x1="1" x2="{W - 1}" y1="90" y2="90" stroke="{LINE}"/>')
    # KPI tiles
    tiles = [("Contributions", total, "last 12 months"), ("Active days", active, "days with commits"),
             ("Current streak", cur, "days in a row"), ("Longest streak", best, "days in a row"),
             ("Public repos", repos, "on GitHub")]
    tw, gap, ty = (W - 48 - 4 * 14) / 5, 14, 106
    for i, (label, val, sub) in enumerate(tiles):
        x = 24 + i * (tw + gap)
        out.append(f'<g class="tile" style="animation-delay:{i * 0.12:.2f}s">'
                   f'<rect x="{x}" y="{ty}" width="{tw}" height="92" rx="8" fill="{BAR}" stroke="{LINE}"/>'
                   f'<rect x="{x}" y="{ty}" width="4" height="92" rx="2" fill="{PBI_YELLOW if i % 2 == 0 else ACCENT}"/>'
                   f'<text x="{x + 18}" y="{ty + 26}" font-family="{SANS}" font-size="12" fill="{SOFT}">{label}</text>'
                   f'<text x="{x + 18}" y="{ty + 62}" font-family="{SANS}" font-size="32" font-weight="700" fill="{INK}">{val}</text>'
                   f'<text x="{x + 18}" y="{ty + 81}" font-family="{SANS}" font-size="11" fill="{SOFT}">{sub}</text></g>')
    # bar chart
    cx, cy, cw, ch = 24, 216, W - 48, 196
    out.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="8" fill="{BAR}" stroke="{LINE}"/>'
               f'<text x="{cx + 18}" y="{cy + 26}" font-family="{SANS}" font-size="13" font-weight="700" fill="{INK}">Contributions by month</text>')
    peak = max((v for _, v in months), default=0) or 1
    px0, py0, pw, ph = cx + 30, cy + 44, cw - 60, ch - 82
    slot = pw / len(months)
    bw = slot * 0.56
    for i, (name, v) in enumerate(months):
        bx = px0 + i * slot + (slot - bw) / 2
        h = max(ph * v / peak, 2 if v else 0)
        color = PBI_YELLOW if v == peak and v > 0 else ACCENT
        if h:
            out.append(f'<rect class="bar" style="animation-delay:{0.4 + i * 0.06:.2f}s" x="{bx:.1f}" y="{py0 + ph - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" fill="{color}"/>')
        out.append(f'<text x="{bx + bw / 2:.1f}" y="{py0 + ph - h - 6:.1f}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{INK}">{v}</text>'
                   f'<text x="{bx + bw / 2:.1f}" y="{py0 + ph + 18:.1f}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{SOFT}">{name}</text>')
    out.append(f'<line x1="{px0}" x2="{px0 + pw}" y1="{py0 + ph}" y2="{py0 + ph}" stroke="{LINE}"/>')
    out.append("</g>")
    # Absolute Batman crouched on the window's roof, watching over the numbers
    bpx = 4
    bw, bh = size(BATMAN, bpx)
    bx = W - 150
    out.append(f'<g class="cape"><g transform="translate({bx},{T - bh + 3})">{pixels(BATMAN, bpx)}</g></g>')
    out.append("</svg>\n")
    return "".join(out)


def main():
    login, outdir = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            data = json.load(f)
        days, repos = [tuple(d) for d in data["days"]], data["repos"]
    else:
        days, repos = fetch(login)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "dashboard.svg"), "w") as f:
        f.write(build(days, repos))


if __name__ == "__main__":
    main()
