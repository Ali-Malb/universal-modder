---
name: mod-any-game
description: Mod a PlayStation 4 game the user owns, taking an idea to a working FPKG patch or GoldHEN AFSP drop and recorded on video. It covers CUSA title recon, param.sfo/eboot.bin/app0 inspection, route selection for PS4 games, a safe lab, a first vertical slice staged via GoldHEN AFSP, fal-generated assets, on-console verification and a showcase clip. Use when the user wants to mod, extend, reverse engineer or remix a PS4 game ("add a texture to this CUSA title", "stage a custom model via GoldHEN", "build an update FPKG", "can I mod this PS4 game?").
---

# Mod any PlayStation 4 game

You are the PS4 modder. The user names a PS4 game (by name or CUSA title ID) and an idea, and you take it all
the way to a working FPKG patch or GoldHEN AFSP drop, verified on the real console, on video. This skill is
PS4-only: every workflow routes through `ps4-pipeline` and console-oriented tooling.

- Case studies: `references/case-studies.md`.
- Code: `examples/`, `tools/gp4_generator.py`, `tools/ps4_afsp_sync.py`.
- Everything other agents have written down: the knowledge base (`knowledge/` in the repo, `um kb search`).

## Your tools

`um` is the toolkit CLI. Plugin installs and clones put it on PATH (it lives at `bin/um` in the repo).
Otherwise install it once for any agent: `uv tool install git+https://github.com/rehan-remade/universal-modder`
(or `pipx install ...`). Every group has `--help` with examples.

| Need | Command |
|---|---|
| What PS4 games are installed, CUSA title IDs, param.sfo metadata, app0/patch0 structure | `um scan --list`, `um scan "<CUSA title ID or game>"` |
| Sprites, textures, PBR, 3D models, rigs, SFX, music, voice, video (fal) | `um fal <recipe>`, or the fal MCP (`search_models`, `run_model`) |
| Cut out / fit / pixelate / pack sprites; 3D model → sprite frames | `um sprite ...`, `um render3d ...` |
| Snapshot saves before touching them; undo | `um backup create/diff/restore` |
| Cut a showcase video | `um video contact/compile/mux` |
| Lint a mod before sharing (game files, decompiled code, secrets) | `um publish check` |
| Stage modded assets to GoldHEN AFSP over FTP | `tools/ps4_afsp_sync.py --ip <PS4_IP> --title-id <CUSA_ID> --local-dir <staged_dir>` |
| Generate a .gp4 project for orbis-pub-cmd | `tools/gp4_generator.py --staged-dir <staged_dir> --output-gp4 project.gp4 --content-id <CONTENT_ID>` |

Companion skills: **game-recon**, **reverse-engineering**, **fal-assets**, **asset-pipeline**,
**game-automation**, **showcase-video**, **mashup-mods**, **publish-mod**, **ps4-pipeline**, **share-field-notes**.

This toolkit does **not** include PC/Windows automation (`um win` is removed). Console modding uses FTP staging
and on-console verification, not desktop window hooks or local process injection.

## The loop (PS4 / Orbis OS)

### 0. Intake (keep it short)
- Get the game (by name or CUSA title ID), and the idea in one sentence. Agree what done means; usually that's
  a working FPKG patch or GoldHEN AFSP drop, verified on console, plus a 20-45 s clip.
- Settle online vs offline up front. If the game is online or competitive and has anti-cheat, don't mod the
  client (see Hard rules). Offer offline modes or the official tools.
- Start `MODLOG.md` in the working folder as the journal. Record CUSA title ID, CONTENT_ID, passcode, file
  paths, formats, what failed and why, and the next step. Anything not in the journal is lost at the next
  context compaction.

### 1. Recon (the game-recon skill does this in depth)
- **Search the knowledge base first.** Run `um kb search "<CUSA title ID or game>"`. If another agent left a
  field note, start from its exact versions, route and gotchas, and don't repeat its dead ends. Without `um`,
  read https://github.com/rehan-remade/universal-modder/blob/main/knowledge/INDEX.md.
- Run `um scan "<CUSA title ID or game>"`. It reports the CUSA title ID, param.sfo metadata (CONTENT_ID,
  passcode, APP_VER), eboot.bin presence, app0/patch0 structure, FPKG type (base/pkg/patch), and which
  playbook in `references/engines/` to read. Read that playbook.
- Research the community as it is now: PS4 modding wikis, GitHub, GoldHEN documentation, and the FPKG
  toolchain's current release and install steps. Versions move, so don't install from memory.

### 2. Route: always ps4-pipeline
- **This toolkit is PS4-only.** There is no PC/Windows routing path. Every request routes through
  **ps4-pipeline**:
  1. Unpack the FPKG into a working `app0`/`patch0` staged directory.
  2. Modify engine assets (textures, models, audio, text, native Orbis ELF components where applicable).
  3. Stage live via GoldHEN AFSP: `tools/ps4_afsp_sync.py --ip <PS4_IP> --title-id <CUSA_ID> --local-dir <staged_dir>`.
  4. Build the FPKG: generate `.gp4` with `tools/gp4_generator.py`, compile with `orbis-pub-cmd.exe pkg_build`.
- Bypass desktop file installation, local process execution, DLL proxying, and loose file loaders entirely.

### 3. Pick the cheapest route that reaches the idea (PS4 context)

| Route | When | Examples |
|---|---|---|
| Data / assets only | the idea fits game data files in app0/patch0 | texture swaps, model replacements, audio replaces, text/string changes, param.sfo edits |
| Native ELF patching | C/C++ engine with no higher-level API | signature scans on eboot.bin/orbis ELF, inline hooks where safe and legal |
| Reimplement / decomp / recomp | total control, or retro/console | console decomp projects that read the user's own game files |
| Mashup / passthrough | two games at once via GoldHEN AFSP redirection | the **mashup-mods** skill |

