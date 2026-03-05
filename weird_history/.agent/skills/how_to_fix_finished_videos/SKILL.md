---
title: how_to_fix_finished_videos
description: How to fix or tweak a video that has already been assembled without regenerating the entire pipeline from scratch.
---

# How to Fix Finished Videos

When a video has already been fully generated and stitched, but a specific element (like audio volume, a single image frame, or a typo) needs fixing, **do not regenerate the entire video pipeline**. This is a waste of API credits and time.

Instead, use the "constituent parts" workflow to isolate, fix, and restitch the video.

---

## The Workflow

### 1. Identify the Constituent Parts
Every finished video is just a compilation of smaller, raw assets (constituent parts). For example:
- **Audio:** TTS voiceover `.wav` files, background music `.mp3`, sound effects `.mp3`
- **Visuals:** Hero video `.mp4` chunks, static image `.png`/`.jpg` files, interstitial `.mp4` cards.
- **Assembly:** FFmpeg filter scripts and concatenation python scripts.

First, determine exactly which raw asset is causing the problem.

### 2. Fix the Specific Part
Instead of running the full pipeline:
- **Audio Volume Issues:** Locate the raw audio file (e.g. `intro_voice.wav`). If it's too quiet, use an FFmpeg filter like `loudnorm` or `volume` on that specific segment's stitch script, rather than regenerating the TTS. Sometimes `amix` is the culprit — adding `normalize=0` to the `amix` filter prevents it from halving the volume of all tracks.
- **Visual Error:** If a single scene is wrong, identify its `scene_N` asset. Manually regenerate or edit that specific image/video file.
- **Timing/Pacing:** Modify the timings in the compilation timeline JSON or tweak the ffmpeg python script (e.g. `assemble_video.py`) to adjust durations.

### 3. Restitch the Parent Segment
Once the raw asset is updated, you need to rebuild the specific chunk it belongs to.
- If you fixed a scene inside a vignette, re-run `python3 publish_video.py` or `python3 pipeline/run_pipeline.py` **using the specific build directory** (this will detect the existing assets and only re-concatenate the `final_render.mp4` for that vignette).
- If you fixed an intro sting, re-run its dedicated assembly script (`python3 pipeline/build_intro.py`).

### 4. Restitch the Whole Episode
Finally, if the video is part of a larger compilation (like an episode), you must run the top-level assembly script to pull the newly updated segment into the final product.
- For Future History episodes, re-run `python3 /tmp/build_episode.py`.

---

## Common Fixes

### "The VO is too quiet when mixed with music"
By default, FFmpeg's `amix` filter divides audio volume by the number of inputs (e.g., 2 tracks = 50% volume each). 
**The Fix:** Add `normalize=0` to the `amix` filter. If the raw VO is still too quiet, run it through the `loudnorm` audio filter to bring it to broadcast standard (`I=-14:LRA=11:TP=-1.5`) before mixing.

### "One image has the wrong aspect ratio"
**The Fix:** Locate the specific image in the build directory. Use ImageMagick or a Python script using Pillow (`PIL`) to crop or pad the image to `1920x1080` or `1080x1920`. Then, rerun the compilation script.

### "The audio is out of sync"
**The Fix:** The timeline JSON controls pacing, but the python assembly script does the actual FFmpeg math. Check if the script calculates image duration dynamically. If it does, ensure the voiceover duration hasn't changed. If it has, force a recalculation by deleting the previous `_main_segment.mp4` and re-running the assembly script so FFmpeg correctly remeasures the audio.
