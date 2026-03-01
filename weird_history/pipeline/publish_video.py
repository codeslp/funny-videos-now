import os
import sys
import json
import re
from datetime import datetime

# Add the src folder to path to import the publisher functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from publisher import upload_to_youtube, upload_to_tiktok, upload_to_facebook_reels, upload_to_instagram_reels

def update_viral_tracking_doc(topic_name: str, final_video_path: str):
    """
    Finds the video in the viral_tracking.md document and automatically marks it as completed,
    linking the new exported video path in the final column.
    """
    tracking_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'production_guidelines', 'viral_tracking.md'))
    if not os.path.exists(tracking_path):
        print(f"Warning: Viral tracking document not found at {tracking_path}")
        return

    # Extract relative path from funny_video_generator folder
    rel_path = final_video_path
    if 'funny_video_generator/' in final_video_path:
        rel_path = final_video_path.split('funny_video_generator/')[1]

    try:
        with open(tracking_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        updated = False
        for i, line in enumerate(lines):
            if topic_name in line and "| ⏳ Not Built |" in line:
                # Replace status block
                line = line.replace("| ⏳ Not Built |", "| ✅ Completed |")
                # Replace empty file cell with backtick link
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
    build_dir = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/wealthy_cow_dung_trick"
    final_video_path = os.path.join(build_dir, "final_render.mp4")
    tracking_topic = "The Wealthy Cow Dung Trick (East African Tribes)"
    
    if not os.path.exists(final_video_path):
        print(f"Error: Could not find final video at {final_video_path}")
        return

    title = "😂 The Wealthy Cow Dung Trick! | Weird History"
    description = (
        "Midwives in some historical East African tribes had the craziest trick for a difficult labor... cow poop! "
        "Because cattle were the ultimate symbol of extreme wealth, if a baby was refusing to come out, they would take fresh, incredibly smelly cow dung and pack it all around the birthing bed.\n\n"
        "They honestly believed the unborn baby could smell the wealth from inside the womb, and would rush out to be born rich! Talk about being born into money.\n\n"
        "📖 Read the full historical research here: https://cafemom.com/\n\n"
        "#weirdhistory #historyfacts #africanhistory #educationalcomedy #history"
    )

    print(f"Publishing {final_video_path}...")
    
    release_info = {
        "title": title,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platforms": {}
    }

    # YouTube Shorts
    try:
        if upload_to_youtube(final_video_path, title, description):
            release_info["platforms"]["youtube"] = "Published"
    except Exception as e:
        print(f"YouTube upload failed: {e}")

    # TikTok
    try:
        if upload_to_tiktok(final_video_path, title):
            release_info["platforms"]["tiktok"] = "Published"
    except Exception as e:
        print(f"TikTok upload failed: {e}")

    # Facebook Reels
    try:
        if upload_to_facebook_reels(final_video_path, title, description):
            release_info["platforms"]["facebook"] = "Published"
    except Exception as e:
        print(f"Facebook upload failed: {e}")

    # Instagram Reels
    try:
        if upload_to_instagram_reels(final_video_path, title, description):
            release_info["platforms"]["instagram"] = "Published"
    except Exception as e:
        print(f"Instagram upload failed: {e}")

    # Save release log
    release_path = os.path.join(build_dir, "publish_log.json")
    with open(release_path, "w") as f:
        json.dump(release_info, f, indent=4)
        
    print(f"Publishing complete. Log saved to {release_path}")
    
    # Automatically log to the git tracking document
    update_viral_tracking_doc(tracking_topic, final_video_path)

if __name__ == "__main__":
    main()