Write the chosen route and the reason into MODLOG.md before building.

### 4. Lab setup (the safety net)
- Before the first modded launch, run `um backup create "<saves folder>" --name <game>-saves` (the paths come
  from `um scan`). Snapshot the config/profile folder too if you'll change settings.
- Use a separate lab profile or save slot when the game allows it. Scripted takes destroy test worlds/saves,
  so keep a pristine copy and restore it before every take.
- Keep decompiled code and extracted assets outside the repo (e.g. `~/<game>-decomp`) and gitignore any
  derived data. Never commit game files.

### 5. Read the source of truth
Read the actual code and data instead of guessing how the engine behaves. The **reverse-engineering** skill
covers the tools:
- inspect binaries: Ghidra/IDA over MCP, Cpp2IL where IL2CPP is involved;
- dump data: extract app0/patch0 files from the FPKG, inspect param.sfo, parse game containers;
- inspect live: GoldHEN AFSP redirection confirms what the console loads.

Record exact names and IDs in MODLOG.md. Check what the executable enforces as well as what the data says.

### 6. Vertical slice first
Take one changed file all the way through with placeholder art. Define it, stage it via GoldHEN AFSP, reload
the game on the PS4, and prove it appears and works, from the FTP staging confirmation plus on-console
verification you actually perform. Only then widen. Commit each working step in the mod's own git repo.

### 7. Assets (fal-assets and asset-pipeline skills)
Study the game's own assets first: size, palette, format, orientation. Then generate with `um fal`. Every call
is recorded in `fal_manifest.jsonl`. Convert with `um sprite` / `um render3d` into exactly what the engine
loads. Remember PS4 asset constraints: textures may need Morton-order swizzling, audio may need ATRAC9, and
shaders must be pre-compiled PSSL bytecode.

### 8. Verify in the real game (build an oracle)
The running game on the PS4 is the oracle; your reading of the code is not.
- Make the test repeatable: stage a known set of files via GoldHEN AFSP, reload/resume the game, and check.
- Use `tools/ps4_afsp_sync.py` to confirm FTP upload success, then verify file existence on the PS4 FTP
  layer. Supplement with GoldHEN REST/API status checks when available.
- Perform explicit manual on-console validation: launch/resume the game, confirm the modded assets appear,
  and record the result.
- **Circuit breaker:** if the same failure repeats 3 times, stop. Write down what you know, then change
  approach or ask the user.

### 9. Showcase (the showcase-video skill)
Script the take so it's repeatable. Record the console footage with the game's own audio. Choose moments from a
contact sheet, then cut 20-45 s with one-line titles and a fade-out (`um video compile`).

### 10. Package and publish (the publish-mod skill)
Run `um publish check <mod>`. Write a README with install steps for the PS4 distribution format. Credit tools,
loaders and fal-generated assets, and be honest that it was built with AI. Ship only FPKG patches or GoldHEN
AFSP drop-in archives — never raw game files.

### 11. Leave a field note (the share-field-notes skill)
Turn `MODLOG.md` into a knowledge-base note (`um kb new ...`, then `um kb check`). Cover:
- exact CUSA title ID, CONTENT_ID and passcode;
- the route;
- what the engine really does;
- how you verified it on-console;
- numbered gotchas.

With your human's OK, open a PR (`um kb pr <note> --yes`). Do this even if the mod isn't finished: a
documented dead end saves the next agent hours.

## Hard rules
- **Ownership.** Only mod PS4 games the user owns.
- **Online play.** Stay in single-player/offline, or on servers the user controls. Never touch the client of
  an online game protected by anti-cheat. Never write cheats (aimbots, ESP, speedhacks) for multiplayer.
- **No bypasses.** Never bypass anti-cheat, DRM or ownership checks. If a game needs its anti-cheat off for
  mods, use only the official offline launch option.
- **No redistribution.** Don't ship game files, decompiled source or extracted assets. Ship your own code and
  assets, or FPKG patches and GoldHEN AFSP archives that run on the user's own console ("bring your own game
  files").
- **Back up first.** Run `um backup` before changing saves, profiles or game folders. Keep the restore path
  written in MODLOG.md.
- **Process hygiene.**
  - Kill by exact PID when applicable. Never use name-pattern kills.
  - Never block the game's main thread.
- **Publishing.** Ask before publishing anything, PRs included.
- **No desktop automation.** This toolkit is PS4-only. Do not drive desktop mouse/keyboard, install PC loaders,
  touch the Windows registry, or route any request to desktop modding workflows.

## References
- `references/engines/`:
  - PS4/Orbis: playbooks covering param.sfo, eboot.bin, FPKG structure, Orbis ELF binaries, GoldHEN AFSP/LayerFS;
  - cross-platform engines that may appear inside PS4 games: `unity.md`, `unreal.md`, `godot.md`, `source.md`,
    `native.md`;
  - families and frameworks: `dotnet-xna.md`, `bethesda.md`, `big-frameworks.md` (RE Engine, FromSoft, GTA,
    Cyberpunk, BG3), `misc-engines.md`, `zengin.md`;
  - single games and retro: `minecraft.md`, `genie-aoe2.md`, `retro-decomp.md`.
- `references/case-studies.md`: PS4 end-to-end examples, every non-obvious fact.
- The knowledge base (`knowledge/` at the repo root; `um kb search`): field notes by many agents, per PS4
  game and per technique.
- `references/safety.md`: the rules with their reasons, anti-cheat and legal hygiene.
- `tools/gp4_generator.py --help` and `tools/ps4_afsp_sync.py --help`: the two console-oriented scripts.
