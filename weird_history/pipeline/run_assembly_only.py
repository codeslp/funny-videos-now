import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR
from generate_audio import generate_tts
from generate_transcription import generate_word_timestamps
from assemble_video import assemble_final_video

def run(timeline_path: str, assets_dir: str):
    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    title = timeline["title"]
    script = timeline["script"]
    voice_id = timeline.get("tts_voice_id", "a0e99841-438c-4a64-b6a9-ae8f1d56cc33")

    build_dir = assets_dir # We use the existing assets dir

    os.makedirs(build_dir, exist_ok=True)
    print(f"Using assets directory: {build_dir}")

    # Step 1: Generate TTS Audio (check if exists, if not generate)
    audio_path = os.path.join(build_dir, "voiceover.wav")
    if not os.path.exists(audio_path):
        print("\n[STEP 1/5] Generating TTS Audio via Cartesia...")
        generate_tts(script, audio_path, voice_id)
        print(f"  Audio saved: {audio_path}\n")
    else:
        print("\n[STEP 1/5] Using existing TTS Audio...")

    # Step 2: Set filepaths for assets
    print("[STEP 2/5] Checking Scene Assets (Images + Video)...")
    missing_assets = False
    for scene in timeline["scenes"]:
        scene_id = scene["id"]
        scene_type = scene["type"]
        
        if scene_type == "image":
            filepath = os.path.join(build_dir, f"{scene_id}_still.jpg")
            # Some browsers save as .jpeg or .png, fallback logic
            if not os.path.exists(filepath):
                 filepath_jpeg = os.path.join(build_dir, f"{scene_id}_still.jpeg")
                 filepath_png = os.path.join(build_dir, f"{scene_id}_still.png")
                 if os.path.exists(filepath_jpeg): filepath = filepath_jpeg
                 elif os.path.exists(filepath_png): filepath = filepath_png
        elif scene_type == "video":
            filepath = os.path.join(build_dir, f"{scene_id}_video.mp4")

        if not os.path.exists(filepath):
            print(f"WARNING: Asset not found: {filepath}")
            missing_assets = True

        scene["filepath"] = filepath
        print(f"  Scene {scene_id}: -> {filepath}")

    print()
    if missing_assets:
        print("There are missing assets. The assembly may fail if ffmpeg expects them.")

    # Step 3: Generate Transcription
    print("[STEP 3/5] Generating word-level timestamps via WhisperX...")
    timestamps_path = os.path.join(build_dir, "word_timestamps.json")
    if not os.path.exists(timestamps_path):
        try:
            word_timestamps = generate_word_timestamps(audio_path, timestamps_path)
            print(f"  Timestamps saved: {timestamps_path}\n")
        except Exception as e:
            print(f"  WARNING: WhisperX failed ({e}). Continuing without captions.")
            word_timestamps = []
            print()
    else:
        with open(timestamps_path, "r") as f:
            word_timestamps = json.load(f)
            print(f"  Using existing Timestamps: {timestamps_path}\n")

    # Step 4: Assemble Final Video
    print("[STEP 4/5] Assembling final video via FFmpeg...")
    final_path = assemble_final_video(
        timeline, audio_path, word_timestamps, "final_render.mp4", output_dir=build_dir
    )
    print(f"  Final video: {final_path}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_assembly_only.py <timeline_json_path> <assets_dir>")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
