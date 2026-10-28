# What real ExpoGenie floor plans look like

These figures come from two sets of floor plans, with no event, client or exhibitor names included:
- 143 published floor plans (28,579 booths), the largest plan of each event on the older ExpoGenie Lite platform for 2023–2026.
- 15 hand-picked live plans on the current platform (65–1,095 booths; most of them mostly sold and priced).

Use them to justify a recommended default and to tell when an answer is unusual. Where the two sets differ, **follow the current platform**.

## Current platform: what good live plans do

**Scale.** 13 of 15 live plans use **100 px = 10 ft** (10 px per foot): 10×10 = 100×100 px, 10×20 = 100×200, 20×20 = 200×200. The venue drawing is resized so that its scale matches. Hobby and collectible shows use tables: 6×2 ft (60×20 px) and 8×2.5 ft (80×25 px).

**Legend labels are mostly booth tiers.** On live plans the most common label kind is **booth size + position/tier**, usually with its own color and often with the price in the name. Examples: "10x10 Inline", "10x10 Corner", "10x20 End Cap", "20x20 Island", "Premium Booth", "Standard Booth", "Island Tier 1 – $3,200". After that come:
- named zones / aisles, e.g. "AI Avenue", "Government Row", "Career Fair";
- non-booth areas, e.g. "Seating Area", "Show Service Spaces", "Non-Public Space", "Area Closed";
- availability, e.g. "Reserved Booth", "Not Available".

**Booth colors are customized.** Unlike older plans, live organizers usually pick their own pair, e.g. light blue available / orange sold, or pale yellow available / blue sold. A clear available color plus a strong sold color is the norm.

**Tags** are used for sponsor level (Diamond / Platinum / Silver), amenities ("Power"), position ("Corner / End Cap") and exhibitor categories.

**Booth types** are named by size and position ("10x10 Corner", "Standard Interior 10x10", "Vendor Table", "Check-in Booth").

**Numbering.** 13 of 15 use numbers by aisle (125, 225, 325… or 101, 102…). Table shows use letter + number (A01, G26).

**Font size** is 35 for 100 px booths (by far the most common), and 14–25 for tables and small booths.

**Price ratios** in priced live plans (a guide only; always confirm):

| Size | Price relative to 10×10 |
|---|---|
| 10×10 | 1× |
| 10×20 | 1.5–2.3× (typically 2×) |
| 20×20 | 2–5× (typically 2.4×) |
| Corner / premium aisle 10×10 | +5–15% |

Price of a 10×10 by kind of show:

| Kind of show | 10×10 price |
|---|---|
| Trade / association shows | $1,200–$4,250 (most $1,500–$3,000) |
| Consumer / hobby shows | $125–$675 |
| Tables | $25–$375 |

## Older Lite platform

## Size

| Measure | p10 | Median | p90 |
|---|---|---|---|
| Booths per floor plan | 33 | 106 | 629 |
| Share of booths sold at show time | 0% | 76% | 97% |

## Booth sizes

- When a plan is drawn without a scaled drawing, the editor convention is **100 px = 10 ft** (10 px per foot). The most common booth sizes are 100×100 px (10×10), 100×200 px (10×20) and 200×200 px (20×20).
- When a plan is drawn over a venue drawing, booths are in the drawing's pixels, e.g. 60×90 px or 45×60 px. Real feet then come only from a known measurement (see floorplan-background).
- 10×10 is the dominant size. In most plans one size covers more than 75% of booths; islands (20×20 and larger) are under 3%.
- 2.5% of booths are **ellipses** (round tables, kiosks, pods). Ask whether there are any.

## Aisles

The most common main aisle is **10 ft** (51 plans), then 12 ft (21), 8 ft (12) and 15 ft (12).

## Booth numbers

- The clearest pattern is **hundreds per aisle** (100s, 200s, 300s…), seen in 51 plans. Odd and even numbers face each other across the aisle.
- 82 plans mix schemes: letter prefixes for halls or islands, named spaces such as "F&B", and lettered sub-booths (101A, 101B).
- Simple sequential numbering (1, 2, 3…) is rare (5 plans) and is mostly used for small table-top shows.

## Label font size

The font size scales with booth size. Use these values:

| Booth short side | Font size |
|---|---|
| 100 px | 35 (editor default; most common) |
| 60 px | 15 |
| 45 px | 12 |

Rule of thumb: font ≈ 0.3 × the booth's short side in px, minimum 10.

## Colors

- Most booths keep the editor default of white for both states. Organizers usually show status and categories through **legend labels** rather than the booth's own colors.
- The most used legend colors are red `#FF2600`, yellow `#FEFB00`, light blue `#75D5FF`, blue `#0096FF`, aqua `#9DF5FB`, lavender `#DBC5F1`, silver `#C0C0C0` and mint `#9EFFB1`.
- Most legend labels use the **same color** for unoccupied and occupied.

## Legend labels (median 3 per plan, p90 14)

Four patterns cover nearly all plans:

1. **Status labels** (most common): Sold, Pending, Reserved / Hold, Unavailable.
2. **Non-booth areas**: F&B (food and beverage) is the single most used label name; others are Entrance and Registration.
3. **Product zones / pavilions**, mainly in food and retail shows: Grocery, Frozen, Chill, Dairy, Produce, Meat & Seafood, Bakery/Deli, Floral, Wellness, Multicultural, Professional Services, Store Supplies, Internal.
4. **Sponsor or price tiers**: Platinum / Gold / Silver / Bronze, Partner Sponsor, or one label per price ("$7,150").

## Booth tags

Only 10% of plans use booth tags. Those that do use them as an **exhibitor directory filter**:

- product or service categories (e.g. HR services: Training & Development, Legal Services, Relocation),
- sponsor level,
- the broker or sales-rep company representing the exhibitor.

Default: no tags unless the organizer wants attendees to filter the exhibitor list.

## Prices

Almost no booths carried an online price on this platform; most booth sales were priced offline. There is no data-driven default price, so always ask.

## Background layer

Both the old and the new editor draw the background image at (0,0) at its natural pixel size and set the page to the image's width and height. Booth coordinates are therefore in the image's pixels. To change the scale, resize the image itself.
