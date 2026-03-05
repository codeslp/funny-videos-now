---
title: how_to_assemble_future_history_episode
description: How to assemble a full Future History episode from 3 pre-rendered vignettes, with episode intro, interstitial cards, sound design, and outro.
---

# Assembling a Future History Episode

This skill covers the **episode-level** assembly — combining 3 pre-rendered vignette clips into a single ~8-10 minute YouTube video with custom intro, interstitial cards, and outro. This is the final production step that runs AFTER individual vignettes have been built using the standard pipeline.

> [!IMPORTANT]
> Each vignette must already be rendered as `final_render.mp4` in its own build directory before episode assembly begins. Use the `stitch_final_render_future_history` skill to build individual vignettes first.

---

## Episode Structure Overview

```
┌──────────────────────────────────────────────────────┐
│  EPISODE INTRO (~15-20s)                             │
│  • Rapid-fire slideshow of past/current episode      │
│  • Serene string + electronic beat music             │
│  • Serene VO: encouragement message → "...coming.    │
│    Sooner than you think." → pre-built intro clip    │
├──────────────────────────────────────────────────────┤
│  INTERSTITIAL CARD 1 (~5s)                           │
│  • Bass thump SFX on appear                          │
│  • Oppressive beat plays behind                      │
│  • Black/white text card with absurd quote from      │
│    upcoming clip                                     │
│  • Second thump at end → card disappears             │
├──────────────────────────────────────────────────────┤
│  VIGNETTE 1 (2-3 min) — most believable entry        │
├──────────────────────────────────────────────────────┤
│  INTERSTITIAL CARD 2 (~5s) — same format             │
├──────────────────────────────────────────────────────┤
│  VIGNETTE 2 (2-3 min) — weirder entry                │
├──────────────────────────────────────────────────────┤
│  INTERSTITIAL CARD 3 (~5s) — same format             │
├──────────────────────────────────────────────────────┤
│  VIGNETTE 3 (2-3 min) — most absurd entry            │
└──────────────────────────────────────────────────────┘
```

---

## Step 1: Select and Order 3 Vignettes

Follow the escalation rule from the `applied_storytelling_future_history` skill (Stage 3.1):

1. **Vignette 1** — Most "believable" entry. Grounds the viewer.
2. **Vignette 2** — Weirder. Higher stakes or bigger societal implications.
3. **Vignette 3** — Most absurd. The one people share.

**Rule:** The episode must feel like it's accelerating. Never put the best entry first.

### Inputs Required

For each vignette, you need:
- The rendered `final_render.mp4` from its build directory
- The timeline JSON (for extracting the `cold_open_candidate` and caption summary)

---

## Step 2: Build Interstitial Cards

Each interstitial card sits between segments and creates a "wait, what?" moment.

### Card Content Rules

The card text should be the **weirdest specific detail** from the upcoming vignette, not its topic title:

- ❌ `"The AI Confession Booth"`
- ✅ `"2.3 million confessions. Searchable. Categorised by sin type."`

Source the quote from either:
- The `cold_open_candidate` in the vignette's storytelling block
- The `caption_summary` from the mashups doc
- A hand-picked absurd line from the script

### Card Design Spec

| Property | Value |
|:---|:---|
| Background | Solid black |
| Text color | White |
| Font | Bold, clean sans-serif (e.g., Inter Bold or Outfit Bold) |
| Text size | Large, centered, max 2 lines |
| Duration | 5 seconds |
| Fade | None — hard cut in and out on the bass thump |

### Card Audio

| Element | Detail |
|:---|:---|
| **Thump SFX** | Single bass thump with electronic flavor — plays at card appear AND at card disappear |
| **Background** | Oppressive beat music asset (`output/future_history/music_assets/oppressive_beat.mp3`) plays quietly behind the card |

---

## Step 3: Build the Episode Intro

The episode intro is a pre-episode hook that primes the viewer emotionally.

### Intro Components

1. **Rapid-fire slideshow** — Quick cuts (0.5-1s each) of still images from past episodes and the current episode's scenes. Use 10-15 images total.

2. **Serene music** — Serene soaring string music with a gentle pulsing electronic beat. This is a distinct asset from the oppressive beat — it should feel hopeful, warm, and slightly otherworldly.

