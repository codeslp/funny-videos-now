import os
import sys
import json
from datetime import datetime
import shutil

sys.path.insert(0, os.path.abspath('src'))
from publisher import upload_to_youtube, upload_to_tiktok, upload_to_facebook_reels, upload_to_instagram_reels
from config import PUBLISHED_DIR

def update_viral_tracking_doc(topic_name: str, final_video_path: str):
    tracking_path = os.path.abspath('weird_history/production_guidelines/viral_tracking.md')
    if not os.path.exists(tracking_path):
        print(f"Warning: Viral tracking document not found at {tracking_path}")
        return

    rel_path = final_video_path
    if 'funny_video_generator/' in final_video_path:
        rel_path = final_video_path.split('funny_video_generator/')[1]

    try:
        with open(tracking_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        updated = False
        for i, line in enumerate(lines):
            if topic_name in line and "| ⏳ Not Built |" in line:
                line = line.replace("| ⏳ Not Built |", "| ✅ Completed |")
                if line.strip().endswith("| - |"):
                    line = line.rstrip()[:-5] + f"| `{rel_path}` |\n"
                lines[i] = line
                updated = True
                break

        if updated:
            with open(tracking_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"Updated viral_tracking.md status to Completed for: {topic_name}")
        else:
            print(f"Notice: '{topic_name}' was not found as 'Not Built' in viral_tracking.md")
    except Exception as e:
        print(f"Failed to update viral tracking doc: {e}")

def main():
    build_dir = "output/weird_history/ready_to_publish/en_secret_code_fake_moles_2026-03-03"
    final_video_path = os.path.join(build_dir, "final_render.mp4")
    tracking_topic = "Secret Code of Fake Moles (17th Century France)"
    
    if not os.path.exists(final_video_path):
        print(f"Error: Could not find final video at {final_video_path}")
        return

    title = "😂 Tinder in 1600s France? Fake Moles! | Weird History"
    description = (
        "In 17th century France, you didn't just tell someone you were single. You stuck a tiny piece of black velvet on your face! \n\n"
        "French aristocrats used fake beauty marks called mouches, and each placement was a secret code. Near the mouth? I want to kiss you. On the cheek? I'm taken, back off. Some people even wore six at once to scream 'I'm available!' \n\n"
        "Would you use this 1600s Tinder method today? Let us know in the comments! \n\n"
        "�� Read the full historical research here: https://en.wikipedia.org/wiki/Beauty_mark \n\n"
        "#weirdhistory #historyfacts #ancientfrance #educationalcomedy #history"
    )

    print(f"Publishing {final_video_path}...")
    
    release_info = {
        "title": title,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platforms": {}
    }

    try:
        if upload_to_youtube(final_video_path, title, description):
            release_info["platforms"]["youtube"] = "Published"
    except Exception as e:
        print(f"YouTube upload failed: {e}")

    try:
        if upload_to_tiktok(final_video_path, title):
            release_info["platforms"]["tiktok"] = "Published"
    except Exception as e:
        print(f"TikTok upload failed: {e}")

    try:
        if upload_to_facebook_reels(final_video_path, title, description):
            release_info["platforms"]["facebook"] = "Published"
    except Exception as e:
        print(f"Facebook upload failed: {e}")

    try:
        if upload_to_instagram_reels(final_video_path, title, description):
            release_info["platforms"]["instagram"] = "Published"
    except Exception as e:
        print(f"Instagram upload failed: {e}")

    release_path = os.path.join(build_dir, "publish_log.json")
    with open(release_path, "w") as f:
        json.dump(release_info, f, indent=4)
        
    print(f"Publishing complete. Log saved to {release_path}")
    update_viral_tracking_doc(tracking_topic, final_video_path)

    try:
        final_published_dir = os.path.join(PUBLISHED_DIR, os.path.basename(build_dir))
        shutil.move(build_dir, final_published_dir)
        print(f"Archived video folder to {final_published_dir}")
    except Exception as e:
        print(f"Error archiving folder to published directory: {e}")

if __name__ == "__main__":
    main()
