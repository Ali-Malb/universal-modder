<p align="center">
  <img src="docs/media/banner.png" alt="universal-modder: mod PlayStation 4 games. Point any AI coding agent at the PS4 games you own. Publish FPKG patches and GoldHEN AFSP drops, and learn how PS4 games were modded." width="100%">
</p>

<p align="center">
  <b>Skills, tools and a shared knowledge base that let any AI coding agent mod PlayStation 4 games you own,
  using FPKG packages and GoldHEN live asset staging.</b><br>
  The agent identifies the CUSA title, reads param.sfo and eboot.bin, unpacks the FPKG, modifies engine assets,
  stages them live through GoldHEN AFSP, builds update/patch FPKGs with orbis-pub-cmd, and writes down what it
  learned for the next agent.
</p>

<p align="center">
  <a href="https://discord.com/invite/sEZWaf7vV"><img alt="community: join us on discord" src="docs/media/badges/discord.png" height="26"></a>
  <a href="#install"><img alt="works with Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and OpenCode" src="docs/media/badges/agents.png" height="26"></a>
  <a href="knowledge/INDEX.md"><img alt="knowledge base: field notes by agents, for agents" src="docs/media/badges/knowledge.png" height="26"></a>
  <a href="https://fal.ai"><img alt="assets: fal" src="docs/media/badges/fal.png" height="26"></a>
  <a href="LICENSE"><img alt="license: MIT" src="docs/media/badges/license.png" height="26"></a>
</p>

<p align="center">
  <img src="docs/media/mods-teaser.gif" alt="universal-modder: modding PlayStation 4 games with AI coding agents. FPKG extraction, GoldHEN AFSP live staging, GP4 generation, and orbis-pub-cmd patch compilation." width="560">
</p>

<p align="center"><b>Coming next: the mod hub.</b> Publish your FPKG patches, remix other people's, and make new ones.<br>
  Share what you make, get help, and follow along:</p>
<p align="center">
  <a href="https://discord.com/invite/sEZWaf7vV"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/discord-dark.svg"><img src="docs/media/discord-light.svg" height="32" alt="join the discord"></picture></a>
</p>

## Install

Pick your agent. Each gets the same skills (Agent Skills format), the fal MCP server, and the `um` CLI.

| Agent | Install |
|---|---|
| **Claude Code** | `/plugin marketplace add rehan-remade/universal-modder`<br>`/plugin install universal-modder@universal-modder` |
| **Codex** | `codex plugin marketplace add rehan-remade/universal-modder`<br>`codex plugin add universal-modder@universal-modder` |
| **Gemini CLI** | `gemini extensions install https://github.com/rehan-remade/universal-modder` |
| **VS Code / Copilot** | Enable `chat.plugins.enabled`, run **Chat: Install Plugin From Source**, and enter this repo's URL |
| **Cursor** | Cursor Marketplace, or clone (Cursor reads `AGENTS.md` and `.cursor/mcp.json`) |
| **OpenCode** | Clone and run `opencode` inside it (`opencode.json` adds the skills and the fal MCP server)<br>or, on OpenCode 2, `opencode plugin add 'github:rehan-remade/universal-modder#main::path:plugins/opencode'` (the `um` tool and fal MCP; add the skills with **Skills only**) |
| **Skills only**<br>(any agent) | `npx skills add https://github.com/rehan-remade/universal-modder` |
| **Anything else** | `git clone https://github.com/rehan-remade/universal-modder` and start your agent inside it |

Inside a clone, each agent finds the skills where it looks for them: `.agents/skills` (Codex, Gemini CLI,
Copilot, Cursor, OpenCode) and `.claude/skills` (Claude Code) are copies of `skills/`. Instructions are in
`AGENTS.md`, which `CLAUDE.md` and `GEMINI.md` point to. MCP config is in `.mcp.json`, `.codex/config.toml`,
`.cursor/mcp.json`, `.vscode/mcp.json` and `opencode.json` (which also points OpenCode at `skills/`).

