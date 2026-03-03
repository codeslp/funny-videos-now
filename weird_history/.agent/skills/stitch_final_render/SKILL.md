---
title: how_to_stitch_final_render_weird_history
description: How to take the compiled in_progress assets and create the stitched final rendered video for Weird History.
---

# Creating the Stitched Final Render

Once all manual visual assets (images and videos) have been successfully generated and placed into their designated project folder (`output/weird_history/in_progress/en_<name-of-video>_<datestamp>/`), the next step in the pipeline is to stitch them together into the final video.

*Note on Folder Naming:* The two-letter prefix at the start of the folder name (`en_`) explicitly defines the language of the video. For English videos, always use `en_`.

## Requisite Inputs
Before generating the final assembly, the staging folder must contain:
1. **Raw Visuals:** 8 still images (`scene_1_still.jpg`, etc.) and 1 hero video (`scene_5_video.mp4`) named sequentially.
2. **The Timeline Logic:** The source JSON timeline file (e.g., `ghost_marriages_timeline.json`), which dictates the prompt metadata, TTS voice, and duration for each scene.

## Visual Style Guide Rules for Assembly
If making modifications to the assembly orchestrator (`assemble_video.py`), the following **Hybrid Pipeline rules** must be strictly enforced:
- **Pacing & Narrative Arc:** Observe the standard 9-scene breakdown (Scenes 1-4 Stills, Scene 5 Hero Video, Scenes 6-9 Stills).
- **Motion on Stills:** The assembly engine (FFmpeg) must apply a steady, slow inward zoom (Ken Burns effect) to all static images. **NEVER use jitter, shake, parallax, or wobble effects.**
- **Color/Vibe:** Retain the highly saturated, pristine cinematic look.

## 1. Automated Generation of Audio & Timestamps
You can execute the automated pipeline script, which has been configured to read from the staging folder:
```bash
python weird_history/pipeline/run_pipeline.py weird_history/pipeline/<timeline_file>.json
```

By doing this, the script will:
- Check for existing visual assets in the staging folder and skip API generation for them.
- Generate high-quality voiceover audio (`voiceover.wav`) using the **Cartesia API**.
- Use **WhisperX** to perform forced alignment on the audio against the script, generating precise millisecond-accurate word timestamps (`word_timestamps.json`) required for bouncy captions.

## 2. FFmpeg Stitching (`assemble_video.py`)
Finally, the pipeline orchestrator automatically takes these pieces and creates the final video. Under the hood, this step uses Python to generate raw **FFmpeg** commands that:
1. Concatenate all generated visuals together in sequential order.
2. Apply the required dynamic zoom-and-pan effect over the static images.
3. Overlay the generated voiceover audio perfectly over the visuals.
4. Render the textual captions natively onto the video (the final "bouncy" TikTok effect) based on the WhisperX timestamps.

## The Final Render Location
The final executed stitched video will be rendered exactly where the assets live, saving as `final_render.mp4` directly inside the `in_progress/en_<name-of-video>_<datestamp>/` folder.

> [!NOTE] 
> This fully completed folder will subsequently be pushed to the `ready_to_publish` directory for the final publishing scripts.
