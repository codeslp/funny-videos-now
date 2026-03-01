# Weird History: Visual Production Style Guide

This folder contains the core guidelines, prompt templates, and artistic direction for generating the final video assets via Veo3 / FlowTV.

## Core Rule: Highly Saturated & Colorful
The default for historical content is usually dusty, brown, or sepia-toned. **We must explicitly prompt the opposite.**
*   **Why?** TikTok/Reels algorithms and users heavily favor high-contrast, vibrant, highly saturated visuals. It immediately signals that this isn't a boring documentary.
*   **Prompt Keywords to always include:** `vibrant colors`, `hyper-saturated`, `cinematic lighting`, `neon highlights`, `colorful`.

---

## Visual Rule: Character Casting (No "Average" People)
To maximize audience retention, the characters generated in the stills and videos must stand out immediately. **Characters must fall into one of two extremes: Extremely Attractive or Comically "Ugly"/Weird.**

*   **Prompting Extremes:**
    *   *The "Hot" Route:* `incredibly handsome`, `jaw-droppingly gorgeous`, `supermodel features`, `chiseled jawline`, `stunningly beautiful`.
    *   *The "Character Actor" Route:* `bizarre funny facial features`, `comically ugly character actor`, `willem dafoe vibes`, `exaggerated historical inbreeding features`, `weird bulging eyes`. 
*   **Female Character Casting Rule:** All female characters included in image prompts MUST be explicitly described as "shapely with full lips". This is a strict visual style rule for consistency.

---

## Winning Visual Aesthetic for "Weird History": Hyper-Realism
We must **stick with realism** for all generated assets. Do not use oil painting styles or claymation.

*   **Vibe:** Authentic, documentary-style photography and video that makes the absurd historical facts look like they really happened. 
*   **Character Consistency:** Do not rely on the video model to "remember" a character if there is a main character. You MUST precisely define the character's physical description, clothing, and features in *every single prompt* for the video to ensure they look identical across shots.
*   **Prompt Keywords:** `hyper-realistic portrait photography`, `8k resolution`, `cinematic lighting`, `documentary style realism`, `shot on 35mm lens`, `photorealistic`, `No painting.`
*   **Dealing with Violence / Gore:** We must never show blood. If the history involves violence, we must find an imaginative way around the violence or avoid showing it altogether. Use strong visual metaphors—for example, showing falling rose petals or waving red fabric instead of blood.

---

## Prompt Formulation Structure
Every video prompt we send to the video generation API should follow this structure to guarantee the visual style holds:

**[EXPLICIT CHARACTER DESCRIPTION]** + **[ACTION FROM RESEARCH]** + **[REALISM STYLE MODIFIER]** + **[SAFETY/MODERATION MODIFIER]**

**CRITICAL RULE FOR STILL IMAGES:** DO NOT include descriptions of motion or movement (e.g., "shaking his head", "falling into a bowl", "running") in prompts intended for static image generation (Stills). Google Flow struggles to render implied motion in stills, often resulting in visual anomalies or completely failing. Motion should ONLY be described in prompts meant for Video (Flow TV).

**Example for "Armpit Apple":**
> *A 25-year-old medieval peasant man with sharp cheekbones, messy brown hair, wearing a rough-spun brown tunic. He is nervously eating an apple given to him by a young woman. Hyper-realistic portrait photography, 8k resolution, cinematic lighting, dramatic shadows, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.*

---

## The Hybrid Production Pipeline (The "Hook & Hold" Method)

To optimize costs, speed up pipeline execution, and maximize audience retention, we utilize a **Hybrid Video Assembly Strategy**. This involves mixing static images (with programmed motion) and high-end AI video clips in a single timeline. 

### Why the Hybrid Strategy Works
1. **Cost & Speed:** It limits the use of expensive/slow video generation APIs by relying heavily on cheap image generation for the bulk of the runtime.
2. **Dynamic Pacing:** Rapidly switching between 2.5D depth-mapped parallax images and bursty video clips resets viewer attention.
3. **9-Scene Narrative Arc (The Standard):** All timelines must follow the 9-scene structure:
   - **Scenes 1-4:** 4 Stills with AI Depth Parallax (Hook & Setup)
   - **Scene 5:** 1 Hero Video (The historical punchline/action)
   - **Scenes 6-9:** 4 Stills with AI Depth Parallax (Explanation & Call to Action)

### Tech Stack & Tooling

*   **Video Generation (The "Hero" Clips):** Flow TV (MANUAL VIA BROWSER: https://labs.google/fx/tools/flow)
*   **Image Generation (The Context Setting):** Flow (Stills) (MANUAL VIA BROWSER: https://labs.google/fx/tools/flow)
*   **Asset Management (CRITICAL VERIFICATION RULE):** All manually generated assets downloaded from Google Flow *MUST* be immediately renamed in the Downloads folder to match their sequential order in the timeline (e.g., `scene_1_still.jpg`, `scene_2_still.jpg`, `scene_3_video.mp4`, etc.) before being moved to the `output` directory. This strict 1-to-1 mapping prevents duplicate images from being accidentally used or swapped during the automated FFmpeg assembly.
*   **Voiceover (TTS):** **Cartesia API** (Excellent speed, highly expressive emotion control, and perfectly suited for pacing comedic voiceovers).
*   **Transcription / Captioning:** **WhisperX** (An open-source library built on top of OpenAI's Whisper model. It forces precise millisecond-accurate word-level alignment, allowing us to generate punchy, perfectly-timed TikTok captions locally without paying API fees).
*   **Video Assembly Engine:** **FFmpeg** orchestrated by a customized Python script. (Libraries like `MoviePy` can be used to prototype the timeline, but raw FFmpeg commands generated by Python provide the most stable, reliable rendering with dynamic text overlays).

### Output and Tracking
To maintain organization, every time a new video is generated, the pipeline automatically creates a unique folder stamped with the current Date and Hour (e.g., `output/2026-02-28_14-16-01/`). 
*   **Crucial Step:** The path to this newly generated output folder MUST be manually linked/logged in the main Viral Tracking Document against the video's title to keep a perfect record of assets vs. virality metrics.

### How the Styles Pair with Hybrid Assembly

1. **Hyper-Realism:**
   * *Stills:* Hyper-realistic portrait photograph. The pipeline will automatically generate a 3D depth map and apply a dynamic 2.5D parallax push-in. **NEVER use jitter, shake, or wobble effects.** 
   * *Video:* The scene matching the subject comes to life natively.
