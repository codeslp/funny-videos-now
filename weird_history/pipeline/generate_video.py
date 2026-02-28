import os
import requests
import time

try:
    from config import ROOT_DIR
    import dotenv
    dotenv.load_dotenv(os.path.join(ROOT_DIR, '.env'))
except ImportError:
    from .config import ROOT_DIR

# Using fal.ai for access to video generation models (like Minimax, Kling, or specific Flow TV endpoints if available).
# Adjust the endpoint URL based on the exact Flow TV API documentation. 
FAL_KEY = os.getenv("FAL_KEY")

def generate_video_clip(prompt: str, output_filepath: str, duration: int = 5) -> str:
    """
    Generates a 1080x1920 portrait video clip using AI video models.
    """
    if not FAL_KEY:
        raise ValueError("FAL_KEY is not set in environment variables.")

    print(f"Generating Video for prompt: '{prompt[:50]}...'")
    
    # Placeholder endpoint for the best matching Video generation API available via FAL
    url = "https://queue.fal.run/fal-ai/minimax-video" 
    
    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "video_size": "portrait_16_9", 
    }

    start_resp = requests.post(url, headers=headers, json=payload)
    if start_resp.status_code != 200:
        raise RuntimeError(f"Video API Error: {start_resp.status_code}\n{start_resp.text}")
        
    request_id = start_resp.json().get('request_id')
    status_url = f"https://queue.fal.run/fal-ai/minimax-video/requests/{request_id}"
    
    while True:
        status_resp = requests.get(status_url, headers={"Authorization": f"Key {FAL_KEY}"})
        status_data = status_resp.json()
        
        status = status_data.get('status')
        if status == "COMPLETED":
            video_url = status_data.get('video', {}).get('url')
            break
        elif status == "FAILED":
            raise RuntimeError(f"Video Generation Failed: {status_data}")
            
        print("Waiting for video rendering (this takes a while)...")
        time.sleep(5)
        
    print(f"Downloading video from {video_url}")
    vid_resp = requests.get(video_url)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, 'wb') as f:
        f.write(vid_resp.content)
        
    print(f"Successfully saved video to: {output_filepath}")
    return os.path.abspath(output_filepath)
