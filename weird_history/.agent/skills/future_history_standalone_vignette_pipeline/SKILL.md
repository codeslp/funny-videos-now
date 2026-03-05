---
title: future_history_standalone_vignette_pipeline
description: Streamlined pipeline for producing standalone Future History vignettes — each published individually as sting + vignette (no episode assembly, no outro).
---

# Future History: Standalone Vignette Pipeline

This pipeline produces **individual standalone videos** — each vignette is its own publishable video. No episode assembly, no interstitial cards, no outro.

> [!IMPORTANT]
> Each `final_render.mp4` from the stitch pipeline already includes the intro sting prepended. That IS the final deliverable.

---

## Pipeline Summary

```
Phase 1: Write timeline JSON (11 scenes, storytelling block)
Phase 2: Generate assets via Google Flow (8 stills + 3 hero videos)
Phase 3: Run pipeline → final_render.mp4 (sting + vignette)
Phase 4: Create title, description (user creates thumbnail)
Phase 5: Publish
```

---

## Phase 1: Write Timeline JSON

Write an 11-scene timeline JSON per the `how_to_write_timeline_json_future_history` skill. Apply storytelling rules from `applied_storytelling_future_history`.

**Output:** `weird_history/future_history/<topic>_timeline_en.json`

---

## Phase 2: Generate Source Assets

Generate 11 assets per vignette via Google Flow browser workflow per `how_to_create_source_images_and_videos_for_future_history`:

- **8 still images** → `scene_X_still.jpg` (scenes 0, 2, 3, 5, 6, 7, 9, 10)
- **3 hero videos** → `scene_X_video.mp4` (scenes 1, 4, 8)
- **Images:** Model "nano banana 2", 16:9 landscape
- **Videos:** Model "Veo 3.1 - Quality", 16:9 landscape

**Build directory:** `output/future_history/in_progress/<build_dir>/`

---

## Phase 3: Run Pipeline

```bash
python3 weird_history/pipeline/run_pipeline.py \
  weird_history/future_history/<topic>_timeline_en.json \
  --build-dir "output/future_history/in_progress/<build_dir>"
```

The pipeline generates TTS, music, and assembles the video with the intro sting prepended.

**Output:** `<build_dir>/final_render.mp4` — this IS the publishable video.

---

## Phase 4: Title & Description

For each vignette, create:

1. **Title** — Short, punchy, YouTube-optimized. Include "Future History" series identifier.
2. **Description** — Hook, context, CTA, source URLs, hashtags.
3. **Thumbnail** — User creates this manually.

Save to: `<build_dir>/description.txt`

---

## Phase 5: Publish

Once user confirms thumbnail is ready:

```bash
python3 weird_history/publish_episode_NNN.py
```

Or publish manually. Then update `viral_tracking.md` and `memory.md`.

---

## Sub-Skills Reference

| Phase | Skill |
|:---|:---|
| Timeline | `how_to_write_timeline_json_future_history`, `applied_storytelling_future_history` |
| Assets | `how_to_create_source_images_and_videos_for_future_history` |
| Stitch | `stitch_final_render_future_history` |
| Publish | `how_to_publish_video_weird_history` |

---

## Quick Checklist (Per Vignette)

```
[ ] Timeline JSON with storytelling block
[ ] 11 assets generated (8 stills + 3 videos)
[ ] Pipeline run → final_render.mp4
[ ] Title + description created
[ ] Thumbnail created (by user)
[ ] Published + tracking updated
```
