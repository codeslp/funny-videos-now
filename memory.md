# Project Memory & Instructions

## Video Generation Workflow ("Google Flow" / Hybrid Strategy)
When the user requests to "create the video" using the "Google flow", the **FULL** manual hybrid pipeline must be executed. Do NOT stop after generating just one asset. 

**The Pipeline Steps:**
1. **Content Source:** Review the chosen historical fact from the research / `viral_tracking.md`.
2. **Script & Prompts Generation:** Run `script_generator.py` to build the 9-scene script (or manually ensure there are 8 Stills and 1 Hero Video).
3. **Google Flow (Browser):** Open Chrome and navigate to Google Flow (labs.google/fx/tools/flow).
    *   **Stills:** Generate 8 static images based on the prompts. Ensure no motion is requested in the prompt.
    *   **Hero Video:** Switch to Video/Ingredients mode and generate 1 high-quality video clip for the climax/punchline.
4. **Download & Rename:** Download all 9 assets from the browser. *CRITICAL:* Immediately rename them sequentially (e.g., `scene_1_still.jpg`, `scene_2_still.jpg`, `scene_5_video.mp4`) to avoid FFmpeg assembly errors.
5. **Asset Staging:** Move the renamed assets into a specific `output/[date_topic]` folder.
6. **Voiceover:** Create or generate the voiceover audio for the script (via Cartesia API or manual recording).
7. **Final Render:** Assemble the stills (with parallax), the hero video, and the voiceover into a final assembled video, complete with WhisperX captions. 
8. **Logging:** Update `viral_tracking.md` with the path to the final assembled video.

*Rule: "Creating the video" means delivering the `final_assembled.mp4` with all components mixed together, not just downloading raw clips.*


