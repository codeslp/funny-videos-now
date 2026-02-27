import json
import sys
import os
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from news_sourcing import fetch_all_curated_news
from script_generator import generate_comedic_script

# Pipeline configuration
DAILY_VIDEO_COUNT = 5
VEO_MODE = "Veo 3.1 Fast"
CREDITS_PER_SCENE = 20
SCENES_PER_VIDEO = 4


def format_video_prompts_for_veo3(script, headline, video_number):
    """Format a single script into a clean Veo3 prompt document."""
    output = []
    output.append(f"\n{'=' * 60}")
    output.append(f"🎬  VIDEO #{video_number}")
    output.append(f"{'=' * 60}")
    output.append(f"\n📰 HEADLINE: {headline}")
    output.append(f"📐 ASPECT RATIO: 9:16 Vertical (Phone)")
    output.append(f"⚡ MODE: {VEO_MODE}")
    output.append(f"\n{'-' * 60}")

    for scene in script:
        num = scene.get('scene_number', '?')
        output.append(f"\n🎥 SCENE {num}")
        output.append(f"\n  VISUAL PROMPT FOR VEO3:")
        output.append(f"  {scene.get('veo3_visual_prompt', '')}")
        output.append(f"\n  🎙️ DIALOGUE:")
        output.append(f"  {scene.get('dialogue', '')}")
        output.append(f"\n  🔊 AUDIO:")
        output.append(f"  {scene.get('audio_cues', '')}")
        output.append(f"\n{'-' * 60}")

    return "\n".join(output)


def main():
    print("\n" + "=" * 60)
    print("  🎭  AUTO FUNNY VIDEO PIPELINE — BATCH MODE  🎭")
    print(f"  📊  Target: {DAILY_VIDEO_COUNT} videos | {VEO_MODE} | 9:16 Vertical")
    print("=" * 60)

    credits_needed = DAILY_VIDEO_COUNT * SCENES_PER_VIDEO * CREDITS_PER_SCENE
    print(f"\n💰 Estimated credit usage: {credits_needed} credits")

    # Step 1: Discover news
    print(f"\n📡 Step 1: Discovering absurd news from the last 24 hours...")
    news_items = fetch_all_curated_news()

    if not news_items:
        print("❌ No safe news found. Check your internet connection.")
        return

    print(f"   Found {len(news_items)} safe, scriptable stories.")

    # Step 2: Pick top stories
    selected = news_items[:DAILY_VIDEO_COUNT]
    print(f"\n🎯 Step 2: Selected top {len(selected)} stories:\n")
    for i, item in enumerate(selected, 1):
        print(f"  {i}. [{item['source']}] {item['title']}")

    # Step 3: Generate scripts for all
    print(f"\n✍️  Step 3: Generating {len(selected)} comedy scripts...\n")

    all_scripts = []
    all_formatted = []

    for i, story in enumerate(selected, 1):
        print(f"{'─' * 40}")
        print(f"📝 Script {i}/{len(selected)}: {story['title'][:70]}...")
        script_json = generate_comedic_script(story)
        all_scripts.append({
            "video_number": i,
            "headline": story['title'],
            "source": story.get('source', ''),
            "url": story.get('url', ''),
            "script": script_json
        })
        formatted = format_video_prompts_for_veo3(script_json, story['title'], i)
        all_formatted.append(formatted)
        print(f"   ✅ Done!")

        # Small delay between API calls to be polite
        if i < len(selected):
            time.sleep(1)

    # Step 4: Save all outputs into per-video folders
    print(f"\n📦 Step 4: Saving outputs into organized folders...\n")

    import re
    def slugify(text, max_len=40):
        """Turn a headline into a safe, short folder name."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        words = text.split()[:5]  # first 5 words
        slug = '_'.join(words)
        return slug[:max_len]

    # Save combined text file (quick reference)
    combined_text = "\n".join(all_formatted)
    header = f"""{'=' * 60}
  🎭  DAILY BATCH — {DAILY_VIDEO_COUNT} VIDEOS
  📅  Generated at pipeline runtime
  📐  Aspect Ratio: 9:16 Vertical
  ⚡  Mode: {VEO_MODE}
  💰  Credits: ~{credits_needed}
{'=' * 60}
"""
    with open("latest_veo3_script.txt", "w") as f:
        f.write(header + combined_text)

    with open("latest_script.json", "w") as f:
        json.dump(all_scripts, f, indent=2)

    # Create per-video folders
    for idx, (entry, fmt) in enumerate(zip(all_scripts, all_formatted)):
        num = entry['video_number']
        slug = slugify(entry['headline'])
        folder_name = f"output/{num:02d}_{slug}"

        os.makedirs(f"{folder_name}/videos", exist_ok=True)

        # Save script JSON
        with open(f"{folder_name}/script.json", "w") as f:
            json.dump(entry, f, indent=2)

        # Save human-readable prompts
        with open(f"{folder_name}/prompts.txt", "w") as f:
            f.write(fmt)

        # Save individual scene prompts for easy copy-paste into Veo3
        for scene in entry['script']:
            scene_num = scene.get('scene_number', 0)
            with open(f"{folder_name}/scene_{scene_num:02d}_prompt.txt", "w") as f:
                f.write(scene.get('veo3_visual_prompt', ''))
                f.write(f"\n\nDIALOGUE: {scene.get('dialogue', '')}")

        # Create a README in the video folder
        with open(f"{folder_name}/videos/README.md", "w") as f:
            f.write(f"# {entry['headline']}\n\n")
            f.write(f"Place rendered Veo3 clips here:\n")
            for scene in entry['script']:
                sn = scene.get('scene_number', 0)
                f.write(f"- scene_{sn:02d}.mp4\n")
            f.write(f"\nFinal assembled video:\n- final.mp4\n")

        print(f"  📁 {folder_name}/")

    # Print all scripts to console
    print(f"\n{header}")
    for fmt in all_formatted:
        print(fmt)

    print(f"\n{'=' * 60}")
    print(f"  ✅ BATCH COMPLETE — {len(all_scripts)} scripts generated")
    print(f"  📄 Combined:  latest_veo3_script.txt")
    print(f"  📦 JSON:      latest_script.json")
    print(f"  📁 Per-video: output/01_.../ → output/{len(all_scripts):02d}_.../")
    print(f"     Each folder contains:")
    print(f"       script.json      — Full script data")
    print(f"       prompts.txt      — Formatted Veo3 prompts")
    print(f"       scene_XX_prompt.txt — Individual scene prompts")
    print(f"       videos/          — Drop rendered clips here")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
