#!/usr/bin/env python3
"""
Full pipeline runner for Weird History video generation.
Usage: python run_pipeline.py <timeline_json_path>
"""
import json
import os
import sys

# Ensure pipeline modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR
from generate_audio import generate_tts
from generate_images import generate_still
from generate_video import generate_video_clip
from generate_transcription import generate_word_timestamps
from assemble_video import assemble_final_video

from datetime import datetime


def run(timeline_path: str):
    """Run the full pipeline from a timeline JSON file."""

    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    title = timeline["title"]
    script = timeline["script"]
    voice_id = timeline.get("tts_voice_id", "a0e99841-438c-4a64-b6a9-ae8f1d56cc33")

    # Create a timestamped output directory for this build
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    build_dir = os.path.join(OUTPUT_DIR, timestamp)
    os.makedirs(build_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  WEIRD HISTORY PIPELINE: {title}")
    print(f"  Output: {build_dir}")
    print(f"{'='*60}\n")

    # ── Step 1: Generate TTS Audio ──────────────────────────────
    print("\n[STEP 1/5] Generating TTS Audio via Cartesia...")
    audio_path = os.path.join(build_dir, "voiceover.wav")
    generate_tts(script, audio_path, voice_id)
    print(f"  Audio saved: {audio_path}\n")

    # ── Step 2: Generate Scene Assets ───────────────────────────
    print("[STEP 2/5] Generating Scene Assets (Images + Video)...")
    for scene in timeline["scenes"]:
        scene_id = scene["id"]
        scene_type = scene["type"]
        prompt = scene["prompt"]

        if scene_type == "image":
            filepath = os.path.join(build_dir, f"scene_{scene_id}_still.jpg")
            print(f"  Scene {scene_id}: Generating still image...")
            generate_still(prompt, filepath)
        elif scene_type == "video":
            filepath = os.path.join(build_dir, f"scene_{scene_id}_video.mp4")
            print(f"  Scene {scene_id}: Generating video clip (this may take a while)...")
            generate_video_clip(prompt, filepath)

        # Update the scene filepath for assembly
        scene["filepath"] = filepath
        print(f"  Scene {scene_id}: Done -> {filepath}")

    print()

    # ── Step 3: Generate Transcription ──────────────────────────
    print("[STEP 3/5] Generating word-level timestamps via WhisperX...")
    try:
        timestamps_path = os.path.join(build_dir, "word_timestamps.json")
        word_timestamps = generate_word_timestamps(audio_path, timestamps_path)
        print(f"  Timestamps saved: {timestamps_path}\n")
    except Exception as e:
        print(f"  WARNING: WhisperX failed ({e}). Continuing without captions.")
        word_timestamps = []
        print()

    # ── Step 4: Assemble Final Video ────────────────────────────
    print("[STEP 4/5] Assembling final video via FFmpeg...")
    final_path = assemble_final_video(
        timeline, audio_path, word_timestamps, "final_render.mp4", output_dir=build_dir
    )
    print(f"  Final video: {final_path}\n")

    # ── Step 5: Save build metadata ─────────────────────────────
    print("[STEP 5/5] Saving build metadata...")
    metadata = {
        "title": title,
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
        json.dump(metadata, f, indent=4)

    print(f"\n{'='*60}")
    print(f"  BUILD COMPLETE!")
    print(f"  Output: {final_path}")
    print(f"  Metadata: {meta_path}")
    print(f"{'='*60}\n")

    return final_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py <timeline_json_path>")
        sys.exit(1)

    run(sys.argv[1])
