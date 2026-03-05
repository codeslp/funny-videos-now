---
title: how_to_stitch_final_render_future_history
description: How to assemble a single Future History vignette from staged assets using the pipeline.
---

# Creating the Stitched Final Render for Future History

Once all visual assets have been generated and placed in the staging folder, the pipeline stitches them into the final video.

## Key Properties

| Property | Value |
|:---|:---|
| Total scenes | 11 per vignette (scenes 0-10) |
| Hero videos | 3 per vignette (scenes 1, 4, 8) |
| Still images | 8 per vignette |
| Video length | ~2-3 minutes per vignette |
| Narration voice | ElevenLabs (`dAlhI9qAHVIjXuVppzhW`) |
| Fallback voice | Edge-TTS (`en-GB-ThomasNeural`) |
| Scene motion | Steady slow inward zoom on stills (Ken Burns) |
| Music | ElevenLabs-generated atmospheric underscore at -18dB |
| Intro | Pre-built clip (`output/future_history/intro_outro/future_history_intro.mp4`) |
| Outro | Disabled — will be built at episode level |

## Content Safety

- **No banned words** in script: `die`, `dying`, `kill`, `dead`, `death`, `died`
- **No minors** referenced
- **No blood/gore** in visual assets
- **NEVER use jitter, shake, parallax, or wobble** on stills — only steady slow inward zoom
- Retain hyper-saturated, vibrant, cinematic look

## Requisite Inputs

Before running the pipeline, the staging folder must contain:
1. **8 still images** named `scene_0_still.jpg` through `scene_10_still.jpg` (skipping video scenes)
2. **3 hero videos** named `scene_1_video.mp4`, `scene_4_video.mp4`, `scene_8_video.mp4`
3. **Timeline JSON** — the source file with script, prompts, TTS config, and storytelling block

## Pipeline Execution

```bash
python weird_history/pipeline/run_pipeline.py \
  weird_history/future_history/<timeline>.json \
  --build-dir "output/future_history/in_progress/<build_dir>"
```

### What the Pipeline Does (5 Steps)

1. **TTS Generation** — Generates voiceover via ElevenLabs API (falls back to Edge-TTS)
2. **Asset Check** — Verifies all scene assets exist in the build directory (skips generation if present)
3. **Music Generation** — Generates atmospheric underscore via ElevenLabs, loops to match voiceover duration
4. **Video Assembly** — FFmpeg assembly with dynamic scene timing:
   - Hero videos play at full duration (~8s each)
   - Still images expand to fill remaining time (voiceover length minus total video time, divided by number of stills)
   - Underscore mixed at -18dB, trimmed to voiceover length
   - Pre-built intro prepended (if present)
   - Explicit `-t` cap ensures video matches voiceover duration exactly
5. **Metadata** — Saves `build_metadata.json` with paths and timestamps

### Dynamic Scene Timing

The assembler calculates timing automatically:

```
voiceover_duration = duration of generated TTS audio
total_video_time = sum of all hero video durations
remaining_time = voiceover_duration - total_video_time
still_duration = remaining_time / number_of_stills
```

This ensures the video matches the voiceover length precisely.

## Final Render Location

```
output/future_history/in_progress/<build_dir>/final_render.mp4
```

> [!NOTE]
> Individual vignettes include the pre-built intro. When assembling into a full episode, strip the first 8 seconds (the intro) from each vignette, since the episode has its own intro. See the `how_to_assemble_future_history_episode` skill.
