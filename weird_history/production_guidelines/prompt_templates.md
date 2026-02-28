# Video Generation Prompt Templates

This document contains the prompt templates to be fed into the Gemini script generator, which will format the final text prompts for the Veo3 / FlowTV API. Each template maps to one of our three core artistic styles defined in the `visual_style_guide.md`.

## Core Guidelines for all Video Prompts:
*   **Motion over Stillness:** Veo3 works best when a clear motion or action is defined. 
*   **Color Saturation Mandatory:** As established, we must over-index on color to combat the "boring history" default. All prompts MUST include high saturation modifiers.
*   **No Text On-Screen in the Image:** The AI struggles with text. Any text needed (captions, subtitles) will be layered in post-production.
*   **Safe for Work (SFW):** The prompt generator must strip graphic descriptions of violence or anatomy and replace them with comedic equivalents or focus on the *reaction* rather than the action.

---

## 🎨 Style 1: The Absurd Renaissance (Hyper-Realistic Classical Painting)

**Use Case:** Highly formal, serious-sounding historical practices (royalty, public ceremonies, complex dating rituals) that look hilarious when depicted with intense realism.

**Template Structure:**
> `[WIDE SHOT / CLOSE UP] of [DETAILED SUBJECT DESCRIPTION] performing [COMEDIC BUT HISTORICALLY ACCURATE ACTION] in [DETAILED HISTORICAL SETTING]. High renaissance oil painting brought to life, hyper-realistic, vivid and highly saturated colorful oil paints. Dramatic chiaroscuro lighting, masterpiece painting style. Comedic exaggerated facial expressions. Hyper-detailed textures on the clothing. Vibrant neon undertones to lighting, cinematic.`

**Example Output (Public Bedding Ceremony):**
> *Wide shot of a terrified European king and queen sitting nervously in a massive, ornate four-poster bed while dozens of nobles awkwardly stare at them. High renaissance oil painting brought to life, hyper-realistic, vivid and highly saturated colorful oil paints. Dramatic chiaroscuro lighting, masterpiece painting style. Comedic exaggerated facial expressions on the nobles. Hyper-detailed textures on the royal clothing. Vibrant neon undertones to lighting, cinematic.*

---

## 🧸 Style 2: Saturated Claymation / Stop-Motion 

**Use Case:** Practices involving gross concepts, medicine (leeches/tapeworms), animals, or anything that would trigger content moderation if rendered highly realistic. The claymation style softens the blow and adds inherent comedy.

**Template Structure:**
> `[MEDIUM SHOT] of a [QUIRKY SUBJECT DESCRIPTION] doing [BIZARRE ACTION]. Vibrant claymation animation style, Aardman stop-motion aesthetic. Plastiline clay textures visible on characters. Bright, primary saturated colors. Studio miniature lighting, slightly jerky comedic motion. Incredibly detailed clay figures, humorous framing.`

**Example Output (Frog Pregnancy Test):**
> *Medium shot of a 1940s scientist in a white lab coat enthusiastically holding up a bewildered-looking green frog. Vibrant claymation animation style, Aardman stop-motion aesthetic. Plastiline clay textures visible on the scientist's face and the frog. Bright, primary saturated electric colors. Studio miniature lighting, slightly jerky comedic motion. Incredibly detailed clay figures, humorous framing.*

---

## 👁️ Style 3: Immersive First-Person (POV)

**Use Case:** Love, intimacy, courting, or any direct interaction. Places the viewer directly into the shoes of the historical subject for maximum "Main Character Energy" engagement on TikTok.

**Template Structure:**
> `[FIRST PERSON POV / GOPRO ANGLE] looking down at [MY OWN HANDS / WHAT IM HOLDING], interacting with [SUBJECT IN FRONT OF ME]. Hyper-realistic modern 8k photography, ultra-wide angle lens distortion. Blindingly vibrant daytime lighting, incredibly saturated colors. Immersive and chaotic atmosphere. [SPECIFIC REACTION FROM SUBJECT IN FRONT].`

**Example Output (Armpit Apple):**
> *First person POV GoPro angle looking down at my own hands offering a shiny red apple to a disgusted-looking medieval woman standing in front of me. Hyper-realistic modern 8k photography, ultra-wide angle lens distortion. Blindingly vibrant daytime lighting, incredibly saturated colors. Immersive and chaotic atmosphere. The woman is reeling backward with a comedic look of total disgust.*
