"""Build the animated hero banner and the Currently Exploring card.

Usage: python scripts/make_svgs.py <out-dir>
"""
import os
import sys
from xml.sax.saxutils import escape

THEMES = {
    "cream": ("#F5ECDD", "#EADBC4", "#E3D3BD", "#5C4033", "#8C7B6B", "#A0674B"),
    "pitwall": ("#0F172A", "#1E293B", "#334155", "#E2E8F0", "#94A3B8", "#EF4444"),
    "purple": ("#1A1033", "#2A1B4D", "#3D2A6B", "#EDE9FE", "#A99BD6", "#C084FC"),
    "terminal": ("#0B0F0C", "#161D18", "#26302A", "#D1FAE5", "#7A9C88", "#22C55E"),
}
BG, BAR, LINE, INK, SOFT, ACCENT = THEMES[os.environ.get("THEME", "pitwall")]
FONT = "'SFMono-Regular', Consolas, 'Liberation Mono', 'Courier New', monospace"
CW = 10.2     # width of one character at 17px, kept exact with textLength
DUR = 14      # seconds per loop


def kt(*pairs):
    """SMIL keyTimes/values from (time-in-seconds, value) pairs."""
    times = ";".join(f"{min(t / DUR, 1):.4f}" for t, _ in pairs)
    vals = ";".join(str(v) for _, v in pairs)
    return times, vals


def hero(path):
    query = "SELECT * FROM profile WHERE name = 'Tarun Sai'\\G"
    rows = [
        ("", "*************************** 1. row ***************************"),
        ("    name", "Tarun Sai"),
        ("    role", "Data Analyst"),
        ("   tools", "SQL, Python, Excel, Power BI"),
        ("   focus", "Data Cleaning, Exploratory Data Analysis"),
        ("location", "Proddatur, Andhra Pradesh, India"),
        ("  status", "Open to full-time roles and internships"),
        ("", "1 row in set (0.00 sec)"),
    ]
    W, LH, X0, Y0 = 1000, 27, 32, 78
    H = Y0 + LH * (len(rows) + 1) + 30
    prompt = "mysql> "
    qx = X0 + len(prompt) * CW
    type_start, per_char = 0.8, 0.06
    type_end = type_start + len(query) * per_char
    hold_end = DUR - 0.8

    # typing: clip width grows one character at a time
    steps = [(0, 0), (type_start, 0)]
    for i in range(1, len(query) + 1):
        steps.append((type_start + i * per_char, i * CW))
    steps += [(hold_end, len(query) * CW), (DUR, 0)]
    times, vals = kt(*steps)

    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="MySQL terminal showing Tarun Sai's profile: Data Analyst, SQL, Python, Excel, Power BI">
<defs>
  <clipPath id="typed"><rect x="{qx}" y="{Y0 - 20}" height="28" width="0">
    <animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{times}" values="{vals}"/>
  </rect></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{LINE}" stroke-width="2"/>
<path d="M1 15 Q1 1 15 1 H{W - 15} Q{W - 1} 1 {W - 1} 15 V38 H1 Z" fill="{BAR}"/>
<circle cx="24" cy="20" r="6.5" fill="#E07A5F"/><circle cx="46" cy="20" r="6.5" fill="#E9B44C"/><circle cx="68" cy="20" r="6.5" fill="#81B29A"/>
<text x="{W / 2}" y="25" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{SOFT}">tarun@profile: ~ mysql</text>
<g font-family="{FONT}" font-size="17" xml:space="preserve">
<text x="{X0}" y="{Y0}" fill="{ACCENT}" font-weight="700" textLength="{len(prompt.rstrip()) * CW}">{prompt.rstrip()}</text>
<text x="{qx}" y="{Y0}" fill="{INK}" clip-path="url(#typed)" textLength="{len(query) * CW}" lengthAdjust="spacingAndGlyphs">{escape(query)}</text>
''']
    # cursor while typing
    ct, cv = kt((0, qx), (type_start, qx), *[(type_start + i * per_char, qx + i * CW) for i in range(1, len(query) + 1)], (DUR, qx + len(query) * CW))
    out.append(f'''<rect y="{Y0 - 15}" width="9" height="19" fill="{ACCENT}" x="{qx}">
  <animate attributeName="x" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{ct}" values="{cv}"/>
  <animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt((0, 1), (type_end + 0.3, 0), (DUR, 0))[0]}" values="1;0;0"/>
