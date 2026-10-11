---
name: publish-mod
description: Package and release a finished PS4 mod. Covers the pre-release lint (no game files, decompiled code or leaked keys), README and install steps for PS4 distribution, credits and AI disclosure, versioning, and the two PS4 distribution formats: standalone update FPKG (pkg_ps4_patch via orbis-pub-cmd) and GoldHEN AFSP drop-in archive (.zip for /data/GoldHEN/AFSP/<TITLE_ID>/). No PC mod distributors. Use when the user wants to ship, share, release or post a PS4 mod.
---

# Publish a PS4 mod

## 1. Lint
```bash
um publish check ./MyMod
```
- **FAIL:** files byte-identical to game files, leaked keys (fal/Anthropic/OpenAI/GitHub/AWS), `.env` files.
- **WARN:** decompiler fingerprints in source (`FUN_`/`DAT_`/`sub_` names, "Decompiled with" headers), large
  engine archives, absolute user paths, a missing README, fal assets without credit.

Fix every FAIL. Resolve each WARN deliberately.

## 2. Package the PS4 way

This toolkit is PS4-only. There are no PC mod distributors (Nexus Mods, Thunderstore, Vortex, Steam Workshop).
Distribute only via the two PS4 formats below.

| Distribution format | Package | How it ships |
|---|---|---|
| Standalone Update FPKG | Build with `orbis-pub-cmd.exe` from a `pkg_ps4_patch` GP4 project that matches the base game `CONTENT_ID` and passcode exactly. | Share the `.pkg` output of `orbis-pub-cmd.exe pkg_build`. The user installs it on their PS4 as an update patch. |
| GoldHEN AFSP Drop-in Archive | A `.zip` structured for drop-in deployment to `/data/GoldHEN/AFSP/<TITLE_ID>/`. | Share the `.zip`. The user extracts it on their PS4 (or via FTP) into the GoldHEN AFSP path and reloads/resumes the game. |

### Standalone Update FPKG
1. Stage the modded `app0`/`patch0` content in a working directory.
2. Generate the `.gp4` project:
   ```bash
   python tools/gp4_generator.py \
     --staged-dir <staged_dir> \
     --output-gp4 project.gp4 \
     --content-id <CONTENT_ID> \
     --passcode <32_CHAR_PASSCODE> \
     --type pkg_ps4_patch
   ```
3. Compile the package:
   ```bash
   orbis-pub-cmd.exe pkg_build project.gp4 ./dist/
   ```
4. The output `.pkg` is the distribution artifact. Distribute it as a standalone update FPKG.

### GoldHEN AFSP Drop-in Archive
1. Stage the modded `app0`/`patch0` content in a working directory with the correct internal layout.
2. Zip the staged directory so that extracting it drops files directly into
   `/data/GoldHEN/AFSP/<TITLE_ID>/`. The zip's internal paths should mirror the `app0`/`patch0` structure
   expected under the AFSP path.
3. Distribute the `.zip`. The user extracts it on the PS4 (via FTP or a USB transfer + manual copy) into
   `/data/GoldHEN/AFSP/<TITLE_ID>/`, then reloads or resumes the game.

Do not distribute raw game files, extracted FPKG contents, or decompiled binaries. Ship the patch FPKG or the
AFSP drop-in archive that applies the user's own mods to their own game install.

## 3. README (in the zip and on the page)
- What it adds: bullets, a GIF or the showcase video.
- Requirements: game version (CUSA title ID, APP_VER from param.sfo), GoldHEN version if AFSP-dependent.
- Install steps for the chosen format:
  - **FPKG:** install the update patch on the PS4.
  - **AFSP drop-in:** extract the zip to `/data/GoldHEN/AFSP/<TITLE_ID>/`, reload/resume the game.
- Uninstall and troubleshooting (where the log is, how to revert the AFSP layer).
- Compatibility: multiplayer? Known conflicts? GoldHEN version requirements?
- Credits:
  - the FPKG toolchain (LibOrbisPkg / orbis-pub-cmd) and GoldHEN;
  - references you learned from;
  - **"Art/audio generated with fal (fal.ai) using <models>"** (`fal_manifest.jsonl` lists them);
  - honest AI disclosure (which agent and model built it).
- License for your code (MIT/Apache is common). Your assets' terms follow the models' licenses.

## 4. Version and changelog
Use semver in the manifest/build file, name the supported game version (CUSA title ID + APP_VER), and keep a
changelog. When the game updates, re-run the on-console test before bumping.

## 5. The post
- Lead with the video: the showcase-video skill; 20-45 s, gameplay within 2-3 s.
- Post text: the hook, what it is, the "how" credit (which agent + fal built it), a link.
- If the video uses anyone else's footage, credit them by handle and ask first.
- Publishing is always the user's call. Draft it, show them, and let them press the button.

## What this skill does NOT cover
- **No PC mod distributors.** Nexus Mods, Thunderstore, Vortex, mod.io, and Steam Workshop are out of scope for
  this PS4-only toolkit.
- **No desktop packaging.** There are no `.tmod`, `.dll` plugin, `manifest.json` BepInEx, or `.jar` Minecraft
  packages here.
- **No game file redistribution.** Never ship the base game's FPKG, extracted app0/patch0, or decompiled
  binaries. Ship only the patch FPKG or the AFSP drop-in archive.
