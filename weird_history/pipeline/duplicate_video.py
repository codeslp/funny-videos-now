#!/usr/bin/env python3
"""
Pipeline runner for Weird History video duplication (e.g., Translation).
Usage: python duplicate_video.py <translated_timeline_json> <original_build_metadata_json>
"""
import json
import os
import sys

# Ensure pipeline modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR
from generate_audio import generate_tts
from generate_transcription import generate_word_timestamps
from assemble_video import assemble_final_video

from datetime import datetime

def run_duplicate(timeline_path: str, metadata_path: str):
    """Run the pipeline using existing visual assets from a previous build metadata."""

    if not os.path.exists(timeline_path):
        raise FileNotFoundError(f"Timeline not found: {timeline_path}")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata not found: {metadata_path}")

    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    title = timeline.get("title", "Translated Video")
    script = timeline.get("script", "")
    voice_id = timeline.get("tts_voice_id", "a0e99841-438c-4a64-b6a9-ae8f1d56cc33")
    language = timeline.get("language", "en")
    
    # ── Step 0: Inject existing visual assets into the timeline ────────────────
    # We map the filepaths from the original build metadata into the new timeline
    if len(timeline["scenes"]) != len(metadata["scenes"]):
        raise ValueError(f"Scene count mismatch! Translated timeline has {len(timeline['scenes'])} scenes and original metadata has {len(metadata['scenes'])}.")
        
    for i, scene in enumerate(timeline["scenes"]):
        # Copy the filepath from the exact same scene index in the original run
        scene["filepath"] = os.path.abspath(metadata["scenes"][i]["filepath"])

    # Create a timestamped output directory for this duplicate build
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).replace(' ', '_').lower()
    
    # For translations, maybe prefix with language
    if language != "en":
        output_dir_name = f"{language}_{clean_title}_{timestamp}"
    else:
        output_dir_name = f"dup_{clean_title}_{timestamp}"
        
    build_dir = os.path.join(OUTPUT_DIR, output_dir_name)
    os.makedirs(build_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  WEIRD HISTORY TRANSLATION PIPELINE: {title}")
    print(f"  Language: {language}")
    print(f"  Output: {build_dir}")
    print(f"{'='*60}\n")

    # ── Step 1: Generate TTS Audio ──────────────────────────────
    print(f"\n[STEP 1/3] Generating TTS Audio ({language}) via Cartesia...")
    audio_path = os.path.join(build_dir, "voiceover.wav")
    generate_tts(script, audio_path, voice_id, language)
    print(f"  Audio saved: {audio_path}\n")

    # ── Step 2: Generate Transcription ──────────────────────────
    print(f"[STEP 2/3] Generating word-level timestamps ({language}) via WhisperX...")
    try:
        timestamps_path = os.path.join(build_dir, "word_timestamps.json")
        word_timestamps = generate_word_timestamps(audio_path, timestamps_path, language)
        print(f"  Timestamps saved: {timestamps_path}\n")
    except Exception as e:
        print(f"  WARNING: WhisperX failed ({e}). Continuing without captions.")
        word_timestamps = []
        print()

    # ── Step 3: Assemble Final Video ────────────────────────────
    print("[STEP 3/3] Assembling final video via FFmpeg using Original Visuals...")
    final_path = assemble_final_video(
        timeline, audio_path, word_timestamps, "final_render_translated.mp4", output_dir=build_dir, allow_duplicates=True
    )
    print(f"  Final video: {final_path}\n")

    # ── Step 4: Save build metadata ─────────────────────────────
    print("[STEP 4/4] Saving duplicate build metadata...")
    new_metadata = {
        "title": title,
        "language": language,
        "original_metadata_source": os.path.abspath(metadata_path),
        "timeline_source": os.path.abspath(timeline_path),
        "build_timestamp": timestamp,
        "audio": audio_path,
        "scenes": [
            {"id": s["id"], "type": s["type"], "filepath": s["filepath"]}
            for s in timeline["scenes"]
        ],
        "word_timestamps_count": len(word_timestamps),
        "final_render": final_path,
    }
    meta_path = os.path.join(build_dir, "build_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(new_metadata, f, indent=4)

    print(f"\n{'='*60}")
    print(f"  DUPLICATION COMPLETE!")
    print(f"  Output: {final_path}")
    print(f"  Metadata: {meta_path}")
    print(f"{'='*60}\n")

    return final_path


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python duplicate_video.py <translated_timeline_json> <original_build_metadata_json>")
        sys.exit(1)

    run_duplicate(sys.argv[1], sys.argv[2])
