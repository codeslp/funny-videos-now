#!/usr/bin/env python3
"""
SCHEDULED PUBLISHER — Run via cron at optimal posting times.
Finds videos that are rendered but not yet published, and publishes
one video to all platforms.

Optimal posting schedule (all times CST):
  - 11:00 AM CST (12 PM EST) — Lunch break engagement peak
  -  2:00 PM CST ( 3 PM EST) — Afternoon scroll peak
  -  6:00 PM CST ( 7 PM EST) — Evening prime time (highest engagement)

Usage: python3 publish_scheduled.py [--dry-run] [--platform youtube,facebook]
"""
import os
import sys
import json
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from script_generator import _load_env
_load_env()

from publisher import (
    upload_to_youtube,
    upload_to_facebook_reels,
    upload_to_tiktok,
    upload_to_instagram_reels,
)

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"publish_{datetime.now().strftime('%Y-%m-%d')}.log")
    with open(log_file, 'a') as f:
        f.write(line + "\n")


def find_next_unpublished():
    """Find the next video that has a final.mp4 but no release_info.json (or not fully published)."""
    if not os.path.exists(OUTPUT_DIR):
        return None

    folders = sorted([
        os.path.join(OUTPUT_DIR, d) for d in os.listdir(OUTPUT_DIR)
        if os.path.isdir(os.path.join(OUTPUT_DIR, d))
    ])

    for folder in folders:
        final_path = os.path.join(folder, 'videos', 'final.mp4')
        release_path = os.path.join(folder, 'release_info.json')
        script_path = os.path.join(folder, 'script.json')

        if not os.path.exists(final_path):
            continue
        if not os.path.exists(script_path):
            continue

        # Check if already published
        if os.path.exists(release_path):
            with open(release_path) as f:
                release = json.load(f)
            platforms = release.get('platforms', {})
            # Consider "published" if at least YouTube is done
            if 'youtube' in platforms:
                continue

        return folder

    return None


def publish_one(folder_path, platforms=None, dry_run=False):
    """Publish a single video folder to specified platforms."""
    script_path = os.path.join(folder_path, 'script.json')
    final_path = os.path.join(folder_path, 'videos', 'final.mp4')

    with open(script_path) as f:
        data = json.load(f)

    headline = data.get('headline', 'Untitled')
    title = f"😂 {headline[:90]}"
    description = (
        f"What REALLY happened? We put you in the room.\n\n"
        f"Original story: {data.get('url', '')}\n"
        f"Source: {data.get('source', '')}\n\n"
        f"#comedy #funny #news #shorts #viral"
    )

    if platforms is None:
        platforms = ['youtube', 'facebook', 'tiktok', 'instagram']

    log(f"📤 Publishing: {headline[:60]}...")
    log(f"   Platforms: {', '.join(platforms)}")

    if dry_run:
        log("   🏃 DRY RUN — skipping actual upload")
        return

    release_info = {
        "headline": headline,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platforms": {}
    }

    if 'youtube' in platforms:
        result = upload_to_youtube(final_path, title, description)
        if result:
            release_info["platforms"]["youtube"] = {
                "status": "published",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    if 'facebook' in platforms:
        result = upload_to_facebook_reels(final_path, title, description)
        if result:
            release_info["platforms"]["facebook"] = {
                "status": "published",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    if 'tiktok' in platforms:
        result = upload_to_tiktok(final_path, title)
        if result:
            release_info["platforms"]["tiktok"] = {
                "status": "published",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    if 'instagram' in platforms:
        result = upload_to_instagram_reels(final_path, title, description)
        if result:
            release_info["platforms"]["instagram"] = {
                "status": "published",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

    # Save release info
    release_path = os.path.join(folder_path, "release_info.json")
    with open(release_path, "w") as f:
        json.dump(release_info, f, indent=2)

    published_count = len(release_info["platforms"])
    log(f"   ✅ Published to {published_count} platform(s)")
    return release_info


def main():
    parser = argparse.ArgumentParser(description='Scheduled video publisher')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be published without uploading')
    parser.add_argument('--platform', type=str, default='youtube,facebook',
                        help='Comma-separated platforms: youtube,facebook,tiktok,instagram')
    parser.add_argument('--all', action='store_true', help='Publish ALL unpublished videos (not just one)')
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platform.split(',')]

    log("=" * 60)
    log("📤 SCHEDULED PUBLISHER STARTING")
    log(f"   Time: {datetime.now().strftime('%I:%M %p CST')}")
    log(f"   Platforms: {', '.join(platforms)}")
    log("=" * 60)

    published = 0
    while True:
        folder = find_next_unpublished()
        if not folder:
            if published == 0:
                log("\n📭 No unpublished videos found. Generate more with generate_overnight.py")
            break

        log(f"\n📁 Found: {os.path.basename(folder)}")
        publish_one(folder, platforms=platforms, dry_run=args.dry_run)
        published += 1

        if not args.all:
            break

    log(f"\n{'=' * 60}")
    log(f"📤 PUBLISHER COMPLETE — {published} video(s) handled")
    log(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
