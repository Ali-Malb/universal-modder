# universal-modder

A PlayStation 4 FPKG and GoldHEN modding toolkit and a shared knowledge base for AI coding agents: Claude
Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode and anything else that reads `AGENTS.md`. When
someone opens an agent in this repo, they want to **mod a PS4 game** they own, or to learn how a PS4 game was
modded via FPKG packages and GoldHEN live staging.

## Target platform
This toolkit targets **PlayStation 4 (Orbis OS)** exclusively. Every workflow, tool and reference in this
repo is oriented around PS4 modding:
- **CUSA Title IDs**, `param.sfo`, `eboot.bin`, `.pkg` packages, `app0`/`patch0` directories.
- **FPKG unpacking and repacking** via LibOrbisPkg or `orbis-pub-cmd`.
- **GoldHEN live asset redirection** via AFSP/LayerFS over FTP at `/data/GoldHEN/AFSP/<TITLE_ID>/`.
- **GP4 project generation** for `orbis-pub-cmd` patch compilation.

PC/Windows modding workflows (desktop loaders, DLL injection, Win32 automation, Steam Workshop, Nexus Mods,
Thunderstore) are **out of scope** for this repository.

## Start here
1. **Read `skills/mod-any-game/SKILL.md` and follow its loop:** intake → recon → route → lab (backups) →
   source of truth → vertical slice → assets → verify in the real game → showcase → publish.
2. **Search the knowledge base first:** `bin/um kb search "<game or CUSA title ID>"`. Other agents may already
   have written down the exact versions, routes and gotchas (`knowledge/INDEX.md`).
3. **At the end, share what you learned:** write a field note (`bin/um kb new ...`) and, once your human
   agrees, open a PR (`bin/um kb pr <note> --yes`). See `knowledge/README.md` and `CONTRIBUTING.md`.

## Tools
- **`bin/um`** is the Python CLI, and it sets itself up with `uv`.
  - Put it on PATH: `export PATH="$PWD/bin:$PATH"`, or install it anywhere with
    `uv tool install git+https://github.com/rehan-remade/universal-modder`.
  - Every group has `--help`:
    - `scan`: PS4 games, CUSA title IDs, param.sfo metadata, eboot.bin, app0/patch0 structure, FPKG routes
    - `fal`: sprites, textures, PBR, 3D, rigs, SFX, music, voice, video via fal's REST API
    - `comfy`: images from a local ComfyUI server, with no API key
    - `sprite` / `render3d`: art → engine-ready frames (`render3d` needs Blender on PATH or `BLENDER=...`)
    - `video`: contact sheets and EDL showcase edits
    - `backup`: snapshot and restore saves
    - `publish`: pre-release lint (FPKG and GoldHEN AFSP distribution checks)
    - `kb`: the knowledge base
  - The `um win` group has been removed from this PS4-only build. There is no desktop window automation, Win32
    input, or local process injection in this toolkit.
- **fal MCP server:** `https://mcp.fal.ai/mcp` with header `Authorization: Bearer $FAL_KEY`.
  - It's pre-configured per agent: `.mcp.json` (Claude Code), `.codex/config.toml` (Codex),
    `.cursor/mcp.json` (Cursor), `.vscode/mcp.json` (VS Code / Copilot), `gemini-extension.json`
    (Gemini CLI), `opencode.json` (OpenCode).
  - No MCP? `um fal` does the same over REST.
- **Skills** (`skills/*/SKILL.md`, Agent Skills format) are copied where agents look for them in a clone:
  `.agents/skills` (Codex, Gemini CLI, Copilot, Cursor, OpenCode) and `.claude/skills` (Claude Code). Edit
  `skills/`, then copy it over; a test fails while the copies differ.
- **PS4 tooling:**
  - `tools/gp4_generator.py` — generate `.gp4` project files for `orbis-pub-cmd` from staged `app0`/`patch0`
    content.
  - `tools/ps4_afsp_sync.py` — recursive FTP sync of modded assets to
    `/data/GoldHEN/AFSP/<TITLE_ID>/` on the PS4.
- **Engine playbooks:** `skills/mod-any-game/references/engines/`.
- **Worked examples:** examples are PS4 FPKG/GoldHEN oriented.

## Rules (full reasoning in `skills/mod-any-game/references/safety.md`)
- **What you can mod:** any PS4 game the user owns, in single-player or on servers the user hosts.
  - Never touch online clients protected by anti-cheat.
  - Never write cheats against other players (aimbots, ESP, speed hacks).
  - Never bypass anti-cheat, DRM or ownership checks.
- **Saves:** `um backup` saves before modded launches.
- **What you ship:** never commit or publish game files, extracted assets or decompiled code. Keep
  decompiles outside the repo. Ship FPKG patches or GoldHEN AFSP drop-in archives.
- **Processes:** kill by exact PID when applicable, never by name pattern.
- **Ask first** before:
  - publishing anything, PRs included.
- **Keep a journal:** a `MODLOG.md` in the mod's working folder. It becomes your field note at the end.

## Working on the toolkit itself
- **Python:** 3.10+, deps Pillow, numpy and PyYAML (`uv` handles them via `bin/um`). Code lives in `um/`,
  one module per CLI group, each with `register(sub)` and a docstring that doubles as `--help`.
- **Tests:** `uv run --with pytest pytest -q tests`. CI also runs `um kb check --index` and
  `um publish check .`.
- **Wording:** keep skills and docs agent-neutral ("the agent", not a product name) except in sections
  about one specific agent.


## Skills directory
| Skill | Description |
|---|---|
| `ps4-pipeline` | Handles PS4 FPKG extraction, GoldHEN AFSP live staging, GP4 generation, and patch compilation. |
| `mod-any-game` | The PS4 modding loop: recon from param.sfo/eboot.bin/app0, route via ps4-pipeline, stage via
  GoldHEN AFSP, build FPKG patches with orbis-pub-cmd. |
| `game-automation` | Console-oriented validation only: FTP file existence checks, GoldHEN status polling,
  on-console verification checklists. No desktop GUI hooks. |
| `publish-mod` | PS4 distribution: standalone update FPKG (`pkg_ps4_patch` via `orbis-pub-cmd`) and GoldHEN
  AFSP drop-in archives (`.zip` for `/data/GoldHEN/AFSP/<TITLE_ID>/`). |

## Workflow / Routing
- **Default target:** PlayStation 4. All modding requests route through `ps4-pipeline`.
- **Entry indicators:** CUSA title IDs, `param.sfo`, `eboot.bin`, `.pkg` files, `app0`/`patch0` directories.
- **Live testing:** stage modded assets to `/data/GoldHEN/AFSP/<TITLE_ID>/` via FTP using
  `tools/ps4_afsp_sync.py`, then reload or resume the game on the PS4.
- **Build:** generate a `.gp4` project with `tools/gp4_generator.py` and compile the FPKG with
  `orbis-pub-cmd.exe pkg_build`.
- **No PC routing:** desktop loaders, DLL proxies, Win32 injection, loose file installs, Steam Workshop,
  Nexus Mods and Thunderstore are out of scope. Agents must not route any request to desktop workflows.
