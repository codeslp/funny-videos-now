---
title: how_to_build_interstitial_cards
description: How to build the interstitial card videos that play between vignettes in a Future History episode, with bass thump SFX and oppressive beat.
---

# Building Future History Interstitial Cards

This skill covers building the **interstitial card clips** — short 6-second black cards with white text and punchy sound design that play between vignettes in a Future History episode.

---

## What You're Building

```
Interstitial Card (~6s)
├── Frame 0.0s: Bass thump SFX → black card appears with white text
├── Frame 6.0s: Second bass thump SFX → card disappears (hard cut)
└── Text: the most absurd short quote from the upcoming vignette - not just the name
```

Each episode needs **3 interstitial cards** — one before each vignette.

---

## Step 1: Generate the Bass Thump SFX

Generate a single bass thump sound effect via ElevenLabs Sound Generation.

### SFX Prompt

```
Single deep bass thump hit with electronic reverb tail, punchy low-end impact, 
cinematic sound design, dark electronic flavor, short 1 second duration
```

### Output Path

```
output/future_history/music_assets/bass_thump_sfx.mp3
```

### How to Generate

```python
from pipeline.generate_music import generate_music_clip
generate_music_clip(
    prompt="Single deep bass thump hit with electronic reverb tail, punchy low-end impact, cinematic sound design, dark electronic flavor, short duration",
    output_path="output/future_history/music_assets/bass_thump_sfx.mp3"
)
```

> [!NOTE]
> This asset is generated once and reused for all interstitial cards across all episodes.

---

## Step 2: Write the Card Text

Each card teases the **upcoming** vignette with its weirdest specific detail.

### Text Selection Rules

- ✅ Use the most absurd short quote from the upcoming vignette as the card text (often the `cold_open_candidate`)
- ❌ Never just use the topic name (e.g., "The Organ Loyalty Programs")
- ❌ Never exceed 2 lines of text

### Examples

| Vignette | ❌ Bad Card Text | ✅ Good Card Text |
|:---|:---|:---|
| Organ Loyalty | "The Organ Loyalty Programs" | "One man mailed his kidney back." |
| AI Confession | "The AI Confession Booth" | "2.3 million confessions. Searchable. Categorised by sin type." |

---

## Step 3: Build Each Interstitial Card with FFmpeg

### 3a. Create the Text Image

Use FFmpeg's `drawtext` filter to render white text on a black background:

```bash
ffmpeg -y \
  -f lavfi -i "color=c=black:s=1920x1080:d=5:r=30" \
  -vf "drawtext=text='<CARD_TEXT>':fontfile=/System/Library/Fonts/Helvetica.ttc:fontsize=64:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20" \
  -c:v libx264 -preset fast -crf 23 \
  _card_visual.mp4
```

For multi-line text, use `\n` (escaped as `\\n` in shell) to break lines:

```bash
drawtext=text='2.3 million confessions.\\nSearchable. Categorised by sin type.'
```

### Text Styling

| Property | Value |
|:---|:---|
| Background | Solid black |
| Text color | White |
| Font | Bold, clean sans-serif (e.g., Inter Bold or Outfit Bold) |
| Text size | Large, centered, max 2 lines |
| Duration | 6 seconds |
| Fade | None — hard cut in and out on the bass thump |

### Card Audio

| Element | Detail |
|:---|:---|
| **Thump SFX** | Single bass thump with electronic flavor — plays at card appear AND at card disappear |

### 3b. Mix Audio Layers

The audio has 2 layers:
1. **Thump at 0.0s** — bass thump SFX at start
2. **Thump at ~5.5s** — second thump near the end

```bash
ffmpeg -y \
  -i _card_visual.mp4 \
  -i output/future_history/music_assets/bass_thump_sfx.mp3 \
  -filter_complex "
    [1:a]volume=1.0,adelay=0|0[thump1];
    [1:a]volume=1.0,adelay=5500|5500[thump2];
    [thump1][thump2]amix=inputs=2:duration=longest:dropout_transition=0[aout]
  " \
  -map 0:v -map "[aout]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -t 6 \
  interstitial_N.mp4
```

---

## Step 4: Build All 3 Cards

For an episode with 3 vignettes, build:

| Card | Teases | Text Source |
|:---|:---|:---|
| `interstitial_1.mp4` | Vignette 1 | `cold_open_candidate` or script line from vignette 1 |
| `interstitial_2.mp4` | Vignette 2 | `cold_open_candidate` or script line from vignette 2 |
| `interstitial_3.mp4` | Vignette 3 | `cold_open_candidate` or script line from vignette 3 |

---

## Output

```
output/future_history/episodes/episode_NNN/
├── interstitial_1.mp4  (6s)
├── interstitial_2.mp4  (6s)
└── interstitial_3.mp4  (6s)
```

---

## Validation

- [ ] Each card is exactly 6 seconds
- [ ] Text is white on black, centered, readable at a glance
- [ ] Bass thump plays at start and at ~5.5 seconds
- [ ] Text teases the upcoming vignette's weirdest detail, not its topic name
- [ ] No text wrapping issues (test at 1920x1080)
- [ ] Hard cut in and out (no fades)
