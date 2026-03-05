import os
import json
import requests
import subprocess
try:
    from config import ROOT_DIR
except ImportError:
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

from dotenv import load_dotenv
env_path = os.path.join(ROOT_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# voice guide:
# good default feminine voice: dAlhI9qAHVIjXuVppzhW
# southern man: Bj9UqZbhQsanLzgalpEG
# v. deep male (maybe interstitial?): qNkzaJoHLLdpvgh5tISm
# Ashley — warm & energetic go-to female (American): bxiObU1YDrf7lrFAyV99
# Freya — silly airhead female (American): jsCqWAovK2LkecY7zXl4



def generate_tts(text: str, output_filepath: str, voice_id: str = "dAlhI9qAHVIjXuVppzhW",
                 language: str = "en", **kwargs) -> str:
    """
    Generates text-to-speech audio using the ElevenLabs API and saves it to a WAV file.
    
    Args:
        text: The script text to convert to speech.
        output_filepath: Where to save the output .wav file.
        voice_id: The ElevenLabs voice ID to use.
        language: Language code (e.g., "en", "es").
    
    Returns:
        Absolute path to the generated audio file.
    """
    if not ELEVENLABS_API_KEY:
        print("WARNING: ELEVENLABS_API_KEY not set. Falling back to Edge-TTS.")
        fallback_voice = kwargs.get("fallback_voice", "en-GB-ThomasNeural")
        return generate_edge_tts(text, output_filepath, language, fallback_voice=fallback_voice)

    url = f"{ELEVENLABS_API_URL}/{voice_id}"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    print(f"Generating TTS via ElevenLabs for text: '{text[:40]}...'")
    print(f"  Voice ID: {voice_id}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 401:
        print("ElevenLabs API Error: 401 Unauthorized. Check your ELEVENLABS_API_KEY.")
        print("Falling back to Edge-TTS...")
        fallback_voice = kwargs.get("fallback_voice", "en-GB-ThomasNeural")
        return generate_edge_tts(text, output_filepath, language, fallback_voice=fallback_voice)
    elif response.status_code != 200:
        print(f"ElevenLabs API Error: {response.status_code} - {response.text[:300]}")
        print("Falling back to Edge-TTS...")
        fallback_voice = kwargs.get("fallback_voice", "en-GB-ThomasNeural")
        return generate_edge_tts(text, output_filepath, language, fallback_voice=fallback_voice)

    # ElevenLabs returns audio/mpeg directly
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    
    # Save as mp3 first, then convert to wav
    temp_mp3 = output_filepath.replace(".wav", ".temp.mp3")
    with open(temp_mp3, "wb") as f:
        f.write(response.content)
    
    # Convert to WAV for pipeline compatibility
    print("Converting ElevenLabs MP3 to WAV...")
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_mp3, "-ar", "44100", "-ac", "1", output_filepath]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)
    
    print(f"Successfully saved TTS audio to: {output_filepath}")
    return os.path.abspath(output_filepath)


def generate_sound_effect(prompt: str, output_filepath: str, duration: float = 3.0) -> str:
    """
    Generates a sound effect using the ElevenLabs Sound Effects API.
    
    Args:
        prompt: Text description of the desired sound effect.
        output_filepath: Where to save the output .wav file.
        duration: Duration in seconds (0.1-30).
    
    Returns:
        Absolute path to the generated audio file.
    """
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not set. Cannot generate sound effects.")

    url = "https://api.elevenlabs.io/v1/sound-generation"
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": prompt,
        "duration_seconds": duration,
        "prompt_influence": 0.5
    }

    print(f"Generating sound effect via ElevenLabs: '{prompt[:50]}...'")
    print(f"  Duration: {duration}s")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs SFX API Error: {response.status_code} - {response.text[:300]}")

    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    
    # Save as mp3 first, then convert to wav
    temp_mp3 = output_filepath.replace(".wav", ".temp.mp3")
    with open(temp_mp3, "wb") as f:
        f.write(response.content)
    
    # Convert to WAV for pipeline compatibility
    print("Converting SFX MP3 to WAV...")
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_mp3, "-ar", "44100", "-ac", "1", output_filepath]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)
    
    print(f"Successfully saved sound effect to: {output_filepath}")
    return os.path.abspath(output_filepath)


def generate_edge_tts(text: str, output_filepath: str, language: str = "en", fallback_voice: str = None) -> str:
    """Generates text-to-speech audio using edge-tts CLI tool as a free fallback and converts to WAV."""
    temp_mp3 = output_filepath.replace(".wav", ".temp.mp3")
    if fallback_voice:
        voice = fallback_voice
    elif language == "es":
        voice = "es-ES-ElviraNeural"
    else:
        voice = "en-GB-ThomasNeural"  # British male default
    
    cmd = ["/Users/bfaris96/Library/Python/3.9/bin/edge-tts", "--voice", voice, "--text", text, "--write-media", temp_mp3]
    print(f"Generating fallback TTS via Edge-TTS ({voice}) for text: '{text[:30]}...'")
    subprocess.run(cmd, check=True)
    
    print(f"Converting Edge-TTS MP3 to WAV using FFmpeg...")
    ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_mp3, "-ar", "44100", "-ac", "1", output_filepath]
    subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)
        
    print(f"Successfully saved fallback TTS audio to: {output_filepath}")
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
    voice_id = timeline.get("tts_voice_id", "dAlhI9qAHVIjXuVppzhW")
    language = timeline.get("language", "en")
    
    output_filepath = os.path.join(output_dir, "voiceover.wav")
    generate_tts(script_text, output_filepath, voice_id, language)
