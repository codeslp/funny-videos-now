import os
import sys
import json
from datetime import datetime

# Add the src folder to path to import the publisher functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from publisher import upload_to_youtube, upload_to_tiktok, upload_to_facebook_reels, upload_to_instagram_reels

def main():
    build_dir = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/sleeping_with_moldy_cake_hyperrealism"
    final_video_path = os.path.join(build_dir, "final_render.mp4")
    
    if not os.path.exists(final_video_path):
        print(f"Error: Could not find final video at {final_video_path}")
        return

    title = "😂 Sleeping with a Wedding Cake? | Weird History"
    description = (
        "Victorian women used to sleep with moldy frosting-covered wedding cake under their pillows to dream about their future husbands!\n\n"
        "If you don't believe me, read the actual research behind this bizarre historical tradition.\n\n"
        "📖 Read the full historical research here: https://en.wikipedia.org/wiki/Wedding_cake#Superstitions\n\n"
        "#weirdhistory #historyfacts #victorianera #educationalcomedy #history"
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

if __name__ == "__main__":
    main()
