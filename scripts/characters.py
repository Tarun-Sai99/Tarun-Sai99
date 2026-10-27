"""Pixel-art 'character select' strip of favourite characters.

Usage: python characters.py <out-dir>
Each sprite is a grid of letters; each letter maps to a colour.
Letters listed in a sprite's 'glow' set flicker (eyes, flames).
"""
import os
import sys

os.environ.setdefault("THEME", "pitwall")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_svgs import BG, BAR, LINE, INK, SOFT, ACCENT, SANS, FONT, window  # noqa: E402

CHARACTERS = [
    {
        "name": "Midnight Spider-Man",
        "colors": {"K": "#05060B", "N": "#1E2A44", "R": "#EF4444", "W": "#F8FAFC"},
        "glow": {"W"},
        "rows": [
            ".....KKKKKK.....",
            "....KNNNNNNK....",
            "...KNWWNNWWNK...",
            "...KNWWNNWWNK...",
            "...KNNNNNNNNK...",
            "....KNNNNNNK....",
            ".....KKKKKK.....",
            "...KKNNNNNNKK...",
            "..KNNNNRRNNNNK..",
            ".KNNKNRRRRNKNNK.",
            ".KNNKNNRRNNKNNK.",
            ".KNNKNRNNRNKNNK.",
            ".KRRKNNNNNNKRRK.",
            "..KK.KNNNNK.KK..",
            ".....KNNNNK.....",
            ".....KNKKNK.....",
            "....KNK..KNK....",
            "....KNK..KNK....",
            "...KRRK..KRRK...",
            "...KKKK..KKKK...",
        ],
    },
    {
        "name": "Absolute Superman",
        "colors": {"H": "#0A0A0A", "S": "#E8B48F", "K": "#0A0A0A", "D": "#2A2D34",
                   "R": "#DC2626", "C": "#991B1B", "E": "#EF4444"},
        "glow": {"E"},
        "rows": [
            ".....HHHHHH.....",
            "....HHSSSSHH....",
            "....HSSSSSSH....",
            "....SSESSESS....",
            "....SSSSSSSS....",
            ".....SSSSSS.....",
            "...CCKDDDDKCC...",
            "..CCDDDDDDDDCC..",
            "..CDDDRRRRDDDC..",
            ".CCDDDRDDRDDDCC.",
            ".CDDDDDRRDDDDDC.",
            ".CDDDDRDDRDDDDC.",
            ".CSDDDDRRDDDDSC.",
            ".C..DDDDDDDD..C.",
            ".CC.DDDDDDDD.CC.",
            "..C.DDD..DDD.C..",
            "....DDD..DDD....",
            "....DDD..DDD....",
            "...KKKK..KKKK...",
        ],
    },
    {
        "name": "Incredible Hulk",
        "colors": {"H": "#111111", "G": "#22C55E", "g": "#15803D", "K": "#0A0A0A",
                   "P": "#7C3AED", "E": "#BBF7D0"},
        "glow": {"E"},
        "rows": [
            ".....HHHHHH.....",
            "....HGGGGGGH....",
            "....GGEGGEGG....",
            "....GGGGGGGG....",
            "....GgKKKKgG....",
            ".....GGGGGG.....",
            "..GGGGGGGGGGGG..",
            ".GGGGgGGGGgGGGG.",
            "GGGGGGGGGGGGGGGG",
            "GGG.GGgGGgGG.GGG",
            "GGG.GGGGGGGG.GGG",
            "GGG.GGGGGGGG.GGG",
            "gGg.PPPPPPPP.gGg",
            "....PPPPPPPP....",
            "....PPP..PPP....",
            "....PP....PP....",
            "....GG....GG....",
            "...GGG....GGG...",
        ],
    },
    {
        "name": "Ghost Rider",
        "colors": {"F": "#F97316", "Y": "#FACC15", "B": "#F1EEDC", "K": "#0A0A0A",
                   "L": "#1C1C22", "s": "#94A3B8", "E": "#F97316"},
        "glow": {"F", "Y", "E"},
        "rows": [
            "...F.Y..F.Y.F...",
            "..FYFFYFFYFFYF..",
            "...FBBBBBBBBF...",
            "...BBBBBBBBBB...",
            "...BEEBBBBEEB...",
            "...BEEBBBBEEB...",
            "...BBBBKKBBBB...",
            "....BKBKBKBB....",
            ".....BBBBBB.....",
            "...LLLLLLLLLL...",
            "..LLLsLLLLsLLL..",
            ".LLLLLsssLLLLLL.",
            ".LL.LLLLLLLL.LL.",
            ".LL.LLLLLLLL.LL.",
            ".BB.LLLLLLLL.BB.",
            "....LLL..LLL....",
            "....LLL..LLL....",
            "....LLL..LLL....",
            "...KKKK..KKKK...",
        ],
    },
    {
        "name": "Doctor Doom",
        "colors": {"G": "#166534", "g": "#0F3D22", "M": "#A1A1AA", "m": "#6B7280",
                   "K": "#18181B", "E": "#4ADE80", "Y": "#CA8A04"},
        "glow": {"E"},
        "rows": [
            "....gGGGGGGg....",
            "...gGGGGGGGGg...",
            "...GGMMMMMMGG...",
            "...GMMMMMMMMG...",
            "...GMEEMMEEMG...",
            "...GMMMMMMMMG...",
            "...GMmKKKKmMG...",
            "...GGMMMMMMGG...",
            "..gGGGMMMMGGGg..",
            ".gGMMMMMMMMMMGg.",
            ".GGMMMMMMMMMMGG.",
            ".GGMM.YYYY.MMGG.",
            ".GG.GGGGGGGG.GG.",
            ".GM.GGGGGGGG.MG.",
            ".GG.GGGGGGGG.GG.",
            ".Gg.GGGGGGGG.gG.",
            ".gg.MMM..MMM.gg.",
            "....MMM..MMM....",
            "...mmmm..mmmm...",
        ],
    },
]


