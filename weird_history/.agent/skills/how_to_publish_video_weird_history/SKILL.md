---
title: how_to_publish_video_weird_history
description: How to publish a finalized Weird History video, format the description, and track the release.
---

# Publishing a Weird History Video

Once you have a fully assembled `final_render.mp4` sitting in a ready-to-publish directory (e.g., `output/weird_history/ready_to_publish/en_<name-of-video>_<datestamp>/`), the final step is to execute the publishing pipeline.

## 1. Preparing the Publishing Command

**CRITICAL:** Make sure you put CAPTIONS ON! Use the platform's native auto-caption generation sticker (TikTok/Reels), or if you are running custom assemblies, ensure captions are explicitly enabled.

The orchestrator script for this phase is `weird_history/pipeline/publish_video.py`. This script handles uploading the video to YouTube Shorts, TikTok, Facebook Reels, and Instagram Reels simultaneously.

It accepts four arguments:
1. `--build_dir`: The path to the folder containing `final_render.mp4`.
2. `--tracking_topic`: The exact string name of the video's topic as it appears in `viral_tracking.md` (e.g., "Ghost Marriages (Minghun) (Ancient China)").
3. `--title`: The title of the video for the social platforms.
4. `--description`: The full, formatted description (using `\n` for newlines).

## 2. Formatting the Description (Visual Style Guide Rules)

According to the publishing guidelines, every video description MUST contain the following elements in this order, formatted properly to avoid algorithmic penalties or broken links:

1. **The Hook:** 1-2 sentences summarizing the premise.
2. **The Context:** A brief explanation of the crazy historical fact.
3. **The Call-To-Action (CTA):** Prompt the viewer to engage (e.g., "Would you try this? Let us know!").
4. **The Research Link (CRITICAL):**
   - You MUST include a link to the foundational research or historical article.
   - **Verification:** You MUST verify the URL is active and resolvable before publishing. Do not post dead links.
   - **Formatting Bug Fix:** There MUST be a trailing space and a double-newline (`\n\n`) directly after the URL before any hashtags begin. If hashtags touch the URL, the link breaks on social platforms.
     - *Format:* `📖 Read the full historical research here: [LINK] \n\n#hashtag1 #hashtag2`
5. **Hashtags:** 5-7 targeted hashtags (#weirdhistory, #historyfacts, etc.)

## 3. Executing the Publish

Run the script from the root or pipeline directory. Example:

```bash
python weird_history/pipeline/publish_video.py \
  --build_dir "/path/to/ready_to_publish/en_ghost_marriages_2026-03-01" \
  --tracking_topic "Ghost Marriages (Minghun) (Ancient China)" \
  --title "😂 Dying Single in Ancient China? Ghost Marriages! | Weird History" \
  --description "Imagine dying single and your parents STILL force you into an arranged marriage... with another dead person! \n\nIn Ancient China, 'Ghost Marriages' were performed to ensure unmarried spirits wouldn't be lonely in the afterlife. Families would dress paper effigies in vibrant red wedding clothes and bury them side-by-side. \n\nWould you want your parents setting you up after you die? Let us know in the comments! \n\n📖 Read the full historical research here: https://example.com/ghost-marriages \n\n#weirdhistory #historyfacts #ancientchina #educationalcomedy #history"
```

## 4. Post-Publishing Automation (What the script does)

When executed successfully, `publish_video.py` performs the following automated cleanup:
1. **Logs the Release:** Creates a `publish_log.json` file inside the build directory noting which platforms succeeded/failed.
2. **Updates Tracking:** Edits `weird_history/production_guidelines/viral_tracking.md` to change the status of the `--tracking_topic` to `✅ Completed` and links the explicit path to the final assembled video.
3. **Archives the Folder:** Moves the entire `en_<name-of-video>_<datestamp>` directory out of `ready_to_publish` and into the permanent `output/weird_history/published/` archive.
