import os
import requests
import json
import time

# Attempt to load API key
try:
    from config import ROOT_DIR
    import dotenv
    dotenv.load_dotenv(os.path.join(ROOT_DIR, '.env'))
except ImportError:
    from .config import ROOT_DIR
    
# Assuming we use a standard Flow TV/Flow endpoint or similar. 
# We'll use fal.ai since it's the standard host for Black Forest Labs' Flux/Flow models.
FAL_KEY = os.getenv("FAL_KEY")

def generate_still(prompt: str, output_filepath: str) -> str:
    """
    Generates a 1080x1920 portrait still using Flow (Flux 1.1 Pro or similar via fal.ai).
    """
    if not FAL_KEY:
        raise ValueError("FAL_KEY is not set in environment variables.")

    print(f"Generating Flow still for prompt: '{prompt[:50]}...'")
    
    url = "https://queue.fal.run/fal-ai/flux-pro/v1.1" # Fal's flux-1.1 endpoint
    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "image_size": "portrait_16_9", # 1080x1920 equivalent
        "num_inference_steps": 30,
        "guidance_scale": 3.5,
        "output_format": "jpeg"
    }

    # Start generation
    start_resp = requests.post(url, headers=headers, json=payload)
    if start_resp.status_code != 200:
        raise RuntimeError(f"Flow API Error: {start_resp.status_code}\n{start_resp.text}")
        
    request_id = start_resp.json().get('request_id')
    status_url = f"https://queue.fal.run/fal-ai/flux-pro/v1.1/requests/{request_id}"
    
    # Poll for completion
    while True:
        status_resp = requests.get(status_url, headers={"Authorization": f"Key {FAL_KEY}"})
        status_data = status_resp.json()
        
        status = status_data.get('status')
        if status == "COMPLETED":
            image_url = status_data.get('images', [])[0].get('url')
            break
        elif status == "FAILED":
            raise RuntimeError(f"Flow Generation Failed: {status_data}")
            
        print("Waiting for Flow still...")
        time.sleep(2)
        
    print(f"Downloading still from {image_url}")
    img_resp = requests.get(image_url)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, 'wb') as f:
        f.write(img_resp.content)
        
    print(f"Successfully saved still to: {output_filepath}")
    return os.path.abspath(output_filepath)