3. **Voiceover (serene voice)** — Words of encouragement for a person struggling in the year 2076. The VO must follow this structure:

   > "You can stay sane in an insane time. I will show you [number] strategies to [positive futuristic outcome]. Because a new world is coming."

   - Always end with **"Because a new world is coming"**
   - This leads directly into the pre-built intro clip which starts with **"SOONER THAN YOU THINK"**

4. **Pre-built intro clip** — Append the existing `output/future_history/intro_outro/future_history_intro.mp4` immediately after the episode intro VO.

### Intro Examples (VO text)

- "You can stay sane in an insane time. I will show you three strategies to find stillness when everything is noise. Because a new world is coming."
- "You can stay sane in an insane time. I will show you five ways to keep your humanity when the machines forget theirs. Because a new world is coming."
- "You can stay sane in an insane time. I will show you four paths to joy when joy feels illegal. Because a new world is coming."

> [!TIP]
> The serene voice should be warm, calm, and slightly otherworldly. Use a different ElevenLabs voice than either the narration voice or the deep intro voice. Consider a gentle, soothing tone.

### Assembly Order

```
1. Episode Intro (slideshow + serene VO + serene music)
2. Pre-built intro clip (future_history_intro_sting.mp4)
3. Interstitial Card 1 (thump + oppressive beat + absurd quote)
4. Vignette 1 final_render.mp4 (NOTE: skip the vignette's own intro)
5. Interstitial Card 2
6. Vignette 2 final_render.mp4 (skip own intro)
7. Interstitial Card 3
8. Vignette 3 final_render.mp4 (skip own intro)
```

> [!WARNING]
> Each vignette's `final_render.mp4` currently has the pre-built intro prepended. When assembling into an episode, you must **strip the first 8 seconds** (the vignette-level intro) from each clip, since the episode has its own intro. Alternatively, re-render vignettes without intro for episode use.

### Technical Notes

- All segments must be re-encoded to matching resolution (1920×1080) during concatenation
- Use `filter_complex` concat (not demuxer concat) to handle any resolution mismatches
- Audio should crossfade smoothly between segments (0.5s fade at boundaries)
- Target total runtime: **8-10 minutes**

---

## Step 6: Validation Checklist

Before publishing, verify:

- [ ] Episode intro has serene VO ending with "Because a new world is coming"
- [ ] Pre-built intro ("Sooner than you think") plays immediately after episode intro
- [ ] Each interstitial card has bass thump SFX + oppressive beat + absurd quote
- [ ] Vignettes are ordered by escalating absurdity (believable → weird → absurd)
- [ ] Vignette-level intros are stripped (no double intro)
- [ ] Total runtime is 8-10 minutes
- [ ] Audio levels are consistent across all segments
- [ ] No abrupt audio cuts at segment boundaries

---

## Audio Asset Summary

| Asset | Location | Usage |
|:---|:---|:---|
| Oppressive beat | `output/future_history/music_assets/oppressive_beat.mp3` | Interstitial cards background |
| Serene episode music | *To be generated* | Episode intro |
| Bass thump SFX | *To be generated* | Interstitial card appear/disappear |
| Pre-built intro clip | `output/future_history/intro_outro/future_history_intro_sting.mp4` | After episode intro |
| Serene VO (intro) | *Generated per episode* | Episode-specific encouragement |

---

## File Structure

```
output/future_history/
├── music_assets/
│   ├── oppressive_beat.mp3          # Interstitial card music
│   ├── serene_episode_music.mp3     # Episode intro/outro music (TO CREATE)
│   └── bass_thump_sfx.mp3          # Interstitial thump SFX (TO CREATE)
├── intro_outro/
│   └── future_history_intro_sting.mp4     # Pre-built "Sooner than you think" clip
├── episodes/
│   └── episode_001/                 # Full assembled episode
│       ├── episode_intro.mp4
│       ├── interstitial_1.mp4
│       ├── interstitial_2.mp4
│       ├── interstitial_3.mp4
│       └── full_episode.mp4         # Final concatenated episode
└── in_progress/
    ├── en_organ_loyalty_2026-03-02/  # Vignette build dirs
    └── en_ai_confession_booth_2026-03-03/
```
