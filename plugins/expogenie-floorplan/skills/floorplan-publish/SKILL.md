---
name: floorplan-publish
description: Run the whole ExpoGenie floor plan build end to end. Interview the organizer, set the background, lay out booths with labels, tags and prices, verify with a rendered preview, and hand over a ready-to-sell floor plan. Use when someone asks to create, build, set up or redo a floor plan or booth map for an ExpoGenie event, or to finish one that floorplan-intake started.
---

# Build and publish an ExpoGenie floor plan

This skill orders the other three skills and owns the final check. Follow the steps in order, and don't skip the checks.

## 0. Before anything

- **Connection:** the ExpoGenie MCP must be connected. Call `list_events`. If it fails, tell the user to connect the ExpoGenie connector, and stop.
- **Event:** find the event with `search_events` and confirm its name and dates with the user.
- **Existing plan:** call `list_floorplans` for the event.
  - If a plan exists, ask: add to it, replace it, or create a second floor plan (e.g. a second hall)?
  - **Replacing** means deleting booths, so get an explicit yes first. Sold booths are never deleted.
- **Permissions:** the API client needs Floorplans Read/Write/Update, Booths Write/Update (Delete only for replacing), and Tags. A `forbidden` error names the missing permission. Tell the user to tick it under **Settings → ExpoGenie REST API**.

## 1. Interview

Run **floorplan-intake**: show recommended defaults, use the fast path when the user wants it, and confirm the brief summary table.

## 2. Background

Run **floorplan-background** if there is a drawing. Otherwise call `create_floorplan` with a canvas that fits the hall: (hall feet + 20) × 10 px on each side.

## 3. Layout

Run **floorplan-layout**: legend labels, then booth types, then booths in batches, then the preview check.

## 4. Final check

Call `render_floorplan_preview` once more on the whole plan. The plan is ready only when all of these are true:

- [ ] `overlappingPairs` = 0, `outsideCanvas` = 0, `repeatedNumbers` empty
- [ ] booth count by size matches the brief (or the difference was agreed with the user)
- [ ] every booth for sale has a price above 0, unless the user chose unpriced
- [ ] booths line up with the drawing in at least two zoomed regions: one corner and one centre
- [ ] the legend shows the agreed labels, and every booth tier has its label

## 5. Hand over

Give the user:

1. the preview image;
2. a short summary: floor plan name, canvas size in feet, booths per size and per label, number range, price range, sold/reserved count;
3. **next steps in the portal:**
   - open the floor plan editor to fine-tune it;
   - check **Shop → Booths** for the booth products;
   - turn on online sales when ready;
   - remember the editor locks the plan while it is open, so close it when done.

Never say the floor plan is ready while a check above fails. Say what is left instead.

## Safety rules

- Ask before deleting a floor plan or any booths, and name what will be deleted.
- Never change a sold booth's owner. Sales go through invoices.
- Prices create real shop products. Confirm prices before creating booths for an event that is already selling.
- When working on a live event (not a test event), say so once before the first write.
