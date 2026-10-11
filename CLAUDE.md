@AGENTS.md

## Claude Code specifics
- Installed as a plugin, the skills are namespaced (`/universal-modder:ps4-pipeline`, `/universal-modder:mod-any-game`),
  the fal MCP server comes from `.mcp.json` (needs `FAL_KEY` in the environment), and a SessionStart hook puts
  `um` on PATH.
- In a clone, `.claude/settings.json` adds the same PATH hook, and `.claude/skills` is a copy of `skills/`.
- This toolkit targets PlayStation 4 exclusively. There are no PC/Windows modding workflows in this repo.


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
- **No PC routing:** desktop workflows are out of scope. Agents must not route any request to desktop modding workflows.
