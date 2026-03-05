---
title: bash_commands_and_troubleshooting
description: Reference for running bash/FFmpeg commands in this project, including known pitfalls and fixes for zsh, paths with spaces, and FFmpeg quirks.
---

# Bash Commands & Troubleshooting

This skill documents common bash/FFmpeg patterns used in this project, plus known issues and their solutions.

---

## Known Issue: zsh Glob Patterns Fail on Paths with Spaces

**Problem:** When running glob patterns like `*.jpg` or `*still*.jpg` on paths that contain spaces (e.g., `Claude Code Markdown/funny_video_generator/...`), zsh throws `no matches found` errors even when the files exist.

**Why:** zsh treats unquoted glob patterns differently from bash. When a path contains spaces and is combined with a glob, zsh can't resolve it.

**Bad (fails in zsh):**
```bash
ls /Users/user/Claude Code Markdown/output/*.jpg
# → (eval):1: no matches found
```

**Fix — use a variable + quoted expansion:**
```bash
DIR="/Users/user/Claude Code Markdown/output"
ls "$DIR"/*.jpg
```

**Fix — use `find` instead of globs:**
```bash
find "/Users/user/Claude Code Markdown/output" -name "*.jpg" -maxdepth 1
```

**Fix — use a `for` loop with `ls` and `sort`:**
```bash
for img in $(ls -1 "$DIR"/*.jpg | sort); do
  echo "$img"
done
```

---

## Known Issue: `cp` Hangs on Large Files or Many Files

**Problem:** When copying many large image files (e.g., 12 JPGs at ~1MB each), a single `cp` command can appear to hang, especially if the destination is on the same volume and Finder is indexing.

**Fix:** Copy files one at a time in a script, or use `rsync`:
```bash
rsync -av --progress "$SRC/" "$DEST/"
```

Or copy individually with explicit paths:
```bash
cp "$BASE/scene_0_still.jpg" "$DEST/01_scene0.jpg"
cp "$BASE/scene_2_still.jpg" "$DEST/02_scene2.jpg"
# ... etc
```

---

## FFmpeg Concat Demuxer for Image Slideshows

When building a slideshow from still images using FFmpeg's concat demuxer:

### 1. Create the concat list file

```bash
SLIDE_DIR="/path/to/slideshow_images"
for img in $(ls -1 "$SLIDE_DIR"/*.jpg | sort); do
  echo "file '$img'"
  echo "duration 0.85"
done > slideshow_list.txt

# IMPORTANT: Add the last image again without duration (FFmpeg requirement)
LAST_IMG=$(ls -1 "$SLIDE_DIR"/*.jpg | sort | tail -1)
echo "file '$LAST_IMG'" >> slideshow_list.txt
```

### 2. Build the slideshow video

```bash
ffmpeg -y -f concat -safe 0 -i slideshow_list.txt \
  -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1/1,format=yuv420p" \
  -c:v libx264 -preset fast -crf 23 -r 30 \
  _slideshow_raw.mp4
```

**Key notes:**
- Use `-safe 0` to allow absolute paths in the concat list
- Use `force_original_aspect_ratio=increase,crop=1920:1080` to handle images with different aspect ratios (some scenes are 16:9, some are square)
- Always add the last file entry without a `duration` line — FFmpeg concat demuxer requires this or the last image will be missing/truncated
- `setsar=1/1` prevents aspect ratio issues in the output

---

## FFmpeg: Mixing Video + Music + Voiceover

Standard pattern for combining a video with background music and a voiceover track:

```bash
VO_DURATION=10.17  # Get from: ffprobe -v quiet -show_entries format=duration -of csv=p=0 voice.wav
FADE_START=$(echo "$VO_DURATION - 1" | bc)

ffmpeg -y \
  -i video.mp4 \
  -i voiceover.wav \
  -i background_music.wav \
  -filter_complex "
    [2:a]volume=0.35,afade=t=out:st=${FADE_START}:d=1[music];
    [1:a][music]amix=inputs=2:duration=first[aout]
  " \
  -map 0:v -map "[aout]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -t $VO_DURATION \
  output.mp4
```

**Key notes:**
- `volume=0.35` keeps music underneath the VO (adjust to taste)
- `afade=t=out` fades music out 1 second before the VO ends
- `amix=inputs=2:duration=first` trims to the VO length
- `-t $VO_DURATION` hard-caps the output duration

---

## FFmpeg: Concatenating Two Videos with Different Properties

When concatenating two videos that may have different resolutions, frame rates, or audio sample rates:

```bash
ffmpeg -y \
  -i segment_1.mp4 \
  -i segment_2.mp4 \
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
  output.mp4
```

**Key notes:**
- Always normalize resolution (`scale=1920:1080`) and pixel format (`format=yuv420p`) for both inputs
- Always `aresample=44100` both audio streams to match sample rates
- Use `filter_complex` concat, NOT the concat protocol or demuxer, when inputs may differ

---

## Getting Media Duration

```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 file.mp4
```

Returns duration in seconds as a decimal (e.g., `10.170340`).

---

## Project Path Convention

All commands in this project use absolute paths because the base directory contains spaces:

```
/Users/bfaris96/Claude Code Markdown/funny_video_generator/
```

**Always quote paths.** Store the base in a variable at the top of any script:

```bash
PROJECT="/Users/bfaris96/Claude Code Markdown/funny_video_generator"
OUTPUT="$PROJECT/output/future_history"
```
