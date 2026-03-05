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
- **Spelling out Numbers and Dates (CRITICAL):** All dates and numbers must be spelled out in the `script` with words, not numbers (e.g., "twenty fifty" instead of "2050", "three million" instead of "3,000,000"). The TTS voice will mispronounce numerical digits.

## 5. Near-Future Visual Style (DIFFERS FROM WEIRD HISTORY)

> [!IMPORTANT]
> **Before writing ANY scene prompts**, you MUST read the full visual style guide at:
> `weird_history/production_guidelines/future_history_visual_style_guide.md`
> This guide defines the "Lived-In Future" aesthetic, prompt keyword system, setting-specific guidelines, and the contrast principle. All prompts must follow it.
>
> **Before writing ANY narration script or structuring entries**, you MUST read the applied storytelling skill at:
> `weird_history/.agent/skills/applied_storytelling_future_history/SKILL.md`
> This skill defines mandatory storytelling rules at three stages: script writing, entry structuring, and compilation assembly. It references the full guide at `weird_history/production_guidelines/future_history_storytelling_guide.md`.

Instead of historical hyper-realism, Future History renders **near-future** scenes in **landscape 16:9 (1920x1080)**:
- **Aspect ratio: Landscape 16:9** — Future History is long-form YouTube, not Shorts
- **Aesthetic: "Lived-In Future"** — futuristic but worn, well-used, slightly dingy around the edges. NOT pristine, NOT sterile, NOT generic sci-fi.
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
- Use **specific numbers, names, dates, and places** — specificity = believability (remember to spell them out!)
- End with an **ironic observation** — the "Why It's Absurd" thesis delivered conversationally

### Pacing and Stills
- **More Stills:** We need more stills in the JSON timelines to keep the viewer visually engaged.
- **Match Timing:** The pacing of the images should better match the voiceover script. Align the transitions and descriptions of the images precisely so that what the VO is describing closely matches the image on screen in real-time.

## 8. Storytelling Metadata (MANDATORY)

Every entry JSON **must** include a `storytelling` block after the `resolution` field. This is not optional — it forces the writer to think structurally about retention.

```json
"storytelling": {
    "cold_open_candidate": "Single most absurd sentence — under 20 words",
    "open_loops": [
        {"opens_at": "scene_X", "text": "what the viewer is now waiting to find out", "closes_at": "scene_Y"}
    ],
    "punchline_scene": "scene_8",
    "specificity_check": ["17 people", "299 dollars", "90-day"],
    "pattern_interrupts": [
        {"scene": "scene_1", "type": "video", "note": "why this breaks the rhythm"}
    ],
    "but_therefore_transitions": [
        "Description of transition using BUT or THEREFORE (label which)"
    ]
}
```

### Rules:
- **`open_loops`**: Minimum 2 per entry. At least 1 must span from scene 0-2 to scene 6+.
- **`cold_open_candidate`**: Must be a single punchy sentence, under 20 words.
- **`punchline_scene`**: Must reference a `video` type scene (never a still).
- **`specificity_check`**: Minimum 3 specific numbers, dates, or amounts. No vague claims.
- **`pattern_interrupts`**: Must have at least 3, spaced so no more than 3 stills appear in a row.
- **`but_therefore_transitions`**: Minimum 2. If you catch yourself writing "and then," rewrite it.

## 9. Compilation Assembly

When assembling multiple entries into a compilation video, create a `compilation_*.json` wrapper:

```json
{
    "compilation_title": "Future History Vol. X",
    "cold_open": {
        "line": "Best cold_open_candidate from any entry",
        "source_entry": 0,
        "source_scene_id": "scene_8"
    },
    "entries": [
        {
            "file": "entry_timeline_en.json",
            "absurdity_rank": 1,
            "transition_hook": "Teases the WEIRDEST detail of the next entry — not its topic"
        }
    ],
    "outro_tease": "Teases future content — never summarizes",
    "escalation_verified": true
}
```

### Rules:
- **Escalation:** `absurdity_rank` 1 = most grounded (first), highest = most absurd (last).
- **Transition hooks:** Must describe the *weirdest specific detail*, not the general topic.
- **Cold open:** Uses the single best `cold_open_candidate` from any entry. The line should make a viewer think "wait, what?"
- **Outro tease:** NEVER summarizes. Always opens a loop for future content.

