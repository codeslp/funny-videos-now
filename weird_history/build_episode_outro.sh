#!/bin/bash
set -e

# ─────────────────────────────────────────────────────────
# Future History — Episode Outro Builder
# ─────────────────────────────────────────────────────────
# Prerequisites:
#   1. Green field video must already exist at:
#      $OUTRO_DIR/outro_field_video_raw.mp4
#      (Generate via Google Video FX — see prompt below)
#   2. Serene music must exist at:
#      $OUTPUT/music_assets/serene_episode_music.mp3
#
# Video FX Prompt (Veo 3.1 Quality, 16:9 Landscape, x1 count, max duration):
#   "A beautiful expansive green field filled with wildflowers stretching
#    to the horizon under a big blue sky with fluffy white cumulus clouds
#    slowly drifting. Rolling green hills in the background. Warm golden
#    sunlight. In the last few seconds, a small solitary figure becomes
#    visible far off on a distant green hill, slowly walking up the far
#    side toward the camera. The figure is barely visible, very far away.
#    He is a man with brown skin, long dark hair, and a beard, wearing a
#    simple white t-shirt and blue jeans. The camera stays wide and still.
#    The mood is peaceful, hopeful, and sacred. Cinematic wide landscape
#    composition. 8k resolution, photorealistic, documentary style, shot
#    on 35mm lens. No painting."
# ─────────────────────────────────────────────────────────

# Absolute paths — required because project path contains spaces
PROJECT="/Users/bfaris96/Claude Code Markdown/funny_video_generator"
OUTPUT="$PROJECT/output/future_history"
OUTRO_DIR="$OUTPUT/episodes/outro"
MUSIC="$OUTPUT/music_assets/serene_episode_music.mp3"
FIELD_RAW="$OUTRO_DIR/outro_field_video_raw.mp4"
FIELD_SLOW="$OUTRO_DIR/outro_field_video.mp4"
OUTRO_VOICE="$OUTRO_DIR/outro_voice.wav"
FINAL_OUTRO="$OUTRO_DIR/episode_outro.mp4"

mkdir -p "$OUTRO_DIR"

# ── Step 1: Generate the Outro Voiceover ──────────────────
echo "=== Step 1: Generating outro voiceover ==="
cd "$PROJECT/weird_history"
python3 -c "
from pipeline.generate_audio import generate_tts
generate_tts(
    text='This world, with you in it, was made beautiful. There will be justice. All will be made right. Sooner than you think.',
    output_filepath='$OUTRO_VOICE',
    voice_id='qNkzaJoHLLdpvgh5tISm'
)
"
echo "Outro VO generated at: $OUTRO_VOICE"

# ── Step 2: Slow down the field video to ~16s ─────────────
echo ""
echo "=== Step 2: Slowing field video to 0.5x ==="

if [ ! -f "$FIELD_RAW" ] && [ ! -f "$FIELD_SLOW" ]; then
    echo "ERROR: No green field video found!"
    echo "  Expected raw at: $FIELD_RAW"
    echo "  Or already slowed at: $FIELD_SLOW"
    echo ""
    echo "Generate via Google Video FX first, save to:"
    echo "  $FIELD_RAW"
    echo "Then re-run this script."
    exit 1
fi

if [ -f "$FIELD_RAW" ] && [ ! -f "$FIELD_SLOW" ]; then
    ffmpeg -y -i "$FIELD_RAW" \
      -vf "setpts=2.0*PTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1/1,format=yuv420p" \
      -af "atempo=0.5" \
      -r 30 -c:v libx264 -preset fast -crf 23 \
      "$FIELD_SLOW"
    echo "Slowed video saved to: $FIELD_SLOW"
elif [ -f "$FIELD_SLOW" ]; then
    echo "Slowed video already exists, skipping."
fi

# ── Step 3: Get durations ─────────────────────────────────
echo ""
echo "=== Step 3: Getting durations ==="
VO_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTRO_VOICE")
VIDEO_DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$FIELD_SLOW")
echo "VO Duration: ${VO_DURATION}s"
echo "Video Duration: ${VIDEO_DURATION}s"

# Calculate fade-out start (VIDEO_DURATION - 3) so music fades near end of video
FADE_START=$(echo "$VIDEO_DURATION - 3" | bc)
echo "Music fade-out starts at: ${FADE_START}s"

# ── Step 4: Assemble the final outro ──────────────────────
echo ""
echo "=== Step 4: Assembling final outro ==="
# VO finishes early, music + video continue to full video length
ffmpeg -y \
  -i "$FIELD_SLOW" \
  -i "$OUTRO_VOICE" \
  -i "$MUSIC" \
  -filter_complex "
    [0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1/1,format=yuv420p[vout];
    [1:a]apad=pad_dur=10[vopad];
    [2:a]afade=t=in:d=2,afade=t=out:st=${FADE_START}:d=3,volume=0.35[music];
    [vopad][music]amix=inputs=2:duration=shortest[aout]
  " \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -shortest \
  "$FINAL_OUTRO"

echo ""
echo "=== Done! ==="
echo "Final outro: $FINAL_OUTRO"
FINAL_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$FINAL_OUTRO")
echo "Duration: ${FINAL_DUR}s"
