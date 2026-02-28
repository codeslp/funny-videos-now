import os
from dotenv import load_dotenv

# Go up two directories from weird_history/pipeline to find the root .env file
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
env_path = os.path.join(ROOT_DIR, '.env')

if os.path.exists(env_path):
    load_dotenv(env_path)

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
TWELVELABS_API_KEY = os.getenv("TWELVELABS_API_KEY") # if needed later
# Add flow/flow tv keys when available

# Output Configuration
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output', 'weird_history')
VIDEO_RESOLUTION = (1080, 1920) # Portrait for Shorts/Reels/TikTok
FPS = 30

# Default Voices (Cartesia UUIDs)
DEFAULT_VOICE_ID = "1f575487-6f3d-40e0-862a-814f55b5fb15"  # Ariane - Captivating Tone
