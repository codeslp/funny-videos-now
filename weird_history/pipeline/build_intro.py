#!/usr/bin/env python3
"""
One-off script to build the Future History intro clip.

Takes the raw intro video, overlays:
  - Oppressive beat music (fading out over the last few seconds)
  - Deep voice saying "sooner than you think"

Outputs a finished intro clip to be prepended to all Future History videos.

Usage:
  python build_intro.py
"""
import os
import sys
import subprocess
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_audio import generate_tts
from generate_music import generate_oppressive_beat, MUSIC_ASSETS_DIR

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INTRO_OUTRO_DIR = os.path.join(PROJECT_ROOT, 'output', 'future_history', 'intro_outro')

# The raw intro video the user created
RAW_INTRO_VIDEO = os.path.join(INTRO_OUTRO_DIR,
    'The_words_sooner_than_you_think_keep_those_words_i_bd2357f3b7.mp4')

# Voice
DEEP_VOICE_ID = "qNkzaJoHLLdpvgh5tISm"
INTRO_TEXT = "Sooner than you think."

# Output
FINISHED_INTRO = os.path.join(INTRO_OUTRO_DIR, 'future_history_intro.mp4')


def get_duration(filepath: str) -> float:
    r = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', filepath],
        capture_output=True, text=True
    )
    return float(json.loads(r.stdout)['format']['duration'])


def build():
    os.makedirs(INTRO_OUTRO_DIR, exist_ok=True)
    os.makedirs(MUSIC_ASSETS_DIR, exist_ok=True)

    # 1. Generate intro voice
    intro_voice = os.path.join(INTRO_OUTRO_DIR, 'intro_voice.wav')
    if not os.path.exists(intro_voice):
        print("[1/3] Generating intro voiceover (deep voice)...")
        generate_tts(INTRO_TEXT, intro_voice, DEEP_VOICE_ID)
    else:
        print("[1/3] Intro voice already exists, skipping.")
    print(f"  Voice: {intro_voice}")

    # 2. Generate oppressive beat (shared music asset)
    beat = os.path.join(MUSIC_ASSETS_DIR, 'oppressive_beat.mp3')
    if not os.path.exists(beat):
        print("[2/3] Generating oppressive beat...")
        generate_oppressive_beat(output_filepath=beat)
    else:
        print("[2/3] Oppressive beat already exists, skipping.")
    print(f"  Beat: {beat}")

    # 3. Assemble: raw video + oppressive beat (fading out) + deep voice
    print("[3/3] Assembling intro clip...")

    if not os.path.exists(RAW_INTRO_VIDEO):
        print(f"ERROR: Raw intro video not found at: {RAW_INTRO_VIDEO}")
        sys.exit(1)

    video_dur = get_duration(RAW_INTRO_VIDEO)
    print(f"  Raw intro video: {video_dur:.1f}s")

    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Theme at 50% volume, fading out starting halfway through
    fade_start = max(video_dur * 0.5, 2.0)
    fade_dur = video_dur - fade_start

    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,setsar=1/1,format=yuv420p[vout];"
        f"[2:a]afade=t=out:st={fade_start:.1f}:d={fade_dur:.1f},volume=0.2[beat];"
        f"[1:a]loudnorm=I=-14:LRA=11:TP=-1.5,volume=2.0,adelay=0|0[voice];"
        f"[beat][voice]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0[aout]"
    )

    filter_file = os.path.join(INTRO_OUTRO_DIR, '_intro_filter.txt')
    with open(filter_file, 'w') as f:
        f.write(filter_complex)

    cmd = [
        ffmpeg_exe, "-y",
        "-i", RAW_INTRO_VIDEO,
        "-i", intro_voice,
        "-i", beat,
        "-filter_complex_script", filter_file,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(video_dur),
        FINISHED_INTRO
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        os.remove(filter_file)
        final_dur = get_duration(FINISHED_INTRO)
        print(f"\n  ✅ Intro clip built: {FINISHED_INTRO}")
        print(f"     Duration: {final_dur:.1f}s")
        print(f"     Ready to prepend to all Future History videos.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed (exit {e.returncode}):")
        print(f"STDERR: {e.stderr[-1000:] if e.stderr else 'empty'}")
        sys.exit(1)


if __name__ == "__main__":
    build()
