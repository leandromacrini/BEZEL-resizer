# RetroArch Overlay Viewport Fixer

Batch-edits every `*.cfg` overlay file inside a folder tree, rescaling and re-centring
`custom_viewport_width`, `custom_viewport_height`, `custom_viewport_x`,
and `custom_viewport_y`.

Originally these overlays were tuned for **1920 × 1080 (16 : 9)**.  
If you use a **1680 × 1050 (16 : 10)** monitor (or any other resolution) the viewport
is no longer centred and the artwork looks off.  
This script fixes that in one go 🛠️.

---

## What it does

1. **Scans** every sub-directory of `ROOT_DIR` for `*.cfg`.
2. **Scales**
```

new_width  = round(old_width  × NEW_W / OLD_W)

new_height = round(old_height × NEW_H / OLD_H)


```markdown
3. **Centres**
```

new_x = (NEW_W − new_width)  // 2

new_y = (NEW_H − new_height) // 2


```yaml
4. **Backs up** the original file to `<name>.cfg.bak`.
5. **Overwrites** the `.cfg` with the new values (all other lines untouched).

---

## Quick start

```bash
git clone https://github.com/your-user/retroarch-overlay-fixer.git
cd retroarch-overlay-fixer

# 1. Edit the script:
#    - ROOT_DIR  : folder that holds your .cfg overlay files
#    - OLD_W/H   : resolution the cfgs were made for
#    - NEW_W/H   : your monitor’s resolution
nano fix_overlay.py

# 2. Run (Python 3.7+)
python3 fix_overlay.py
```

Each processed file is logged like:


```bash
↻ arcade-artwork/baluba.cfg
```



---


Options & tweaks
| Need | How | 
| --- | --- | 
| Dry-run (see changes without writing) | Comment out the final write_text() or add a --dry-run CLI flag (PRs welcome!). | 
| Different resolutions | Change the four constants at the top of the script. | 
| Backups elsewhere | Edit BACKUP_SUFFIX or copy to another folder before overwriting. | 
| CLI tool | Wrap constants with argparse – contributions appreciated! | 



---


Tested on
 
- Python 3.11 (Linux)
 
- RetroPie / Raspberry Pi (overlay files from `arcade-artwork/`)

Pure-Python → should also run on Windows and macOS.


---


License
MIT © 2025 Your Name — use freely, no warranty.
Enjoy your perfectly centred overlays! 🎮

