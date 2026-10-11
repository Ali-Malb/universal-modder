---
name: game-automation
description: Console-oriented validation for PS4 mods staged via GoldHEN AFSP. Covers FTP file existence checks, GoldHEN status polling, on-console verification checklists, and safe validation workflows. PS4-only: no desktop GUI hooks, no Win32 input, no local window capture. Use when a PS4 mod must be verified on-console, when validating staged assets via FTP, or when building a repeatable on-console test checklist.
---

# PS4 game validation: verify staged mods on-console

The real PS4 is the oracle. The loop is: stage assets via GoldHEN AFSP → confirm FTP upload → reload/resume the
game on the PS4 → perform manual on-console verification → record the result. Build the checklist once per game,
then every change you make can be checked in a minute.

This skill is PS4-only. It does **not** include desktop GUI automation (`pyautogui`, Win32 foreground/input APIs,
`um win drive`), local window capture, or any Windows-specific hooks.

## Remote validation via GoldHEN AFSP

### Stage the modded assets
```bash
python tools/ps4_afsp_sync.py \
  --ip <PS4_IP> \
  --port 2121 \
  --title-id <CUSA_TITLE_ID> \
  --local-dir <staged_assets_dir>
```
This recursively uploads the staged `app0`/`patch0` content to `/data/GoldHEN/AFSP/<CUSA_TITLE_ID>/` on the
PS4 over GoldHEN FTP (default port 2121, fallback 1337).

### Confirm the staging succeeded
After running `ps4_afsp_sync.py`:
1. **FTP listing check:** reconnect to the PS4 FTP and list
   `/data/GoldHEN/AFSP/<CUSA_TITLE_ID>/` to confirm every expected file is present with the correct relative
   path.
2. **Size check:** compare local file sizes against the remote files visible via FTP `SIZE` commands where the
   server supports it.
3. **Directory structure check:** confirm the `app0`/`patch0` directory tree under the AFSP path matches the
   staged layout.

Record the FTP confirmation in MODLOG.md before proceeding to on-console verification.

## GoldHEN status polling

When GoldHEN exposes a REST API or status endpoint:
- Poll the GoldHEN status to confirm it is running and AFSP redirection is active.
- Confirm the target TITLE_ID is recognized by GoldHEN.
- After staging, poll again to confirm the new files are seen by the redirection layer.

If no GoldHEN API is available, fall back to the FTP checks above and manual on-console verification.

## On-console verification checklist

The agent cannot drive the PS4 directly. Verification is manual, performed by the user on the console, guided
by a checklist written in MODLOG.md.

For each modded asset or change:
1. **Reload or resume the game** on the PS4 after GoldHEN AFSP staging.
2. **Confirm the asset appears:** load the scene, menu, character, weapon, or level that should show the modded
   texture/model/audio/text.
3. **Record the result:** take a screenshot or video of the console screen showing the modded content working.
4. **Check for errors:** note any crash, missing asset, fallback to stock content, or visual artifact.
5. **Sign off:** mark the item verified or failed in MODLOG.md with the console evidence.

Keep the checklist specific and repeatable: named scenes, characters, weapons, menus, or levels that exercise
each staged asset.

## What this skill does NOT do

- **No desktop window hooks.** There is no `um win` drive, screenshot, or record for PS4 modding.
- **No Win32 input.** The agent never drives the PS4 mouse/keyboard/gamepad directly.
- **No local process injection.** PS4 mods are staged via GoldHEN AFSP, not via local DLL proxies or process
  hijacking.
- **No pyautogui / desktop GUI automation.** Console validation is remote (FTP) + manual on-console.

## Crashes and cleanup

- If the game crashes on the PS4 after staging:
  1. Note the crash in MODLOG.md with the staged file set that triggered it.
  2. Restore the previous known-good staged set (or remove the AFSP layer) and retry.
  3. Re-stage only the changed files and narrow down the culprit.
- Keep a pristine backup of the original staged set so you can revert AFSP redirection quickly.

## Logging

- MODLOG.md is the primary record: CUSA title ID, CONTENT_ID, passcode, staged file list, FTP confirmation,
  on-console verification result, and any crash or fallback.
- Where the game or GoldHEN writes logs accessible via FTP or coninfo, read them as part of verification.

## References
- `tools/ps4_afsp_sync.py --help`: the FTP staging script.
- `tools/gp4_generator.py --help`: GP4 project generation for final FPKG builds.
- `skills/ps4-pipeline/SKILL.md`: the PS4 pipeline skill.
- `skills/mod-any-game/SKILL.md`: the PS4 modding loop (section 8, Verify in the real game).
