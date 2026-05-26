---
name: nano-banana
description: Generate and edit AI images via Google's Gemini image models (Nano Banana / Nano Banana Pro) using a direct REST call to the Generative Language API — no MCP server, no npm install. Ships one bundled Python CLI (`scripts/generate.py`, pure stdlib) that handles generate / edit / continue-edit / history / get against an on-disk session log. Use when the user asks to generate an image, edit a photo, build an infographic or diagram, or iterate on a prior generation.
---

# Nano Banana — Direct Gemini API Skill

> Image generation that doesn't depend on an MCP server you forgot to install. One Python script, one API key, on-disk history.

## When to use

Invoke when the user asks to:

- generate an image from a text prompt;
- edit an existing image with instructions;
- refine the last image you made (the "continue editing" workflow);
- compose a multi-step series of images that need to reference each other (character consistency, before/after).

## Prerequisites

1. **`GEMINI_API_KEY`** in the environment. Get one at <https://aistudio.google.com/>. Free tier works for prototyping; image generation is metered.
2. **Python 3.9+** (uses only stdlib — no `pip install` needed).
3. The bundled CLI: `scripts/generate.py` (relative to this skill's directory).

The skill *does not* need an MCP server. The previous nano-banana skill required `nanobanana-mcp` / `nano-banana-mcp` via npx; this one talks to the Gemini REST API directly via `urllib`.

## The CLI surface

```
scripts/generate.py <subcommand> [args]
```

| Subcommand       | What it does                                                     |
|------------------|------------------------------------------------------------------|
| `generate`       | New image from a text prompt.                                    |
| `edit`           | Modify an existing image with text instructions.                 |
| `continue-edit`  | Refine the most recent image in history (or a specific index).   |
| `history`        | List past generations, most recent first.                        |
| `get`            | Print the path (or a meta field) for a history entry.            |

Always pass paths absolute. The script prints the final image path to stdout — capture it and reuse.

## Calling the CLI

The skill exists so you remember to call the CLI correctly. The contract:

```bash
SKILL_DIR="$(dirname "$(claude skill path nano-banana 2>/dev/null || echo ~/.claude/skills/nano-banana)")/nano-banana"
python3 "$SKILL_DIR/scripts/generate.py" generate \
  --prompt "<your prompt>" \
  --aspect 4:3 \
  --size 2K \
  --out /absolute/path/to/output.png
```

If you can't determine the skill's path programmatically, fall back to `~/.claude/skills/nano-banana/scripts/generate.py` (user-level install) or `<repo>/plugins/nano-banana/skills/nano-banana/scripts/generate.py` (when running inside the marketplace plugin).

### Generate

```bash
python3 .../scripts/generate.py generate \
  --prompt "Cozy coffee shop interior, watercolor illustration style, warm lighting, wooden furniture, steaming cup on table" \
  --aspect 16:9 \
  --size 2K \
  --out /tmp/coffee.png
```

`--out` is optional. The history copy is always written to `~/Documents/nanobanana_generated/<id>/image.<ext>` regardless; `--out` just copies it where you want.

Valid aspect ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`.
Valid sizes: `1K`, `2K`, `4K` (4K = up to 5632×3072 on `gemini-3-pro-image-preview`).

### Edit an existing image

```bash
python3 .../scripts/generate.py edit \
  --image /path/to/source.png \
  --instructions "Transform to winter scene: add snow on ground, frost on windows, overcast sky, cool blue grading" \
  --out /tmp/winter.png
```

If the source image lives inside the history dir, the new entry's `parent_id` is set automatically so you can walk lineage later.

### Continue editing the last image

```bash
# Defaults to the most recent entry (--index 0)
python3 .../scripts/generate.py continue-edit \
  --instructions "Make the lighting warmer, add golden hour glow"

# Or refine a specific past entry:
python3 .../scripts/generate.py continue-edit --index 3 --instructions "..."
python3 .../scripts/generate.py continue-edit --entry-id 1779825667-bbff19ad --instructions "..."
```

This is the session-aware feature the old MCP exposed as `continue_editing` — implemented here against the on-disk `history.jsonl`, so it survives session restarts.

### Inspect history

```bash
python3 .../scripts/generate.py history --limit 10
# [  0] 1779825667-bbff19ad  generate  Cozy coffee shop interior, watercolor illustration ...
# [  1] 1779825612-1f2a9d04  edit      Make the lighting warmer (edit of 1779825667)
```

For programmatic use, add `--json`.

### Resolve a history reference

```bash
# Path to the most recent image:
python3 .../scripts/generate.py get --index 0

# A specific meta field:
python3 .../scripts/generate.py get --index 0 --field prompt
```

## Selecting a model

The default is `gemini-3-pro-image-preview` (highest quality, 4K, best text rendering). Pass `--model gemini-2.0-flash-exp` for the faster/cheaper Gemini 2 path. The API returns whatever resolution the model produces; aspect ratio is a hint the server may interpret or ignore depending on model version.

## Prompting practice

Conceptual over prescriptive. Tell the model *what* and *why*; let it figure out *how*.

```
[Subject] + [Style] + [Mood] + [Constraints]
```

| Specify                | Examples                                              |
|------------------------|-------------------------------------------------------|
| **Subject**            | "A professional woman in a modern office"            |
| **Style**              | "watercolor illustration", "photorealistic", "3D render" |
| **Mood / lighting**    | "golden hour", "studio lighting", "overcast"         |
| **Constraints**        | "use teal (#557373) as primary color"                |
| **Negative prompt**    | append "Avoid: text, watermarks, deformed hands"     |

Aspect ratio cheat sheet:

| `--aspect` | Use case                                |
|------------|-----------------------------------------|
| `16:9`     | Slides, widescreen, dashboards          |
| `1:1`      | Social, profile, avatar                 |
| `9:16`     | Stories, mobile, vertical video         |
| `4:3`      | Traditional presentations, PR previews  |
| `3:2`      | Photography, print                      |
| `2:3`      | Vertical infographics, posters          |

## Critical limitations

### Text in images is unreliable for anything longer than 1-3 words.

Gemini's image models cannot consistently render legible multi-word text. For infographics or diagrams:

1. **Keep all in-image labels short** (1-3 words).
2. **Leave space** for any longer text and overlay it in an editor (ImageMagick, Figma, Keynote).
3. **Carry the full sentence in the surrounding markdown**, not the image.

Logos and brand wordmarks are even worse — never expect a generated logo to be correct. Designate space in the prompt ("clean empty space in the bottom-right for a logo") and composite the real logo file post-generation with ImageMagick.

### History dir defaults

By default, all generations land under `~/Documents/nanobanana_generated/`. Override with `--history-dir <path>` or `$NANO_BANANA_HOME`. Each entry is a subdirectory:

```
~/Documents/nanobanana_generated/
├── history.jsonl                 # append-only index, newest at bottom
└── 1779825667-bbff19ad/
    ├── image.jpg                 # or .png / .webp depending on model
    └── meta.json                 # prompt, model, parent_id, timestamps
```

`history.jsonl` is append-only; deleting individual entry dirs is fine but the JSONL line stays (and `get` will fail with "image_path does not exist" — clean both).

## Workflows

### One-shot infographic

```bash
python3 .../scripts/generate.py generate \
  --prompt "Sketchnote-style infographic explaining the 5 steps of a value stream — hand-drawn feel, single teal accent on white background, short labels only, 4:3 layout" \
  --aspect 4:3 --size 2K \
  --out /tmp/vsm-infographic.png
```

### Iterate on lighting / composition without redrawing

```bash
# First pass
python3 .../scripts/generate.py generate --prompt "..." --out /tmp/v1.png

# Refine
python3 .../scripts/generate.py continue-edit \
  --instructions "Soften the shadows, push the accent color slightly more teal (#557373)" \
  --out /tmp/v2.png

# Refine again
python3 .../scripts/generate.py continue-edit \
  --instructions "Tighten the typography" --out /tmp/v3.png
```

### Character consistency across multiple scenes

```bash
# Establish the character once
python3 .../scripts/generate.py generate \
  --prompt "A young woman with red curly hair, freckles, green eyes, blue jacket. Portrait, studio lighting." \
  --out /tmp/char.png

# Get the entry id you just produced
ID=$(python3 .../scripts/generate.py get --index 0 --field id)

# Subsequent scenes: edit from the established character
python3 .../scripts/generate.py continue-edit --entry-id "$ID" \
  --instructions "The same woman, now seated at a cafe reading a book, soft window light"
```

## Calling this skill from another skill

If you're writing another skill that needs an image, don't reinvent the prompt construction — invoke this skill via the Skill tool (or shell out to the CLI directly):

```bash
python3 ~/.claude/skills/nano-banana/scripts/generate.py generate \
  --prompt "<your prompt>" --aspect <ratio> --size <size> \
  --out <where the calling skill wants the file>
```

That's the entire integration surface. The CLI prints the final path to stdout; the calling skill picks it up from there.

## Troubleshooting

| Symptom                                | Likely cause / fix                                       |
|----------------------------------------|----------------------------------------------------------|
| `GEMINI_API_KEY not set`               | `export GEMINI_API_KEY=...` in the shell before invoking |
| HTTP 400 from API                      | Prompt rejected (safety) or aspect/size invalid for model |
| HTTP 403                               | API key invalid or quota exhausted                       |
| `no image returned; model said: ...`   | The model responded with text instead of an image — usually a safety / refusal. Re-phrase the prompt. |
| Garbled text in the output             | Expected for anything > 3 words. Overlay text post-gen.  |
| Wrong aspect ratio                     | Some model versions ignore the `aspectRatio` hint. Mention the ratio in the prompt too. |

## References

- API docs: <https://ai.google.dev/gemini-api/docs/image-generation>
- Models: `gemini-3-pro-image-preview` (default, 4K), `gemini-2.0-flash-exp` (faster), `gemini-2.0-flash-preview-image-generation`
- This skill's source: `plugins/nano-banana/` in `github.com/difflabai/marketplace`

End each session by printing the path of the file you produced (or the error you hit). Don't editorialise — the caller will use the path or read the error.
