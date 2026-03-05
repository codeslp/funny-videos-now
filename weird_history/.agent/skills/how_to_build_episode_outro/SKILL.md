---
title: how_to_build_episode_outro
description: How to build the Future History episode outro with the green field video, serene VO, and serene music.
---

# Building the Future History Episode Outro

This skill covers building the **episode outro** — a beautiful, contemplative closing sequence with a green field, distant figure, serene music, and a fixed voiceover.

> [!NOTE]
> The outro is a **reusable asset** — the same outro video and VO are used for every episode. Only build it once, then prepend/append as needed during episode assembly.

---

## What You're Building

```
Episode Outro (~15-20s)
├── Video: Beautiful green field with wildflowers, blue sky, cumulus clouds
│   └── In the last few seconds: a distant figure (brown-skinned man with
│       long hair, beard, white t-shirt, jeans) walks up a far hill toward camera
├── Serene music: Same track used in episode intro
└── VO (serene voice): "This world, with you in it, was made beautiful.
    There will be justice. All will be made right. Sooner than you think."
```

---

## Step 1: Generate the Outro Video

Generate the landscape video via **Google Video FX** (browser subagent).

### Video Prompt

```
A beautiful expansive green field filled with wildflowers stretching to the horizon under a big blue sky with fluffy white cumulus clouds slowly drifting. Rolling green hills in the background. Warm golden sunlight. In the last few seconds, a small solitary figure becomes visible far off on a distant green hill, slowly walking up the far side toward the camera. The figure is barely visible, very far away. He is a man with brown skin, long dark hair, and a beard, wearing a simple white t-shirt and blue jeans. The camera stays wide and still. The mood is peaceful, hopeful, and sacred. Cinematic wide landscape composition. 8k resolution, photorealistic, documentary style, shot on 35mm lens. No painting.
```

### Settings
- **Aspect ratio:** 16:9 Landscape
- **Duration:** As long as possible (8 seconds on Video FX)
- **Model:** Veo 3.1 Quality

### Output Path

```
output/future_history/intro_outro/outro_field_video.mp4
```

> [!TIP]
> Since the VO is ~12-15 seconds, you may need to slow the video down or loop part of it. Use FFmpeg's `setpts` filter to slow to 0.5x speed (doubling duration to ~16s), which also enhances the contemplative mood.

### Slowing the video (if needed)

```bash
ffmpeg -y -i outro_field_video_raw.mp4 \
  -vf "setpts=2.0*PTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1/1,format=yuv420p" \
  -af "atempo=0.5" \
  -r 30 -c:v libx264 -preset fast -crf 23 \
  outro_field_video.mp4
```

---

## Step 2: Generate the Outro Voiceover

### Fixed Text (never changes)

> "This world, with you in it, was made beautiful. There will be justice. All will be made right. Sooner than you think."

### Voice

Use the same **serene voice** as the episode intro. This should be warm, calm, fatherly, slightly mystical. The deep voice (`qNkzaJoHLLdpvgh5tISm`) works well here at a measured pace.

### Generate TTS

```python
from pipeline.generate_audio import generate_tts
generate_tts(
    text="This world, with you in it, was made beautiful. There will be justice. All will be made right. Sooner than you think.",
    output_filepath="output/future_history/intro_outro/outro_voice.wav",
    voice_id="qNkzaJoHLLdpvgh5tISm"
)
```

### Output Path

```
output/future_history/intro_outro/outro_voice.wav
```

---

## Step 3: Assemble the Outro with FFmpeg

Mix the video + serene music + voiceover. The music fades in gently and plays under the VO.

```bash
ffmpeg -y \
  -i outro_field_video.mp4 \
  -i output/future_history/intro_outro/outro_voice.wav \
  -i output/future_history/music_assets/serene_episode_music.mp3 \
  -filter_complex "
    [0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1/1,format=yuv420p[vout];
    [2:a]afade=t=in:d=2,afade=t=out:st=<VO_DURATION-2>:d=2,volume=0.35[music];
    [1:a][music]amix=inputs=2:duration=first[aout]
  " \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -t <VO_DURATION> \
  output/future_history/intro_outro/episode_outro.mp4
```

Replace `<VO_DURATION>` with the actual duration of `outro_voice.wav` (typically ~10-12s).

### Audio Mixing Notes

| Layer | Volume | Behavior |
|:---|:---|:---|
| Voiceover | 1.0 (full) | Plays from start |
| Serene music | 0.35 | Fades in over 2s, fades out at end over 2s |
| Video audio | Muted | Not used (generated video has no meaningful audio) |

---

## Output

```
output/future_history/intro_outro/episode_outro.mp4
```

Expected duration: **~10-15 seconds** (matches VO length)

---

## Reusability

This outro is built **once** and reused across all episodes:

- `outro_field_video.mp4` — the video asset (reusable forever)
- `outro_voice.wav` — the fixed VO (reusable forever)  
- `serene_episode_music.mp3` — shared with episode intro (reusable forever)
- `episode_outro.mp4` — the final assembled outro (reusable forever)

Only rebuild if you want to change the VO text, voice, music, or video.

---

## Validation

- [ ] Video shows a beautiful green field with wildflowers and blue sky
- [ ] Distant figure is visible on far hill in the last few seconds
- [ ] Serene music fades in gently and plays under VO
- [ ] VO says exactly: "This world, with you in it, was made beautiful. There will be justice. All will be made right. Sooner than you think."
- [ ] VO tone is warm, calm, fatherly — NOT the narration voice tone
- [ ] Duration matches VO length (no trailing silence or abrupt cutoff)
- [ ] Video resolution is 1920×1080 for clean concatenation
