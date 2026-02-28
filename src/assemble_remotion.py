import os
import sys
import json
import subprocess
import argparse

def get_video_duration(video_path):
    """Use ffprobe to get the duration of a video in frames, assuming 30fps."""
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
        print(f"⚠️ Warning: Could not detect frames for {video_path}, falling back to 150 frames (5s). Error: {e}")
        return 150  # 5 seconds at 30fps as fallback

def assemble_video(folder_path):
    """Generates props and calls Remotion CLI to render the final video."""
    folder_path = os.path.abspath(folder_path)
    script_path = os.path.join(folder_path, "script.json")
    videos_dir = os.path.join(folder_path, "videos")
    
    if not os.path.exists(script_path):
        print(f"❌ No script.json found in {folder_path}")
        return False
        
    with open(script_path) as f:
        data = json.load(f)
        
    scenes = data.get('script', [])
    remotion_props = {"scenes": []}
    
    print(f"\n🎬 Assembling chunks for: {data.get('headline', 'Unknown')}")
    
    missing_clips = False
    for scene in scenes:
        scene_num = scene.get('scene_number')
        expected_video_path = os.path.join(videos_dir, f"scene_{scene_num:02d}.mp4")
        
        if not os.path.exists(expected_video_path):
            print(f"  ❌ Missing video for Scene {scene_num}: {expected_video_path}")
            missing_clips = True
            continue
            
        frames = get_video_duration(expected_video_path)
        
        remotion_props["scenes"].append({
            "videoUrl": f"file://{expected_video_path}",
            "durationInFrames": frames,
            "dialogue": scene.get('dialogue', '')
        })
        print(f"  ✅ Scene {scene_num}: Found ({frames} frames)")
        
    if missing_clips:
        print("❌ Cannot assemble video. Missing clips.")
        return False
        
    # Write props file for Remotion
    props_file = os.path.join(folder_path, "remotion_props.json")
    with open(props_file, 'w') as f:
        json.dump(remotion_props, f, indent=2)
        
    final_output = os.path.join(videos_dir, "final_assembled.mp4")
    
    # Path to the Remotion project
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    remotion_app_dir = os.path.join(project_root, 'remotion_app')
    
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
