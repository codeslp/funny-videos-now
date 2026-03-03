---
title: how_to_write_timeline_json_weird_history
description: How to design the 9-scene Hybrid Timeline JSON and write prompts using the Weird History visual style rules.
---

# Designing the Weird History Timeline JSON

Before generating any visual assets, a narrative pipeline configuration file (`<topic>_timeline.json`) must be created. This JSON file defines the script, the TTS voice, and the sequential visual prompts for the entire video.

## 1. The "Hook & Hold" Hybrid Production Pipeline

Weird History relies on a strictly paced 10-scene narrative arc mixed between static images and two expensive AI video clips per timeline. This manages cost while maximizing algorithmic retention.

**The 10-Scene Arc (Required Structure):**
- **Scene 0 (Thumbnail Rule):** `image` (1 clean still of an attractive woman from the time period, no text/captions) - Placed at the very front of the video to control the thumbnail.
- **Scene 1:** `video` (1 Hero Video) - A beautiful woman from the time period, holding and looking at a relevant item or piece of clothing to act as the hook.
- **Scenes 2-4:** `image` (3 Stills with Steady Slow Zoom) - Used for the Hook & Setup.
- **Scene 5:** `video` (1 Hero Video) - The historical punchline or main bizarre action.
- **Scenes 6-9:** `image` (4 Stills with Steady Slow Zoom) - Explanation & Call to Action.

## 2. Prompt Formulation Structure

Every single prompt in the JSON must follow this exact formula:
**`[EXPLICIT CHARACTER DESCRIPTION] + [ACTION FROM RESEARCH] + [REALISM STYLE MODIFIER] + [SAFETY MODIFIER]`**

### Core Safety & Script Rules
- **Voiceover Banned Words:** Do NOT use the words `die`, `dying`, `kill`, `dead`, `death`, or `died` in the `script` parameter. Always use family-friendly euphemisms (e.g., "ended his life", "met their end"). Do NOT use words referencing minors, such as `teenagers`, `teens`, `preteens`, `school kids`, or `school dances`.
- **Violence/Gore:** NEVER prompt for blood. If the history is violent, use strong visual metaphors (e.g., falling rose petals or waving red fabric instead of blood).
- **Motion in Stills (CRITICAL):** Do NOT include descriptions of motion or movement (e.g., "shaking his head", "falling", "running") in `image` prompts. Motion is ONLY allowed in `video` prompts, as Google Flow struggles to render implied motion in stills.

### Character Casting Rules
1. **Extremes:** All characters must either be *Extremely Attractive* (`jaw-droppingly gorgeous`, `supermodel features`) OR *Comically Ugly/Weird* (`bizarre funny facial features`, `exaggerated historical inbreeding`, `Willem Dafoe vibes`). Avoid "average" people.
2. **Female Characters:** All female characters in image prompts MUST be explicitly described as gorgeous and shapely.
3. **Consistency:** Do not rely on AI to remember characters. You MUST precisely define their physical description, clothing, and features in *every single prompt* in the JSON sequence.

### Aesthetic Rules
- **Color:** Explicitly prompt for `vibrant colors`, `hyper-saturated`, `cinematic lighting`. Never default to dusty, brown, or sepia tones.
- **Settings:** Render settings as vibrant living worlds. Force `pristine condition`, `brand new construction`, `gleaming`. NEVER prompt `ancient`, `ruins`, `weathered`, or `dusty`.
- **Hyper-Realism Base:** Every prompt must end with: `8k resolution, cinematic lighting, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.`

## Example JSON Structure
```json
{
    "title": "Title of the Video",
    "script": "The full spoken script goes here...",
    "tts_voice_id": "a0e99841-438c-4a64-b6a9-ae8f1d56cc33",
    "scenes": [
        {
            "id": "scene_0",
            "type": "image",
            "prompt": "Hyper-realistic portrait photography of a jaw-droppingly gorgeous 25-year-old medieval peasant woman with beautiful features, wearing a pristine historical dress. Looking directly at the camera. 8k resolution, cinematic lighting, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.",
            "duration": 2.0
        },
        {
            "id": "scene_1",
            "type": "video",
            "prompt": "A jaw-droppingly gorgeous 25-year-old medieval peasant woman with beautiful features, wearing a pristine historical dress, holding and admiring a rustic wooden spoon. She turns her head slightly to look at the camera. 8k resolution, cinematic lighting, dramatic shadows, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.",
            "duration": 4.0
        },
        ...
    ]
}
```
