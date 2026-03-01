import os
import sys
import json
import subprocess
import argparse
import urllib.parse

def get_video_duration(video_path):
    """Use ffprobe to get the duration of a video in frames, assuming 24fps."""
    try:
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-select_streams', 'v:0', 
            '-count_packets',
            '-show_entries', 'stream=nb_read_packets', 
            '-of', 'csv=p=0', 
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        frames = int(result.stdout.strip())
        return frames
    except Exception as e:
        print(f"⚠️ Warning: Could not detect frames for {video_path}, falling back to 120 frames (5s). Error: {e}")
        return 120  # 5 seconds at 24fps as fallback

import shutil
import wave

def get_audio_duration(audio_path, fps=24):
    """Get audio duration in frames using ffprobe."""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            audio_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration_sec = float(result.stdout.strip())
        return int(duration_sec * fps)
    except Exception as e:
        print(f"⚠️ Warning: Could not detect audio duration for {audio_path}. Error: {e}")
        return 0

def assemble_video(timeline_path):
    """Generates props, copies assets to Remotion's public folder, and renders."""
    timeline_path = os.path.abspath(timeline_path)
    output_dir = os.path.dirname(timeline_path)
    output_basename = os.path.basename(output_dir)
    
    # Path to the Remotion project
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    remotion_app_dir = os.path.join(project_root, 'remotion_app')
    public_dir = os.path.join(remotion_app_dir, 'public', output_basename)
    
    os.makedirs(public_dir, exist_ok=True)
    
    if not os.path.exists(timeline_path):
        print(f"❌ No timeline JSON found at {timeline_path}")
        return False
        
    with open(timeline_path) as f:
        data = json.load(f)
        
    scenes = data.get('scenes', [])
    remotion_props = {"scenes": []}
    
    # Try finding an audio file in the same directory as the first scene
    audio_frames = 0
    if scenes:
        first_scene_dir = os.path.dirname(os.path.abspath(scenes[0].get('filepath', '')))
        possible_audio_path = os.path.join(first_scene_dir, "voiceover.wav")
        if os.path.exists(possible_audio_path):
             # Copy to public
             dest_audio = os.path.join(public_dir, "voiceover.wav")
             shutil.copy2(possible_audio_path, dest_audio)
             remotion_props["voiceoverUrl"] = f"{output_basename}/voiceover.wav"
             audio_frames = get_audio_duration(possible_audio_path)
             print(f"  🎙 Copied voiceover to public folder ({audio_frames} frames expected overall)")
             
             # Generate Whisper Captions
             whisper_json_path = os.path.join(first_scene_dir, "voiceover.json")
             if not os.path.exists(whisper_json_path):
                 print("  💬 Generating Whisper captions (this may take a minute)...")
                 try:
                     cmd = [
                         sys.executable, "-m", "whisper",
                         possible_audio_path,
                         "--model", "base",
                         "--output_format", "json",
                         "--output_dir", first_scene_dir,
                         "--word_timestamps", "True"
                     ]
                     subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
                 except Exception as e:
                     print(f"  ⚠️ Warning: Whisper caption generation failed. Error: {e}")
             
             if os.path.exists(whisper_json_path):
                 with open(whisper_json_path, 'r') as wf:
                     whisper_data = json.load(wf)
                     words = []
                     for seg in whisper_data.get('segments', []):
                         for w in seg.get('words', []):
                             words.append({
                                 "text": w.get("text", w.get("word", "")).strip(),
                                 "start": w["start"],
                                 "end": w["end"]
                             })
                     remotion_props["captions"] = words
                     print(f"  📝 Loaded {len(words)} caption words")
    
    print(f"\n🎬 Assembling chunks for: {data.get('topic', 'Unknown')}")
    
    missing_clips = False
    valid_scenes = []
    total_video_frames = 0
    num_images = 0

    for scene in scenes:
        scene_id = scene.get('id')
        media_type = scene.get('type')
        filepath = scene.get('filepath')

        if not filepath:
            print(f"  ❌ Missing filepath for Scene {scene_id}")
            missing_clips = True
            continue

        # Convert relative to absolute if needed
        if not os.path.isabs(filepath):
            expected_media_path = os.path.join(project_root, filepath)
        else:
            expected_media_path = filepath
        
        if not os.path.exists(expected_media_path):
            print(f"  ❌ Missing media for Scene {scene_id}: {expected_media_path}")
            missing_clips = True
            continue
            
        scene_info = {
            "id": scene_id,
            "type": media_type,
            "path": expected_media_path,
            "filename": os.path.basename(expected_media_path)
        }

        if media_type == 'video':
            frames = get_video_duration(expected_media_path)
            total_video_frames += frames
            scene_info["frames"] = frames
        else:
            num_images += 1
            
        valid_scenes.append(scene_info)

    if missing_clips:
        print("❌ Cannot assemble video. Missing clips.")
        return False

    frames_per_image = 120 # 5s at 24fps
    remainder_frames = 0
    if audio_frames > 0 and num_images > 0:
        remaining_frames = audio_frames - total_video_frames
        if remaining_frames > 0:
            frames_per_image = remaining_frames // num_images
            remainder_frames = remaining_frames % num_images
        else:
            frames_per_image = 24 # fallback if video is longer than audio
            
    images_processed = 0
    for scene_info in valid_scenes:
        media_type = scene_info['type']
        expected_media_path = scene_info['path']
        filename = scene_info['filename']
        scene_id = scene_info['id']
        
        # Copy to public
        dest_media = os.path.join(public_dir, filename)
        shutil.copy2(expected_media_path, dest_media)
            
        if media_type == 'image':
            images_processed += 1
            frames = frames_per_image
            if images_processed == num_images:
                frames += remainder_frames
        else:
            frames = scene_info["frames"]
        
        remotion_props["scenes"].append({
            "videoUrl": f"{output_basename}/{filename}",
            "durationInFrames": frames,
            "type": media_type
        })
        print(f"  ✅ Scene {scene_id}: Copied ({frames} frames - {media_type})")
        
    # Write props file for Remotion
    props_file = os.path.join(output_dir, "remotion_props.json")
    with open(props_file, 'w') as f:
        json.dump(remotion_props, f, indent=2)
    final_output_dir = output_dir
    if scenes:
        first_scene_dir = os.path.dirname(os.path.abspath(scenes[0].get('filepath', '')))
        final_output_dir = first_scene_dir
        
    final_output = os.path.join(final_output_dir, "final_assembled.mp4")
    
    # Execute Remotion CLI
    print(f"\n🚀 Launching Remotion Render Engine...")
    cmd = [
        "npx", "remotion", "render",
        "src/index.ts",  # Entry file
        "MainVideo",     # Composition ID
        final_output,
        f"--props={props_file}"
    ]
    
    try:
        subprocess.run(cmd, cwd=remotion_app_dir, check=True)
        print(f"\n✨ Video assembled successfully: {final_output}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Remotion rendering failed.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Path to the output folder (e.g., output/01_some_video)")
    args = parser.parse_args()
    
    assemble_video(args.folder)
