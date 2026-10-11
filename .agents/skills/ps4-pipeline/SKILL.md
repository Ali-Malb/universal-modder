---
name: ps4-pipeline
description: Handles PS4 FPKG unpacking, GoldHEN live asset redirection (AFSP/LayerFS), GP4 project generation, and FPKG patch rebuilding.
---

# PS4 FPKG Pipeline Workflow

## 1. Tooling Prerequisites
- **LibOrbisPkg** (cross-platform open-source CLI) or **orbis-pub-cmd** (official SDK tool).
- **GoldHEN FTP/AFSP**: Console on the same LAN with GoldHEN 2.3+ running.
- **param.sfo Editor/Reader**: For extracting metadata without full extraction.

## 2. Reconnaissance & Extraction
- Inspect the target PKG or dumped files:
  - Extract `sce_sys/param.sfo` to obtain `TITLE_ID` (e.g., `CUSAXXXXX`), `APP_VER`, and `CONTENT_ID`.
  - Unpack the update patch or base PKG into a working workspace:
    ```bash
    orbis-pub-cmd pkg_extract input.pkg ./workspace/app0
    ```

## 3. Rapid Iteration (Live Staging via GoldHEN AFSP)
Do not build full FPKGs during mod development:
1. Connect via FTP to the PS4 (default GoldHEN port: 2121 or 1337).
2. Place modified loose files into `/data/GoldHEN/AFSP/<TITLE_ID>/`.
3. Launch or restart the game on the PS4. The console redirects file reads from `app0/` to your modded files on disk.

## 4. Final FPKG Compilation (Packaging Phase)
Once testing is verified on-console:
1. Generate the `.gp4` project file matching the base game's parameters:
   - **Volume Type**: `pkg_ps4_patch` (for an update patch) or `pkg_ps4_app` (for a standalone base game).
   - **Content ID**: Must match the base game's content ID exactly.
   - **Passcode**: Must match the original package passcode (usually 32 zeros for standard FPKGs).
2. Compile the package:
   ```bash
   orbis-pub-cmd.exe pkg_build project.gp4 ./dist/
   ```
