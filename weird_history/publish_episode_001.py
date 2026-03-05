import os
import sys
import json
from datetime import datetime

# Add the src folder and weird_history to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
try:
    from publisher import upload_to_youtube, upload_to_tiktok, upload_to_facebook_reels, upload_to_instagram_reels
    from set_thumbnail import set_youtube_thumbnail
except ImportError:
    pass

def main():
    final_video_path = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/future_history/episodes/episode_001/full_episode.mp4"
    thumbnail_path = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/future_history/episodes/episode_001/thumbnail_1.jpeg"
    build_dir = os.path.dirname(final_video_path)
    
    with open(os.path.join(build_dir, "description.txt"), "r") as f:
        desc_content = f.read()
    
    # Extract title and description
    # We will use TITLE IDEA 1 from the description file
    title = "Life After AI: AI Priests & The Pet Awakening"
    
    # Split description after DESCRIPTION:
    parts = desc_content.split("DESCRIPTION:\n")
    if len(parts) > 1:
        description = parts[1].strip()
    else:
        description = desc_content

    print(f"Publishing {final_video_path}...")
    print(f"Title: {title}")
    
    release_info = {
        "title": title,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platforms": {}
    }

    # YouTube Shorts / YouTube Video
    try:
        video_id = upload_to_youtube(final_video_path, title, description)
        if video_id:
            release_info["platforms"]["youtube"] = {"status": "Published", "video_id": video_id}
            # Set thumbnail
            if os.path.exists(thumbnail_path):
                print(f"Setting thumbnail for video {video_id}...")
                set_youtube_thumbnail(video_id, thumbnail_path)
            else:
                print(f"⚠️ Thumbnail not found at {thumbnail_path}, skipping")
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
