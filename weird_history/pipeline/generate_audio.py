import os
import json
import requests
try:
    from config import CARTESIA_API_KEY, DEFAULT_VOICE_ID
except ImportError:
    from .config import CARTESIA_API_KEY, DEFAULT_VOICE_ID

CARTESIA_API_URL = "https://api.cartesia.ai/tts/bytes"

def generate_tts(text: str, output_filepath: str, voice_id: str = DEFAULT_VOICE_ID) -> str:
    """
    Generates text-to-speech audio using the Cartesia API and saves it to a WAV file.
    
    Args:
        text (str): The script text to convert to speech.
        output_filepath (str): The path where the output .wav file should be saved.
        voice_id (str): The Cartesia voice UUID to use.
        
    Returns:
        str: The absolute path to the generated audio file.
    """
    if not CARTESIA_API_KEY:
        raise ValueError("CARTESIA_API_KEY is not set in the environment variables.")

    headers = {
        "Cartesia-Version": "2024-06-10",
        "X-API-Key": CARTESIA_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "sonic-english",
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": voice_id
        },
        "output_format": {
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100
        }
    }

    print(f"Generating TTS via Cartesia for text: '{text[:30]}...'")
    
    response = requests.post(CARTESIA_API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise RuntimeError(f"Cartesia API Error: {response.status_code} - {response.text}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

    with open(output_filepath, "wb") as f:
        f.write(response.content)

    print(f"Successfully saved TTS audio to: {output_filepath}")
    return os.path.abspath(output_filepath)

if __name__ == "__main__":
    # Simple test execution if run directly
    test_text = "This is a test of the Cartesia text to speech API. It should be incredibly fast and expressive."
    testing_output = os.path.join(os.path.dirname(__file__), 'test_audio.wav')
    generate_tts(test_text, testing_output)
