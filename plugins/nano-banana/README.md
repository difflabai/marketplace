# nano-banana

Direct Gemini image-generation skill for Claude Code. No MCP server, no npm install.

## What this is

A single skill (`/nano-banana`) wrapping a pure-stdlib Python CLI that calls Google's Gemini Generative Language API directly. Replaces the MCP-based nano-banana skill whose recommended npm package (`nanobanana-mcp`) does not exist on the registry.

The CLI supports the same session-aware features the MCP exposed (`continue_editing`, `get_image_history`) implemented against an on-disk `history.jsonl` log — so sessions survive restarts.

## Install

Add this plugin to your marketplace:

```bash
claude marketplace add https://github.com/difflabai/marketplace
claude plugin install nano-banana
```

Set the API key in your environment (get one at <https://aistudio.google.com/>):

```bash
export GEMINI_API_KEY=...
```

That's it. No `claude mcp add`. The skill just shells out to `scripts/generate.py`.

## Use

Once installed, the `/nano-banana` skill becomes available. You can also invoke the bundled CLI directly:

```bash
python3 ~/.claude/skills/nano-banana/scripts/generate.py generate \
  --prompt "A clean infographic explaining ..." \
  --aspect 4:3 --size 2K --out /tmp/out.png

python3 ~/.claude/skills/nano-banana/scripts/generate.py history --limit 5

python3 ~/.claude/skills/nano-banana/scripts/generate.py continue-edit \
  --instructions "Make the lighting warmer"
```

See `skills/nano-banana/SKILL.md` for the full surface.

## On-disk history

All generations land under `~/Documents/nanobanana_generated/` by default (override with `--history-dir` or `$NANO_BANANA_HOME`). Each entry is a subdirectory with `image.<ext>` + `meta.json`, plus an appended line in `history.jsonl`.

## License

MIT.
