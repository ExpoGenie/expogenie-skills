"""Generate an exhibit-hall booth grid for the ExpoGenie create_booths tool.

Usage:  python layout.py spec.json > booths.json
Reads a layout spec (feet, plus the hall area in floorplan px) and prints booths with floorplan px positions:
  [{"boothNumber": "101", "x": 120, "y": 340, "width": 100, "height": 100, "kind": "inline"}, ...]

Layout model (the standard trade-show grid):
- Booths stand in back-to-back DOUBLE ROWS separated by aisles. With "orientation": "vertical" the rows run
  top-to-bottom (aisles are vertical); with "horizontal" they run left-to-right.
- Every `crossAisleEvery` booths a row is broken by a cross aisle; booths at the ends of a row segment are corners.
- Optional single rows along the two long walls ("perimeter": true), backed against the wall.
- Booths that touch an exclusion box (stage, F&B, pillars, doors + clearance) are left out.
- Numbering "hundreds-by-aisle": the booths facing aisle k are numbered k*100 + n, odd on the left/top side of the
  aisle, even on the right/bottom side, counting from the entrance end. "sequential" numbers 1, 2, 3...

Spec (all lengths in feet unless noted):
{
  "pxPerFt": 10,
  "area": {"x": 200, "y": 150, "width": 3000, "height": 1800},   # floorplan px: where booths may stand
  "exclusions": [{"x": 1200, "y": 150, "width": 600, "height": 400, "label": "Stage"}],   # floorplan px
  "orientation": "vertical",
  "boothWidthFt": 10, "boothDepthFt": 10,
  "aisleFt": 10, "crossAisleFt": 10, "crossAisleEvery": 10,
  "perimeter": false, "perimeterGapFt": 10,
  "entrance": "bottom",            # where numbering starts along each aisle: bottom/top (vertical), left/right
  "numbering": "hundreds-by-aisle", "firstAisle": 1, "prefix": ""
}
"""

import json
import math
import sys


def _overlaps(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def generate(spec):
    s = float(spec.get("pxPerFt", 10))
    area = spec["area"]
    vertical = spec.get("orientation", "vertical") == "vertical"
    bw = spec.get("boothWidthFt", 10) * s          # along the row
    bd = spec.get("boothDepthFt", 10) * s          # across the row
    aisle = spec.get("aisleFt", 10) * s
    cross = spec.get("crossAisleFt", 10) * s
    every = max(1, int(spec.get("crossAisleEvery", 10)))
    gap = spec.get("perimeterGapFt", 10) * s
    exclusions = [(e["x"], e["y"], e["width"], e["height"]) for e in spec.get("exclusions", [])]

    # Work in a frame where rows run along v (length L) and stack along u (width W); map back at the end.
    W, L = (area["width"], area["height"]) if vertical else (area["height"], area["width"])
    ox, oy = area["x"], area["y"]

    def to_canvas(u, v, du, dv):
        return (ox + u, oy + v, du, dv) if vertical else (ox + v, oy + u, dv, du)

    # Rows across u, in order. "-" faces the aisle on its low-u side, "+" the aisle on its high-u side.
    rows = []
    perimeter = bool(spec.get("perimeter"))
    u, u_end = 0.0, W - ((bd + aisle) if perimeter else 0)
    if perimeter:
        rows.append((u, "+"))
        u += bd + aisle
    while u + 2 * bd <= u_end + 1e-6:
        rows.append((u, "-"))
        rows.append((u + bd, "+"))
        u += 2 * bd + aisle
    if perimeter:
        rows.append((W - bd, "-"))

    # Row segments along v, broken by cross aisles; perimeter rows leave `gap` at both ends.
    def segments(is_perimeter):
        start, end = (gap, L - gap) if is_perimeter else (0.0, L)
        out, v = [], start
        while v + bw <= end + 1e-6:
            n = min(every, int((end - v + 1e-6) // bw))
            out.append([v + i * bw for i in range(n)])
            v += n * bw + cross
        return out

    perimeter_rows = {0, len(rows) - 1} if perimeter else set()
    # Aisle k lies between the k-th "+" row and the "-" row after it; a leading "-" row faces aisle 0 (the edge).
    plus_seen, row_aisle = 0, []
    for _, faces in rows:
        if faces == "+":
            plus_seen += 1
            row_aisle.append(plus_seen)
        else:
            row_aisle.append(plus_seen)

    booths = []
    for index, (u_left, faces) in enumerate(rows):
        for segment in segments(index in perimeter_rows):
            for k, v in enumerate(segment):
                box = to_canvas(u_left, v, bd, bw)
                if any(_overlaps(box, e) for e in exclusions):
                    continue
                kind = "perimeter" if index in perimeter_rows else (
                    "corner" if k in (0, len(segment) - 1) else "inline")
                booths.append({"v": v, "faces": faces, "box": box, "kind": kind, "aisle": row_aisle[index]})

    entrance = spec.get("entrance", "bottom" if vertical else "left")
    from_far_end = entrance in ("bottom", "right")
    first = int(spec.get("firstAisle", 1))
    prefix = spec.get("prefix", "")
    scheme = spec.get("numbering", "hundreds-by-aisle")
    by_aisle = {}
    for b in booths:
        by_aisle.setdefault(b["aisle"], []).append(b)

    out, seq = [], 1
    for rank, a in enumerate(sorted(by_aisle)):
        group = by_aisle[a]
        a = rank  # aisles that have booths are numbered consecutively: firstAisle*100, (firstAisle+1)*100, ...
        # Odd numbers on the low side of the aisle (the "+" row), even numbers across it (the "-" row).
        odd = sorted([b for b in group if b["faces"] == "+"], key=lambda b: b["v"], reverse=from_far_end)
        even = sorted([b for b in group if b["faces"] == "-"], key=lambda b: b["v"], reverse=from_far_end)
        for side, start in ((odd, 1), (even, 2)):
            for i, b in enumerate(side):
                if scheme == "sequential":
                    number = seq
                    seq += 1
                else:
                    number = (first + a) * 100 + start + 2 * i
                x, y, w, h = b["box"]
                out.append({"boothNumber": f"{prefix}{number}", "x": round(x), "y": round(y),
                            "width": round(w), "height": round(h), "kind": b["kind"]})
    return out


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else json.load(sys.stdin)
    booths = generate(spec)
    json.dump(booths, sys.stdout, indent=1)
    kinds = {}
    for b in booths:
        kinds[b["kind"]] = kinds.get(b["kind"], 0) + 1
    print(f"\n{len(booths)} booths: {kinds}", file=sys.stderr)