def sprite(ch, px):
    """Pixels as rects, one rect per run of the same colour; glowing letters flicker."""
    out = []
    for y, row in enumerate(ch["rows"]):
        x = 0
        while x < len(row):
            c = row[x]
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            if c != ".":
                cls = ' class="glow"' if c in ch["glow"] else ""
                out.append(f'<rect{cls} x="{x * px}" y="{y * px}" width="{run * px}" height="{px + 0.4}" fill="{ch["colors"][c]}"/>')
            x += run
    return "".join(out)


def characters(path, chars=CHARACTERS):
    W, H = 1000, 280
    n = len(chars)
    px = 6
    gap = 14
    tw = (W - 48 - gap * (n - 1)) / n
    th, ty = 196, 54
    step = 2.0  # seconds the highlight stays on each character
    loop = step * n
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-label="Pixel-art character select: {", ".join(c["name"] for c in chars)}">',
           '<style>'
           '.bob{animation:bob 1.6s ease-in-out infinite}@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}'
           '.glow{animation:glow 1.2s steps(2) infinite}@keyframes glow{0%{opacity:1}50%{opacity:.35}}'
           '</style>',
           window(W, H, "favourite_characters  ·  Player Select")]
    for i, ch in enumerate(chars):
        x = 24 + i * (tw + gap)
        sw = 16 * px
        sh = len(ch["rows"]) * px
        sx = x + (tw - sw) / 2
        sy = ty + 18 + (120 - sh)
        out.append(f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="10" fill="{BAR}" stroke="{LINE}"/>')
        # floor shadow
        out.append(f'<ellipse cx="{x + tw / 2:.1f}" cy="{ty + 142}" rx="40" ry="6" fill="#000" opacity=".35"/>')
        out.append(f'<g class="bob" style="animation-delay:{-i * 0.3:.1f}s"><g shape-rendering="crispEdges" transform="translate({sx:.1f},{sy:.1f})">{sprite(ch, px)}</g></g>')
        out.append(f'<text x="{x + tw / 2:.1f}" y="{ty + 172}" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="700" fill="{INK}">{ch["name"]}</text>')
        out.append(f'<text x="{x + 12:.1f}" y="{ty + 22}" font-family="{FONT}" font-size="11" fill="{SOFT}">P{i + 1}</text>')
        # highlight that walks across the tiles like a game's select screen
        a, b = i / n, (i + 1) / n
        kt, vals = (f"0;{b:.3f}", "1;0") if i == 0 else (f"0;{a:.3f};{b:.3f}", "0;1;0")
        out.append(f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" dur="{loop}s" repeatCount="indefinite" '
                   f'calcMode="discrete" keyTimes="{kt}" values="{vals}"/>'
                   f'<rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="10" fill="none" stroke="{ACCENT}" stroke-width="3"/>'
                   f'<text x="{x + tw - 12:.1f}" y="{ty + 22}" text-anchor="end" font-family="{FONT}" font-size="11" font-weight="700" fill="{ACCENT}">READY</text></g>')
    out.append(f'<text x="{W / 2}" y="{H - 10}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{SOFT}">fan art, drawn pixel by pixel</text>')
    out.append("</svg>\n")
    with open(path, "w") as f:
        f.write("".join(out))


if __name__ == "__main__":
    os.makedirs(sys.argv[1], exist_ok=True)
    characters(os.path.join(sys.argv[1], "characters.svg"))
