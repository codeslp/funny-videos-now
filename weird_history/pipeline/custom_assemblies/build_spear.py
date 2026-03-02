import json
import os
import sys
import shutil

# PyTorch 2.6 security bug workaround: Pyannote needs typing.Any, which can't be added to safe_globals
import torch
_original_load = torch.load
def _patched_load(*args, **kwargs):
    kwargs["weights_only"] = False
    return _original_load(*args, **kwargs)
torch.load = _patched_load

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from generate_transcription import generate_word_timestamps
from assemble_video import assemble_final_video
from generate_audio import generate_tts

def run():
    base_dir = "/Users/bfaris96/Claude Code Markdown/funny_video_generator"
    build_dir = os.path.join(base_dir, "output/weird_history/spartan_spear")
    os.makedirs(build_dir, exist_ok=True)
    
    timeline_path = os.path.join(base_dir, "weird_history/spartan_spear_timeline.json")
    with open(timeline_path, "r") as f:
        timeline = json.load(f)

    # The user has 8 files for the video
    # 1. Roman_bride_in_dressing_room_0434ecbd63.jpeg (Scene 1)
    # 2. Older_woman_holding_spear_f64a6c1b58.jpeg (Scene 2)
    # 3. Hyperrealistic_portrait_photography_of_an_incredib_ec5f5b298b.jpeg (Scene 3)
    # 4. Brides_eyes_terrified_by_spear_a3cfb0022e.jpeg (Scene 4)
    # 5. Curly_dark_hair_on_spear_15c4357594.mp4 (Scene 5)
    # 6. Roman_woman_parts_brides_hair_717794eee4.mp4 (Scene 6)
    # 7. Roman_groom_giving_thumbsup_472d8c3e95.jpeg (Scene 7)
    # 8. Hyperrealistic_group_photography_of_a_crowd_of_che_f63aafd6da.jpeg (Scene 8)
    
    downloads_dir = "/Users/bfaris96/Downloads"
    files_to_copy = [
        ("Roman_bride_in_dressing_room_0434ecbd63.jpeg", "scene_1_still.jpeg"),
        ("Older_woman_holding_spear_f64a6c1b58.jpeg", "scene_2_still.jpeg"),
        ("Hyperrealistic_portrait_photography_of_an_incredib_ec5f5b298b.jpeg", "scene_3_still.jpeg"),
        ("Brides_eyes_terrified_by_spear_a3cfb0022e.jpeg", "scene_4_still.jpeg"),
        ("Curly_dark_hair_on_spear_15c4357594.mp4", "scene_5_video.mp4"),
        ("Maidens_partying_in_plaza_7ce4a62f12.mp4", "scene_6_video.mp4"),
        ("Roman_groom_giving_thumbsup_472d8c3e95 (2).jpeg", "scene_7_still.jpeg"), # Using the latest one
        ("Hyperrealistic_group_photography_of_a_crowd_of_che_f63aafd6da.jpeg", "scene_8_still.jpeg")
    ]
    
    # Trim the timeline to 8 scenes
    timeline["scenes"] = timeline["scenes"][:8]
    
    for i, (src_name, dst_name) in enumerate(files_to_copy):
        if src_name == "Maidens_partying_in_plaza_7ce4a62f12.mp4":
            src_path = os.path.join(build_dir, src_name)
        else:
            src_path = os.path.join(downloads_dir, src_name)
        dst_path = os.path.join(build_dir, dst_name)
        
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Missing downloaded asset: {src_path}")
            
        if src_path != dst_path:
            shutil.copy2(src_path, dst_path)
        timeline["scenes"][i]["filepath"] = dst_path

    audio_path = os.path.join(build_dir, "voiceover.wav")
    timestamps_path = os.path.join(build_dir, "word_timestamps.json")
    
    # 1. Generate Voiceover
    print("Generating voiceover...")
    script_text = timeline.get("script", "")
    voice_id = "1f575487-6f3d-40e0-862a-814f55b5fb15"
    generate_tts(script_text, audio_path, voice_id)
    
    # 2. Generate transcriptions (using whisperx inline as in manual_assembly)
    print("Generating transcriptions...")
    import whisperx
    device = "cpu" 
    audio = whisperx.load_audio(audio_path)
    model = whisperx.load_model("base.en", device, compute_type="int8")
    result = model.transcribe(audio, batch_size=4)
    
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
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

    # 3. Assemble Video
    print("Assembling video...")
    final_path = assemble_final_video(
        timeline, audio_path, words, "final_spear_video.mp4", output_dir=build_dir
    )
    print(f"Done! Saved to {final_path}")

if __name__ == "__main__":
    run()
