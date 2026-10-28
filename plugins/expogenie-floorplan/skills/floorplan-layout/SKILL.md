---
name: floorplan-layout
description: Place the booths of an ExpoGenie floor plan, either by copying the booth grid printed on the venue drawing or by generating standard back-to-back rows with aisles, corners and hundreds-by-aisle numbering. Produces exact booth positions for the MCP create_booths tool. Use after floorplan-background (or on a blank canvas), or when someone asks to add, lay out, renumber or move many booths.
---

# Floor plan layout

Turn the floor plan brief (from floorplan-intake) into exact booth rectangles in floorplan pixels (**10 px = 1 ft**).

**Never compute hundreds of coordinates in your head.** Use `scripts/layout.py` for generated grids. When copying a drawing, write the booths to a JSON file as you read them and check them with the preview.

Tools (ExpoGenie MCP): `preview_drawing`, `render_floorplan_preview`, `create_booths`, `update_booths`, `delete_booths`, `upsert_legend_labels`, `create_booth_type`, `list_booths`.

## Choose a mode

| The drawing… | Mode |
|---|---|
| already shows numbered booth outlines (most decorator / venue CAD plans) | **A: copy the drawing** |
| shows only the empty hall | **B: generate a grid** |
| shows some booths and some empty space | A for the drawn booths, then B for the empty part |

Ask the user if you're unsure. Copying the drawing is what organizers expect when their decorator already drew the booths.

## Mode A: copy the booths on the drawing

1. Use the background as set by floorplan-background. All coordinates must be in **floorplan px** (after its crop and scale).
2. Call `preview_drawing` on the floor plan's `backgroundImageUrl`. Work through it **region by region** (e.g. one block of rows at a time) with `region` zoomed so booth edges and numbers are readable.
3. For each booth, record `{boothNumber, x, y, width, height}`. Snap sizes to whole feet (multiples of 10 px), and snap edges to neighbours so back-to-back booths share an edge.
4. After each block, `create_booths` that block (up to 500 per call), then `render_floorplan_preview` with the same `region`. Compare it with the drawing and fix mismatches with `update_booths` before moving on.
5. **Colors over a printed plan:** use white booths (`#ffffff`), not transparent ones (`none`). A white booth covers the number printed on the drawing and shows its own label cleanly. A transparent booth shows both numbers slightly offset, which looks blurry. Use `none` only when the drawing has no numbers inside the booths.
6. **Spaces that are drawn but not sold** (sponsor kiosks, held spaces): create them with `forSale: false` and a "Not Available" label, so they stay on the map without a sellable product.

## Mode B: generate a grid

1. **Write the spec.** Turn the brief into a spec (format at the top of `scripts/layout.py`):
   - `area`: the free floor inside the walls, in floorplan px.
   - `exclusions`: stage, F&B, registration, pillars, and doors plus 10 ft clearance.
   - Also `aisleFt`, `crossAisleEvery`, `perimeter`, `entrance` and `numbering`.
   - Get `area` and `exclusions` from the background with `preview_drawing`, or from the hall size when there is no drawing.
2. **Run it:** `python scripts/layout.py spec.json > booths.json`. It prints the count per kind (inline / corner / perimeter). If the count is far from the booth count in the brief, adjust aisles, `crossAisleEvery` or the area and run it again. Tell the user the trade-off, e.g.: "With 10 ft aisles the hall fits 298 booths. You asked for 320; 8 ft aisles would fit 330."
3. **Apply other sizes.** For booths that aren't 10×10, change `width` / `height` in `booths.json` and remove the booths they cover. Islands (20×20) usually replace 4 booths at a row end or in the centre.

## Before creating booths

1. **Legend labels first.** Call `upsert_legend_labels` with the brief's labels: tiers like "10x10 Inline", "10x10 Corner", "20x20 Island", plus areas and zones. Keep the returned ids.
2. **Booth types** for each size: `create_booth_type` (e.g. "10x20 Inline", 100 × 200 px). It is safe to call again.
3. **Map each booth:**
   - `kind` → legend label: `corner` → "10x10 Corner", `inline` / `perimeter` → "10x10 Inline", islands → "20x20 Island".
   - price → from the brief, by size and kind.
   - `fontSize` → about 0.3 × the booth's short side (35 for 100 px booths).
   - Colors → from the brief.
4. **Reserved / sold booths** from the brief: create them with `companyId` (look the company up with `search_companies`). This marks them Sold without creating an invoice. Say so to the user.

## Create, then verify

1. Send `create_booths` in batches of up to 500. The tool refuses booth numbers that already exist, so retrying a batch after a timeout is safe.
2. Call `render_floorplan_preview`. Fix everything it reports **before** telling the user the plan is done:
   - `overlappingPairs` > 0 → move or resize with `update_booths`. Overlaps of 1–3 px are drawing noise, common when copying hand-drawn plans: push the lower or right-hand booth by that many px;
   - `outsideCanvas` > 0 → move inside, or enlarge the canvas (`update_floorplan`);
   - `repeatedNumbers` → renumber with `update_booths`;
   - booths over walls, pillars or stages on the background → move or delete them (`delete_booths` asks for confirmation).
3. Show the user the preview image and a summary: count by size and label, number range, price range.

## Changing an existing plan

- Read the booths with `search_booths`: `where` floorplanId, `select` boothId, boothNumber, x, y, width, height. It returns at most 100 rows per call, so page with `offset`.
- Move, renumber or recolor with `update_booths`. Only remove booths with `delete_booths`, after the user confirms. Sold booths can't be deleted or moved off their owner.
- If you get `floorplan_locked`, the plan is open in the editor: ask the user to close it. The editor's next save would otherwise overwrite your changes.
