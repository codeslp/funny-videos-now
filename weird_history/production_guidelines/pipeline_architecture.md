# Weird History: Automated Video Pipeline Architecture

This document defines the complete end-to-end pipeline used for generating "Weird History" videos, ensuring strict asset management, 2.5D visual dynamic standards, and verifiable publishing.

## 1. Research & Content Selection
1.  **Select Topic:** Pick a historical fact from `production_guidelines/viral_tracking.md`.
2.  **Modulation:** Read `historic_research/[category].md` and apply content moderation rules (no blood, hide violence with visual metaphors).
3.  **Draft Timeline:** Create a new `[video_name]_timeline.json` containing the script voiceover and the 9-scene breakdown (4 Stills + 1 Video + 4 Stills).

## 2. Voiceover & Folder Initialization (`generate_audio.py`)
*   **The Command:** `python3 generate_audio.py [timeline.json] [output_folder_path]`
*   **Action:** This script sends the JSON script to the Cartesia API to generate the highly expressive TTS voiceover.
*   **Timestamped Directory Rule:** The pipeline heavily relies on timestamped output folders to prevent accidental overwrites. When creating the `output_folder_path` argument for `generate_audio.py` or any subsequent script, ALWAYS append a timestamp.
    *   *Correct format example:* `output/weird_history/tudor_needle_2026-02-28_20-50-00/`

## 3. Visual Asset Generation (Google Flow)
1.  **Stills:** Using the Image Generation prompt from the timeline, manually generate scenes 1-4 and 6-9 in Google Flow. **CRITICAL:** Do NOT include descriptions of motion in these still prompts.
2.  **Video:** Using the Video Generation prompt, generate scene 5 (The Hero Video) in Google Flow TV.
3.  **Renaming Constraint:** As the assets are downloaded, they MUST be renamed exactly to `scene_1_still.jpg`, `scene_2_still.jpg`, `scene_5_video.mp4`, etc., and moved strictly into the current project's timestamped directory.

## 4. Automation & Assembly (`manual_assembly.py`)
*   **Action:** Point `manual_assembly.py` to the timestamped `build_dir` and the original timeline JSON.
*   The script executes the following automated pipeline:
    1.  **Transcription:** Uses WhisperX to perfectly frame word-by-word timestamps locally.
    2.  **Duplicate Hash Check:** Scans all visual assets using cryptographic hashing to ensure no two files are identical (preventing upload errors).
    3.  **Slow Smooth Zoom Filter:** Detects `.jpg` images and applies an FFmpeg `zoompan` upscale displacement filter to apply continuous smooth camera zoom movement in 2D space.
    4.  **Final FFmpeg Render:** Combines the visual assets, the Cartesia audio track, dynamic text captions, and writes everything to `final_render.mp4` inside the timestamped output directory.

## 5. Multi-Lingual Duplication (`duplicate_video.py`)
*   **Action:** To create a foreign language version of an existing video, use `python3 duplicate_video.py [translated_timeline.json] [original_build_metadata.json]`.
*   **Workflow:** 
    1.  Create a translated copy of the timeline JSON (e.g. `timeline_es.json`). 
    2.  Update the `language` field (e.g. "es").
    3.  Update the `tts_voice_id` to a voice that supports the target language.
    4.  Run the duplication script. It will bypass visual rendering and reuse the original assets defined in the old build metadata, only generating the new TTS and translated captions.

## 5. Multi-Platform Publishing (`publish_video.py`)
*   **Action:** Edit `publish_video.py` to point to the correct timestamped `build_dir` and `final_render.mp4`, providing a catchy title and description.
*   **Platform Push:** Uploads the final video via API endpoints to YouTube Shorts, Facebook Reels, TikTok, and Instagram Reels.
*   **Logging Output:** Outputs an automated `publish_log.json` confirming receipt on each platform.
*   **Viral Tracker Sync:** The publisher script automatically searches `viral_tracking.md` for the topic name, shifts the status to `✅ Completed`, and writes the direct markdown link to the MP4 file in the table.
