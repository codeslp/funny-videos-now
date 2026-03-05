---
title: how_to_build_episode_intro
description: How to build the episode-level intro video with rapid-fire slideshow, serene VO, and serene music for Future History.
---

# Building the Future History Episode Intro

This skill covers building the **episode-level intro** — a rapid-fire slideshow of images with serene music and a hopeful voiceover, followed by the pre-built "Sooner than you think" clip.

> [!IMPORTANT]
> This is different from `build_intro.py` which builds the "Sooner than you think" **clip-level intro**. This skill builds the **episode-level intro** that plays before that clip.

---

## What You're Building

```
Episode Intro (~15-20s total)
├── Rapid-fire slideshow of 12-15 images (0.5-1s each)
│   └── Images from past episodes + current episode scenes
├── Serene music underneath (soaring strings + gentle electronic pulse)
├── Serene VO: "You can stay sane in an insane time..."
└── Then cut to → pre-built future_history_intro.mp4 ("Sooner than you think")
```

---

## Step 1: Generate the Serene Episode Music

Generate a single shared music asset via ElevenLabs. This track is reused for the episode outro too.

### Music Prompt

```
Serene soaring orchestral strings with a gentle pulsing electronic beat underneath. 
Hopeful and warm, slightly otherworldly. Slow tempo, 70 BPM. 
Ambient pads, soft reverb, cinematic warmth. No vocals. 
Think: sunrise over a quiet future city.
```

### Output Path

```
output/future_history/music_assets/serene_episode_music.mp3
```

### How to Generate

Use `generate_music.py`'s ElevenLabs integration or call the API directly:

```python
from pipeline.generate_music import generate_music_clip
generate_music_clip(
    prompt="Serene soaring orchestral strings with gentle pulsing electronic beat, hopeful warm slightly otherworldly, slow tempo 70 BPM, ambient pads, soft reverb, cinematic warmth, no vocals",
    output_path="output/future_history/music_assets/serene_episode_music.mp3"
)
```

---

## Step 2: Gather Slideshow Images

Collect 12-15 still images for the rapid-fire slideshow:

- **From current episode's 3 vignettes:** Pick 2-3 of the most striking stills from each vignette's build directory (e.g., `scene_2_still.jpg`, `scene_7_still.jpg`)
- **From past episodes:** If past vignette build dirs exist, grab 3-4 memorable stills

### Selection Criteria

Pick images that are:
- Visually striking and colorful
- Self-explanatory without context (no text-heavy images)
- Varied in subject matter (don't pick 3 similar-looking images in a row)

Copy selected images to a working directory:
```
output/future_history/episodes/episode_NNN/slideshow_images/
```

---

## Step 3: Write the Episode-Specific VO Text

The voiceover must follow this exact template:

> "You can stay sane in an insane time. I will show you [number] strategies to [positive futuristic outcome]. Because a new world is coming."

### Rules
- `[number]` = always "three" (since there are 3 vignettes)
- `[positive futuristic outcome]` = something hopeful that contrasts with the episode's dark humor
- Always end with **"Because a new world is coming."**
- The tone is warm, fatherly, slightly mystical — NOT the narration voice

### Voice

Use a **serene male voice** distinct from the narration voice and the deep intro voice. Consider ElevenLabs voice IDs that sound warm and calm. If no ideal voice is available, the deep voice (`qNkzaJoHLLdpvgh5tISm`) at a slower, gentler pace works as fallback.

### Generate TTS

```python
from pipeline.generate_audio import generate_tts
generate_tts(
    text="You can stay sane in an insane time. I will show you three strategies to find stillness when everything is noise. Because a new world is coming.",
    output_filepath="output/future_history/episodes/episode_NNN/episode_intro_voice.wav",
    voice_id="qNkzaJoHLLdpvgh5tISm"  # or serene voice ID
)
```

---

## Step 4: Assemble the Episode Intro with FFmpeg

### 4a. Build the Slideshow Segment

Each image shows for **0.8 seconds** (adjust to fit VO length). Use FFmpeg concat demuxer:

```bash
# Create a concat list file
for img in slideshow_images/*.jpg; do
  echo "file '$img'"
  echo "duration 0.8"
done > slideshow_list.txt

ffmpeg -y -f concat -safe 0 -i slideshow_list.txt \
  -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1/1,format=yuv420p" \
  -c:v libx264 -preset fast -crf 23 -r 30 \
  _slideshow_raw.mp4
```

### 4b. Mix Slideshow + Serene Music + VO

```bash
ffmpeg -y \
  -i _slideshow_raw.mp4 \
  -i episode_intro_voice.wav \
  -i serene_episode_music.mp3 \
  -filter_complex "
    [2:a]volume=0.4,afade=t=out:st=<VO_DURATION-1>:d=1[music];
    [1:a][music]amix=inputs=2:duration=first[aout]
  " \
  -map 0:v -map "[aout]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -t <VO_DURATION> \
  episode_intro.mp4
```

Key: The slideshow duration should match the VO duration. If the VO is ~10s, use ~12 images at 0.8s each.

### 4c. Append the Pre-Built Intro Clip

Concatenate `episode_intro.mp4` + `future_history_intro.mp4` using filter_complex concat (to handle any resolution differences):

```bash
ffmpeg -y \
  -i episode_intro.mp4 \
  -i output/future_history/intro_outro/future_history_intro.mp4 \
  -filter_complex "
    [0:v]scale=1920:1080,setsar=1/1,format=yuv420p[v0];
    [1:v]scale=1920:1080,setsar=1/1,format=yuv420p[v1];
    [0:a]aresample=44100[a0];
    [1:a]aresample=44100[a1];
    [v0][a0][v1][a1]concat=n=2:v=1:a=1[vout][aout]
  " \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  full_episode_intro.mp4
```

---

## Output

```
output/future_history/episodes/episode_NNN/full_episode_intro.mp4
```

Expected duration: **~18-25 seconds** (serene slideshow VO + 8s pre-built intro)

---

## Validation

- [ ] Slideshow shows 12-15 varied, striking images at rapid-fire pace
- [ ] Serene music is warm and hopeful (not the oppressive beat)  
- [ ] VO ends with "Because a new world is coming."
- [ ] Pre-built intro ("Sooner than you think") plays immediately after
- [ ] No audio gap or pop between episode intro and pre-built intro
- [ ] Total duration ~18-25 seconds