</rect>
''')
    t = type_end + 0.5
    for i, (key, val) in enumerate(rows):
        y = Y0 + LH * (i + 1)
        t0 = t + i * 0.18
        times, vals = kt((0, 0), (t0, 0), (t0 + 0.2, 1), (hold_end, 1), (DUR, 0))
        anim = f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" keyTimes="{times}" values="{vals}"/>'
        if key:
            out.append(f'<g opacity="0">{anim}<text x="{X0 + 9 * CW}" y="{y}" fill="{SOFT}" text-anchor="end">{key.strip()}:</text>'
                       f'<text x="{X0 + 10 * CW}" y="{y}" fill="{INK}" font-weight="{700 if key.strip() == "name" else 400}" textLength="{len(val) * CW}" lengthAdjust="spacingAndGlyphs">{escape(val)}</text></g>\n')
        else:
            out.append(f'<g opacity="0">{anim}<text x="{X0}" y="{y}" fill="{SOFT}" textLength="{len(val) * CW}" lengthAdjust="spacingAndGlyphs">{escape(val)}</text></g>\n')
    # final prompt with blinking cursor
    y = Y0 + LH * (len(rows) + 1)
    t_last = t + len(rows) * 0.18 + 0.3
    times, vals = kt((0, 0), (t_last, 0), (t_last + 0.01, 1), (hold_end, 1), (DUR, 0))
    out.append(f'''<g opacity="0"><animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{times}" values="{vals}"/>
<text x="{X0}" y="{y}" fill="{ACCENT}" font-weight="700" textLength="{6 * CW}">mysql&gt;</text>
<rect x="{qx}" y="{y - 15}" width="9" height="19" fill="{ACCENT}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></rect>
</g>
</g>
</svg>
''')
    with open(path, "w") as f:
        f.write("".join(out))


def exploring(path):
    W, H = 1000, 190
    cards = [
        ("Power BI", "Interactive dashboards and", "advanced visualizations", "#F2C811", "pbi"),
        ("Python", "Deeper statistical analysis", "with Pandas and NumPy", "#3776AB", "py"),
    ]
    icons = {
        # simple Power BI bars
        "pbi": '<rect x="0" y="22" width="11" height="26" rx="2" fill="#E8B10A"/><rect x="14" y="12" width="11" height="36" rx="2" fill="#F2C811"/><rect x="28" y="0" width="11" height="48" rx="2" fill="#F7D84A"/>',
        # simple Python mark
        "py": '<path d="M24 0c-9 0-12 4-12 8v6h12v2H7c-5 0-7 4-7 10s3 10 7 10h5v-7c0-4 3-7 7-7h12c4 0 6-3 6-6V8c0-4-4-8-13-8z" fill="#3776AB"/><circle cx="18" cy="6" r="2" fill="#fff"/>'
              '<path d="M24 48c9 0 12-4 12-8v-6H24v-2h17c5 0 7-4 7-10s-3-10-7-10h-5v7c0 4-3 7-7 7H17c-4 0-6 3-6 6v8c0 4 4 8 13 8z" fill="#FFD43B"/><circle cx="30" cy="42" r="2" fill="#fff"/>',
    }
    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Currently exploring: Power BI dashboards and deeper Python analysis">
<style>
  .t {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }}
  .bar {{ animation: fill 3.2s ease-in-out infinite; transform-box: fill-box; transform-origin: left; }}
  .b2 {{ animation-delay: .6s; }}
  .dot {{ animation: pulse 1.4s ease-in-out infinite; }}
  @keyframes fill {{ 0% {{ transform: scaleX(.08); }} 70% {{ transform: scaleX(1); }} 100% {{ transform: scaleX(1); opacity: .35; }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
</style>
''']
    cw, gap = (W - 30) / 2, 30
    for i, (name, l1, l2, color, icon) in enumerate(cards):
        x = i * (cw + gap)
        out.append(f'''<g transform="translate({x + 1},1)">
  <clipPath id="c{i}"><rect width="{cw - 2}" height="{H - 2}" rx="14"/></clipPath>
  <rect width="{cw - 2}" height="{H - 2}" rx="14" fill="{BG}"/>
  <rect width="8" height="{H - 2}" fill="{color}" clip-path="url(#c{i})"/>
  <rect width="{cw - 2}" height="{H - 2}" rx="14" fill="none" stroke="{LINE}" stroke-width="2"/>
  <g transform="translate(30,30)">{icons[icon]}</g>
  <text class="t" x="96" y="50" font-size="24" font-weight="700" fill="{INK}">{name}</text>
  <g transform="translate({cw - 150},34)">
    <rect width="122" height="24" rx="12" fill="{BAR}"/>
    <circle class="dot" cx="16" cy="12" r="5" fill="{ACCENT}"/>
    <text class="t" x="28" y="17" font-size="12" font-weight="700" fill="{ACCENT}" letter-spacing="1">EXPLORING</text>
  </g>
  <text class="t" x="96" y="80" font-size="16" fill="{SOFT}">{l1}</text>
  <text class="t" x="96" y="102" font-size="16" fill="{SOFT}">{l2}</text>
  <rect x="30" y="134" width="{cw - 62}" height="10" rx="5" fill="{BAR}"/>
  <rect class="bar{' b2' if i else ''}" x="30" y="134" width="{cw - 62}" height="10" rx="5" fill="{color}"/>
  <text class="t" x="30" y="168" font-size="12" fill="{SOFT}" letter-spacing="1">LEARNING IN PROGRESS</text>
</g>
''')
    out.append("</svg>\n")
    with open(path, "w") as f:
        f.write("".join(out))


