---
title: master_weird_history_pipeline_english
description: Complete end-to-end pipeline for creating and publishing Weird History short-form comedy videos in English — from idea selection through research, timeline JSON authoring, visual asset generation, final render assembly, and multi-platform publishing.
---

# Master Weird History Pipeline (English)

This is the definitive, end-to-end reference for producing a Weird History short-form video in English. It consolidates every sub-skill into a single linear workflow. Follow each phase in order.

---

## Phase 0: Idea Selection

### 0.1 Open the Tracking Document
- File: `weird_history/production_guidelines/viral_tracking.md`
- Scan for entries marked `⏳ Not Built`
- Skip any entries marked `🔄 In Progress` or `✅ Completed`

### 0.2 Pick a Topic
- **User preference:** Select from **Tier 2** (middle of the list) first — save Tier 1 bangers for later.
- Each tracking row has a `[Link]` column pointing to the research file + heading anchor in `weird_history/historic_research/`.

### 0.3 Mark as In Progress
- Change the selected topic's status from `⏳ Not Built` to `🔄 In Progress` in `viral_tracking.md`.

---

## Phase 1: Research & Validation

### 1.1 Read the Research Entry
Research files live in `weird_history/historic_research/` (9 categories, 450 entries across 18 files). Each entry follows this exact format:

```markdown
## [Number]. [Catchy Title] ([Region/Era])
**Description:** 3-4 entertaining sentences.
**Visual Elements:**
- [Scene/shot description 1]
- [Scene/shot description 2]
- [Scene/shot description 3]
- [Optional scene/shot description 4]
**Caption Summary:** "[Punchy social media line]"
**Citation & Link:**
- [Source Name - Article Title](URL)
```

Extract: Description, Visual Elements, Caption Summary, and Citation URLs.

### 1.2 Verify Sources
- Every historical claim must be traceable to at least one reputable source (Wikipedia, academic journals, museum collections, Britannica, Atlas Obscura, NPR, BBC, Smithsonian).
- If a claim seems too wild, find an extra citation.
- Note scholarly debates when they exist.

### 1.3 Run the Content Moderation Pre-Check
Before proceeding, mentally verify the topic against these rules:

| Rule | Requirement |
|------|-------------|
| **Banned words** | Never use `die`, `dying`, `kill`, `dead`, `death`, `died`, `sexual`, `drugs`, `cocaine`, `heroin`, `teenagers`, `teens`, `preteens`, `school kids`, `school dances` in scripts or prompts. |
| **No minors** | Age-up all characters to "young adults," "men," "women." If the absurdity relies on participants being children, drop the fact entirely. |
| **No blood/gore** | Use visual metaphors (falling rose petals, red fabric) instead. |
| **Intimacy implied** | Show reactions, never explicit acts. Prompt "fully clothed," "G-rated," "comedic." Ban "sheer," "see through," "skimpy clothing." |
| **Medical references** | Soften to "ancient remedies." Frame the historical doctor as foolish, not the patient as suffering. |
| **Cultural sensitivity** | Humor targets the ABSURDITY of the situation, never the people or culture. |
| **Violence** | Frame as slapstick/cartoonish. Drop human sacrifice facts entirely. |

---

## Phase 2: Choose a Visual Style

Pick ONE of three styles based on the topic:

| Style | Best For | Key Prompt Modifiers |
|-------|----------|---------------------|
| **Hyper-Realism** (default) | Most topics — makes absurd facts look real | `hyper-realistic portrait photography, 8k resolution, cinematic lighting, documentary style realism, shot on 35mm lens, photorealistic. No painting.` |


---

## Phase 3: Write the Timeline JSON

### 3.1 The 10-Scene Arc (Required Structure)

Every Weird History video follows this exact scene structure:

| Scene | Type | Purpose | Duration |
|-------|------|---------|----------|
| **Scene 0** | `image` | Thumbnail — 1 clean still of an attractive woman from the time period, no text/captions | ~2.0s |
| **Scene 1** | `video` | Hero hook — a beautiful woman holding/looking at a relevant item | ~4.0s |
| **Scenes 2-4** | `image` | Hook & Setup — establishing the bizarre historical context | ~3-4s each |
| **Scene 5** | `video` | Punchline — the main bizarre action comes to life | ~4-5s |
| **Scenes 6-9** | `image` | Explanation & CTA — expanding on the fact, modern comparison, call to action | ~3-4s each |

