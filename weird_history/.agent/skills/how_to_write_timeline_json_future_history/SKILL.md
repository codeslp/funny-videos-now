---
title: how_to_write_timeline_json_future_history
description: How to design the multi-scene timeline JSON for Future History videos using the compilation format and near-future visual style.
---

# Designing the Future History Timeline JSON

Future History uses a longer-form compilation format compared to Weird History's 10-scene short-form structure. Each video contains 3-4 entries at ~11 scenes each, totaling ~45-50 scenes per compilation video.

## 1. Per-Entry Scene Structure (11 Scenes, 3 Hero Videos)

Each entry follows this rhythm:

| Scene | Beat | Type | Purpose |
|:---|:---|:---|:---|
| 0 | Thumbnail/Hook | `image` | Clean establishing shot of the future concept |
| 1 | Hook | `video` | **Hero Video** — motion grabs attention at entry open |
| 2 | Setup | `image` | Establishes the trend/world context |
| 3 | Setup | `image` | Deepens the context — data, comparisons |
| 4 | Escalation | `video` | **Hero Video** — the "wait, WHAT?" moment |
| 5 | Escalation | `image` | The custom/practice at its peak absurdity |
| 6 | Consequence | `image` | Social fallout, reactions, ironic twist |
| 7 | Consequence | `image` | The human moment — dinner party, protest, quiet realization |
| 8 | Punchline | `video` | **Hero Video** — the visual punchline |
| 9 | Coda | `image` | The aftermath — press release, policy change, final irony |
| 10 | Thesis | `image` | "Why It's Absurd" thesis — the freeze frame that makes you think |

**Per entry: 3 hero videos + 8 stills = 11 scenes**

## 2. Full Compilation Video Structure

For a 4-entry compilation video (~8-10 minutes):

```
COLD OPEN (1 scene — most shocking line + still from the strongest entry)
ENTRY 1 — 11 scenes (~2 min)
TRANSITION CARD — text on gradient (no asset needed)
ENTRY 2 — 11 scenes (~2 min)
TRANSITION CARD
ENTRY 3 — 11 scenes (~2 min)
TRANSITION CARD
ENTRY 4 (BANGER) — 12 scenes (~2.5 min, extra scene for closer)
OUTRO — reusable template (subscribe/comment CTA)
```

**Full video totals: ~13 hero videos + ~33 stills + 3 transition cards + outro = ~50 scenes**

## 3. Voice Configuration

- **Primary TTS:** Cartesia — Voice: **Toby (Genuine Guide)** — `3d5ce2fb-e56c-42f0-9ed9-4662484063b4`
- **Fallback TTS:** Edge-TTS — Voice: **en-GB-ThomasNeural** (deeper British male)
- **Tone:** Dry, factual, occasionally snarky about negative aspects. Like a well-read British friend with opinions who wants to present the facts without exaggeration.

## 4. Core Safety & Script Rules (SAME AS WEIRD HISTORY)

- **Voiceover Banned Words:** Do NOT use `die`, `dying`, `kill`, `dead`, `death`, or `died` in the `script` parameter. Always use family-friendly euphemisms.
- **No Minors:** Do NOT use words referencing minors such as `teenagers`, `teens`, `preteens`, `school kids`, or `school dances`.
- **Violence/Gore:** NEVER prompt for blood. Use visual metaphors if needed.
- **Motion in Stills (CRITICAL):** Do NOT include descriptions of motion or movement in `image` prompts. Motion is ONLY allowed in `video` prompts.

## 5. Near-Future Visual Style (DIFFERS FROM WEIRD HISTORY)

Instead of historical hyper-realism, Future History renders **near-future** scenes in **landscape 16:9 (1920x1080)**:
- **Aspect ratio: Landscape 16:9** — Future History is long-form YouTube, not Shorts
- Settings look like 2040s-2050s: recognizable modern cities with subtle futuristic elements
- NOT full sci-fi — no spaceships, laser guns, or alien worlds (unless the entry specifically requires it)
- Think: clean architecture, holographic UIs, slightly more advanced clothing, recognizable technology evolved 20 years
- **Same core aesthetic rules:** vibrant colors, hyper-saturated, cinematic lighting, 8k resolution, 35mm lens, photorealistic, No painting.

### Character Casting (SAME EXTREMES RULE)
- **Hot Route:** `incredibly handsome`, `jaw-droppingly gorgeous`, `supermodel features`
- **Character Actor Route:** `bizarre funny facial features`, `comically ugly`, `exaggerated features`
- All female characters in image prompts MUST be explicitly described as gorgeous and shapely.
- Repeat full character descriptions in EVERY prompt — AI does not remember across scenes.

### Prompt Formula
**`[EXPLICIT CHARACTER DESCRIPTION] + [NEAR-FUTURE SCENARIO] + [REALISM STYLE MODIFIER] + [SAFETY MODIFIER]`**

Every prompt must end with:
`8k resolution, cinematic lighting, documentary style realism, highly detailed, shot on 35mm lens, photorealistic. No painting.`

## 6. JSON Schema

```json
{
    "title": "Entry Title",
    "script": "Full narration text — dry, factual, British buddy tone...",
    "tts_voice_id": "3d5ce2fb-e56c-42f0-9ed9-4662484063b4",
    "tts_fallback_voice": "en-GB-ThomasNeural",
    "language": "en",
    "entry_number": 13,
    "series": "future_history",
    "scenes": [
        {
            "id": "scene_0",
            "type": "image",
            "prompt": "Hyper-realistic photograph of...",
            "duration": 4.0
        },
        {
            "id": "scene_1",
            "type": "video",
            "prompt": "A hyper-realistic...",
            "duration": 5.0
        }
    ]
}
```

## 7. Script Writing Style

The narration should:
- Be written in **past tense** — looking back from ~2076
- Feel **dry and factual** — like a documentary, not a breathless YouTube narrator
- Include **occasional snark** about truly negative aspects — deadpan observations, not outrage
- Sound like a **well-read buddy with opinions** — informed, wry, never condescending
- **Never exaggerate** — the facts are absurd enough; let them land
- Use **specific numbers, names, dates, and places** — specificity = believability
- End with an **ironic observation** — the "Why It's Absurd" thesis delivered conversationally
