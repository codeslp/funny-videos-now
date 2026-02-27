#!/usr/bin/env python3
"""
NIGHTLY GENERATOR — Run via cron at 2 AM CST
Fetches trending news, scores for visual comedy potential,
picks the top N stories, generates scripts, and renders via Veo 3.1.

Usage: python3 generate_overnight.py [--count 3]
"""
import os
import sys
import json
import time
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from script_generator import _load_env, generate_comedic_script
from news_sourcing import fetch_all_curated_news
from veo3_renderer import render_video_folder

_load_env()

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"generate_{datetime.now().strftime('%Y-%m-%d')}.log")
    with open(log_file, 'a') as f:
        f.write(line + "\n")


def get_next_video_number():
    """Find the next available video number based on existing output folders."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    existing = [d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))]
    numbers = []
    for d in existing:
        try:
            num = int(d.split('_')[0])
            numbers.append(num)
        except (ValueError, IndexError):
            pass
    return max(numbers, default=0) + 1


def create_video_folder(video_num, news_item, script):
    """Create a video folder with script and prompts."""
    safe_name = news_item['title'][:50].lower()
    safe_name = ''.join(c if c.isalnum() or c in ' _-' else '' for c in safe_name)
    safe_name = safe_name.strip().replace(' ', '_')
    folder_name = f"{video_num:02d}_{safe_name}"
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(os.path.join(folder_path, 'videos'), exist_ok=True)

    # Save script.json
    data = {
        "video_number": video_num,
        "headline": news_item['title'],
        "source": news_item.get('source', ''),
        "url": news_item.get('url', ''),
        "comedy_score": news_item.get('total_comedy_score', 0),
        "pitch": news_item.get('pitch', ''),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "script": script
    }
    with open(os.path.join(folder_path, 'script.json'), 'w') as f:
        json.dump(data, f, indent=2)

    # Save prompt files
    prompts_text = ''
    for scene in script:
        num = scene['scene_number']
        prompt = scene.get('veo3_visual_prompt', '')
        dialogue = scene.get('dialogue', '')
        full_prompt = prompt
        if dialogue:
            full_prompt += f"\n\nDialogue: {dialogue}"
        with open(os.path.join(folder_path, f'scene_{num:02d}_prompt.txt'), 'w') as f:
            f.write(full_prompt)
        prompts_text += f"=== SCENE {num} ===\n{full_prompt}\n\n"

    with open(os.path.join(folder_path, 'prompts.txt'), 'w') as f:
        f.write(prompts_text)

    return folder_path


def main():
    parser = argparse.ArgumentParser(description='Nightly video generator')
    parser.add_argument('--count', type=int, default=3, help='Number of videos to generate (default: 3)')
    parser.add_argument('--skip-render', action='store_true', help='Skip Veo rendering (scripts only)')
    parser.add_argument('--retry-delay', type=int, default=120, help='Seconds between Veo retries on rate limit')
    parser.add_argument('--max-retries', type=int, default=3, help='Max retries per video on rate limit')
    args = parser.parse_args()

    log("=" * 60)
    log("🌙 NIGHTLY VIDEO GENERATOR STARTING")
    log(f"   Target: {args.count} videos")
    log("=" * 60)

    # Step 1: Source and score news
    log("\n📡 Step 1: Sourcing and scoring news...")
    news = fetch_all_curated_news(score=True)
    if not news:
        log("❌ No news found. Exiting.")
        return

    # Filter out already-used headlines
    used_headlines = set()
    if os.path.exists(OUTPUT_DIR):
        for d in os.listdir(OUTPUT_DIR):
            script_path = os.path.join(OUTPUT_DIR, d, 'script.json')
            if os.path.exists(script_path):
                try:
                    with open(script_path) as f:
                        data = json.load(f)
                    used_headlines.add(data.get('headline', '').lower())
                except Exception:
                    pass

    available = [n for n in news if n['title'].lower() not in used_headlines]
    log(f"   {len(available)} new stories available (filtered {len(news) - len(available)} already used)")

    # Pick top N by comedy score
    picks = available[:args.count]
    if not picks:
        log("❌ No new stories to generate. Exiting.")
        return

    log(f"\n🎯 Step 2: Selected {len(picks)} stories:")
    for i, pick in enumerate(picks, 1):
        log(f"   {i}. [Score: {pick.get('total_comedy_score', '?')}] {pick['title'][:70]}")

    # Step 3: Generate scripts
    log("\n🤖 Step 3: Generating scripts...")
    next_num = get_next_video_number()
    generated_folders = []

    for i, pick in enumerate(picks):
        video_num = next_num + i
        log(f"\n   Video {video_num:02d}: {pick['title'][:60]}...")
        try:
            script = generate_comedic_script(pick)
            folder = create_video_folder(video_num, pick, script)
            generated_folders.append(folder)
            log(f"   ✅ Script saved to {os.path.basename(folder)}")
        except Exception as e:
            log(f"   ❌ Script generation failed: {e}")

    # Step 4: Render via Veo
    if args.skip_render:
        log("\n⏭️  Skipping Veo rendering (--skip-render)")
    else:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            log("\n❌ No GEMINI_API_KEY — cannot render.")
        else:
            log(f"\n🎬 Step 4: Rendering {len(generated_folders)} videos via Veo 3.1...")
            for folder in generated_folders:
                retries = 0
                while retries <= args.max_retries:
                    try:
                        render_video_folder(folder, api_key)
                        # Check if any scenes rendered
                        videos_dir = os.path.join(folder, 'videos')
                        clips = [f for f in os.listdir(videos_dir) if f.startswith('scene_') and f.endswith('.mp4')]
                        if clips:
                            log(f"   ✅ {os.path.basename(folder)}: {len(clips)} scenes rendered")

                            # Assemble with ffmpeg
                            if len(clips) > 1:
                                clips_sorted = sorted(clips)
                                inputs = ' '.join([f'-i {os.path.join(videos_dir, c)}' for c in clips_sorted])
                                n = len(clips_sorted)
                                filter_parts = ''.join([f'[{i}:v][{i}:a]' for i in range(n)])
                                filter_complex = f'{filter_parts}concat=n={n}:v=1:a=1[outv][outa]'
                                final_path = os.path.join(videos_dir, 'final.mp4')
                                cmd = f'ffmpeg -y {inputs} -filter_complex "{filter_complex}" -map "[outv]" -map "[outa]" -c:v libx264 -c:a aac {final_path}'
                                os.system(cmd)
                                if os.path.exists(final_path):
                                    log(f"   ✅ Assembled final.mp4")
                            break
                        else:
                            log(f"   ⚠️  No scenes rendered (possible rate limit)")
                            retries += 1
                            if retries <= args.max_retries:
                                log(f"   ⏳ Retrying in {args.retry_delay}s... ({retries}/{args.max_retries})")
                                time.sleep(args.retry_delay)
                    except Exception as e:
                        log(f"   ❌ Render error: {e}")
                        retries += 1
                        if retries <= args.max_retries:
                            log(f"   ⏳ Retrying in {args.retry_delay}s...")
                            time.sleep(args.retry_delay)

    log(f"\n{'=' * 60}")
    log(f"🌙 NIGHTLY GENERATOR COMPLETE")
    log(f"   Generated: {len(generated_folders)} videos")
    log(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
