---
title: weird_history_end_to_end_pipeline
description: Master pipeline outlining the end-to-end production workflow for Weird History episodes.
---

# Weird History: End-to-End Pipeline

This master skill outlines the structured 7-phase process for creating **Weird History** episodes. Each episode consists of standalone historical vignettes compiled into a single long-form video.

> [!NOTE]
> Weird History (the original series) uses 10-scene narratives with an escalating structure. Unlike Future History, it relies on historical or pseudo-historical settings.

---

## The 7-Phase Workflow

### Phase 1: Planning & Timeline JSONs

For each vignette planned for the episode:
1. Select a topic from the research files.
2. Write a `timeline_en.json` file using the `how_to_write_timeline_json_weird_history` skill.
3. Ensure the script follows the 10-scene limitation and strict content moderation (no death, no minors) per the `weird_history_video_production` knowledge item.

### Phase 2: Source Asset Generation

1. Use the `browser_subagent` to manually generate assets on Google Flow.
2. Follow the instructions in `how_to_create_source_images_and_videos_for_weird_history`.
3. Organize all downloaded assets sequentially (`scene_X_still.jpg`, `scene_X_video.mp4`) in the build directory:
   `output/weird_history/in_progress/en_<topic>_<date>/`

### Phase 3: Run the Content Pipeline

For each vignette, execute the automated runner:

```bash
python3 weird_history/pipeline/run_pipeline.py \
  weird_history/templates/<topic>_timeline_en.json \
  --build-dir "output/weird_history/in_progress/en_<topic>_<date>"
```

### Phase 4: Build Episode Intro (Global context)

1. Use `how_to_build_episode_intro` to generate the custom episode introduction.
2. Ensure the intro voiceover, music, and compilation of preview slideshow images are successfully merged into an `episode_intro_segment.mp4`.

### Phase 5: Build Interstitial Cards

1. Follow `how_to_build_interstitial_cards` to generate text-based separator cards to bridge between the vignettes.
2. Ensure the bass thump SFX is timed correctly for each card.

### Phase 6: Episode Assembly

1. Follow `how_to_assemble_episode` (or `how_to_assemble_future_history_episode` adapted for Weird History).
2. Use FFmpeg to concatenate: `Intro Segment` → `Vignette 1` → `Interstitial` → `Vignette 2` → `Interstitial` → `Vignette 3` → `Outro`.
3. The result is the `full_episode.mp4`.

### Phase 7: Publishing & Tracking

1. Generate standard YouTube descriptions and titles according to `how_to_publish_video_weird_history`.
2. Ensure a thumbnail is extracted and staged.
3. Execute `publish_video.py` or the designated publishing script.
4. Keep track of all statuses in `viral_tracking.md` and document the run in `memory.md`.
