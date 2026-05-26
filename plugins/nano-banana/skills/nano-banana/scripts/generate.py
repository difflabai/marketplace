#!/usr/bin/env python3
"""Direct Gemini image-generation CLI for the nano-banana skill.

Replaces the MCP-server dependency with a plain HTTP call. Pure stdlib —
no pip install. Reads ``GEMINI_API_KEY`` from environment.

Subcommands:

  generate         Create a new image from a text prompt.
  edit             Modify an existing image with text instructions.
  continue-edit    Refine the most recent image in history.
  history          List past generations (most recent first).
  get              Print the on-disk path of a history entry by index or id.

Every call appends a record to ``history.jsonl`` and writes the image and
its meta under ``<history_dir>/<entry-id>/``. The default history dir is
``~/Documents/nanobanana_generated`` (matches the legacy MCP convention so
existing skill prose still points at the right place); override with
``--history-dir`` or ``$NANO_BANANA_HOME``.

Examples::

    generate.py generate --prompt "Sketchnote VSM" --aspect 4:3 --size 2K \\
      --out /tmp/out.png

    generate.py edit --image /path/in.png \\
      --instructions "Make the lighting warmer" --out /tmp/out.png

    generate.py continue-edit --instructions "Tighten the typography"

    generate.py history --limit 5

    generate.py get --index 0
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_HISTORY_DIR = Path("~/Documents/nanobanana_generated").expanduser()
HISTORY_FILE = "history.jsonl"

VALID_ASPECTS = {"1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"}
VALID_SIZES = {"1K", "2K", "4K"}


# --------------------------------------------------------------------- utils
def die(msg: str, code: int = 1) -> None:
    print(f"generate.py: {msg}", file=sys.stderr)
    sys.exit(code)


def api_key() -> str:
    k = os.environ.get("GEMINI_API_KEY")
    if not k:
        die("GEMINI_API_KEY not set in environment", code=2)
    return k


def history_dir(override: Path | None) -> Path:
    if override:
        return override.expanduser().resolve()
    env = os.environ.get("NANO_BANANA_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_HISTORY_DIR


def ensure_history_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def history_jsonl(hdir: Path) -> Path:
    return hdir / HISTORY_FILE


def new_entry_id() -> str:
    return f"{int(time.time())}-{uuid.uuid4().hex[:8]}"


def append_history(hdir: Path, record: dict) -> None:
    with history_jsonl(hdir).open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, separators=(",", ":")) + "\n")


def read_history(hdir: Path) -> list[dict]:
    p = history_jsonl(hdir)
    if not p.is_file():
        return []
    return [
        json.loads(line) for line in p.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def resolve_history_ref(hdir: Path, *, index: int | None,
                       entry_id: str | None) -> dict:
    items = read_history(hdir)
    if not items:
        die("history is empty", code=3)
    if entry_id is not None:
        for r in items:
            if r.get("id") == entry_id:
                return r
        die(f"no history entry with id {entry_id!r}", code=3)
    # Index: 0 means the most recent, like the old `history:0` reference.
    idx = index if index is not None else 0
    items.reverse()
    if idx < 0 or idx >= len(items):
        die(f"history index {idx} out of range (have {len(items)} entries)",
            code=3)
    return items[idx]


# ----------------------------------------------------------- API request shape
def _build_image_config(aspect: str | None, size: str | None) -> dict:
    """Construct the model's image-generation config block.

    The Gemini image API accepts an ``imageConfig`` block under
    ``generationConfig`` for aspectRatio / imageSize hints. Specifics
    drift between model versions; we send what's documented and let the
    server ignore anything unsupported.
    """
    cfg: dict = {}
    if aspect:
        cfg["aspectRatio"] = aspect
    if size:
        cfg["imageSize"] = size
    return cfg


def _call_api(model: str, payload: dict, *, timeout: float) -> dict:
    url = f"{API_BASE}/{model}:generateContent"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key(),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        die(f"HTTP {e.code} from Gemini API: {err_body[:600]}", code=4)
    except urllib.error.URLError as e:
        die(f"URL error talking to Gemini API: {e.reason}", code=4)
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        die(f"could not parse Gemini API response as JSON: {e}", code=4)


def _extract_image_bytes(api_response: dict) -> tuple[bytes, str]:
    """Pull the first inline image part out of the response.

    Returns (raw_bytes, mime_type). Raises via die() on a malformed
    response.
    """
    candidates = api_response.get("candidates") or []
    for cand in candidates:
        parts = (cand.get("content") or {}).get("parts") or []
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if not inline:
                continue
            data_b64 = inline.get("data")
            mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
            if data_b64:
                try:
                    return base64.b64decode(data_b64), mime
                except (TypeError, ValueError) as e:
                    die(f"could not base64-decode image: {e}", code=4)
    # No image part found — surface the model's textual reply if any, plus
    # safety/finish reasons, then die.
    text_parts: list[str] = []
    finish_reasons: list[str] = []
    for cand in candidates:
        if cand.get("finishReason"):
            finish_reasons.append(str(cand["finishReason"]))
        parts = (cand.get("content") or {}).get("parts") or []
        for part in parts:
            if "text" in part and part["text"]:
                text_parts.append(part["text"])
    msg = "no image returned"
    if finish_reasons:
        msg += f" (finishReason={','.join(finish_reasons)})"
    if text_parts:
        snippet = " | ".join(t.strip() for t in text_parts)[:400]
        msg += f"; model said: {snippet}"
    if "promptFeedback" in api_response:
        msg += f"; promptFeedback={json.dumps(api_response['promptFeedback'])[:300]}"
    die(msg, code=5)
    raise AssertionError("unreachable")  # for type-checkers


def _mime_to_ext(mime: str) -> str:
    return {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
    }.get(mime, "png")


# ---------------------------------------------------------------- subcommands
def cmd_generate(args: argparse.Namespace) -> int:
    hdir = ensure_history_dir(history_dir(args.history_dir))
    parts: list[dict] = [{"text": args.prompt}]
    payload: dict = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    img_cfg = _build_image_config(args.aspect, args.size)
    if img_cfg:
        payload["generationConfig"]["imageConfig"] = img_cfg
    resp = _call_api(args.model, payload, timeout=args.timeout)
    img_bytes, mime = _extract_image_bytes(resp)

    entry_id = new_entry_id()
    entry_dir = ensure_history_dir(hdir / entry_id)
    ext = _mime_to_ext(mime)
    img_path = entry_dir / f"image.{ext}"
    img_path.write_bytes(img_bytes)

    meta = {
        "id": entry_id,
        "kind": "generate",
        "model": args.model,
        "prompt": args.prompt,
        "aspect": args.aspect,
        "size": args.size,
        "mime": mime,
        "image_path": str(img_path),
        "parent_id": None,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (entry_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    append_history(hdir, meta)

    final_path = Path(args.out).expanduser() if args.out else img_path
    if args.out:
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_path.write_bytes(img_bytes)
    print(str(final_path))
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    hdir = ensure_history_dir(history_dir(args.history_dir))
    img_path = Path(args.image).expanduser()
    if not img_path.is_file():
        die(f"image not found: {img_path}", code=2)
    img_bytes = img_path.read_bytes()
    # Crude mime detection from suffix.
    suffix = img_path.suffix.lower().lstrip(".") or "png"
    mime_in = {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "webp": "image/webp",
    }.get(suffix, "image/png")

    payload = {
        "contents": [{
            "parts": [
                {"inlineData": {
                    "mimeType": mime_in,
                    "data": base64.b64encode(img_bytes).decode("ascii"),
                }},
                {"text": args.instructions},
            ],
        }],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    resp = _call_api(args.model, payload, timeout=args.timeout)
    out_bytes, out_mime = _extract_image_bytes(resp)

    entry_id = new_entry_id()
    entry_dir = ensure_history_dir(hdir / entry_id)
    ext = _mime_to_ext(out_mime)
    out_img = entry_dir / f"image.{ext}"
    out_img.write_bytes(out_bytes)

    # If the input image came from history, link the new entry to it.
    parent_id = None
    try:
        rel = img_path.resolve().relative_to(hdir.resolve())
        # Path is <entry-id>/image.<ext>
        if len(rel.parts) >= 2:
            parent_id = rel.parts[0]
    except (ValueError, OSError):
        pass

    meta = {
        "id": entry_id,
        "kind": "edit",
        "model": args.model,
        "instructions": args.instructions,
        "mime": out_mime,
        "image_path": str(out_img),
        "parent_id": parent_id,
        "source_image": str(img_path),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (entry_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    append_history(hdir, meta)

    final_path = Path(args.out).expanduser() if args.out else out_img
    if args.out:
        final_path.parent.mkdir(parents=True, exist_ok=True)
        final_path.write_bytes(out_bytes)
    print(str(final_path))
    return 0


def cmd_continue(args: argparse.Namespace) -> int:
    hdir = ensure_history_dir(history_dir(args.history_dir))
    prev = resolve_history_ref(hdir, index=args.index, entry_id=args.entry_id)
    # Re-enter edit with the previous image as source.
    edit_args = argparse.Namespace(
        image=prev["image_path"],
        instructions=args.instructions,
        out=args.out,
        model=args.model,
        timeout=args.timeout,
        history_dir=args.history_dir,
    )
    return cmd_edit(edit_args)


def cmd_history(args: argparse.Namespace) -> int:
    hdir = history_dir(args.history_dir)
    items = read_history(hdir)
    if not items:
        print("(empty)")
        return 0
    items.reverse()
    if args.limit:
        items = items[: args.limit]
    if args.json:
        print(json.dumps(items, indent=2))
        return 0
    for idx, r in enumerate(items):
        label = r.get("prompt") or r.get("instructions") or "(no description)"
        label = label[:80].replace("\n", " ")
        marker = "" if r.get("parent_id") is None else f" (edit of {r['parent_id'][:8]})"
        print(f"[{idx:>3}] {r.get('id', '?')}  {r.get('kind', '?'):<8}  {label}{marker}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    hdir = history_dir(args.history_dir)
    entry = resolve_history_ref(
        hdir, index=args.index, entry_id=args.entry_id,
    )
    if args.field:
        if args.field not in entry:
            die(f"history entry has no field {args.field!r}", code=3)
        print(entry[args.field])
    else:
        print(entry["image_path"])
    return 0


# ----------------------------------------------------------------- argparse
def _add_common_api_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Gemini model id (default: {DEFAULT_MODEL}).")
    p.add_argument("--timeout", type=float, default=120.0,
                   help="HTTP timeout in seconds (default 120).")
    p.add_argument("--history-dir", type=Path, default=None,
                   help=f"Override history dir (default: {DEFAULT_HISTORY_DIR}).")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=(
            "Direct Gemini image-generation CLI for the nano-banana skill. "
            "Pure stdlib. Reads GEMINI_API_KEY from environment."
        ),
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Create a new image from a text prompt.")
    g.add_argument("--prompt", required=True)
    g.add_argument("--aspect", choices=sorted(VALID_ASPECTS), default=None)
    g.add_argument("--size", choices=sorted(VALID_SIZES), default=None)
    g.add_argument("--out", default=None,
                   help="Also write a copy here. The history copy is always written.")
    _add_common_api_args(g)
    g.set_defaults(func=cmd_generate)

    e = sub.add_parser("edit", help="Modify an existing image.")
    e.add_argument("--image", required=True,
                   help="Path to source image.")
    e.add_argument("--instructions", required=True)
    e.add_argument("--out", default=None)
    _add_common_api_args(e)
    e.set_defaults(func=cmd_edit)

    c = sub.add_parser(
        "continue-edit",
        help="Refine a prior image (defaults to most recent).",
    )
    ref = c.add_mutually_exclusive_group()
    ref.add_argument("--index", type=int, default=None,
                     help="History index (0 = most recent).")
    ref.add_argument("--entry-id", default=None,
                     help="Specific history entry id.")
    c.add_argument("--instructions", required=True)
    c.add_argument("--out", default=None)
    _add_common_api_args(c)
    c.set_defaults(func=cmd_continue)

    h = sub.add_parser("history", help="List past generations, most recent first.")
    h.add_argument("--limit", type=int, default=20)
    h.add_argument("--json", action="store_true",
                   help="Emit JSON instead of a human-readable list.")
    h.add_argument("--history-dir", type=Path, default=None)
    h.set_defaults(func=cmd_history)

    gt = sub.add_parser("get", help="Print the path (or a meta field) of a history entry.")
    ref2 = gt.add_mutually_exclusive_group()
    ref2.add_argument("--index", type=int, default=None,
                      help="History index (0 = most recent).")
    ref2.add_argument("--entry-id", default=None)
    gt.add_argument("--field", default=None,
                    help="Print this meta field instead of the image path.")
    gt.add_argument("--history-dir", type=Path, default=None)
    gt.set_defaults(func=cmd_get)

    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
