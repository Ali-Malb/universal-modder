# PS4 FPKG + GoldHEN Reference

## Update patch GP4 template (`pkg_ps4_patch`)
```xml
<?xml version="1.0" encoding="utf-8"?>
<psproject fmt="gp4" version="1000">
  <volume>
    <volume_type>pkg_ps4_patch</volume_type>
    <volume_id>CUSA00000</volume_id>
    <package content_id="UP0000-CUSA00000_00-GAMEPATCH000000" passcode="00000000000000000000000000000000"/>
  </volume>
  <files img_no="0">
    <file targ_path="sce_sys/param.sfo" orig_path="./staged/sce_sys/param.sfo"/>
    <file targ_path="eboot.bin" orig_path="./staged/eboot.bin"/>
  </files>
  <rootdir>
    <dir targ_name=""/>
  </rootdir>
</psproject>
```

## `param.sfo` keys to preserve
- `TITLE_ID`: Region/title code (example: `CUSA12345`) and AFSP folder selector.
- `APP_VER`: Patch application version string (example: `01.23`).
- `CONTENT_ID`: Full package content ID; must match the base title for patch builds.

## GoldHEN defaults
- FTP control port: `2121` (common alternative: `1337`).
- AFSP live-redirection root: `/data/GoldHEN/AFSP/`.
- Per-game staging layout: `/data/GoldHEN/AFSP/<TITLE_ID>/...` (mirror app file paths under this directory).