### 3.2 Prompt Formulation (STRICT)

Every prompt must follow this formula:
**`[EXPLICIT CHARACTER DESCRIPTION] + [ACTION FROM RESEARCH] + [REALISM STYLE MODIFIER] + [SAFETY MODIFIER]`**

#### Core Prompt Rules

1. **Character Casting Extremes:** All characters must be either *Extremely Attractive* (`jaw-droppingly gorgeous`, `supermodel features`) OR *Comically Ugly/Weird* (`bizarre funny facial features`, `Willem Dafoe vibes`). No average-looking people.
2. **Female Characters:** All female characters in image prompts MUST be explicitly described as gorgeous and shapely.
3. **Character Consistency:** Do NOT rely on AI to "remember" characters. Precisely define the character's physical description, clothing, and features in *every single prompt*.
4. **No Motion in Image Prompts (CRITICAL):** Do NOT describe motion or movement in `image` type prompts. Motion is ONLY for `video` type prompts. Google Flow struggles with implied motion in stills.
5. **Color:** Always prompt for `vibrant colors`, `hyper-saturated`, `cinematic lighting`. Never default to dusty, brown, or sepia.
6. **Settings:** Force `pristine condition`, `brand new construction`, `gleaming`. NEVER prompt `ancient`, `ruins`, `weathered`, `dusty`.
7. **Realism Suffix:** Every prompt must end with: `8k resolution, cinematic lighting, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.`

### 3.3 Script Writing Rules

- Do NOT use banned words in the `script` field (see Phase 1.3).
- Use euphemisms: "ended his life," "met their end," "passed away."
- Write in a surprised, entertaining tone: "But here's the thing...", "The wildest part?", "It gets better..."
- Include modern comparisons: "basically the medieval version of Tinder."

### 3.4 JSON File Format

Save to: `weird_history/pipeline/<snake_case_topic>_timeline.json`

```json
{
    "title": "Title of the Video",
    "script": "The full spoken voiceover script goes here...",
    "tts_voice_id": "1f575487-6f3d-40e0-862a-814f55b5fb15",
    "language": "en",
    "series": "weird_history",
    "scenes": [
        {
            "id": "scene_0",
            "type": "image",
            "prompt": "Hyper-realistic portrait photography of a jaw-droppingly gorgeous 25-year-old [era] woman with beautiful features, wearing a pristine [era-appropriate dress]. Looking directly at the camera. 8k resolution, cinematic lighting, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.",
            "duration": 2.0
        },
        {
            "id": "scene_1",
            "type": "video",
            "prompt": "...",
            "duration": 4.0
        }
    ]
}
```

**Voice ID:** `1f575487-6f3d-40e0-862a-814f55b5fb15` (Cartesia "Ariane - Captivating Tone" — sultry woman narrator).

---

## Phase 4: Generate Visual Assets (Manual)

Because we do NOT use fal.ai (costs money), all image and video assets are generated manually via browser.

### 4.1 Create the Staging Directory

```
output/weird_history/in_progress/en_<topic_name>_<YYYY-MM-DD>/
```

Example: `output/weird_history/in_progress/en_ghost_marriages_2026-03-01/`

### 4.2 Generate Each Scene in Google Flow

For **each scene** in the timeline JSON:

