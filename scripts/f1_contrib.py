"""Draw an F1 car lapping the GitHub contribution grid.

The car drives every row of the grid like a track. On days with
contributions it opens DRS and speeds up. Your best days are purple
"fastest sector" squares, where it goes faster still. Writes a light and a
dark SVG.

Usage: python f1_contrib.py <github-login> <out-dir> [sample.json]
Needs GITHUB_TOKEN in the environment unless a sample file is given.
"""
import json
import os
import sys
import urllib.request

CELL, GAP = 11, 3
STEP = CELL + GAP
PAD_X, PAD_TOP, PAD_BOTTOM = 36, 30, 34
BASE_T = 0.085     # seconds per empty square
DRS_T = 0.03       # seconds per contribution square
PURPLE_T = 0.018   # seconds per best-day (purple) square
PURPLE = {"light": "#8250df", "dark": "#b07cff"}
TURN_T = 0.12      # seconds for a turn between rows
FINISH_T = 1.2     # pause after the lap before restarting

THEMES = {
    "light": {"bg": "#ffffff", "levels": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
              "text": "#57606a", "panel": "#f6f8fa", "border": "#d0d7de"},
    "dark": {"bg": "#0d1117", "levels": ["#161b22", "#2ea043", "#3fbf5a", "#4ade80", "#86efac"],
             "text": "#8b949e", "panel": "#161b22", "border": "#30363d"},
}

QUERY = """query($login:String!){user(login:$login){contributionsCollection{
contributionCalendar{weeks{contributionDays{contributionCount date weekday}}}}}}"""


def fetch(login):
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [[(d["weekday"], d["contributionCount"], d["date"]) for d in w["contributionDays"]] for w in weeks]


def levels(weeks):
    counts = sorted(c for w in weeks for _, c, *_ in w if c > 0)
    if not counts:
        return lambda c: 0
    q = [counts[int(len(counts) * f)] for f in (0.25, 0.5, 0.75)]
    return lambda c: 0 if c == 0 else 1 + sum(c > x for x in q)