Without a clone, OpenCode 2 installs the plugin in `plugins/opencode/` with `opencode plugin add`: one
`um_run` tool that passes its arguments straight to the CLI and runs `um` from PATH (see below), plus the
fal MCP server when `FAL_KEY` is set and none is configured. A clone doesn't need it. See
`plugins/opencode/README.md`.

**The `um` CLI.** Plugin installs and clones put it on PATH (OpenCode's plugin install doesn't). Anywhere else:
```bash
uv tool install git+https://github.com/rehan-remade/universal-modder     # or: pipx install git+...
```
**For assets,** get a [fal API key](https://fal.ai/dashboard/keys). It powers both the fal MCP server and
`um fal` (for images without a key, `um comfy` uses a local ComfyUI server):
```bash
export FAL_KEY=...
```
You also need Git, Python 3.10+ and ffmpeg. `uv` is recommended. Blender is needed for 3D → sprite renders.

This toolkit targets PlayStation 4 (Orbis OS) exclusively. It does not cover PC/Windows modding workflows.

## Try it
> Mod a PS4 game: unpack its FPKG, change a texture or model, stage it live through GoldHEN AFSP, then build an
> update FPKG with orbis-pub-cmd.

> Put a custom character model into a PS4 game via GoldHEN AFSP and record the result on the console.

> What is the TITLE_ID of a PS4 game, and what is its CONTENT_ID and passcode?

The agent starts with the **mod-any-game** skill and runs the same PS4 loop every time:
1. search the knowledge base for the CUSA title or game;
2. recon: read param.sfo, eboot.bin, app0/patch0 from the FPKG dump;
3. route: hand off to ps4-pipeline for staging and compilation;
4. set up a safe lab (saves backed up);
5. read the actual code and assets;
6. build one working slice (one changed file staged via GoldHEN AFSP);
7. generate assets with fal where needed;
8. verify on the real PS4 (FTP check + on-console validation);
9. record the console footage;
10. package the FPKG patch or GoldHEN AFSP archive;
11. write a field note for the next agent.

## A knowledge base that AIs write for AIs
[`knowledge/`](knowledge/) holds **field notes**: how specific PS4 games were actually modded via FPKG and
GoldHEN. Each note gives:
- the exact CUSA title ID, CONTENT_ID and passcode that worked;
- the route, and why;
- what the engine really does;
- how it was verified on-console;
- the gotchas (symptom → cause → fix).

**Every agent that finishes a mod can open a pull request with its note**, so the next agent starts where it
left off instead of rediscovering the same traps.

```bash
um kb search "CUSA00000"                 # before you start: prior art (works outside the repo too)
um kb new --game "<game name>" --title "A new mod" --from-scan <CUSA_TITLE_ID> --agent "Codex (gpt-6)"
um kb check knowledge/games/<game>/a-new-mod.md
um kb pr knowledge/games/<game>/a-new-mod.md --yes    # after your human says OK: branch, push, PR
```
Browse [`knowledge/INDEX.md`](knowledge/INDEX.md). Contribution rules, for humans and AIs, are in
[`CONTRIBUTING.md`](CONTRIBUTING.md): no game files, no decompiled dumps, no cheating other players, and an
honest status and verification.

## What's inside

**Skills** (`skills/`, Agent Skills format)

<table>
  <thead><tr><th width="200">Skill</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td><a href="skills/mod-any-game"><code>mod-any-game</code></a></td><td>The PS4 modding loop: intake, recon from param.sfo/eboot.bin/app0, route via ps4-pipeline, GoldHEN
  AFSP staging, orbis-pub-cmd FPKG build. PS4-only; no PC/Windows workflows.</td></tr>
    <tr><td><a href="skills/game-recon"><code>game-recon</code></a></td><td>Prior field notes, CUSA title IDs, param.sfo metadata, eboot.bin, FPKG structure, GoldHEN routes →
  <code>MODDING_PLAN.md</code></td></tr>
    <tr><td><a href="skills/game-research-websearch"><code>game-research-websearch</code></a></td><td>Open-web research that survives dead forums: Wayback/archive.today, GitHub/code searches, Reddit/YouTube,
  login-gated handoff, screenshots as evidence</td></tr>
    <tr><td><a href="skills/reverse-engineering"><code>reverse-engineering</code></a></td><td>Ghidra/IDA over MCP, Cpp2IL, Vineflower; reverse-engineer PS4 binary formats and prove them with a round
  trip</td></tr>
    <tr><td><a href="skills/fal-assets"><code>fal-assets</code></a></td><td>Textures, PBR maps, image-to-3D models (GLB), auto-rigging, SFX, music, voice, cutscene video — for
  PS4 asset preparation</td></tr>
    <tr><td><a href="skills/asset-pipeline"><code>asset-pipeline</code></a></td><td>Art → engine-exact frames: cutout, nearest-neighbour fit, palettes, sheets, team-colour masks, 3D →
  sprite frames where the game needs them</td></tr>
    <tr><td><a href="skills/game-automation"><code>game-automation</code></a></td><td>Console-oriented validation only: FTP file existence checks, GoldHEN REST/API status polling, on-console
  verification checklists. No desktop GUI hooks.</td></tr>
    <tr><td><a href="skills/showcase-video"><code>showcase-video</code></a></td><td>Record console footage, pick moments, cut a styled video from an EDL</td></tr>
    <tr><td><a href="skills/mashup-mods"><code>mashup-mods</code></a></td><td>Content ports and passthrough-style mods on PS4 via GoldHEN AFSP redirection.</td></tr>
    <tr><td><a href="skills/publish-mod"><code>publish-mod</code></a></td><td>PS4 distribution: standalone update FPKG (`pkg_ps4_patch` via `orbis-pub-cmd`) and GoldHEN AFSP
  drop-in archives (`.zip` for `/data/GoldHEN/AFSP/<TITLE_ID>/`). No PC mod distributors.</td></tr>
    <tr><td><a href="skills/share-field-notes"><code>share-field-notes</code></a></td><td>Search the knowledge base, write your own note, open the PR</td></tr>
  </tbody>
</table>

**The `um` CLI** (Python). Every command has `--help` with examples.

<!-- GitHub lets images in auto-width tables shrink to nothing: the widths and the no-break spaces keep the icons at 36 px. -->
<table>
  <thead><tr><th width="62">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</th><th width="170">Command</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/scan-dark.svg"><img src="docs/media/icons/scan-light.svg" width="36" height="36" alt=""></picture></td><td><code>um scan</code></td><td>Find PS4 game installs; fingerprint CUSA title ID, param.sfo metadata, eboot.bin, app0/patch0 structure,
  FPKG routes</td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/fal-dark.svg"><img src="docs/media/icons/fal-light.svg" width="36" height="36" alt=""></picture></td><td><code>um fal</code></td><td><code>sprite</code>, <code>image</code>, <code>edit</code>, <code>rmbg</code>, <code>pixelate</code>, <code>upscale</code>, <code>texture</code>, <code>pbr</code>, <code>model3d</code>, <code>rig</code>, <code>sfx</code>, <code>music</code>, <code>voice</code>, <code>video</code>, <code>run</code>, <code>search</code>, <code>schema</code>, <code>price</code>. Plain REST, with a manifest of every generation</td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/comfy-dark.svg"><img src="docs/media/icons/comfy-light.svg" width="36" height="36" alt=""></picture></td><td><code>um comfy</code></td><td><code>status</code>, <code>image</code> (<code>--sprite</code> cuts it out), <code>run</code> (any workflow saved with Export (API)). Images from a local ComfyUI server, no API key</td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/sprite-dark.svg"><img src="docs/media/icons/sprite-light.svg" width="36" height="36" alt=""></picture></td><td><code>um sprite</code></td><td><code>cutout</code>, <code>fit</code>, <code>pixelate</code>, <code>palette</code>, <code>sheet</code>, <code>slice</code>, <code>frames</code>, <code>team-mask</code>, <code>seamless</code>, <code>preview</code></td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/render3d-dark.svg"><img src="docs/media/icons/render3d-light.svg" width="36" height="36" alt=""></picture></td><td><code>um render3d</code></td><td>GLB → sprite frames from the game's camera (<code>aoe2</code>, <code>iso8</code>, <code>trueiso</code>, <code>topdown</code>, <code>side</code>, <code>turntable</code>) with Blender</td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/video-dark.svg"><img src="docs/media/icons/video-light.svg" width="36" height="36" alt=""></picture></td><td><code>um video</code></td><td><code>contact</code> sheets, <code>compile</code> (EDL → titled, beat-cut video with music), <code>mux</code>, <code>beats</code>, <code>first-frame</code></td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/backup-dark.svg"><img src="docs/media/icons/backup-light.svg" width="36" height="36" alt=""></picture></td><td><code>um backup</code></td><td>Snapshot, diff and restore save folders</td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/publish-dark.svg"><img src="docs/media/icons/publish-light.svg" width="36" height="36" alt=""></picture></td><td><code>um publish check</code></td><td>Blocks shipping game files, decompiled code and leaked keys; validates FPKG and GoldHEN AFSP distribution
  packages</td></tr>
    <tr><td align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/icons/kb-dark.svg"><img src="docs/media/icons/kb-light.svg" width="36" height="36" alt=""></picture></td><td><code>um kb</code></td><td>The knowledge base: <code>search</code>, <code>show</code>, <code>new</code>, <code>check</code>, <code>index</code>, <code>sync</code>, <code>pr</code></td></tr>
  </tbody>
</table>

<p align="center"><img src="docs/media/pipeline.png" alt="The PS4 route: unpack FPKG, modify assets, stage via GoldHEN AFSP, build GP4, compile with orbis-pub-cmd." width="100%"></p>

## Built with it
PS4 FPKG and GoldHEN examples live in the examples directory. Each has a field note with every non-obvious
lesson: [knowledge/INDEX.md](knowledge/INDEX.md).

## Rules it follows
- **Any PS4 game you own: single-player, or servers you host.** It refuses to inject into online games with
  anti-cheat, write cheats against other players, or bypass anti-cheat, DRM or ownership checks.
- **It never ships game files or decompiled code.** Mods ship as FPKG patches or GoldHEN AFSP drop-in
  archives that run on the user's own console.
- **It backs up before touching saves**, and uses safe process handling.
- **It asks before** publishing, PRs included.

Full reasoning: [`skills/mod-any-game/references/safety.md`](skills/mod-any-game/references/safety.md).

## Made a mod with it?
Show it off in the [Discord](https://discord.com/invite/sEZWaf7vV), and put the badge on your mod's page:

<p>
  <a href="https://github.com/rehan-remade/universal-modder"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/media/made-with-dark.svg"><img src="docs/media/made-with-light.svg" height="32" alt="made with universal-modder"></picture></a>
</p>

```markdown
[![made with universal-modder](https://raw.githubusercontent.com/rehan-remade/universal-modder/main/docs/media/made-with-dark.svg)](https://github.com/rehan-remade/universal-modder)
```
Use `made-with-light.svg` on a light page.

## Credits
- Built from real agent sessions modding PS4 games via FPKG and GoldHEN.
- Assets: [fal](https://fal.ai) (GPT Image 2, Nano Banana 2, FLUX, Trellis 2, ElevenLabs...).
- Standing on the shoulders of LibOrbisPkg, orbis-pub-cmd, GoldHEN, and every PS4 modding community that
  documented its game.

MIT licensed. Brand type: Geist Pixel, Sometype Mono and Instrument Sans. Video titles: Space Grotesk and JetBrains Mono. All under the SIL OFL.

## Star history

<p align="center">
  <a href="https://github.com/rehan-remade/universal-modder/stargazers"><img src="https://raw.githubusercontent.com/rehan-remade/universal-modder/star-chart/stars.svg" width="800" alt="universal-modder's GitHub stars over time"></a>
</p>
