---
name: floorplan-intake
description: Interview an event organizer and produce a complete floor plan brief for ExpoGenie, covering the venue drawing, scale, booth sizes, numbering, prices, unoccupied and occupied colors, legend labels and booth tags. Every question has a recommended default. Use when someone wants to create, set up, draw or build a floor plan, booth layout or exhibit hall map in ExpoGenie, before any floor plan is written through the ExpoGenie MCP.
---

# Floor plan intake

Your job is to collect everything needed to build one ExpoGenie floor plan, and nothing more. The output is a **floor plan brief** (JSON, format at the end). The floorplan-background, floorplan-layout and floorplan-publish skills consume it.

## How to ask

- Ask in **rounds**, at most 3–5 questions per round. Never ask everything at once.
- **Every question shows its recommended default.** The customer can answer "default" or "ok" to accept it.
- Start with a fast path: *"I can set this up with recommended defaults and only ask about your venue, booth sizes and prices. Or we can go through every option. Which do you prefer?"* On the fast path, ask only the questions marked **(required)** and use defaults for the rest.
- If the customer uploads a venue drawing or a booth spreadsheet, read it first. Pre-fill every answer you can from it (booth count, sizes, numbers, categories), then ask the customer to confirm those values instead of asking from scratch.
- Use the customer's units (feet or meters) throughout, and convert to pixels only in the brief.
- Do not invent prices. If the customer has none, say so and offer the options in round 4.

## Round 1: event and venue

| # | Question | Recommended default |
|---|----------|---------------------|
| 1.1 | Which event is this floor plan for? **(required)** (Look it up with the MCP `search_events` tool and confirm the name.) | — |
| 1.2 | The event already has its floor plan (`list_floorplans`; one per event). Tell the user its name and booth count. Keep that name or rename it? If it already has booths: keep them and add, or replace the unsold ones? | Keep the name; keep existing booths and add |
| 1.3 | Do you have a venue drawing (PDF, PNG, JPG, or DWG exported to PDF)? **(required: yes or no)** | No drawing → draw booths on a blank grid |
| 1.4 | One known real-world measurement on the drawing, e.g. "the back wall is 240 ft". **(required if there is a drawing)** | — |
| 1.5 | Feet or meters? | Feet |
| 1.6 | Approximate hall size, if there is no drawing (width × depth)? | Fit to the booth count + aisles |

## Round 2: booth sizes and layout

| # | Question | Recommended default |
|---|----------|---------------------|
| 2.1 | Which booth sizes are you selling, and how many of each? **(required)** | 10×10 (only size) |
| 2.2 | Name each size (this becomes the booth type)? | "10×10 Inline", "10×20 Inline", "20×20 Island" |
| 2.3 | Layout style: back-to-back rows, perimeter (along the walls), islands, or a mix? | Back-to-back rows + a perimeter row |
| 2.4 | Aisle width? | 10 ft (cross aisles 10 ft) |
| 2.5 | Areas to keep empty (entrances, F&B, stage, pillars, registration)? | Keep 10 ft clear in front of every door marked on the drawing |
| 2.6 | Should corners be priced or marked differently? | No |
| 2.7 | Any round tables, kiosks or pods? | None (drawn as ellipses when present) |

## Round 3: booth numbers and titles

| # | Question | Recommended default |
|---|----------|---------------------|
| 3.1 | Numbering scheme? | Hundreds per aisle: 100s, 200s, 300s…; odd numbers on one side of the aisle, even on the other |
| 3.2 | Where does numbering start? | Front-left (nearest the main entrance), increasing to the back |
| 3.3 | Prefix for each hall/room? | None. With more than one hall, use a letter prefix (A101, B101) |
| 3.4 | Booth title shown on the map? | The booth number |
| 3.5 | Font size on the map? | 0.3 × the booth's short side in px (35 for 100 px booths, 15 for 60 px), minimum 10 |

## Round 4: selling and prices

