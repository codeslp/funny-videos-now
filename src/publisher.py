"""
Multi-Platform Publisher
Publishes rendered videos from output/*/videos/ to YouTube Shorts,
TikTok, Facebook Reels, and Instagram Reels.

Each platform requires its own API credentials configured in .env.
This module handles:
  1. Assembling scene clips into a single final video (via ffmpeg)
  2. Uploading to YouTube Shorts via YouTube Data API v3
  3. Uploading to TikTok via Content Posting API
  4. Uploading to Facebook Reels via Graph API
  5. Uploading to Instagram Reels via Instagram Graph API
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.parse
import ssl

sys.path.insert(0, os.path.dirname(__file__))
from script_generator import _load_env

_load_env()


# ─── VIDEO ASSEMBLY ──────────────────────────────────────────────

def assemble_video(video_folder):
    """
    Uses ffmpeg to concatenate scene clips into a single final.mp4.
    Returns the path to the assembled video, or None on failure.
    """
    clips = sorted([
        f for f in os.listdir(video_folder)
        if f.startswith("scene_") and f.endswith(".mp4")
    ])

    if not clips:
        print(f"    ⚠️  No scene clips found in {video_folder}")
        return None

    # Create ffmpeg concat file
    concat_path = os.path.join(video_folder, "concat_list.txt")
    with open(concat_path, "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    output_path = os.path.join(video_folder, "final.mp4")

    try:
        result = subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_path,
            "-c", "copy",
            output_path
        ], capture_output=True, text=True, cwd=video_folder)

        if result.returncode != 0:
            print(f"    ❌ ffmpeg error: {result.stderr[:200]}")
            return None

        # Clean up concat list
        os.remove(concat_path)
        print(f"    ✅ Assembled: {output_path}")
        return output_path

    except FileNotFoundError:
        print("    ❌ ffmpeg not found. Install it: brew install ffmpeg")
        return None


# ─── YOUTUBE SHORTS ───────────────────────────────────────────────

def upload_to_youtube(video_path, title, description):
    """
    Upload a video to YouTube Shorts via the YouTube Data API v3.

    Required .env variables:
      YOUTUBE_CLIENT_ID
      YOUTUBE_CLIENT_SECRET
      YOUTUBE_REFRESH_TOKEN

    First-time setup:
      1. Go to console.cloud.google.com
      2. Enable YouTube Data API v3
      3. Create OAuth 2.0 credentials (Desktop app)
      4. Run the OAuth flow once to get a refresh token
      5. Add all three to your .env file
    """
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("    ⏭️  YouTube: Skipping (credentials not configured in .env)")
        return False

    # Refresh the access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode()

    try:

        req = urllib.request.Request(token_url, data=token_data, method='POST')
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as resp:
            token_response = json.loads(resp.read().decode())
            access_token = token_response['access_token']
    except Exception as e:
        print(f"    ❌ YouTube: Token refresh failed: {e}")
        return False

    # Upload via resumable upload
    # Step 1: Initiate upload
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": ["comedy", "funny", "news", "shorts"],
            "categoryId": "23"  # Comedy
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
            "madeForKids": False
        }
    }

    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    init_data = json.dumps(metadata).encode()
    init_req = urllib.request.Request(
        init_url,
        data=init_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Upload-Content-Type': 'video/mp4'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(init_req, context=context) as resp:
            upload_url = resp.headers.get('Location')
    except Exception as e:
        print(f"    ❌ YouTube: Upload initiation failed: {e}")
        return False

    # Step 2: Upload the video file
    with open(video_path, 'rb') as f:
        video_data = f.read()

    upload_req = urllib.request.Request(
        upload_url,
        data=video_data,
        headers={'Content-Type': 'video/mp4'},
        method='PUT'
    )

    try:
        with urllib.request.urlopen(upload_req, context=context) as resp:
            result = json.loads(resp.read().decode())
            video_id = result.get('id', 'unknown')
            print(f"    ✅ YouTube: Uploaded! https://youtube.com/shorts/{video_id}")
            return True
    except Exception as e:
        print(f"    ❌ YouTube: Upload failed: {e}")
        return False


# ─── TIKTOK ──────────────────────────────────────────────────────

def upload_to_tiktok(video_path, title):
    """
    Upload a video to TikTok via the Content Posting API.

    Required .env variables:
      TIKTOK_ACCESS_TOKEN

    First-time setup:
      1. Register at developers.tiktok.com
      2. Create an app with Content Posting API access
      3. Complete OAuth flow to get an access token
      4. Add TIKTOK_ACCESS_TOKEN to .env
    """
    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        print("    ⏭️  TikTok: Skipping (TIKTOK_ACCESS_TOKEN not in .env)")
        return False

    context = ssl._create_unverified_context()
    file_size = os.path.getsize(video_path)

    # Step 1: Initialize upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    init_payload = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": file_size,
            "total_chunk_count": 1
        }
    }

    init_data = json.dumps(init_payload).encode()
    init_req = urllib.request.Request(
        init_url,
        data=init_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(init_req, context=context) as resp:
            result = json.loads(resp.read().decode())
            upload_url = result['data']['upload_url']
            publish_id = result['data']['publish_id']
    except Exception as e:
        print(f"    ❌ TikTok: Init failed: {e}")
        return False

    # Step 2: Upload video
    with open(video_path, 'rb') as f:
        video_data = f.read()

    upload_req = urllib.request.Request(
        upload_url,
        data=video_data,
        headers={
            'Content-Type': 'video/mp4',
            'Content-Range': f'bytes 0-{file_size - 1}/{file_size}'
        },
        method='PUT'
    )

    try:
        with urllib.request.urlopen(upload_req, context=context) as resp:
            print(f"    ✅ TikTok: Uploaded! (publish_id: {publish_id})")
            return True
    except Exception as e:
        print(f"    ❌ TikTok: Upload failed: {e}")
        return False


# ─── FACEBOOK / INSTAGRAM REELS ──────────────────────────────────

def upload_to_facebook_reels(video_path, title, description):
    """
    Upload a video to Facebook Reels via the Graph API.

    Required .env variables:
      FACEBOOK_PAGE_ID
      FACEBOOK_ACCESS_TOKEN

    First-time setup:
      1. Create a Meta Business account
      2. Create a Facebook Page
      3. Set up a Meta App with pages_manage_posts permission
      4. Generate a Page Access Token
      5. Add both to .env
    """
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not all([page_id, access_token]):
        print("    ⏭️  Facebook: Skipping (credentials not in .env)")
        return False

    context = ssl._create_unverified_context()
    file_size = os.path.getsize(video_path)

    # Step 1: Initialize Reels upload
    init_url = f"https://graph.facebook.com/v25.0/{page_id}/video_reels"
    init_payload = urllib.parse.urlencode({
        "upload_phase": "start",
        "access_token": access_token
    }).encode()

    try:
        init_req = urllib.request.Request(init_url, data=init_payload, method='POST')
        with urllib.request.urlopen(init_req, context=context) as resp:
            result = json.loads(resp.read().decode())
            video_id = result['video_id']
            upload_url = result.get('upload_url')
    except Exception as e:
        print(f"    ❌ Facebook: Init failed: {e}")
        if hasattr(e, 'read'):
            print(f"       Detail: {e.read().decode()[:300]}")
        return False

    # Step 2: Upload video binary
    with open(video_path, 'rb') as f:
        video_data = f.read()

    # Use the upload_url if provided, otherwise use the standard endpoint
    if not upload_url:
        upload_url = f"https://rupload.facebook.com/video-upload/v25.0/{video_id}"

    upload_req = urllib.request.Request(
        upload_url,
        data=video_data,
        headers={
            'Authorization': f'OAuth {access_token}',
            'Content-Type': 'application/octet-stream',
            'offset': '0',
            'file_size': str(file_size)
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(upload_req, context=context) as resp:
            upload_result = json.loads(resp.read().decode())
            if not upload_result.get('success', True):
                print(f"    ❌ Facebook: Upload returned failure: {upload_result}")
                return False
    except Exception as e:
        print(f"    ❌ Facebook: Upload failed: {e}")
        if hasattr(e, 'read'):
            print(f"       Detail: {e.read().decode()[:300]}")
        return False

    # Step 3: Publish
    publish_url = f"https://graph.facebook.com/v25.0/{page_id}/video_reels"
    publish_payload = urllib.parse.urlencode({
        "upload_phase": "finish",
        "video_id": video_id,
        "title": title[:100],
        "description": description[:1000],
        "access_token": access_token
    }).encode()

    try:
        pub_req = urllib.request.Request(publish_url, data=publish_payload, method='POST')
        with urllib.request.urlopen(pub_req, context=context) as resp:
            result = json.loads(resp.read().decode())
            print(f"    ✅ Facebook Reels: Published! (video_id: {video_id})")
            return True
    except Exception as e:
        print(f"    ❌ Facebook: Publish failed: {e}")
        if hasattr(e, 'read'):
            print(f"       Detail: {e.read().decode()[:300]}")
        return False


# ─── INSTAGRAM REELS ─────────────────────────────────────────────

def upload_to_instagram_reels(video_path, title, description):
    """
    Upload a video to Instagram Reels via the Instagram Graph API.

    Required .env variables:
      INSTAGRAM_ACCOUNT_ID  (your Instagram Business/Creator account ID)
      FACEBOOK_ACCESS_TOKEN (same token — Meta uses one token for both)

    To find your Instagram Account ID:
      1. In Graph API Explorer, query: GET /me/accounts
      2. Find your Page, then query: GET /{page_id}?fields=instagram_business_account
      3. The 'id' inside instagram_business_account is your INSTAGRAM_ACCOUNT_ID
    """
    ig_account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not all([ig_account_id, access_token]):
        print("    ⏭️  Instagram: Skipping (INSTAGRAM_ACCOUNT_ID not in .env)")
        return False

    context = ssl._create_unverified_context()


    # Instagram Reels require a publicly accessible video URL.
    # For local files, we need to host temporarily or upload directly.
    # The Graph API supports container-based publishing:

    # Step 1: Create a media container
    container_url = f"https://graph.facebook.com/v18.0/{ig_account_id}/media"

    # For Reels, the video needs to be accessible via URL.
    # We'll upload to Facebook first, then cross-post, OR use a direct upload.
    # Using the direct video upload approach:
    file_size = os.path.getsize(video_path)

    # Initialize resumable upload
    init_data = urllib.parse.urlencode({
        "media_type": "REELS",
        "caption": f"{title}\n\n{description}"[:2200],
        "share_to_feed": "true",
        "access_token": access_token,
        "upload_type": "resumable",
        "video_file_size": file_size
    }).encode()

    try:
        init_req = urllib.request.Request(container_url, data=init_data, method='POST')
        with urllib.request.urlopen(init_req, context=context) as resp:
            result = json.loads(resp.read().decode())
            container_id = result.get('id')
            upload_uri = resp.headers.get('Location') or result.get('uri')
    except Exception as e:
        print(f"    ❌ Instagram: Container creation failed: {e}")
        return False

    # Step 2: Upload the video file
    if upload_uri:
        with open(video_path, 'rb') as f:
            video_data = f.read()

        upload_req = urllib.request.Request(
            upload_uri,
            data=video_data,
            headers={
                'Authorization': f'OAuth {access_token}',
                'Content-Type': 'video/mp4'
            },
            method='POST'
        )

        try:
            with urllib.request.urlopen(upload_req, context=context) as resp:
                pass
        except Exception as e:
            print(f"    ❌ Instagram: Video upload failed: {e}")
            return False

    # Step 3: Wait for processing, then publish
    import time
    for attempt in range(30):  # Wait up to 5 minutes
        status_url = f"https://graph.facebook.com/v18.0/{container_id}?fields=status_code&access_token={access_token}"
        try:
            status_req = urllib.request.Request(status_url)
            with urllib.request.urlopen(status_req, context=context) as resp:
                status = json.loads(resp.read().decode())
                if status.get('status_code') == 'FINISHED':
                    break
                elif status.get('status_code') == 'ERROR':
                    print(f"    ❌ Instagram: Processing error: {status}")
                    return False
        except Exception:
            pass
        time.sleep(10)

    # Step 4: Publish the container
    publish_url = f"https://graph.facebook.com/v18.0/{ig_account_id}/media_publish"
    publish_data = urllib.parse.urlencode({
        "creation_id": container_id,
        "access_token": access_token
    }).encode()

    try:
        pub_req = urllib.request.Request(publish_url, data=publish_data, method='POST')
        with urllib.request.urlopen(pub_req, context=context) as resp:
            result = json.loads(resp.read().decode())
            media_id = result.get('id', 'unknown')
            print(f"    ✅ Instagram Reels: Published! (media_id: {media_id})")
            return True
    except Exception as e:
        print(f"    ❌ Instagram: Publish failed: {e}")
        return False


# ─── MAIN PIPELINE ───────────────────────────────────────────────

def publish_video_folder(folder_path):
    """Assemble and publish a single video folder to all platforms."""
    script_path = os.path.join(folder_path, "script.json")
    if not os.path.exists(script_path):
        return

    with open(script_path) as f:
        data = json.load(f)

    headline = data.get('headline', 'Untitled')
    source = data.get('source', '')
    title = f"😂 {headline[:90]}"
    description = (
        f"What REALLY happened? We put you in the room.\n\n"
        f"Original story: {data.get('url', '')}\n"
        f"Source: {source}\n\n"
        f"#comedy #funny #news #shorts #viral"
    )

    videos_dir = os.path.join(folder_path, "videos")
    
    # Use Remotion assembled video if available
    remotion_path = os.path.join(videos_dir, "final_assembled.mp4")
    if os.path.exists(remotion_path):
        final_path = remotion_path
    else:
        final_path = os.path.join(videos_dir, "final.mp4")
        # Assemble with ffmpeg if not already done
        if not os.path.exists(final_path):
            final_path = assemble_video(videos_dir)
            if not final_path:
                return

    # Manual Approval Gate
    approved_file = os.path.join(folder_path, ".approved")
    if not os.path.exists(approved_file):
        print(f"    ⚠️  Skipping publish: Manual review required. Create an empty '.approved' file in this folder to authorize publishing.")
        return

    print(f"    📤 Publishing to all platforms...")
    from datetime import datetime
    release_info = {
        "headline": headline,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platforms": {}
    }

    # YouTube
    yt_result = upload_to_youtube(final_path, title, description)
    if yt_result:
        release_info["platforms"]["youtube"] = {"status": "published", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # TikTok
    tt_result = upload_to_tiktok(final_path, title)
    if tt_result:
        release_info["platforms"]["tiktok"] = {"status": "published", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # Facebook
    fb_result = upload_to_facebook_reels(final_path, title, description)
    if fb_result:
        release_info["platforms"]["facebook"] = {"status": "published", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # Instagram
    ig_result = upload_to_instagram_reels(final_path, title, description)
    if ig_result:
        release_info["platforms"]["instagram"] = {"status": "published", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # Save release info to folder
    release_path = os.path.join(folder_path, "release_info.json")
    with open(release_path, "w") as f:
        json.dump(release_info, f, indent=2)
    print(f"    📋 Release info saved to {release_path}")


def main():
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_dir):
        print("❌ No output/ directory found. Run main.py first.")
        return

    folders = sorted([
        os.path.join(output_dir, d) for d in os.listdir(output_dir)
        if os.path.isdir(os.path.join(output_dir, d))
    ])

    print("\n" + "=" * 60)
    print("  📤  MULTI-PLATFORM PUBLISHER  📤")
    print(f"  🎯  Platforms: YouTube Shorts, TikTok, Facebook Reels")
    print(f"  📁  Videos to publish: {len(folders)}")
    print("=" * 60)

    # Show credential status
    print("\n  📋 Credential Status:")
    yt = all([os.getenv(k) for k in ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"]])
    tt = bool(os.getenv("TIKTOK_ACCESS_TOKEN"))
    fb = all([os.getenv(k) for k in ["FACEBOOK_PAGE_ID", "FACEBOOK_ACCESS_TOKEN"]])
    ig = all([os.getenv(k) for k in ["INSTAGRAM_ACCOUNT_ID", "FACEBOOK_ACCESS_TOKEN"]])
    print(f"    YouTube:   {'✅ Ready' if yt else '⏭️  Not configured'}")
    print(f"    TikTok:    {'✅ Ready' if tt else '⏭️  Not configured'}")
    print(f"    Facebook:  {'✅ Ready' if fb else '⏭️  Not configured'}")
    print(f"    Instagram: {'✅ Ready' if ig else '⏭️  Not configured'}")
    for folder in folders:
        folder_name = os.path.basename(folder)
        print(f"\n{'─' * 60}")
        print(f"📁 {folder_name}")
        publish_video_folder(folder)

    print(f"\n{'=' * 60}")
    print(f"  ✅ PUBLISHING COMPLETE")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
