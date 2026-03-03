---
title: how_to_stitch_final_render_spanish_weird_history
description: How to take the compiled in_progress assets and create the stitched final rendered video for Weird History in Spanish.
---

# Creating the Stitched Final Render (Spanish)

The process for assembling a Spanish Weird History video is nearly identical to the English version, with a few critical modifications regarding the output directory and the source files. Once you have generated and gathered your assets in the designated `in_progress` folder:

`/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/in_progress/es_<name-of-video>_<datestamp>/`

*Note on Folder Naming:* The two-letter prefix at the start of the folder name explicitly defines the language of the video. For Spanish videos, always use `es_`.

## Requisite Inputs
Ensure the staging folder contains:
1. **Raw Visuals:** 8 still images (`scene_1_still.jpg`, etc.) and 1 hero video (`scene_5_video.mp4`) named sequentially.
2. **The Timeline Logic:** The source JSON timeline file (e.g., `ghost_marriages_timeline_es.json`). 

### Critical Difference: The Timeline JSON
For the pipeline to correctly generate audio in Spanish instead of English, the timeline JSON file **MUST** contain the language attribute:

```json
{
  "title": "TÍTULO DEL VÍDEO",
  "script": "Texto del guion en español...",
  "language": "es",
  "scenes": [...]
}
```

This `"language": "es"` flag instructs `generate_audio.py` to use a Spanish TTS voice (e.g., `es-ES-ElviraNeural`) and ensures `generate_transcription.py` (WhisperX) aligns the timing to spoken Spanish rather than English.

## Visual Style Guide Rules for Assembly
If making modifications to the assembly orchestrator (`assemble_video.py`), the following **Hybrid Pipeline rules** must be strictly enforced:
- **Pacing & Narrative Arc:** Observe the standard 9-scene breakdown (Scenes 1-4 Stills, Scene 5 Hero Video, Scenes 6-9 Stills).
- **Motion on Stills:** The assembly engine (FFmpeg) must apply a steady, slow inward zoom (Ken Burns effect) to all static images. **NEVER use jitter, shake, parallax, or wobble effects.**
- **Color/Vibe:** Retain the highly saturated, pristine cinematic look.

## 1. Automated Generation of Audio & Timestamps
You can execute the automated pipeline script just like the English version:
```bash
python weird_history/pipeline/run_pipeline.py weird_history/pipeline/<timeline_file_es>.json
```

By doing this, the script will:
- Check for existing visual assets in the staging folder (`es_<title>_<timestamp>`).
- Skip API visual generation because the manual assets are already placed there.
- Generate high-quality Spanish voiceover audio (`voiceover.wav`).
- Use **WhisperX** to perform forced alignment on the audio against the Spanish script, generating exact millisecond timestamps (`word_timestamps.json`) required for bouncy captions.

## 2. FFmpeg Stitching (`assemble_video.py`)
The pipeline runs the exact same FFmpeg compilation logic to piece together the visual elements, applying the Ken Burns zoom onto the stills, syncing the Spanish voiceover, and overlaying the timestamped captions.

## The Final Render Location
The final executed stitched video will be rendered exactly where the assets live, saving as `final_render.mp4` directly inside the `in_progress/es_<name-of-video>_<datestamp>/` folder.

> [!NOTE] 
> This fully completed folder will subsequently be pushed to the `ready_to_publish` directory for the final publishing scripts.

## 3. Creating the Spanish Description for Publishing
Before the Spanish video can be published, you must manually create a Spanish description holding the formatted text (including the Title, Hook, Context, CTA, Research Link, and Hashtags).
Right now, you must do this manually by creating a text file with the Spanish description in the respective video folder (e.g., inside `ready_to_publish/es_<name-of-video>_<datestamp>/`) so that it can be used during the publishing phase.
