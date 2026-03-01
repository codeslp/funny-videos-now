import os
import json
import requests
import subprocess
try:
    from config import CARTESIA_API_KEY, DEFAULT_VOICE_ID
except ImportError:
    from .config import CARTESIA_API_KEY, DEFAULT_VOICE_ID

CARTESIA_API_URL = "https://api.cartesia.ai/tts/bytes"

def generate_edge_tts(text: str, output_filepath: str, language: str = "en") -> str:
    """Generates text-to-speech audio using edge-tts CLI tool as a free fallback and converts to WAV."""
    temp_mp3 = output_filepath.replace(".wav", ".temp.mp3")
    voice = "es-ES-ElviraNeural" if language == "es" else "en-US-AriaNeural"
    
    cmd = ["/Users/bfaris96/Library/Python/3.9/bin/edge-tts", "--voice", voice, "--text", text, "--write-media", temp_mp3]
    print(f"Generating fallback TTS via Edge-TTS for text: '{text[:30]}...'")
    subprocess.run(cmd, check=True)
    
    print(f"Converting Edge-TTS MP3 to WAV using FFmpeg...")
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_mp3, "-ar", "44100", "-ac", "1", output_filepath]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)
        
    print(f"Successfully saved fallback TTS audio to: {output_filepath}")
    return os.path.abspath(output_filepath)

def generate_tts(text: str, output_filepath: str, voice_id: str = DEFAULT_VOICE_ID, language: str = "en") -> str:
    """
    Generates text-to-speech audio using the Cartesia API and saves it to a WAV file.
    
    Args:
        text (str): The script text to convert to speech.
        output_filepath (str): The path where the output .wav file should be saved.
        voice_id (str): The Cartesia voice UUID to use.
        language (str): Language code (e.g., "en", "es").
        
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

    model_id = "sonic-multilingual" if language != "en" else "sonic-english"
    
    payload = {
        "model_id": model_id,
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": voice_id
        },
        "language": language,
        "output_format": {
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100
        }
    }

    print(f"Generating TTS via Cartesia for text: '{text[:30]}...'")
    
    response = requests.post(CARTESIA_API_URL, headers=headers, json=payload)
    
    if response.status_code == 402:
        print("Cartesia API Error: 402 Insufficient credits. Falling back to free Edge-TTS.")
        return generate_edge_tts(text, output_filepath, language)
    elif response.status_code != 200:
        raise RuntimeError(f"Cartesia API Error: {response.status_code} - {response.text}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

    with open(output_filepath, "wb") as f:
        f.write(response.content)

    print(f"Successfully saved TTS audio to: {output_filepath}")
    return os.path.abspath(output_filepath)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python generate_audio.py <timeline_json_path> <output_dir>")
        sys.exit(1)
        
    timeline_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    with open(timeline_path, "r") as f:
        timeline = json.load(f)
        
    script_text = timeline.get("script", "")
    voice_id = timeline.get("tts_voice_id", DEFAULT_VOICE_ID)
    language = timeline.get("language", "en")
    
    output_filepath = os.path.join(output_dir, "voiceover.wav")
    generate_tts(script_text, output_filepath, voice_id, language)
