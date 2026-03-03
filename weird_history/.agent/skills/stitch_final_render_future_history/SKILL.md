---
title: how_to_stitch_final_render_future_history
description: How to assemble the final rendered Future History video from staged assets using the pipeline.
---

# Creating the Stitched Final Render for Future History

Once all visual assets have been generated and placed in the staging folder (e.g., `/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/future_history/in_progress/en_organ_loyalty_2026-03-02/`), the pipeline stitches them into the final video.

## Key Differences from Weird History

| Property | Weird History | Future History |
|:---|:---|:---|
| Total scenes | 10 (1 thumbnail + 9 content) | 11 per entry, ~50 for compilation |
| Hero videos | 1-2 | 3 per entry |
| Video length | ~90-150 seconds | ~2 min per entry, ~8-10 min compilation |
| Voice | Various (US English) | Toby — British male (Cartesia) |
| Fallback voice | en-US-AriaNeural | en-GB-ThomasNeural |
| Scene motion | Steady slow inward zoom on stills | Same — steady slow inward zoom on stills |

## Content Safety (SAME AS WEIRD HISTORY)

- **No banned words** in script: `die`, `dying`, `kill`, `dead`, `death`, `died`
- **No minors** referenced
- **No blood/gore** in visual assets
- **NEVER use jitter, shake, parallax, or wobble** on stills — only steady slow inward zoom (Ken Burns)
- Retain hyper-saturated, vibrant, cinematic look

## Requisite Inputs

Before generating the final assembly, the staging folder must contain:
1. **Raw Visuals:** 8 still images and 3 hero videos per entry, named sequentially (`scene_0_still.jpg`, `scene_1_video.mp4`, etc.)
2. **The Timeline JSON:** The source timeline file (e.g., `organ_loyalty_timeline_en.json`) with prompts, TTS voice, and scene durations.

## Pipeline Execution

### Single Entry (Pilot)
```bash
python weird_history/pipeline/run_pipeline.py weird_history/future_history/organ_loyalty_timeline_en.json
```

The script will:
- Check for existing visual assets in the staging folder and skip API generation
- Generate voiceover audio (`voiceover.wav`) using **Cartesia API** (Toby voice)
- If Cartesia credits are exhausted, fall back to **Edge-TTS** (en-GB-ThomasNeural)
- Use **WhisperX** for forced alignment → word timestamps for bouncy captions
- Assemble via **FFmpeg** with steady slow zoom on stills + hero videos + voiceover + captions

### Compilation Video (Full 4-Entry)
For compilation videos, each entry's assets are assembled in sequence with transition cards between them. The pipeline handles concatenation automatically.

## Final Render Location

The final stitched video saves as `final_render.mp4` inside the staging folder:
`output/future_history/in_progress/en_<name-of-video>_<datestamp>/final_render.mp4`

> [!NOTE]
> Once approved, move the folder to `output/future_history/ready_to_publish/` for the publishing pipeline.