| # | Question | Recommended default |
|---|----------|---------------------|
| 4.1 | Will exhibitors buy booths online from the floor plan? **(required)** | Yes |
| 4.2 | Price for each booth size? **(required if 4.1 = yes)** | No default. Offer: (a) the customer gives a price per size, (b) a price per sq ft × area, (c) comparable-event recommendation when the recommend_booth_price tool is available, (d) leave unpriced and not for sale for now |
| 4.3 | Prices for the other sizes, if the customer gave only a 10×10 price? | Suggest 10×20 = 2×, 20×20 = 2.4×, corner +10% (typical ratios on live plans; confirm each) |
| 4.4 | Who can buy (exhibitor levels)? | Everyone |
| 4.5 | Booths that are reserved or already sold (sponsors, the organizer's own booths)? | None. If any, list booth number → company |
| 4.6 | Deposits / installments on booths? | Off |

## Round 5: colors and legend labels

The legend always has two built-in rows, **Unoccupied** and **Occupied**. Legend labels are optional extra rows, and each one has its own unoccupied and occupied color. Real plans use four kinds (see `references/corpus-defaults.md`): status, non-booth areas, product zones, and sponsor or price tiers.

| # | Question | Recommended default |
|---|----------|---------------------|
| 5.0 | Show each booth tier (size + position, e.g. "10x10 Inline", "10x10 Corner", "20x20 Island") as its own legend color? This is the most common legend on live plans. | Yes: one label per booth type sold, colored from the palette, with the price in the name only if the customer agrees |
| 5.1 | Booth colors: **Classic** (available white `#FFFFFF`, sold red `#FF2600`), **Soft** (available light blue `#B6CEEF`, sold orange `#F27405`), or **High contrast** (available yellow `#FEFB00`, sold red `#FF2600`)? | Classic; Soft when tier labels are used (5.0) |
| 5.2 | Track extra booth statuses on the map? | Yes: add status labels **Pending** `#FEFB00`, **Reserved / Hold** `#75D5FF`, **Unavailable** `#C0C0C0` |
| 5.3 | Non-booth areas to label (F&B, registration, lounge, stage)? | **F&B** `#9EFFB1` if the drawing shows catering |
| 5.4 | Group booths by product zone / pavilion, or by sponsor tier? | No |
| 5.5 | If yes: label names, and which booths or rows belong to each? | — |
| 5.6 | If yes: colors per label? | Use the palette below, with the **same color** for unoccupied and occupied, as most real plans do. If the customer wants sold booths to stand out inside a zone, use a darker shade of the label's color for occupied. |

Default label palette, from the colors real plans use most: `#FF2600` red, `#FEFB00` yellow, `#75D5FF` light blue, `#0096FF` blue, `#9DF5FB` aqua, `#DBC5F1` lavender, `#9EFFB1` mint, `#FFB347` orange, `#F7C6C9` pink, `#C0C0C0` silver.

## Round 6: booth tags

Booth tags are **filters for the exhibitor list** on the floor plan sidebar. They are not colors. Only about 1 plan in 10 uses them.

| # | Question | Recommended default |
|---|----------|---------------------|
| 6.1 | Should attendees be able to filter exhibitors by a tag? | No tags |
| 6.2 | If yes, which kind? Product or service categories, sponsor level, or the broker / sales rep representing the exhibitor? | Product or service categories |
| 6.3 | Also tag booth positions automatically (Corner, Island, Perimeter)? | No; offer only if corner pricing is used |
| 6.4 | Which booths or exhibitors get each tag? | Assign when exhibitors are added, not now |

## Before you finish

1. Summarize the brief in a short table: booths per size, number range, prices, colors, labels and tags. Mark every value the customer did not set as **(default)**.
2. Ask: *"Build it like this?"* Change only what they correct.
3. Output the brief below, then hand off to **floorplan-background** (if there is a drawing) or **floorplan-layout**.

## Floor plan brief (output)

Scale: **10 px = 1 ft** (a 10×10 booth = 100×100 px, matching the portal's built-in booth types). For meters, use 33 px = 1 m.

```json
{
  "eventId": "uuid",
  "floorplanId": "uuid of the event's existing floor plan",
  "floorplanName": "string (current name unless the user renames it)",
  "existingBooths": "keep-and-add | replace-unsold",
  "units": "ft",
  "pxPerUnit": 10,
  "background": { "file": "path-or-null", "knownMeasurement": { "label": "back wall", "length": 240 } },
  "hall": { "width": 300, "depth": 200 },
  "layoutStyle": "rows+perimeter",
  "aisle": 10,
  "keepClear": [{ "label": "Main entrance", "note": "10 ft clear" }],
  "boothTypes": [
    { "name": "10x10 Inline", "width": 10, "depth": 10, "count": 80, "price": 1500 },
    { "name": "20x20 Island", "width": 20, "depth": 20, "count": 4, "price": 5500 }
  ],
  "premiums": { "corner": 0.10, "island": 0.25 },
  "numbering": { "scheme": "hundreds-per-aisle", "start": "front-left", "oddEven": true, "prefix": "" },
  "title": "number",
  "fontSize": 35,
  "selling": { "online": true, "levels": "all", "deposits": false },
  "reserved": [{ "booth": "101", "company": "Sponsor Co" }],
  "colors": { "preset": "classic", "unoccupied": "#FFFFFF", "occupied": "#FF2600" },
  "legendLabels": [
    { "name": "Pending", "kind": "status", "unoccupied": "#FEFB00", "occupied": "#FEFB00", "booths": [] },
    { "name": "F&B", "kind": "area", "unoccupied": "#9EFFB1", "occupied": "#9EFFB1", "booths": ["F&B"] },
    { "name": "Grocery", "kind": "zone", "unoccupied": "#75D5FF", "occupied": "#75D5FF", "booths": ["100-199"] }
  ],
  "boothTags": [],
  "roundBooths": [],
  "defaultsUsed": ["colors", "aisle", "numbering"]
}
```
