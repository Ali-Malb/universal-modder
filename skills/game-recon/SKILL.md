---
name: game-recon
description: Figure out how a specific installed game can be modded, before writing any mod code. Covers where it's installed, the engine and version, managed vs native code, anti-cheat, loaders already present, save and config folders, and the community's modding route. Use when the user asks "can I mod <game>?", "what engine is <game>", "how do people mod <game>", or at the start of any modding task. Produces MODDING_PLAN.md.
---

# Game recon

Goal: in about five minutes, know what you're dealing with and which route to take. Write the answer down
so every later step can rely on it.

## 0. Has another agent been here?
`um kb search "<game>"` (and the engine name). A field note in the shared knowledge base can hand you the
working versions, the route, and the gotchas before you touch anything. See the **share-field-notes** skill.

## 1. Find it and fingerprint it
```bash
um scan --list                 # PS4 game installs: CUSA title IDs, param.sfo metadata, eboot.bin, app0/patch0
um scan "<CUSA title ID or folder>"     # engine, version, eboot.bin (SELF/ELF), anti-cheat, FPKG type, routes
um scan "<game>" --json        # the same, machine-readable
```
`um` lives at `bin/um` in the universal-modder repo (plugins and clones put it on PATH). Anywhere else:
`uv tool install git+https://github.com/rehan-remade/universal-modder`.

`um scan` reads files only. It indexes the PS4 install (bounded), reads param.sfo, checks eboot.bin encryption
state (SELF vs decrypted ELF), maps known PS4 games to their FPKG structure, and points to the playbook to
read: `skills/mod-any-game/references/engines/<engine>.md`.

The scan can't see everything, so check these by hand:
- **Game not in a store library** (standalone folder): pass the folder path.
- **Several engines' signals:** launchers and web helpers are common. The top score wins, but read the
  "also" line.
- **Online-only or live-service games:** treat them as protected even if nothing was detected.

## 2. Research the living community (always; versions move)
Search, in order:
1. "<game> PS4 modding" / "<game> GoldHEN" / "<game> FPKG". The game's modding community may have a wiki
   or documentation.
2. GitHub: "<game> PS4 mod", "<game> modding api", "<game> decompile", "<game> sdk", "<engine> PS4 mod
   loader".
3. Recent posts (X/Reddit/Discord announcements) for new frameworks. The loader might be days old.

Capture: the toolchain's name, repo, **current version and install steps**, the game versions it supports, a
"hello world" example mod, and where logs go.

## 3. Decide
- **Can it be modded safely?** Look at anti-cheat, online-only parts, the EULA or mod policy, and the
  ownership checks (see `skills/mod-any-game/references/safety.md`). If not: say so, and offer what is
  possible (official tools, offline modes, a different game with the same idea).
- **Route:** data/asset mod (app0/patch0) > native ELF patching > reimplementation/mashup. Pick the first
  that reaches the user's idea. All routes go through ps4-pipeline.

## 4. Write MODDING_PLAN.md
```markdown
# <Game> PS4 modding plan
- CUSA Title ID: <CUSAXXXXX>
- CONTENT_ID: <content_id>   Passcode: <32_char_passcode>
- APP_VER: <x>   FPKG type: <base | patch>
- Engine: <engine + version>, code: native / IL2CPP / managed, 64-bit
- Anti-cheat / online: <none | what + verdict>
- Saves: <path>   Config: <path>   Logs: <path>
- Toolchain: <FPKG tool + version>, GoldHEN <version>
- Chosen route for "<idea>": <route> because <reason>
- Lab plan: backup <folders> (um backup), staged dir <how>, GoldHEN AFSP sync <how>
- Unknowns to resolve first: <list>
```
Then continue with the mod-any-game PS4 loop (lab setup → source of truth → vertical slice → GoldHEN AFSP
 staging → on-console verify).
