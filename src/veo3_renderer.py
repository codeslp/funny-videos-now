"""
Veo3 Auto-Renderer
Reads generated scripts from output/ folders, submits all scene prompts
to the Veo 3.1 Fast API in parallel, polls for completion, and downloads
the rendered clips into each video's videos/ folder.
"""

import os
import sys
import json
import time
import urllib.request
import ssl

sys.path.insert(0, os.path.dirname(__file__))
from script_generator import _load_env

_load_env()

# Configuration
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "veo-3.1-generate-preview"  # Quality mode: 100 credits/clip
ASPECT_RATIO = "9:16"
POLL_INTERVAL = 10  # seconds between status checks
MAX_POLL_TIME = 600  # 10 minutes max wait per clip (quality takes longer)
SUBMIT_DELAY = 15   # seconds between scene submissions to avoid 429s


def submit_video_job(prompt, api_key):
    """Submit a video generation job to Veo3. Returns the operation name."""
    url = f"{BASE_URL}/models/{MODEL}:predictLongRunning"

    payload = {
        "instances": [{
            "prompt": prompt
        }],
        "parameters": {
            "aspectRatio": ASPECT_RATIO,
            "personGeneration": "allow_all"
        }
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'x-goog-api-key': api_key
        },
        method='POST'
    )
    context = ssl._create_unverified_context()

    with urllib.request.urlopen(req, context=context) as response:
        result = json.loads(response.read().decode())
        operation_name = result.get('name')
        if not operation_name:
            raise Exception(f"No operation name in response: {result}")
        return operation_name


def poll_video_job(operation_name, api_key):
    """Poll a video job until complete. Returns the video download URI."""
    url = f"{BASE_URL}/{operation_name}"
    context = ssl._create_unverified_context()
    elapsed = 0

    while elapsed < MAX_POLL_TIME:
        req = urllib.request.Request(
            url,
            headers={'x-goog-api-key': api_key}
        )
        with urllib.request.urlopen(req, context=context) as response:
            result = json.loads(response.read().decode())

        if result.get('done'):
            # Extract video URI
            try:
                video_uri = result['response']['generateVideoResponse']['generatedSamples'][0]['video']['uri']
                return video_uri
            except (KeyError, IndexError) as e:
                raise Exception(f"Video done but couldn't extract URI: {result}")

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL
        print(f"      ⏳ Waiting... ({elapsed}s)")

    raise TimeoutError(f"Video generation timed out after {MAX_POLL_TIME}s")


def download_video(video_uri, output_path, api_key):
    """Download a rendered video to disk."""
    context = ssl._create_unverified_context()
    req = urllib.request.Request(
        video_uri,
        headers={'x-goog-api-key': api_key}
    )
    with urllib.request.urlopen(req, context=context) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())


def render_video_folder(folder_path, api_key):
    """Render all scenes for a single video folder."""
    script_path = os.path.join(folder_path, "script.json")
    if not os.path.exists(script_path):
        print(f"  ⚠️  No script.json found in {folder_path}, skipping.")
        return False

    with open(script_path) as f:
        data = json.load(f)

    headline = data.get('headline', 'Unknown')
    scenes = data.get('script', [])
    videos_dir = os.path.join(folder_path, "videos")
    os.makedirs(videos_dir, exist_ok=True)

    print(f"\n  📰 {headline}")
    print(f"  🎬 Submitting {len(scenes)} scenes to Veo3...\n")

    # Submit all scenes at once (parallel generation)
    jobs = []
    for scene in scenes:
        scene_num = scene.get('scene_number', 0)
        prompt = scene.get('veo3_visual_prompt', '')
        dialogue = scene.get('dialogue', '')

        # Combine visual prompt + dialogue for Veo3
        full_prompt = prompt
        if dialogue:
            full_prompt += f"\n\nDialogue: {dialogue}"

        try:
            print(f"    Scene {scene_num}: Submitting...")
            op_name = submit_video_job(full_prompt, api_key)
            jobs.append({
                'scene_number': scene_num,
                'operation_name': op_name,
                'output_path': os.path.join(videos_dir, f"scene_{scene_num:02d}.mp4")
            })
            print(f"    Scene {scene_num}: ✅ Queued ({op_name[:40]}...)")
            # Pace submissions to avoid 429 rate limits
            if scene_num < len(scenes):
                time.sleep(SUBMIT_DELAY)
        except Exception as e:
            print(f"    Scene {scene_num}: ❌ Failed to submit: {e}")

    # Poll and download all
    print(f"\n    ⏳ Waiting for {len(jobs)} scenes to render...")
    for job in jobs:
        try:
            print(f"\n    Scene {job['scene_number']}: Polling...")
            video_uri = poll_video_job(job['operation_name'], api_key)
            print(f"    Scene {job['scene_number']}: Downloading...")
            download_video(video_uri, job['output_path'], api_key)
            print(f"    Scene {job['scene_number']}: ✅ Saved to {job['output_path']}")
        except Exception as e:
            print(f"    Scene {job['scene_number']}: ❌ {e}")

    return True


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found. Add it to your .env file.")
        return

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_dir):
        print("❌ No output/ directory found. Run main.py first to generate scripts.")
        return

    # Find all video folders
    folders = sorted([
        os.path.join(output_dir, d) for d in os.listdir(output_dir)
        if os.path.isdir(os.path.join(output_dir, d))
    ])

    if not folders:
        print("❌ No video folders found in output/.")
        return

    print("\n" + "=" * 60)
    print("  🎬  VEO3 AUTO-RENDERER  🎬")
    print(f"  📊  Mode: {MODEL}")
    print(f"  📐  Aspect Ratio: {ASPECT_RATIO}")
    print(f"  📁  Videos to render: {len(folders)}")
    print("=" * 60)

    for folder in folders:
        folder_name = os.path.basename(folder)
        print(f"\n{'─' * 60}")
        print(f"📁 {folder_name}")
        render_video_folder(folder, api_key)

    print(f"\n{'=' * 60}")
    print(f"  ✅ RENDERING COMPLETE")
    print(f"  Check output/*/videos/ for your rendered clips.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
