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

---

## Winning Visual Aesthetics for "Weird History"
Based on TikTok trends, AI virality metrics, and our need for comedy, here are the top 3 visual styles we will use. We should experiment to see which one performs best, or rotate them to keep the feed fresh.

### Style 1: "The Absurd Renaissance" (Hyper-Realistic Classical Painting brought to life)
This style takes the very serious, highly detailed aesthetic of a Baroque or Renaissance painting and applies it to an incredibly stupid or funny situation. The juxtaposition is what makes it viral.
*   **Vibe:** Looks like a masterpiece hanging in the Louvre, but the subject is a guy getting hit with a fish.
*   **Prompt Keywords:** `high renaissance oil painting style, hyper-realistic, vivid colorful oil paints, dramatic chiaroscuro lighting, masterpiece, incredibly detailed faces, historical clothing.`
*   **Best For:** Serious-sounding practices like "The Public Bedding Ceremony" or "Roman Cults." 

#### 🌍 Regional Variation: Traditional & Romanticized Painting
If a custom originates from a specific non-Western European region, substitute the "Renaissance" keywords with that region's traditional or romanticized painting style to make the absurdity fit the culture:
*   **Middle East / North Africa:** Use `19th-century Orientalist painting style, vibrant desert colors, romanticized lighting, hyper-detailed textiles.`
*   **East Asia (China/Japan/Korea):** Use `Traditional Ukiyo-e woodblock print style with hyper-saturated colors` or `Vibrant traditional silk painting brought to vivid life, detailed brushwork.`
*   **South Asia (India):** Use `Traditional Mughal miniature painting style, vibrant jewel tones, intricate gold leaf detailing.`
*   **The Americas / Indigenous:** Use `Vivid historical Codex-style illustrations brought to life` or `19th-century romanticized frontier painting, dramatic sweeping lighting.`


### Style 2: "Saturated Claymation / Stop-Motion" (The Adult Swim Style)
Claymation inherently looks quirky and slightly unsettling, which perfectly matches weird history. It softens any violence/grossness because it looks like a toy, bypassing content moderation easily.
*   **Vibe:** Robot Chicken meets the History Channel.
*   **Prompt Keywords:** `vibrant claymation style, stop-motion animation aesthetic, plastiline clay textures, bright primary colors, studio miniature lighting, highly detailed clay figures, comedic framing.`
*   **Best For:** Medical horrors (leeches, tapeworms) or things involving animals (frogs, snakes, goat skins).

### Style 3: "Immersive First-Person POV" 
A massive trend on TikTok involves putting the viewer directly into the shoes of a historical person. Since many of our facts are relatable (dating, marriage), putting the camera in the eyes of the suitor is incredibly engaging.
*   **Vibe:** You are literally standing in an ancient village experiencing this firsthand.
*   **Prompt Keywords:** `GoPro POV style, first-person perspective, hyper-realistic photography, vibrant daytime lighting, ultra-wide angle lens, looking down at hands, immersive.`
*   **Best For:** Love/Romance (e.g., being handed an armpit apple, or looking at a giant cheese wheel).



---

## Prompt Formulation Structure
Every video prompt we send to the video generation API should follow this structure to guarantee the aesthetic holds:

**[SUBJECT/ACTION FROM RESEARCH]** + **[VISUAL STYLE MODIFIER]** + **[COLOR/LIGHTING MODIFIER]** + **[SAFETY/MODERATION MODIFIER]**

**Example for "Armpit Apple" (Using Style 1):**
> *A handsome young medieval man nervously eating an apple given to him by a young woman. High renaissance oil painting style, vivid colorful oil paints, dramatic chiaroscuro lighting. Vibrant colors, highly saturated. Comedic facial expressions, PG-rated, fully clothed.*

---

## The Hybrid Production Pipeline (The "Hook & Hold" Method)

To optimize costs, speed up pipeline execution, and maximize audience retention, we utilize a **Hybrid Video Assembly Strategy**. This involves mixing static images (with programmed motion) and high-end AI video clips in a single timeline. 

### Why the Hybrid Strategy Works
1. **Cost & Speed:** It limits the use of expensive/slow video generation APIs to just 1–2 "hero" moments per Short/Reel.
2. **Dynamic Pacing:** Rapidly switching between "Ken Burns" panning images and bursty video clips resets viewer attention.
3. **Narrative Focus:** Cheaper still images set up the context, and the expensive video generation delivers the weird, funny punchline.

### Tech Stack & Tooling

*   **Video Generation (The "Hero" Clips):** Flow TV
*   **Image Generation (The Context Setting):** Flow (Stills)
*   **Voiceover (TTS):** **Cartesia API** (Excellent speed, highly expressive emotion control, and perfectly suited for pacing comedic voiceovers).
*   **Transcription / Captioning:** **WhisperX** (An open-source library built on top of OpenAI's Whisper model. It forces precise millisecond-accurate word-level alignment, allowing us to generate punchy, perfectly-timed TikTok captions locally without paying API fees).
*   **Video Assembly Engine:** **FFmpeg** orchestrated by a customized Python script. (Libraries like `MoviePy` can be used to prototype the timeline, but raw FFmpeg commands generated by Python provide the most stable, reliable rendering with dynamic text overlays).

### Output and Tracking
To maintain organization, every time a new video is generated, the pipeline automatically creates a unique folder stamped with the current Date and Hour (e.g., `output/2026-02-28_14-16-01/`). 
*   **Crucial Step:** The path to this newly generated output folder MUST be manually linked/logged in the main Viral Tracking Document against the video's title to keep a perfect record of assets vs. virality metrics.

### How the Styles Pair with Hybrid Assembly

1. **The Absurd Renaissance:**
   * *Stills:* Hyper-detailed Renaissance paintings with slow, dramatic digital pans or zooms.
   * *Video:* The painting suddenly "comes to life" for the punchline. Provides a seamless and highly engaging transition.
2. **Saturated Claymation:**
   * *Stills:* Static clay scenes with programmatic "stop-motion jitter" added (shifting the image slightly simulating frame-by-frame movement). Digital panning should be avoided to preserve the physical miniature illusion.
   * *Video:* Full claymation action.
3. **Immersive First-Person POV:**
   * *Stills:* Focus strictly on establishing the environment or objects using subtle parallax. Keep "hands" out of frame during stills.
   * *Video:* Action shots involving the character's hands (reaching, grabbing, reacting).
