---
title: future_history_end_to_end_pipeline
description: Master skill covering the complete Future History production pipeline from idea selection through publishing, referencing all sub-skills at each stage.
---

# Future History: End-to-End Production Pipeline

This is the **master pipeline** for producing a complete Future History episode. Follow each phase in order. Each phase references a dedicated sub-skill with full technical details.

> [!IMPORTANT]
> Do NOT skip phases. Each phase depends on the outputs of the previous one. If a reusable asset already exists (e.g., outro video, serene music), skip its generation step but still verify it exists.

---

## Phase 0: Episode Planning

**Goal:** Select 3 entries from the research docs and order them by escalating absurdity.

### Steps

1. **Review available entries** in `weird_history/future_history/viral_tracking.md` — choose 3 entries marked `⏳ Not Built`.
2. **Order by escalation:**
   - Vignette 1 = most grounded/believable
   - Vignette 2 = weirder, higher stakes
   - Vignette 3 = most absurd (the one people share)
3. **Create the working directory:** `output/future_history/in_progress/episode_NNN/`
4. **Update `viral_tracking.md`:** Mark selected entries as `🎬 In Progress` and note the episode number.

### Reference
- Entry descriptions: `weird_history/future_history/future_customs_mashups*.md`
- Escalation rules: `applied_storytelling_future_history` skill (Stage 3.1)

---

## Phase 1: Write Timeline JSONs

**Goal:** Create the 11-scene timeline JSON for each vignette with script, prompts, and storytelling metadata.

### Steps

1. **Read the full visual style guide:** `weird_history/production_guidelines/future_history_visual_style_guide.md`
2. **Read the storytelling skill** to apply addictive narrative structure.
3. **Write 3 timeline JSONs** — one per vignette — following the 11-scene beat structure.
4. **Validate each timeline** has the mandatory `storytelling` block with all required fields.
5. **Save timelines** to `weird_history/future_history/<topic>_timeline_en.json`

### Sub-Skills
| Skill | What It Covers |
|:---|:---|
| [how_to_write_timeline_json_future_history](../how_to_write_timeline_json_future_history/SKILL.md) | Scene structure, JSON schema, voice config, safety rules, prompt formula |
| [applied_storytelling_future_history](../applied_storytelling_future_history/SKILL.md) | Script writing rules, open loops, but/therefore, specificity, dry tone |

### Outputs
```
weird_history/future_history/<topic_1>_timeline_en.json
weird_history/future_history/<topic_2>_timeline_en.json
weird_history/future_history/<topic_3>_timeline_en.json
```

---

## Phase 2: Generate Source Assets

**Goal:** Create all images and videos for each vignette using Google Flow via browser.

### Steps

1. **For each vignette** (3 vignettes × 11 scenes = 33 total assets):
   - Navigate to Google Flow (`https://labs.google/fx/tools/flow`)
   - **Images:** Select model "nano banana 2", set to 16:9 landscape
   - **Videos:** Select model "Veo 3.1 - Quality", set to 16:9 landscape
   - Paste the exact prompt from the timeline JSON
   - Generate, download, rename to `scene_X_still.jpg` or `scene_X_video.mp4`
2. **Create build directories** for each vignette:
   ```
   output/future_history/in_progress/episode_NNN/en_<topic>_<datestamp>/
   ```
3. **Move all assets** into the correct build directory with proper naming.

### Sub-Skills
| Skill | What It Covers |
|:---|:---|
| [how_to_create_source_images_and_videos_for_future_history](../how_to_create_source_images_and_videos_for_future_history/SKILL.md) | Browser workflow, near-future style, naming convention, safety rules |

### Outputs
```
output/future_history/in_progress/episode_NNN/en_<topic>_<datestamp>/
├── scene_0_still.jpg
├── scene_1_video.mp4
├── scene_2_still.jpg
├── ...
├── scene_8_video.mp4
├── scene_9_still.jpg
└── scene_10_still.jpg
```

---

## Phase 3: Stitch Individual Vignettes

**Goal:** Run the pipeline to generate TTS, music, and assemble each vignette into a `final_render.mp4`.

### Steps

1. **Run the pipeline for each vignette:**
   ```bash
   python3 weird_history/pipeline/run_pipeline.py \
     weird_history/future_history/<topic>_timeline_en.json \
     --build-dir "output/future_history/in_progress/episode_NNN/en_<topic>_<datestamp>"
   ```
2. **Verify** each `final_render.mp4` exists and plays correctly.
3. Repeat for all 3 vignettes.

### Sub-Skills
| Skill | What It Covers |
|:---|:---|
| [stitch_final_render_future_history](../stitch_final_render_future_history/SKILL.md) | Pipeline execution, dynamic scene timing, TTS, music generation |
| [bash_commands_and_troubleshooting](../bash_commands_and_troubleshooting/SKILL.md) | FFmpeg issues, common errors |

### Outputs
```
output/future_history/in_progress/episode_NNN/en_<topic>_<datestamp>/final_render.mp4  (×3)
```

---

## Phase 4: Build Episode Components

**Goal:** Create the episode intro, interstitial cards, and outro (if not already built).

### 4A: Episode Intro (~18-25s)

1. Gather 12-15 slideshow images from current + past vignettes
2. Write episode-specific serene VO ("You can stay sane in an insane time...")
3. Generate TTS for the VO
4. Assemble slideshow + VO + serene music
5. Append the pre-built intro sting (`future_history_intro_sting.mp4`)

**Skill:** [how_to_build_episode_intro](../how_to_build_episode_intro/SKILL.md)

### 4B: Interstitial Cards (3 × ~6s)

1. Select the weirdest quote from each upcoming vignette
2. Generate text-on-black card video with FFmpeg
3. Add bass thump SFX at start and end

