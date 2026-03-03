---
title: how_to_create_source_images_and_videos_for_weird_history
description: how to create source images and videos for weird history videos
---

# Creating Source Images and Videos for Weird History

Because the programmatic AI Video APIs are sometimes rate-limited or unconfigured (such as missing `FAL_KEY`), we rely on a manual asset generation workflow using the `browser_subagent` to orchestrate Google Flow via the browser.

## The Process

### 1. Identify the Timeline
Read the target timeline JSON file (e.g., `ghost_marriages_timeline.json`) to extract all scenes. Pay attention to:
- The **type** (`image` or `video`).
- The **prompt** string.
- The **id** (e.g., `scene_0`, `scene_1`).

### 2. Invoke the Browser Subagent
Use the `browser_subagent` tool with detailed instructions to perform the following steps for **each scene**:
1. **Navigate** to Google Flow: `https://labs.google/fx/tools/flow`.
2. **Select Mode:** Choose the appropriate generation tab ("Image" for still scenes, "Video" for video scenes).
3. **Configure Settings:** Ensure dimensions match the target resolution (1080x1920 portrait) or the required format.
4. **Prompt Input:** Paste the exact prompt from the timeline JSON.
5. **Generate & Wait:** Trigger generation and hold until completion.
6. **Download:** Click to download the output from Flow.
7. **Organize & Rename (CRITICAL VERIFICATION RULE):** 
   All manually generated assets downloaded from Google Flow **MUST** be immediately renamed in the Downloads folder to match their sequential order *before* being moved to the `in_progress` directory. This strict 1-to-1 mapping prevents duplicate images from being accidentally used or swapped during the automated FFmpeg assembly.
   Use `run_command` in the subagent or main agent to move the downloaded file to the project's staging directory:
   `/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/in_progress/en_<name-of-video>_<datestamp>/`
   - *Naming Convention:* The folder name should start with a 2-letter language code (`en` for English, `es` for Spanish), followed by the topic name, and then a datestamp (e.g., `en_ghost_marriages_2026-03-01`).
   - *File Naming Rule:* Inside the folder, the assets must use the exact sequential format (`scene_X_still.jpg` or `scene_X_video.mp4`).

### 3. Verification using the Visual Style Guide
The `timeline.json` file dictates the exact prompts, which should already follow the visual laws of Weird History (Hyper-realism, pristine conditions, exaggerated casting, no motion in stills). 
*For the complete guide on drafting these prompts and the 10-scene narrative arc (including the Scene 0 Thumbnail Rule), consult the `how_to_write_timeline_json_weird_history/SKILL.md` skill.*

### 4. Pipeline Finalization
Once all assets are properly generated and systematically named inside their `in_progress/en_<topic>_<datestamp>` staging folder, simply run `run_pipeline.py`. The script will automatically detect the manually generated assets inside `in_progress` and skip API generation for those files, proceeding directly to audio generation and FFmpeg assembly.