1. Navigate to [Google Flow](https://labs.google/fx/tools/flow) in browser.
2. Select the appropriate mode:
   - **"Image"** for `type: "image"` scenes
   - **"Video"** (Flow TV) for `type: "video"` scenes
3. Set dimensions to **1080x1920 portrait**.
4. **CRITICAL:** Always select **x1** in the generation count selector — do NOT use x2/x3/x4. Use PORTRAIT MODE.
5. Paste the exact prompt from the timeline JSON.
6. Generate and wait for completion.
7. Download the result.

### 4.3 Rename & Organize (CRITICAL VERIFICATION RULE)

All downloaded assets MUST be immediately renamed to match their sequential order **before** being moved to the staging directory:

| Scene Type | File Name |
|------------|-----------|
| Image scene | `scene_0_still.jpg`, `scene_2_still.jpg`, etc. |
| Video scene | `scene_1_video.mp4`, `scene_5_video.mp4`, etc. |

This strict 1-to-1 mapping prevents duplicate images from being accidentally used or swapped during FFmpeg assembly.

Move renamed files into the staging directory:
```bash
PROJECT="/Users/bfaris96/Claude Code Markdown/funny_video_generator"
DEST="$PROJECT/output/weird_history/in_progress/en_<topic>_<date>"
cp ~/Downloads/renamed_file.jpg "$DEST/scene_0_still.jpg"
```

### 4.4 Verify All Assets Present

Before proceeding, verify the staging folder contains all expected files:
```bash
DIR="/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/in_progress/en_<topic>_<date>"
ls -la "$DIR"
```

Expected: 8 still images (`scene_0_still.jpg`, `scene_2_still.jpg`, `scene_3_still.jpg`, `scene_4_still.jpg`, `scene_6_still.jpg`, `scene_7_still.jpg`, `scene_8_still.jpg`, `scene_9_still.jpg`) + 2 hero videos (`scene_1_video.mp4`, `scene_5_video.mp4`).

---

## Phase 5: Run the Pipeline (Audio + Assembly)

### 5.1 Execute the Pipeline Runner

```bash
python weird_history/pipeline/run_pipeline.py \
  weird_history/pipeline/<topic>_timeline.json \
  --build-dir "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/in_progress/en_<topic>_<date>"
```

The pipeline automatically:
1. **Detects existing visual assets** in the build directory and skips API generation.
2. **Generates TTS voiceover** (`voiceover.wav`) via Cartesia API.
3. **Generates underscore music** (`background_music.mp3`) via ElevenLabs (if configured).
4. **Runs WhisperX** for forced alignment → `word_timestamps.json` (millisecond-accurate word-level timestamps for bouncy captions).
5. **Assembles final video** via FFmpeg (`assemble_video.py`):
   - Concatenates all visuals in sequential order.
   - Applies steady slow inward zoom (Ken Burns effect) on all static images. **NEVER jitter, shake, parallax, or wobble.**
   - Overlays voiceover audio over visuals.
   - Renders textual captions (bouncy TikTok-style) based on WhisperX timestamps.

### 5.2 Output Location

The final render is saved as: `final_render.mp4` inside the staging folder:
```
output/weird_history/in_progress/en_<topic>_<date>/final_render.mp4
```

Build metadata is saved alongside it as `build_metadata.json`.

---

## Phase 6: Review & Fix (If Needed)

### 6.1 Watch the Final Render

Review `final_render.mp4` for issues. Common problems:

| Problem | Fix |
|---------|-----|
| **VO too quiet with music** | Add `normalize=0` to the `amix` filter in `assemble_video.py`. If still quiet, run VO through `loudnorm` filter (`I=-14:LRA=11:TP=-1.5`) before mixing. |
| **Wrong image aspect ratio** | Use Pillow or ImageMagick to crop/pad the specific image to `1080x1920`, then re-run the assembly. |
| **Audio out of sync** | Delete the previous `_main_segment.mp4` and re-run assembly so FFmpeg recalculates durations. |
| **Single scene wrong** | Regenerate only that specific `scene_N` asset, replace it in the staging folder, and re-run. |

### 6.2 Do NOT Regenerate the Entire Pipeline

Isolate the broken part, fix it, and restitch. Only re-run the assembly step, not the full pipeline.

---

## Phase 7: Move to Ready-to-Publish

Once the `final_render.mp4` passes review:

```bash
PROJECT="/Users/bfaris96/Claude Code Markdown/funny_video_generator"
mv "$PROJECT/output/weird_history/in_progress/en_<topic>_<date>" \
   "$PROJECT/output/weird_history/ready_to_publish/en_<topic>_<date>"
```

---

## Phase 8: Publish to All Platforms

### 8.1 Prepare the Description

Every video description MUST contain these elements in this exact order:

1. **The Hook:** 1-2 sentences summarizing the premise.
2. **The Context:** Brief explanation of the historical fact.
3. **The CTA:** "Would you try this? Let us know!"
4. **The Research Link (CRITICAL):**
   - Include a link to the source article.
   - **Verify the URL is active** before publishing.
   - **Formatting rule:** There MUST be a trailing space and double-newline (`\n\n`) after the URL before hashtags begin. If hashtags touch the URL, the link breaks on social platforms.
   - Format: `📖 Read the full historical research here: [LINK] \n\n#hashtag1 #hashtag2`
5. **Hashtags:** 5-7 targeted hashtags (#weirdhistory, #historyfacts, etc.)

### 8.2 Execute the Publish Script

```bash
python weird_history/pipeline/publish_video.py \
  --build_dir "/path/to/ready_to_publish/en_<topic>_<date>" \
  --tracking_topic "Exact Topic Name from viral_tracking.md" \
  --title "😂 Short Catchy Title | Weird History" \
  --description "Hook sentence here.\n\nContext explanation.\n\nWould you try this? Let us know!\n\n📖 Read the full historical research here: https://source-url.com \n\n#weirdhistory #historyfacts #history #educationalcomedy #storytime"
```

### 8.3 Target Platforms

The publish script uploads to all four platforms simultaneously:

| Platform | API / Method | Required .env Keys |
|----------|-------------|-------------------|
| **YouTube Shorts** | YouTube Data API v3 (OAuth resumable upload) | `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` |
| **TikTok** | Content Posting API | `TIKTOK_ACCESS_TOKEN` |
| **Facebook Reels** | Graph API v25.0 | `FACEBOOK_PAGE_ID`, `FACEBOOK_ACCESS_TOKEN` |
| **Instagram Reels** | Instagram Graph API (container-based) | `INSTAGRAM_ACCOUNT_ID`, `FACEBOOK_ACCESS_TOKEN` |

A `.approved` file must exist in the build directory for publishing to proceed (manual approval gate).

### 8.4 Post-Publish Automation

On success, the publish script automatically:
1. Creates `publish_log.json` inside the build directory noting which platforms succeeded/failed.
2. Updates `viral_tracking.md` — changes the topic status to `✅ Completed` and links the output path.
3. Archives the folder from `ready_to_publish/` to `output/weird_history/published/`.

---

## Quick Reference: File Paths

| Asset | Path |
|-------|------|
| Viral tracking (master idea list) | `weird_history/production_guidelines/viral_tracking.md` |
| Research entries | `weird_history/historic_research/` (9 categories, 18 files) |
| Research master index | `weird_history/historic_research/master_index.md` |
| Content moderation rules | `weird_history/production_guidelines/content_moderation_review.md` |
| Visual style guide | `weird_history/production_guidelines/visual_style_guide.md` |
| Prompt templates | `weird_history/production_guidelines/prompt_templates.md` |
| Pipeline runner | `weird_history/pipeline/run_pipeline.py` |
| Assembly script | `weird_history/pipeline/assemble_video.py` |
| Audio generation | `weird_history/pipeline/generate_audio.py` |
| Timeline JSONs | `weird_history/pipeline/<topic>_timeline.json` |
| Staging (in-progress) | `output/weird_history/in_progress/en_<topic>_<date>/` |
| Ready to publish | `output/weird_history/ready_to_publish/en_<topic>_<date>/` |
| Published archive | `output/weird_history/published/` |
| Publisher script | `src/publisher.py` |

## Quick Reference: Bash Troubleshooting

### Paths with Spaces (zsh)
This project lives in a path with spaces. Always quote paths or use variables:
```bash
PROJECT="/Users/bfaris96/Claude Code Markdown/funny_video_generator"
ls "$PROJECT/output/weird_history/in_progress/"
```

### Getting Media Duration
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 file.mp4
```

### Mixing Video + Music + Voiceover
```bash
VO_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 voice.wav)
FADE_START=$(echo "$VO_DURATION - 1" | bc)
ffmpeg -y -i video.mp4 -i voiceover.wav -i background_music.wav \
  -filter_complex "[2:a]volume=0.35,afade=t=out:st=${FADE_START}:d=1[music];[1:a][music]amix=inputs=2:duration=first:normalize=0[aout]" \
  -map 0:v -map "[aout]" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 192k -t $VO_DURATION output.mp4
```

---

## Sub-Skills Referenced

This master skill consolidates the following individual skills:
1. `how_to_research_weird_history_content` — Phase 1
2. `how_to_write_timeline_json_weird_history` — Phases 2-3
3. `how_to_create_source_images_and_videos_for_weird_history` — Phase 4
4. `stitch_final_render` — Phase 5
5. `how_to_fix_finished_videos` — Phase 6
6. `how_to_publish_video_weird_history` — Phase 8
7. `bash_commands_and_troubleshooting` — Quick Reference
