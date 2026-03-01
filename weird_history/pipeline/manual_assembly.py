import json
import os
import sys

# PyTorch 2.6 security bug workaround: Pyannote needs typing.Any, which can't be added to safe_globals
import torch
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_transcription import generate_word_timestamps
from assemble_video import assemble_final_video

def run():
    build_dir = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/tudor_needle_test_2026-02-28"
    timeline_path = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/weird_history/pipeline/tudor_needle_timeline.json"
    
    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    # Set filepaths dynamically based on type for all scenes
    for i, scene in enumerate(timeline["scenes"]):
        ext = "mp4" if scene["type"] == "video" else "jpg"
        suffix = "video" if scene["type"] == "video" else "still"
        scene["filepath"] = os.path.join(build_dir, f"scene_{i+1}_{suffix}.{ext}")

    audio_path = os.path.join(build_dir, "voiceover.wav")
    timestamps_path = os.path.join(build_dir, "word_timestamps.json")
    
    # We will try the native WhisperX python wrapper if the CLI failed. We added the PyTorch globals patch above.
    import whisperx
    
    print("Generating transcriptions...")
    device = "cpu" 
    audio = whisperx.load_audio(audio_path)
    model = whisperx.load_model("base.en", device, compute_type="int8")
    result = model.transcribe(audio, batch_size=4)
    
    # Align timestamps
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    # Format the same way generate_word_timestamps expects
    words = []
    for segment in result.get('segments', []):
        for word in segment.get('words', []):
            if 'start' in word and 'end' in word:
                words.append({
                    "word": word.get("word").strip(),
                    "start": word.get("start"),
                    "end": word.get("end")
                })
                
    with open(timestamps_path, 'w') as f:
        json.dump(words, f, indent=4)
    print(f"Generated {len(words)} word timestamps")
    word_timestamps = words

    print("Assembling video...")
    
    # Workaround assemble bug (output_dir_name issue) by passing output_dir explicitly
    final_path = assemble_final_video(
        timeline, audio_path, word_timestamps, "final_render.mp4", output_dir=build_dir
    )
    print(f"Done! Saved to {final_path}")

if __name__ == "__main__":
    run()
