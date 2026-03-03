---
title: how_to_create_source_images_and_videos_for_future_history
description: How to generate visual assets for Future History videos using Google Flow via browser, with near-future prompting guidelines.
---

# Creating Source Images and Videos for Future History

Future History uses the same manual Google Flow browser workflow as Weird History, but with a near-future visual style and a higher scene count (11 scenes per entry, 3 hero videos + 8 stills).

## The Process

### 1. Identify the Timeline
Read the target timeline JSON file (e.g., `organ_loyalty_timeline_en.json`) to extract all scenes. Pay attention to:
- The **type** (`image` or `video`).
- The **prompt** string.
- The **id** (e.g., `scene_0`, `scene_1`).

**Key difference from Weird History:** Future History timelines have 11 scenes per entry (not 10), and for full compilation videos, 45-50 scenes total split across 3-4 entries.

### 2. Invoke the Browser Subagent
Use the `browser_subagent` tool with detailed instructions to perform the following steps for **each scene**:
1. **Navigate** to Google Flow: `https://labs.google/fx/tools/flow`.
2. **Select Mode:** Choose the appropriate generation tab ("Image" for still scenes, "Video" for video scenes).
3. **Configure Settings:** Set dimensions to **landscape 16:9 (1920x1080)**. Future History is long-form YouTube content, not Shorts — landscape is required.
4. **Prompt Input:** Paste the exact prompt from the timeline JSON.
5. **Generate & Wait:** Trigger generation and hold until completion.
6. **Download:** Click to download the output from Flow.
7. **Organize & Rename (CRITICAL VERIFICATION RULE):**
   All manually generated assets downloaded from Google Flow **MUST** be immediately renamed in the Downloads folder to match their sequential order *before* being moved to the `in_progress` directory.
   Use `run_command` in the subagent or main agent to move the downloaded file to the staging directory:
   `/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/future_history/in_progress/en_<name-of-video>_<datestamp>/`
   - *Naming Convention:* The folder name should start with `en`, followed by the topic name, and a datestamp (e.g., `en_organ_loyalty_2026-03-02`).
   - *File Naming Rule:* Inside the folder, assets must use the exact sequential format (`scene_X_still.jpg` or `scene_X_video.mp4`).

### 3. Near-Future Visual Style (Key Differences from Weird History)

**Weird History prompts** render pristine historical settings.
**Future History prompts** render **near-future** settings (2040s-2050s):

| Element | Weird History | Future History |
|:---|:---|:---|
| Settings | Pristine historical buildings, ancient architecture | Modern+ architecture with subtle futuristic elements |
| Technology | Period-accurate tools and objects | Holographic UIs, bioprinters, AR glasses, BCI headbands |
| Clothing | Historical garments, corsets, tunics | Contemporary clothing evolved 20 years (cleaner, more minimal) |
| Mood | "A vibrant, living ancient world" | "A recognizable near-future — not full sci-fi" |

**What to AVOID in Future History prompts:**
- Full sci-fi tropes (spaceships, laser guns, aliens, chrome everything)
- Dystopian grimdark aesthetics (the tone is comedy, not Black Mirror)
- Overly abstract/unrecognizable technology

**What to INCLUDE:**
- Recognizable modern environments with subtle upgrades
- Everyday human moments in slightly futuristic settings
- Corporate branding, apps, subscription UIs (these ground the absurdity)
- Emotional close-ups — the human reaction to the absurd situation

### 4. Content Safety Rules (SAME AS WEIRD HISTORY — NO CHANGES)

- **No banned words** in prompts or script: `die`, `dying`, `kill`, `dead`, `death`, `died`
- **No minors** in any suggestive or dangerous context
- **No blood or gore** — use metaphors (falling rose petals, red fabric)
- **No motion in still prompts** — motion ONLY in `video` type scenes
- **Character extremes** — all characters must be extremely attractive or comically ugly/weird
- **Female characters** — always described as gorgeous and shapely in image prompts
- **Full character descriptions** in every prompt — AI doesn't remember between scenes

### 5. Pipeline Finalization
Once all assets are properly generated and named in their `in_progress/en_<topic>_<datestamp>` staging folder, the pipeline script handles audio generation and FFmpeg assembly automatically.

### 6. Asset Count Reference

| Video Type | Hero Videos | Stills | Transitions | Total Scenes |
|:---|:---|:---|:---|:---|
| Single entry (pilot) | 3 | 8 | 0 | 11 |
| 4-entry compilation | 12-13 | 33 | 3-4 | ~50 |
