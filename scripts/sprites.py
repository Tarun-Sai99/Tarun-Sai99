"""Pixel-art fan-art sprites used as cameos across the profile.

Each sprite is a list of equal-width strings; each letter maps to a colour
and '.' is transparent. Letters in `glow` get class="glow" so the SVG can
make them flicker (eyes, flames).
"""

SPIDER = {  # Midnight Spider-Man
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
}

SUPERMAN_BACK = {  # Absolute Superman, seen from the row behind
    "colors": {"H": "#0A0A0A", "h": "#1F2937", "S": "#C8936E", "C": "#B91C1C", "c": "#7F1D1D"},
    "glow": set(),
    "rows": [
        "......HHHH......",
        ".....HHHHHH.....",
        "....HHHhHHHH....",
        "....HHHHHHHH....",
        "....HHHHHHhH....",
        ".....HHHHHH.....",
        "......SSSS......",
        "..CCCCCCCCCCCC..",
        ".CCCCCCCCCCCCCC.",
        "CCCCCCCCCCCCCCCC",
        "CCCcCCCCCCCCcCCC",
        "CCCcCCCCCCCCcCCC",
        "CCCcCCCCCCCCcCCC",
        "CCCcCCCCCCCCcCCC",
    ],
}

HULK = {
    "colors": {"H": "#111111", "G": "#22C55E", "g": "#15803D", "K": "#0A0A0A",
               "P": "#7C3AED", "E": "#BBF7D0"},
    "glow": set(),
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
}

GHOST_RIDER = {
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
}

# Doctor Doom with his left arm stretched out to cast (hand at the far left).
DOOM = {
    "colors": {"G": "#166534", "g": "#0F3D22", "M": "#A1A1AA", "m": "#6B7280",
               "K": "#18181B", "E": "#4ADE80", "Y": "#CA8A04"},
    "glow": {"E"},
    "rows": [
        "........gGGGGGGg....",
        ".......gGGGGGGGGg...",
        ".......GGMMMMMMGG...",
        ".......GMMMMMMMMG...",
        ".......GMEEMMEEMG...",
        ".......GMMMMMMMMG...",
        ".......GMmKKKKmMG...",
        ".......GGMMMMMMGG...",
        "......gGGGMMMMGGGg..",
        "mMGGGGGMMMMMMMMMMGg.",
        "MMGGGGGMMMMMMMMMMGG.",
        ".....GGMM.YYYY.MMGG.",
        ".....GG.GGGGGGGG.GG.",
        ".....GG.GGGGGGGG.MG.",
        ".......GGGGGGGGG.GG.",
        ".......GGGGGGGGG.gG.",
        "........MMM..MMM.gg.",
        "........MMM..MMM....",
        ".......mmmm..mmmm...",
    ],
}

BATMAN = {  # Absolute Batman, crouched like a gargoyle
    "colors": {"K": "#050505", "D": "#1F2937", "G": "#6B7280", "W": "#F8FAFC", "S": "#B98463"},
    "glow": {"W"},
    "rows": [
        "...K........K...",
        "...KK......KK...",
        "...KKK....KKK...",
        "...KKKKKKKKKK...",
        "...KKWWKKWWKK...",
        "...KKKKKKKKKK...",
        "....KSSSSSSK....",
        ".....KSSSSK.....",
        ".KKKDDDDDDDDKKK.",
        "KKKDGGDDDDGGDKKK",
        "KKDDDGGGGGGDDDKK",
        "KKDDDDGGGGDDDDKK",
        "KKDDDDDGGDDDDDKK",
        "KK.DDDDDDDDDD.KK",
        "KK.DDD....DDD.KK",
        "K..DDD....DDD..K",
        "...KKK....KKK...",
    ],
}


def pixels(sprite, px, flip=False):
    """SVG rects for a sprite, one rect per run of one colour.

    flip=True draws it upside down. Rects overlap by a hair so no seams show
    when the image is scaled.
    """
    rows = sprite["rows"][::-1] if flip else sprite["rows"]
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            if c != ".":
                cls = ' class="glow"' if c in sprite["glow"] else ""
                out.append(f'<rect{cls} x="{x * px}" y="{y * px}" width="{run * px + 0.3}" '
                           f'height="{px + 0.3}" fill="{sprite["colors"][c]}"/>')
            x += run
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


def size(sprite, px):
    return len(sprite["rows"][0]) * px, len(sprite["rows"]) * px


GLOW_CSS = ".glow{animation:glow 1.2s steps(2) infinite}@keyframes glow{0%{opacity:1}50%{opacity:.35}}"
