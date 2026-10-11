@AGENTS.md

## Claude Code specifics
- Installed as a plugin, the skills are namespaced (`/universal-modder:mod-any-game`), the fal MCP server comes
  from `.mcp.json` (needs `FAL_KEY` in the environment), and a SessionStart hook puts `um` on PATH.
- In a clone, `.claude/settings.json` adds the same PATH hook, and `.claude/skills` is a copy of `skills/`.


## Skills directory
| Skill | Description |
|---|---|
| `ps4-pipeline` | Handles PS4 FPKG extraction, GoldHEN AFSP live staging, GP4 generation, and patch compilation. |

## Workflow / Routing
- If the target game contains PS4 indicators (CUSA title IDs, `param.sfo`, `eboot.bin`, `.pkg`, `app0/patch0` directories), route mod staging and compilation through `ps4-pipeline` instead of desktop file installation.
