# ExpoGenie skills for Claude

Claude skills and plugins for [ExpoGenie](https://expo-genie.com). They work with the ExpoGenie MCP connector (`https://api.expogenie.io/mcp`).

## expogenie-floorplan

This plugin builds an event floor plan from a short interview with the organizer:

| Skill | What it does |
|---|---|
| `floorplan-intake` | Asks the organizer about the venue, booth sizes, numbering, prices, colors, legend labels and tags. Every question has a recommended default. |
| `floorplan-background` | Sets the venue drawing as the background, scaled to 10 px = 1 ft from one known measurement. |
| `floorplan-layout` | Places booths by copying the drawing's booth grid or by generating standard rows (`scripts/layout.py`). |
| `floorplan-publish` | Runs the full build, checks the result with a rendered preview, and hands the plan over. |

## Install

### claude.ai or the Claude desktop app (Pro / Max)

1. Turn on **Settings → Capabilities → Code execution and file creation**.
2. Download the four skills:
   - [floorplan-intake.zip](https://github.com/ExpoGenie/expogenie-skills/releases/latest/download/floorplan-intake.zip)
   - [floorplan-background.zip](https://github.com/ExpoGenie/expogenie-skills/releases/latest/download/floorplan-background.zip)
   - [floorplan-layout.zip](https://github.com/ExpoGenie/expogenie-skills/releases/latest/download/floorplan-layout.zip)
   - [floorplan-publish.zip](https://github.com/ExpoGenie/expogenie-skills/releases/latest/download/floorplan-publish.zip)
3. Go to **Settings → Skills → + Add → Upload a skill**, and upload each ZIP.

### Team / Enterprise organizations

An owner adds the plugin once for everyone:

- go to **Organization settings → Plugins & skills**;
- sync it from this GitHub repository, or upload [expogenie-floorplan-plugin.zip](https://github.com/ExpoGenie/expogenie-skills/releases/latest/download/expogenie-floorplan-plugin.zip);
- set it to *Installed by default*.

### Claude Code

```
/plugin marketplace add ExpoGenie/expogenie-skills
/plugin install expogenie-floorplan@expogenie
```

## Connect ExpoGenie

1. In the ExpoGenie portal, go to **Settings → ExpoGenie REST API** and create an API client for your event. Give it these permissions:
   - **Floorplans**: Read, Write, Update
   - **Booths**: Write, Update
   - **Tags** and **Company**: Read
2. In Claude, go to **Settings → Connectors → Add custom connector**:
   - **URL**: the MCP endpoint shown on that portal page;
   - **Advanced settings**: your Client ID and Client Secret.
3. Click **Connect**, then **Approve**.

Then start a chat: *"Create the floor plan for <your event>. The venue drawing is at <link>."*

## License

MIT
