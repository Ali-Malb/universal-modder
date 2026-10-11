---
name: showcase-video
description: Record and cut a short showcase video of a PS4 mod, or a compilation of clips, ready to post. Records console footage (HDMI capture or screen capture of the PS4 output), picks moments from contact sheets, and edits with one-line animated titles, creator credits, transitions, music, watermark and fade-out via an EDL JSON. PS4-only: no desktop window capture. Use when the user wants a demo video, trailer, clip or montage of a PS4 mod, or wants to combine existing console clips into a styled video.
---

# PS4 showcase video

A mod isn't finished until you can show it on the console. The toolchain is: **capture the PS4's video output**
(HDMI capture card, or a screen capture of the console display), then `um video contact` (look), `um video compile`
(edit), all ffmpeg + Pillow.

This skill is PS4-only. It does **not** include desktop window capture (`um win record`), gfxcapture, WASAPI
process-loopback audio, or any Windows-specific recording hooks.

## 1. Make the take repeatable
- **Script the action.** Use a GoldHEN AFSP-staged mod-side change, a scene/level that shows the modded asset, or
  an on-console sequence the user performs. The first clean take should be reproducible, so you can reshoot after
  a fix.
- **Restore before each take.** If the mod affects saves or game state, keep a pristine backup with `um backup`
  and restore it every take.
- **Clean frame.** Confirm the modded asset is visible on the PS4 display before recording. Hide any debug overlays
  if the game supports it.

## 2. Record the console output
```bash
# HDMI capture card (preferred): record the PS4's HDMI output to a file
ffmpeg -f <capture_device> -i <input_uri> -c:v <codec> -preset fast caps/take1.mkv

# Screen capture of the PS4 display (alternative): capture what's on the screen showing the PS4
# (e.g. a capture of the TV/monitor output, or a direct console screen capture tool)
ffmpeg -f <screen_capture> -i <input_uri> -c:v <codec> caps/take1.mkv
```
- **Video:** capture the PS4's actual output — the modded asset as it appears on the console. Use the capture
  method that gives a clean, timestamped file.
- **Audio:** capture the console/game audio from the same output path (HDMI carries both video and audio).
  Sync video and audio from the same capture source when possible.
- **Timestamps:** capture with a timestamp or use a visual sync event (a flash vs its boom) for later muxing
  offset fine-tuning.

## 3. Look before you cut
```bash
um video probe caps/take1.mkv
um video contact caps/take1.mkv sheet.png --every 1.5 --cols 6     # a timestamped grid; read it, pick in/out points
um video contact caps/take1.mkv zoom.png --start 20 --end 30 --every 0.5
```
Pick the peak moments: the modded texture appearing, the custom model loading, the changed audio playing, the
edited text showing. Write in/out times into the EDL.

## 4. Edit with an EDL
`um video compile edl.json out.mp4` (`--preview` renders half size and fast). The full format is in
`um video --help`.
```json
{
  "size": [1920, 1080], "fps": 30,
  "theme": {"accent": "#B6FF3B"},
  "transition": {"type": "fade", "duration": 0.3},
  "clip_volume": 0.8,
  "music": {"path": "music.mp3", "volume": 0.5},
  "watermark": {"path": "logo.png", "height": 54, "corner": "br"},
  "segments": [
    {"clip": "take1.mp4", "in": 9.0, "dur": 3.0, "hook": "PS4 mod: custom texture in <game>."},
    {"clip": "take1.mp4", "in": 24.2, "dur": 4.5, "title": "Custom Model", "transition": {"type": "pixelize"}},
    {"clip": "take2.mp4", "in": 3.0, "dur": 5.0, "title": "GoldHEN AFSP staging"},
    {"card": {"title": "<Mod Name>", "sub": "a PS4 mod via FPKG/GoldHEN"}, "dur": 2.5}
  ]
}
```
- **Transitions:** any ffmpeg xfade type (fade, pixelize, slideleft, smoothleft, circleopen, zoomin,
  radial...) or `cut`.
- **Fills:** for non-16:9 clips, `fill: blur` (blurred backdrop), `crop` or `pad`.
- **Per clip:** `speed` and `volume`, `zoom` to punch in past UI, `crop` [x, y, w, h] to reframe.
- **Music:** `um fal music \"...\" --seconds 60` makes a bed. Set `bpm` and use `beats` instead of `dur` to
  cut on the beat; `um video beats music.mp3` estimates tempo and first beat.

## Style that works (from real feedback)
- **Titles:** one line naming what's on screen (\"PS4 <game>: custom <asset> via GoldHEN AFSP\"). No small
  explanatory captions about how it was made; that goes in the post text.
- **Pace:** get into gameplay/asset display within 2-3 s. Clips run 3-5 s each. End on the mod name or URL and
  fade out.
- **Sound:** keep the console/game audio. It sells impacts. Music under a compilation, clip audio around 0.5-0.8.
- **Compilations of other people's clips:** credit every creator on screen (`credit: \"@handle\"`) and in the
  post, and ask permission when it's promotional. Don't imply their clips were made with your tool. Download
  only public posts, and only what you'll use.
- **Last step:** look at a contact sheet of the finished video before sharing it.

## What this skill does NOT do
- **No desktop window capture.** There is no `um win record` in this PS4-only toolkit.
- **No gfxcapture/WASAPI loopback.** Console recording uses HDMI capture or screen capture of the PS4 output.
- **No Windows-specific hooks.** All recording is of the PS4's video output, not a desktop window.
