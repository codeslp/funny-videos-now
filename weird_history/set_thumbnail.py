import os
import sys
import json
import urllib.request
import urllib.parse
import ssl
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
try:
    from script_generator import _load_env
    _load_env()
except Exception:
    pass

def set_youtube_thumbnail(video_id, image_path):
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("❌ Missing YouTube credentials in .env")
        return False

    # 1. Refresh token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode()

    context = ssl._create_unverified_context()
    try:
        req = urllib.request.Request(token_url, data=token_data, method='POST')
        with urllib.request.urlopen(req, context=context) as resp:
            token_response = json.loads(resp.read().decode())
            access_token = token_response['access_token']
    except Exception as e:
        print(f"❌ Token refresh failed: {e}")
        return False

    # 2. Upload thumbnail
    upload_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Determine content type
    ext = image_path.lower().split('.')[-1]
    content_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"

    req = urllib.request.Request(
        upload_url,
        data=image_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': content_type
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, context=context) as resp:
            result = json.loads(resp.read().decode())
            print(f"✅ Thumbnail updated successfully for video {video_id}!")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_id", help="YouTube Video ID")
    parser.add_argument("image_path", help="Path to the thumbnail image")
    args = parser.parse_args()
    
    set_youtube_thumbnail(args.video_id, args.image_path)
