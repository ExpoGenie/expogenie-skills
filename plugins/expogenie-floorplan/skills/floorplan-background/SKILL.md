---
name: floorplan-background
description: Put a venue drawing (PDF, PNG or JPEG) behind an ExpoGenie floor plan at the right scale, so booths drawn at 10 px = 1 ft line up with the drawing. Measures one known length on the drawing, then crops, rotates and rescales it through the ExpoGenie MCP. Use after floorplan-intake when the organizer has a hall drawing, or when someone says the background is the wrong size, misaligned, blurry, rotated or needs replacing.
---

# Floor plan background

The ExpoGenie editor draws the background image at its natural pixel size, with its top-left corner at (0, 0). The canvas becomes the image's size. Booths are drawn at **10 px = 1 ft**, so the drawing itself must be at 10 px per foot or the booths won't line up. Your job is to get the drawing to that scale.

Tools (ExpoGenie MCP): `preview_drawing`, `set_floorplan_background`, `render_floorplan_preview`, `create_floorplan`.

## 1. Get the drawing

`set_floorplan_background` needs an **https URL** (`imageUrl`) or base64 (`imageBase64`). In order of preference:

1. **A link** the organizer already has: the venue or decorator PDF on their website, or a shared Drive/Dropbox link that downloads the file directly.
2. **Upload it in the portal:** ask the user to open the floor plan editor, choose **Change background**, upload the file and close the editor. Then call `list_floorplans` (select `backgroundImageUrl`) and use that URL.
3. **Base64**, only for small files (under ~2 MB) that you can read from disk, e.g. in Claude Code.

For a PDF, ask which page holds the hall if there are several. Keep `pdfDpi` at 150 unless lines look too thin, and use the same `pdfDpi` in every call.

## 2. Measure one known length

1. Call `preview_drawing` with the drawing. It returns the image with a red (x) and blue (y) grid labelled in **source pixels**, plus the source size.
2. Find a feature whose real length you know. Best is the one from intake round 1.4 (e.g. "back wall = 240 ft"). Otherwise use a dimension printed on the drawing, or the scale bar. If none exists, use a booth outline printed on the drawing whose size the organizer confirms (e.g. 10 ft).
3. Zoom in with `region` on each end of the feature and read its pixel coordinates. Measuring the **longest** feature you can find gives the smallest error.
4. Compute `pixels` = distance between the two ends, then tell the user the result, e.g.: "The back wall is 1,850 px on the drawing = 240 ft, so I'll scale the drawing to 10 px per foot."

If you can't find anything to measure, ask the user. Don't guess a scale.

## 3. Set the background

Call `set_floorplan_background` with:

- `knownLength`: `{pixels, feet}` from step 2 (`pxPerFoot` stays 10).
- `crop`: `auto` (trims white margins). Use an explicit box to cut away title blocks, legends or a second hall printed on the same sheet.
- `rotate`: 90/180/270 only if the user wants the hall turned (e.g. entrance at the bottom).
- `scaleExistingBooths`: `true` only when you re-process the drawing the current booths were placed on (e.g. fixing the scale of an existing plan, with `imageUrl` = the current background). `false` for a new drawing.

If the floor plan doesn't exist yet, call `create_floorplan` first. A `floorplan_locked` error means the plan is open in the editor: ask the user to close the editor, then retry.

## 4. Check the scale

1. Call `render_floorplan_preview` and check the canvas size: `pageWidth` / 10 should be roughly the hall width in feet.
2. If the drawing shows booth outlines, call `preview_drawing` on the new `backgroundImage` URL and measure one. A 10 ft booth must be about **100 px** (±5%). If it isn't, fix it with `scaleFactor` = expected / measured on the current background (`crop: "none"`).
3. Report the result in one line, e.g.: "Background set: 3,240 × 2,180 px = about 324 × 218 ft, scale checked on booth 101 (100 px = 10 ft)."

## Limits

- Largest file: 25 MB.
- Largest scaled result: 30,000 px on a side. If the tool reports the result is too large, crop tighter.
- Very large halls (more than 1,500 ft long) can't fit at 10 px/ft. Tell the user and offer `pxPerFoot: 5`, but then every booth size and position must also use 5 px per foot.