def best_days(weeks):
    """Top 10% of active days by count (at least the single best day)."""
    counts = sorted((c for w in weeks for _, c, *_ in w if c > 0), reverse=True)
    if not counts:
        return float("inf")
    return counts[max(0, len(counts) // 10 - 1)]


def toggles(pts, idx, lap):
    """Opacity keyframes that switch on while pts[i][idx] is true."""
    frames, state = ["0%{opacity:0}"], False
    for p in pts:
        on = bool(p[idx])
        if on != state:
            frames.append(f"{max(p[0] / lap * 100 - 0.001, 0):.3f}%{{opacity:{int(state)}}}")
            frames.append(f"{p[0] / lap * 100:.3f}%{{opacity:{int(on)}}}")
            state = on
    return "".join(frames)


def car_svg():
    # Top-down F1 car, pointing right, centred on (0, 0). About 26 x 11 px.
    return """
    <g class="trail">
      <rect x="-30" y="-1.6" width="16" height="1.2" rx=".6" fill="#7dd3fc"/>
      <rect x="-26" y="1.2" width="12" height="1.2" rx=".6" fill="#7dd3fc"/>
    </g>
    <rect x="-13" y="-5.5" width="5" height="3.2" rx=".8" fill="#2a2a2a" stroke="#666" stroke-width=".4"/>
    <rect x="-13" y="2.3" width="5" height="3.2" rx=".8" fill="#2a2a2a" stroke="#666" stroke-width=".4"/>
    <rect x="5" y="-5" width="4.4" height="2.8" rx=".8" fill="#2a2a2a" stroke="#666" stroke-width=".4"/>
    <rect x="5" y="2.2" width="4.4" height="2.8" rx=".8" fill="#2a2a2a" stroke="#666" stroke-width=".4"/>
    <rect class="rw" x="-14.5" y="-4.8" width="2.4" height="9.6" rx=".6" fill="#E10600"/>
    <path d="M-12 -2.6 L-2 -3.4 L4 -1.6 L12 -0.9 L12 0.9 L4 1.6 L-2 3.4 L-12 2.6 Z" fill="#1E3FB0"/>
    <path d="M-9 -0.7 L11 -0.4 L11 0.4 L-9 0.7 Z" fill="#E10600"/>
    <circle cx="-1.5" cy="0" r="1.5" fill="#FFD400"/>
    <rect x="11" y="-4.8" width="1.8" height="9.6" rx=".5" fill="#E10600"/>"""


def build(weeks, theme):
    t = THEMES[theme]
    lvl = levels(weeks)
    best = best_days(weeks)
    cols = len(weeks)
    grid_w = cols * STEP - GAP
    width = grid_w + 2 * PAD_X
    height = PAD_TOP + 7 * STEP - GAP + PAD_BOTTOM

    def cx(col):
        return PAD_X + col * STEP + CELL / 2

    def cy(row):
        return PAD_TOP + row * STEP + CELL / 2

    count = {}
    for c, w in enumerate(weeks):
        for row, n, *_ in w:
            count[(c, row)] = n

    # Build the lap: rows left to right, then right to left, like a track.
    pts = []  # (time, x, y, angle, drs, purple)
    time = 0.0
    pts.append((0.0, cx(0) - 30, cy(0), 0, False, False))
    time += 0.4
    for row in range(7):
        order = range(cols) if row % 2 == 0 else range(cols - 1, -1, -1)
        ang = 0 if row % 2 == 0 else 180
        for c in order:
            if (c, row) not in count:
                continue
            n = count[(c, row)]
            drs, purple = n > 0, n > 0 and n >= best
            pts.append((time, cx(c), cy(row), ang, drs, purple))
            time += PURPLE_T if purple else DRS_T if drs else BASE_T
        if row < 6:
            last = pts[-1]
            pts.append((time, last[1], last[2] + STEP / 2, 90, False, False))
            time += TURN_T
    last = pts[-1]
    pts.append((time, last[1] + (30 if last[3] == 0 else -30), last[2], last[3], False, False))
    lap = time + FINISH_T

    def pct(x):
        return f"{x / lap * 100:.3f}%"

    # Keep the angle continuous so the car never spins the long way round.
    move, drs_frames, prev_ang = [], [], None
    for tm, x, y, a, *_ in pts:
        if prev_ang is not None:
            while a - prev_ang > 180:
                a -= 360
            while prev_ang - a > 180:
                a += 360
        prev_ang = a
        move.append(f"{pct(tm)}{{transform:translate({x:.1f}px,{y:.1f}px) rotate({a}deg)}}")
    move.append(f"100%{{transform:translate({pts[-1][1]:.1f}px,{pts[-1][2]:.1f}px) rotate({prev_ang}deg)}}")

    drs_frames = toggles(pts, 4, lap)
    purple_frames = toggles(pts, 5, lap)

    # Contribution squares flash when the car passes them.
    passed = {(round(p[1], 1), round(p[2], 1)): p[0] for p in pts if p[4]}

    cells = []
    flash_css = []
    for c, w in enumerate(weeks):
        for row, n, *_ in w:
            x, y = PAD_X + c * STEP, PAD_TOP + row * STEP
            fill = PURPLE[theme] if n > 0 and n >= best else t["levels"][lvl(n)]
            key = (round(cx(c), 1), round(cy(row), 1))
            cls = ""
            if n > 0 and key in passed:
                i = len(flash_css)
                cls = f' class="f{i}"'
                p0 = passed[key] / lap * 100
                flash_css.append(
                    f".f{i}{{animation:fl{i} {lap:.2f}s linear infinite}}"
                    f"@keyframes fl{i}{{0%,{max(p0 - 0.01, 0):.3f}%{{fill:{fill}}}"
                    f"{p0:.3f}%{{fill:#ffffff}}{min(p0 + 1.2, 100):.3f}%,100%{{fill:{fill}}}}}"
                )
            cells.append(f'<rect{cls} x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}"/>')

    by = height - 22

    # Month labels on top and Mon/Wed/Fri on the left, like GitHub's graph.
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    labels, prev, last_c = [], None, -9
    for c, w in enumerate(weeks):
        dated = [d for d in w if len(d) > 2]
        if not dated:
            continue
        m = int(dated[0][2][5:7])
        if m != prev and c < cols - 2 and c - last_c >= 3:
            if prev is not None or int(dated[0][2][8:10]) <= 7:
                last_c = c
                labels.append(f'<text x="{PAD_X + c * STEP}" y="{PAD_TOP - 8}">{months[m - 1]}</text>')
        prev = m
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        labels.append(f'<text x="{PAD_X - 6}" y="{cy(row) + 4}" text-anchor="end" style="font-size:10px">{name}</text>')
    total = sum(n for w in weeks for _, n, *_ in w)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="F1 car lapping the contribution graph">
<style>
.car{{animation:lap {lap:.2f}s linear infinite}}
@keyframes lap{{{''.join(move)}}}
.trail,.drs-on{{opacity:0;animation:drs {lap:.2f}s step-end infinite}}
.fs-on{{opacity:0;animation:fs {lap:.2f}s step-end infinite}}
@keyframes drs{{{drs_frames}}}
@keyframes fs{{{purple_frames}}}
{''.join(flash_css)}
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;font-size:11px;fill:{t['text']}}}
</style>
<rect width="{width}" height="{height}" rx="6" fill="{t['bg']}"/>
{''.join(cells)}
{''.join(labels)}
<text x="{PAD_X}" y="{by + 12}">{total} contributions in the last year · green opens DRS · purple = fastest sector (best days)</text>
<g transform="translate({width - PAD_X - 44},{by})">
  <rect width="44" height="16" rx="3" fill="{t['panel']}" stroke="{t['border']}"/>
  <text x="22" y="12" text-anchor="middle" style="font-weight:700">DRS</text>
  <g class="drs-on"><rect width="44" height="16" rx="3" fill="#2ea043"/><text x="22" y="12" text-anchor="middle" style="font-weight:700;fill:#fff">DRS</text></g>
</g>
<g transform="translate({width - PAD_X - 44 - 8 - 104},{by})">
  <rect width="104" height="16" rx="3" fill="{t['panel']}" stroke="{t['border']}"/>
  <text x="52" y="12" text-anchor="middle" style="font-weight:700">FASTEST SECTOR</text>
  <g class="fs-on"><rect width="104" height="16" rx="3" fill="{PURPLE[theme]}"/><text x="52" y="12" text-anchor="middle" style="font-weight:700;fill:#fff">FASTEST SECTOR</text></g>
</g>
<g class="car"><g transform="scale(1.6)">{car_svg()}</g></g>
</svg>
"""


def main():
    login, out = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            weeks = json.load(f)
    else:
        weeks = fetch(login)
    os.makedirs(out, exist_ok=True)
    for theme in THEMES:
        with open(os.path.join(out, f"f1-contrib-{theme}.svg"), "w") as f:
            f.write(build(weeks, theme))


if __name__ == "__main__":
    main()
