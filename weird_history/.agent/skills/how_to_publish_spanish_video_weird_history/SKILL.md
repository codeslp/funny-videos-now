---
title: how_to_publish_spanish_video_weird_history
description: How to publish a finalized Weird History video in Spanish, format the relatable description, and track the release.
---

# Publishing a Spanish Weird History Video

Once you have a fully assembled Spanish video (`final_render.mp4`) sitting in a ready-to-publish directory (e.g., `output/weird_history/ready_to_publish/es_<name-of-video>_<datestamp>/`), the final step is to execute the publishing pipeline.

## 1. Preparing the Publishing Command

The orchestrator script for this phase is `weird_history/pipeline/publish_video.py`. This script handles uploading the video to YouTube Shorts, TikTok, Facebook Reels, and Instagram Reels simultaneously.

It accepts five arguments:
1. `--build_dir`: The path to the folder containing `final_render.mp4`.
2. `--tracking_topic`: The exact string name of the video's topic as it appears in `viral_tracking.md`.
3. `--title`: The title of the video for the social platforms, written in modern, relatable Spanish.
4. `--description`: The full, formatted description in Spanish (using `\n` for newlines).
5. `--lang`: The language code, which MUST be set to `es` for Spanish videos to route them to the correct Spanish YouTube channel.

## 2. Formatting the Description in Spanish (Visual Style Guide Rules)

According to the publishing guidelines, every description MUST be written in modern, relatable language and spoken from the **first-person perspective of a girl** (e.g., "¡No podía creer que él no quisiera mi amor en la pista de baile!"). 

**CRITICAL:** Do NOT mention historic periods in the title. Frame it purely as a relatable love/dating/life experience. The description must avoid stuffy historical framing and emphasize humor and the dating/relationship aspect.

It must contain the following elements in this order:

1. **El Gancho (The Hook):** 1-2 sentences in Spanish summarizing the premise in a relatable way.
2. **El Contexto (The Context):** A brief explanation of the crazy historical fact in Spanish.
3. **El Llamado a la Acción (The Call-To-Action - CTA):** Prompt the viewer to engage in Spanish (e.g., "¿Harías esto por amor? ¡Déjanos saber en los comentarios!").
4. **El Enlace de Investigación (The Research Link - CRITICAL):**
   - You MUST include a link to the foundational research or historical article.
   - **Verification:** You MUST verify the URL is active and resolvable before publishing.
   - **Formatting Bug Fix:** There MUST be a trailing space and a double-newline (`\n\n`) directly after the URL before any hashtags begin. If hashtags touch the URL, the link breaks.
   - *Format:* `📖 Lee la investigación histórica completa aquí: [LINK] \n\n#hashtag1 #hashtag2`
5. **Hashtags:** 5-7 targeted hashtags in Spanish and English (e.g., `#historiarara`, `#datoscuriosos`, `#historiasdeamor`, `#weirdhistory`).

## 3. Executing the Publish

**IMPORTANT: As the AI Agent, YOU are responsible for autonomously generating the relatable Spanish description from the `viral_tracking.md` topic and executing this publication command yourself using the `run_command` tool. Do NOT just print the command and ask the user to run it.**

Run the script from the root or pipeline directory. Example:

```bash
python weird_history/pipeline/publish_video.py \
  --build_dir "/path/to/ready_to_publish/es_ghost_marriages_2026-03-01" \
  --tracking_topic "Ghost Marriages (Minghun) (Ancient China)" \
  --title "😂 ¿Morir soltera? ¡Ni de broma! | Historia Rara" \
  --description "¡Imagina morir soltera y que tus padres AÚN ASÍ te obliguen a tener un matrimonio arreglado... con otro muerto! \n\nEn la antigua China, los 'Matrimonios Fantasma' se realizaban para asegurar que los espíritus solteros no estuvieran solos en la vida del más allá. Las familias vestían efigies de papel con trajes de novia rojos y los enterraban juntos. \n\n¿Dejarías que tus padres te buscaran pareja después de morir? ¡Déjanos saber en los comentarios! \n\n📖 Lee la investigación histórica completa aquí: https://example.com/ghost-marriages \n\n#historiarara #datoscuriosos #antiguachina #historiasdeamor #historia" \
  --lang es
```

## 4. Post-Publishing Automation & Manual Fallback

When executed successfully, `publish_video.py` performs the following automated cleanup:
1. **Logs the Release:** Creates a `publish_log.json` file inside the build directory.
2. **Updates Tracking:** Edits `weird_history/production_guidelines/viral_tracking.md` to change the status of the `--tracking_topic` to `✅ Completed`.
3. **Archives the Folder:** Moves the entire `es_<name-of-video>_<datestamp>` directory out of `ready_to_publish` and into the permanent `output/weird_history/published/` archive.

**IMPORTANT: Manual Uploading Required for Spanish Videos**
Because of Google OAuth account routing issues and platform preferences, the AI agent **cannot** automatically upload Spanish videos to YouTube or Facebook Reels. 
After the AI runs the `publish_video.py` script:
1. The AI MUST inform the user that the video file and metadata are ready, and that they need to manually upload it to their Spanish platforms.
2. The AI MUST tell the user to open the `youtube_metadata.txt` file located in the newly archived `output/weird_history/published/es_...` folder to copy the generated title and description for their manual uploads.
