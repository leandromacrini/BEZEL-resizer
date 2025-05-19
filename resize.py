#!/usr/bin/env python3
"""
Batch-adjust RetroArch overlay *.cfg files:

1. Scales custom_viewport_width / _height from 1920×1080 → 1680×1050.
2. Re-centres the viewport by recalculating custom_viewport_x / _y.
3. Creates a *.bak backup next to each edited file.

Author: <your name>
"""

import pathlib
import re
import shutil

# ------------------------------ SETTINGS ------------------------------------
ROOT_DIR      = pathlib.Path("./roms")  # <-- EDIT THIS
OLD_W, OLD_H  = 1920, 1080     # original target resolution
NEW_W, NEW_H  = 1680, 1050     # your monitor’s resolution (16:10)
BACKUP_SUFFIX = ".bak"         # backup extension
# ---------------------------------------------------------------------------

ratio_w = NEW_W / OLD_W        # width scale factor
ratio_h = NEW_H / OLD_H        # height scale factor

# Regex that matches:  custom_viewport_width/height/x/y = <number>
cfg_line = re.compile(
    r"^(custom_viewport_(width|height|x|y))\s*=\s*(\d+)\s*$",
    re.I
)

def process_file(path: pathlib.Path) -> None:
    """Read, transform, and overwrite one .cfg file."""
    print("↻", path.relative_to(ROOT_DIR))

    # --- create backup ------------------------------------------------------
    shutil.copy2(path, path.with_suffix(path.suffix + BACKUP_SUFFIX))

    values = {}          # will store new width/height (and later x/y)
    parsed_lines = []    # keep order of lines

    # First pass: scale width/height; keep placeholders for x/y
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        m = cfg_line.match(line)
        if not m:
            parsed_lines.append(line)
            continue

        key, kind, num = m.group(1), m.group(2).lower(), int(m.group(3))

        if kind == "width":
            new_val = round(num * ratio_w)
            values["width"] = new_val
            parsed_lines.append(f"{key} = {new_val}\n")
        elif kind == "height":
            new_val = round(num * ratio_h)
            values["height"] = new_val
            parsed_lines.append(f"{key} = {new_val}\n")
        else:
            # store a placeholder; we’ll fill x/y after width/height are known
            parsed_lines.append((key, kind))

    # Ensure width & height were found
    if "width" not in values or "height" not in values:
        print("   ! width/height missing, skipped.")
        return

    # Compute centred x / y
    values["x"] = (NEW_W - values["width"]) // 2
    values["y"] = (NEW_H - values["height"]) // 2

    # Second pass: replace placeholders for x/y
    final_lines = []
    for item in parsed_lines:
        if isinstance(item, tuple):           # it was a placeholder
            key, kind = item
            final_lines.append(f"{key} = {values[kind]}\n")
        else:
            final_lines.append(item)

    # Overwrite file with the updated lines
    path.write_text("".join(final_lines), encoding="utf-8")

def main() -> None:
    print("The Bezel Project - Custom Aspect Ratio Resizer\n")
    for cfg_file in ROOT_DIR.rglob("*.cfg"):
        process_file(cfg_file)
    print("\nOperation completed")

if __name__ == "__main__":
    main()
