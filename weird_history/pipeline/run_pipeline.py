#!/usr/bin/env python3
"""
Full pipeline runner for Weird History / Future History video generation.
Usage: python run_pipeline.py <timeline_json_path> [--build-dir <path>]

If --build-dir is provided, the pipeline uses that directory (with pre-staged
assets) instead of creating a new timestamped one. Any existing scene files
in the build directory are reused (not regenerated).
"""
import argparse
import json
import os
import sys

# Ensure pipeline modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import OUTPUT_DIR
from generate_audio import generate_tts
from generate_images import generate_still
from generate_video import generate_video_clip
from generate_music import generate_music
from assemble_video import assemble_final_video

from datetime import datetime

# Voice IDs
NARRATION_VOICE = "dAlhI9qAHVIjXuVppzhW"   # Default feminine narrator
DEEP_VOICE = "qNkzaJoHLLdpvgh5tISm"         # Deep male for intro/outro

# Pre-built intro clip (built once via build_intro.py)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PREBUILT_INTRO = os.path.join(PROJECT_ROOT, 'output', 'future_history', 'intro_outro', 'future_history_intro.mp4')


def run(timeline_path: str, build_dir: str = None):
    """Run the full pipeline from a timeline JSON file."""

    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    title = timeline["title"]
    script = timeline["script"]
    voice_id = timeline.get("tts_voice_id", NARRATION_VOICE)
    fallback_voice = timeline.get("tts_fallback_voice", "en-GB-ThomasNeural")
    language = timeline.get("language", "en")
    series = timeline.get("series", "weird_history")
    music_prompt = timeline.get("music_prompt", None)
    series_name = timeline.get("series_display_name", "Future History")

    # Outro voice text
    outro_text = timeline.get("outro_text", f"{series_name}.")

    # Determine output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if build_dir:
        os.makedirs(build_dir, exist_ok=True)
    else:
        series_output_dir = os.path.join(os.path.dirname(OUTPUT_DIR), series)
        build_dir = os.path.join(series_output_dir, timestamp)
        os.makedirs(build_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  {series.upper().replace('_', ' ')} PIPELINE: {title}")
    print(f"  Output: {build_dir}")
    print(f"{'='*60}\n")

    # ── Step 1: Generate TTS Audio ──────────────────────────────
    print("\n[STEP 1/5] Generating TTS Audio...")

    # Main narration voiceover
    audio_path = os.path.join(build_dir, "voiceover.wav")
    if os.path.exists(audio_path):
        print(f"  Voiceover already exists, skipping.")
    else:
        generate_tts(script, audio_path, voice_id, language=language, fallback_voice=fallback_voice)
    print(f"  Narration: {audio_path}")

    # Outro disabled — will be built later
    outro_audio_path = None
    print()

    word_timestamps_path = os.path.join(build_dir, "word_timestamps.json")
    if not os.path.exists(word_timestamps_path) and os.path.exists(audio_path):
        print("  Generating WhisperX word timestamps...")
        from generate_transcription import generate_word_timestamps
        generate_word_timestamps(audio_path, word_timestamps_path, language=language)

    # ── Step 2: Generate Scene Assets ───────────────────────────
    print("[STEP 2/5] Generating Scene Assets (Images + Video)...")
    for scene in timeline["scenes"]:
        scene_id = scene["id"]
        scene_type = scene["type"]
        prompt = scene["prompt"]

        if scene_type == "image":
            filepath = os.path.join(build_dir, f"{scene_id}_still.jpg")
            if os.path.exists(filepath):
                print(f"  Scene {scene_id}: Still image already exists, skipping.")
            else:
                print(f"  Scene {scene_id}: Generating still image...")
                generate_still(prompt, filepath)
        elif scene_type == "video":
            filepath = os.path.join(build_dir, f"{scene_id}_video.mp4")
            if os.path.exists(filepath):
                print(f"  Scene {scene_id}: Video already exists, skipping.")
            else:
                print(f"  Scene {scene_id}: Generating video clip (this may take a while)...")
                generate_video_clip(prompt, filepath)

        scene["filepath"] = filepath
        print(f"  Scene {scene_id}: -> {filepath}")

    # Apply sentence-based timings
    if "sentences" in timeline and os.path.exists(word_timestamps_path):
        import re
        with open(word_timestamps_path, "r") as wf:
            word_ts = json.load(wf)
            
        # Reconstruct sentence timings from words
        sentence_timings = []
        words = word_ts.get('words', [])
        
        current_sentence_idx = 0
        current_sentence_words = []
        
        # A simple heuristic: try to map chunks of words to the sentences in the timeline
        sentence_text_list = timeline["sentences"]
        
        scene_idx = 0
        word_idx = 0
        
        for i, scene in enumerate(timeline["scenes"]):
            if scene_idx >= len(sentence_text_list):
                break
                
            sentence_target = sentence_text_list[scene_idx].strip()
            # Clean target for matching (remove punctuation)
            clean_target = re.sub(r'[^\w\s]', '', sentence_target.lower()).split()
            
            # Find the start and end word in the word_timestamps
            if word_idx < len(words):
                start_time = words[word_idx].get('start', 0)
                
                # Advance word_idx by the number of words in the target sentence
                words_matched = 0
                while word_idx < len(words) and words_matched < len(clean_target):
                    word_obj = words[word_idx]
                    word_clean = re.sub(r'[^\w\s]', '', word_obj.get('word', '').lower())
                    if word_clean:
                        words_matched += 1
                    word_idx += 1
                
                # The end time is the end of the last matched word
                if word_idx > 0 and 'end' in words[word_idx - 1]:
                    end_time = words[word_idx - 1]['end']
                else:
                    end_time = start_time + 3.0 # Fallback
                
                duration = end_time - start_time
                # Store it in the scene dict for assembly
                scene["_actual_duration"] = duration
                print(f"  Mapped Scene {scene['id']} to audio [{start_time:.2f}s - {end_time:.2f}s] (dur: {duration:.2f}s) -> '{sentence_target[:30]}...'")
            scene_idx += 1
            
        print()

    # ── Step 3: Generate Underscore Music ───────────────────────
    print("[STEP 3/5] Generating underscore music via ElevenLabs...")
    if series == "weird_history":
        print("  Skipping underscore music for weird_history.")
        music_path = None
    else:
        music_path = os.path.join(build_dir, "background_music.mp3")
        if os.path.exists(music_path):
            print(f"  Underscore already exists, skipping.")
        else:
            try:
                generate_music(prompt=music_prompt, output_filepath=music_path)
            except Exception as e:
                print(f"  WARNING: Underscore generation failed ({e}). Continuing without.")
                music_path = None
    print()

    # ── Step 4: Assemble Final Video ────────────────────────────
    # Check for pre-built intro
    intro_path = PREBUILT_INTRO if os.path.exists(PREBUILT_INTRO) else None
    if intro_path:
        print(f"[STEP 4/5] Assembling final video (with pre-built intro)...")
    else:
        print(f"[STEP 4/5] Assembling final video (no intro — run build_intro.py first)...")

    # Outro disabled — no theme needed for now
    theme_path = None

    final_path = assemble_final_video(
        timeline, audio_path, [], "final_render.mp4",
        output_dir=build_dir,
        music_path=music_path,
        theme_path=theme_path,
        intro_clip_path=intro_path,
        outro_audio_path=outro_audio_path,
    )
    print(f"  Final video: {final_path}\n")

    # ── Step 5: Save build metadata ─────────────────────────────
    print("[STEP 5/5] Saving build metadata...")
    metadata = {
        "title": title,
        "timeline_source": os.path.abspath(timeline_path),
        "build_timestamp": timestamp,
        "audio": audio_path,
        "outro_voice": outro_audio_path,
        "music": music_path,
        "intro_clip": intro_path,
        "scenes": [
            {"id": s["id"], "type": s["type"], "filepath": s["filepath"]}
            for s in timeline["scenes"]
        ],
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
    parser = argparse.ArgumentParser(description="Video generation pipeline")
    parser.add_argument("timeline", help="Path to the timeline JSON file")
    parser.add_argument("--build-dir", help="Path to a pre-staged build directory with assets")
    args = parser.parse_args()

    run(args.timeline, build_dir=args.build_dir)