def theatre(path):
    """Cinema screen with curtains; the profile rolls up like end credits."""
    W, H = 1000, 420
    sx, sy, sw, sh = 165, 62, 670, 250
    serif = "Georgia, 'Times New Roman', serif"
    sans = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
    credits = [
        ("small", "GITHUB STUDIOS PRESENTS"),
        ("gap", 30),
        ("title", "TARUN SAI"),
        ("handle", "@Tarun-Sai99"),
        ("gap", 10),
        ("small", "IN"),
        ("sub", "A Data Analyst Story"),
        ("gap", 60),
        ("label", "STARRING"), ("name", "Tarun Sai as the Data Analyst"),
        ("label", "TOOLS OF THE TRADE"), ("name", "SQL · Python · Excel · Power BI"),
        ("label", "SPECIAL FOCUS"), ("name", "Data Cleaning · Exploratory Data Analysis"),
        ("label", "FILMED ON LOCATION IN"), ("name", "Proddatur, Andhra Pradesh, India"),
        ("label", "NOW CASTING"), ("name", "Open to full-time roles and internships"),
        ("gap", 40),
        ("small", "THE END?  NOT YET."),
    ]
    style = {
        "small": (13, sans, "#9CA3AF", 600, 4, 30),
        "title": (52, serif, "#F8FAFC", 700, 6, 62),
        "sub": (22, serif, "#E5E7EB", 400, 1, 34),
        "handle": (16, FONT, "#EF4444", 600, 2, 30),
        "label": (12, sans, "#EF4444", 700, 4, 50),
        "name": (21, serif, "#F8FAFC", 400, 0, 28),
    }
    y, lines = 0, []
    for kind, val in credits:
        if kind == "gap":
            y += val
            continue
        size, font, color, weight, ls, adv = style[kind]
        y += adv if kind != "title" else adv - 10
        lines.append(f'<text x="{W / 2}" y="{y}" text-anchor="middle" font-family="{font}" font-size="{size}" '
                     f'font-weight="{weight}" letter-spacing="{ls}" fill="{color}">{escape(val)}</text>')
    total = y + 20
    roll = 22  # seconds per pass
    start, end = sy + sh + 10, sy - total
    folds = "".join(
        f'<stop offset="{i / 10:.2f}" stop-color="{"#7A0E19" if i % 2 else "#B3192A"}"/>' for i in range(11))
    seats = []
    for row, (yy, r, col) in enumerate([(372, 17, "#07080D"), (398, 19, "#040509")]):
        n = 15 if row == 0 else 14
        off = 0 if row == 0 else 34
        for i in range(n):
            cx = 40 + off + i * 68
            seats.append(f'<circle cx="{cx}" cy="{yy - r}" r="{r * 0.62:.1f}" fill="{col}"/>'
                         f'<rect x="{cx - r}" y="{yy - r * 0.6:.1f}" width="{2 * r}" height="{H - yy + r}" rx="{r * 0.7:.1f}" fill="{col}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Cinema screen rolling credits: Tarun Sai, Data Analyst. Tools: SQL, Python, Excel, Power BI. Focus: data cleaning and exploratory data analysis. Proddatur, Andhra Pradesh, India. Open to full-time roles and internships.">
<style>
  .roll {{ animation: roll {roll}s linear infinite; }}
  .beam {{ animation: flicker 3s ease-in-out infinite; }}
  @keyframes roll {{ from {{ transform: translateY({start}px); }} to {{ transform: translateY({end}px); }} }}
  @keyframes flicker {{ 0%,100% {{ opacity: .9; }} 45% {{ opacity: .75; }} 50% {{ opacity: .95; }} 70% {{ opacity: .8; }} }}
</style>
<defs>
  <radialGradient id="hall" cx="50%" cy="40%" r="70%"><stop offset="0" stop-color="#1A1426"/><stop offset="1" stop-color="#07060B"/></radialGradient>
  <linearGradient id="curtain" x1="0" x2="1">{folds}</linearGradient>
  <linearGradient id="shade" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>
  <linearGradient id="beamG" x1="0" x2="0" y1="1" y2="0"><stop offset="0" stop-color="#FDE68A" stop-opacity=".35"/><stop offset="1" stop-color="#FDE68A" stop-opacity="0"/></linearGradient>
  <radialGradient id="screenG" cx="50%" cy="45%" r="65%"><stop offset="0" stop-color="#151B2B"/><stop offset="1" stop-color="#05070C"/></radialGradient>
  <clipPath id="screen"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4"/></clipPath>
  <clipPath id="hallC"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#hallC)">
<rect width="{W}" height="{H}" fill="url(#hall)"/>
<rect x="{sx - 18}" y="{sy - 18}" width="{sw + 36}" height="{sh + 36}" rx="14" fill="#93C5FD" opacity=".05"/>
<rect x="{sx - 4}" y="{sy - 4}" width="{sw + 8}" height="{sh + 8}" rx="6" fill="#1F2937"/>
<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="url(#screenG)"/>
<g clip-path="url(#screen)"><g class="roll">{"".join(lines)}</g></g>
<path d="M0 0 H150 Q140 200 120 {H} H0 Z" fill="url(#curtain)"/>
<path d="M{W} 0 H{W - 150} Q{W - 140} 200 {W - 120} {H} H{W} Z" fill="url(#curtain)"/>
<path d="M0 0 H150 Q140 200 120 {H} H0 Z M{W} 0 H{W - 150} Q{W - 140} 200 {W - 120} {H} H{W} Z" fill="url(#shade)"/>
<path d="M0 0 H{W} V30 {"".join(f"Q{W - i * 100 - 50} 58 {W - (i + 1) * 100} 30 " for i in range(10))}Z" fill="#9B1424"/>
<path d="M0 0 H{W} V12 H0 Z" fill="#5E0A14"/>
<polygon class="beam" points="{W / 2 - 8},{H} {W / 2 + 8},{H} {sx + sw - 40},{sy + sh} {sx + 40},{sy + sh}" fill="url(#beamG)"/>
{"".join(seats)}
</g>
</svg>
'''
    with open(path, "w") as f:
        f.write(svg)


def outro(path):
    """Closing terminal: commits the visit, exits, and teases a post-credits scene."""
    W, X0, Y0, LH = 1000, 32, 78, 28
    lines = [
        # (start time, prompt?, text, colour, typed?)
        (0.8, True, "COMMIT;", INK, True),
        (2.0, False, "Query OK, 1 visit recorded. Thanks for watching. (0.00 sec)", INK, False),
        (3.2, True, "exit;", INK, True),
        (4.2, False, "Session closed.", SOFT, False),
        (5.0, False, "[ POST-CREDITS SCENE ]  next project loading", ACCENT, False),
    ]
    H = Y0 + LH * (len(lines) - 1) + 30
    hold = DUR - 0.8
    per = 0.1
    qx = X0 + 7 * CW

    def show(t):
        tt, vv = kt((0, 0), (t, 0), (t + 0.01, 1), (hold, 1), (DUR, 0))
        return f'<animate attributeName="opacity" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{tt}" values="{vv}"/>'

    defs, body = [], []
    for i, (t, is_cmd, text, color, typed) in enumerate(lines):
        y = Y0 + i * LH
        if is_cmd:
            steps = [(0, 0), (t, 0)] + [(t + k * per, k * CW) for k in range(1, len(text) + 1)] + [(hold, len(text) * CW), (DUR, 0)]
            tt, vv = kt(*steps)
            defs.append(f'<clipPath id="ty{i}"><rect x="{qx}" y="{y - 20}" height="28" width="0"><animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{tt}" values="{vv}"/></rect></clipPath>')
            body.append(f'<g opacity="0">{show(t - 0.3)}<text x="{X0}" y="{y}" fill="{ACCENT}" font-weight="700">mysql&gt;</text>'
                        f'<text x="{qx}" y="{y}" fill="{color}" clip-path="url(#ty{i})" textLength="{len(text) * CW}" lengthAdjust="spacingAndGlyphs">{escape(text)}</text></g>')
        else:
            extra = ""
            if text.startswith("[ POST"):
                bx = X0 + (len(text) + 2) * CW
                extra = (f'<rect x="{bx}" y="{y - 13}" width="150" height="14" rx="3" fill="{BAR}" stroke="{LINE}"/>'
                         f'<rect x="{bx + 2}" y="{y - 11}" width="0" height="10" rx="2" fill="{ACCENT}">'
                         f'<animate attributeName="width" values="0;146;146" keyTimes="0;0.8;1" dur="3s" repeatCount="indefinite"/></rect>'
                         f'<text x="{bx + 160}" y="{y}" fill="{ACCENT}">...</text>')
            body.append(f'<g opacity="0">{show(t)}<text x="{X0}" y="{y}" fill="{color}" font-weight="{700 if extra else 400}">{escape(text)}</text>{extra}</g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="mysql> COMMIT; Query OK, 1 visit recorded. Thanks for watching. mysql> exit; Session closed. Post-credits scene: next project loading.">
<defs>{"".join(defs)}</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{LINE}" stroke-width="2"/>
<path d="M1 15 Q1 1 15 1 H{W - 15} Q{W - 1} 1 {W - 1} 15 V38 H1 Z" fill="{BAR}"/>
<circle cx="24" cy="20" r="6.5" fill="#E07A5F"/><circle cx="46" cy="20" r="6.5" fill="#E9B44C"/><circle cx="68" cy="20" r="6.5" fill="#81B29A"/>
<text x="{W / 2}" y="25" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{SOFT}">tarun@profile: ~ mysql</text>
<g font-family="{FONT}" font-size="17">
{"".join(body)}
</g>
</svg>
'''
    with open(path, "w") as f:
        f.write(svg)

if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    hero(os.path.join(out, "hero.svg"))
    exploring(os.path.join(out, "exploring.svg"))
    theatre(os.path.join(out, "theatre.svg"))
    outro(os.path.join(out, "outro.svg"))
