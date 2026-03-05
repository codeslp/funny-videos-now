#!/usr/bin/env python3
"""
Music generation using ElevenLabs Sound Generation API.
Generates two types of tracks:
  1. Atmospheric underscore for narration segments (looped)
  2. Oppressive beat for opening, interstitials, and outro (single clip)

Music assets are stored in output/future_history/music_assets/
"""
import os
import sys
import json
import requests
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import ROOT_DIR
except ImportError:
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

from dotenv import load_dotenv
env_path = os.path.join(ROOT_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_SOUND_URL = "https://api.elevenlabs.io/v1/sound-generation"

# Shared music assets directory
MUSIC_ASSETS_DIR = os.path.join(ROOT_DIR, 'output', 'future_history', 'music_assets')

# ── Underscore: atmospheric bed that sits under narration ──────────
DEFAULT_UNDERSCORE_PROMPT = (
    "Minimal atmospheric electronic instrumental music, slow tempo 80-90 BPM, "
    "soft synth pads, subtle pulsing bass, light plucked textures, "
    "documentary underscore, ambient and contemplative, slightly ominous warmth, "
    "no percussion, loopable, background music for narration"
)

# ── Oppressive beat: fast catchy beat for intro/interstitials/outro ─
DEFAULT_OPPRESSIVE_BEAT_PROMPT = (
    "Fast catchy bouncy electronic beat, dark melodic synth hook, "
    "punchy kick drum with energy, addictive rhythm, "
    "cinematic documentary theme music, futuristic and driving, 120 BPM"
)


def _generate_elevenlabs_sound(prompt: str, output_filepath: str,
                                duration_seconds: float = 22.0) -> str:
    """Core function: generate a sound clip via ElevenLabs Sound Generation API."""
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is not set in .env")

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": prompt,
        "duration_seconds": min(duration_seconds, 22.0),
        "prompt_influence": 0.3
    }

    response = requests.post(ELEVENLABS_SOUND_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"ElevenLabs Sound Generation Error: {response.status_code} - {response.text[:500]}"
        )

    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, "wb") as f:
        f.write(response.content)

    return os.path.abspath(output_filepath)


def _loop_audio(filepath: str, target_duration: float) -> str:
    """Loop an audio file to reach the target duration using FFmpeg concat."""
    base_duration = 22.0
    loop_count = int(target_duration / base_duration) + 1

    looped_path = filepath.replace(".mp3", "_looped.mp3")
    concat_file = filepath.replace(".mp3", "_concat.txt")

    with open(concat_file, "w") as cf:
        for _ in range(loop_count):
            cf.write(f"file '{os.path.abspath(filepath)}'\n")

    ffmpeg_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file,
        "-t", str(target_duration),
        "-c", "copy",
        looped_path
    ]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(filepath)
    os.rename(looped_path, filepath)
    os.remove(concat_file)
    return filepath


def generate_music(prompt: str = None, output_filepath: str = None,
                   duration_seconds: float = 120.0) -> str:
    """
    Generate atmospheric underscore music for narration segments.
    Generates a 22s clip and loops it to the target duration.
    """
    if prompt is None:
        prompt = DEFAULT_UNDERSCORE_PROMPT
    if output_filepath is None:
        os.makedirs(MUSIC_ASSETS_DIR, exist_ok=True)
        output_filepath = os.path.join(MUSIC_ASSETS_DIR, "underscore.mp3")

    print(f"Generating underscore music via ElevenLabs...")
    print(f"  Prompt: '{prompt[:80]}...'")

    _generate_elevenlabs_sound(prompt, output_filepath, duration_seconds=22.0)
    file_size = os.path.getsize(output_filepath)
    print(f"  Base clip saved: {output_filepath} ({file_size // 1024}KB)")

    if duration_seconds > 22.0:
        print(f"  Looping to ~{duration_seconds}s...")
        _loop_audio(output_filepath, duration_seconds)
        print(f"  Looped underscore saved.")

    return os.path.abspath(output_filepath)


def generate_oppressive_beat(prompt: str = None, output_filepath: str = None) -> str:
    """
    Generate the oppressive beat for opening, interstitials, and outro.
    Single ~22s clip — not looped.
    """
    if prompt is None:
        prompt = DEFAULT_OPPRESSIVE_BEAT_PROMPT
    if output_filepath is None:
        os.makedirs(MUSIC_ASSETS_DIR, exist_ok=True)
        output_filepath = os.path.join(MUSIC_ASSETS_DIR, "oppressive_beat.mp3")

    print(f"Generating oppressive beat via ElevenLabs...")
    print(f"  Prompt: '{prompt[:80]}...'")

    _generate_elevenlabs_sound(prompt, output_filepath, duration_seconds=22.0)
    file_size = os.path.getsize(output_filepath)
    print(f"  Oppressive beat saved: {output_filepath} ({file_size // 1024}KB)")

    return os.path.abspath(output_filepath)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_music.py [underscore|oppressive_beat|both]")
        sys.exit(1)

    mode = sys.argv[1]
    os.makedirs(MUSIC_ASSETS_DIR, exist_ok=True)

    if mode in ("underscore", "both"):
        generate_music()
    if mode in ("oppressive_beat", "both"):
        generate_oppressive_beat()