**Skill:** [how_to_build_interstitial_cards](../how_to_build_interstitial_cards/SKILL.md)

### 4C: Episode Outro (~10-15s) — REUSABLE

> [!NOTE]
> The outro is built once and reused across all episodes. If `output/future_history/intro_outro/custom_episode_outro.mp4` already exists, **skip this step**.

1. Use the existing outro field video
2. Use the existing outro VO
3. Assemble with serene music

**Skill:** [how_to_build_episode_outro](../how_to_build_episode_outro/SKILL.md)

### Reusable Assets Checklist

| Asset | Path | Build Once? |
|:---|:---|:---|
| Intro sting | `intro_outro/future_history_intro_sting.mp4` | ✅ Already exists |
| Outro video | `intro_outro/custom_episode_outro.mp4` | ✅ Build once |
| Serene music | `music_assets/serene_episode_music.mp3` | ✅ Already exists |
| Oppressive beat | `music_assets/oppressive_beat.mp3` | ✅ Already exists |

### Outputs
```
output/future_history/episodes/episode_NNN/
├── full_episode_intro.mp4
├── interstitials/
│   ├── interstitial_1.mp4
│   ├── interstitial_2.mp4
│   └── interstitial_3.mp4
```

---

## Phase 5: Assemble Full Episode

**Goal:** Concatenate all components into the final episode video.

### Assembly Order

```
1. full_episode_intro.mp4          (episode intro + intro sting)
2. interstitial_1.mp4              (card teasing vignette 1)
3. vignette_1/final_render.mp4     (skip first 8s — vignette-level intro)
4. interstitial_2.mp4              (card teasing vignette 2)
5. vignette_2/final_render.mp4     (skip first 8s)
6. interstitial_3.mp4              (card teasing vignette 3)
7. vignette_3/final_render.mp4     (skip first 8s)
8. custom_episode_outro.mp4        (reusable outro)
```

### Steps

1. **Strip vignette intros** — each `final_render.mp4` has its own 8s intro prepended; remove it with `-ss 8`.
2. **Concatenate all segments** using FFmpeg `filter_complex` concat.
3. **Verify** total runtime is ~8-10 minutes.
4. **Save** to `output/future_history/episodes/episode_NNN/full_episode.mp4`.

### Sub-Skills
| Skill | What It Covers |
|:---|:---|
| [how_to_assemble_future_history_episode](../how_to_assemble_future_history_episode/SKILL.md) | Full assembly order, FFmpeg commands, validation checklist |

### Output
```
output/future_history/episodes/episode_NNN/full_episode.mp4
```

---

## Phase 6: Title, Description & Thumbnail

**Goal:** Create YouTube metadata and thumbnail.

### Steps

1. **Title:** Short, punchy, describes the episode theme. Include "Future History" or the series identifier.
2. **Description:** Include:
   - Hook (1-2 sentence summary)
   - Vignette summaries with timestamps
   - Source article URLs from each entry's `Citation & Links`
   - Call-to-action
   - Hashtags
3. **Thumbnail:** Generate a striking image via Google Flow or `generate_image` tool. Save to `episodes/episode_NNN/thumbnail_1.jpeg`.
4. **Save description** to `episodes/episode_NNN/description.txt`.

---

## Phase 7: Publish

**Goal:** Upload to YouTube (and other platforms), set thumbnail, update tracking.

### Steps

1. **Run the publish script** or publish manually:
   ```bash
   python3 weird_history/publish_episode_NNN.py
   ```
   - The script uploads to YouTube, sets the thumbnail, and publishes to Facebook Reels.
   - It saves `publish_log.json` with video IDs and statuses.

2. **Set thumbnail** (if not handled by publish script):
   ```bash
   python3 weird_history/set_thumbnail.py <VIDEO_ID> <thumbnail_path>
   ```

3. **Update tracking:**
   - Mark entries as `✅ Published (EN)` in `viral_tracking.md`
   - Add YouTube URL to the publishing log table
   - Update `memory.md` with completion status

4. **Organize assets:**
   - Move vignette build folders from `in_progress/episode_NNN/` into `episodes/episode_NNN/vignettes/`
   - Copy any new music to `music_assets/`

### Sub-Skills
| Skill | What It Covers |
|:---|:---|
| [how_to_publish_video_weird_history](../how_to_publish_video_weird_history/SKILL.md) | Description formatting, publish command, post-publish automation |

---

## Quick Reference: Full Pipeline Checklist

```
[ ] Phase 0: Select 3 entries, order by escalation, create working dir
[ ] Phase 1: Write 3 timeline JSONs with storytelling blocks
[ ] Phase 2: Generate 33 assets via Google Flow (11 per vignette)
[ ] Phase 3: Run pipeline → 3 × final_render.mp4
[ ] Phase 4: Build episode intro + 3 interstitial cards (+ outro if needed)
[ ] Phase 5: Assemble full_episode.mp4 (~8-10 min)
[ ] Phase 6: Create title, description, thumbnail
[ ] Phase 7: Publish, set thumbnail, update tracking, organize files
```

---

## Troubleshooting

| Issue | Solution |
|:---|:---|
| Google Flow prompt error | Refresh the page completely, re-enter prompt from scratch |
| TTS banned word rejection | Check script for `die`, `dying`, `kill`, `dead`, `death`, `died` — use euphemisms |
| FFmpeg concat resolution mismatch | Use `filter_complex` concat with `scale=1920:1080` on all inputs |
| Vignette has double intro | Strip first 8s with `-ss 8` before concatenation |
| Audio gap between segments | Use 0.5s crossfade at segment boundaries |

**Skill:** [bash_commands_and_troubleshooting](../bash_commands_and_troubleshooting/SKILL.md)
