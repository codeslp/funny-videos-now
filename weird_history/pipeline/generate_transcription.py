import os
import json
import subprocess

def generate_word_timestamps(audio_filepath: str, output_filepath: str = None) -> list[dict]:
    """
    Transcribes audio using WhisperX to get millisecond-accurate word-level timestamps.
    Returns a list of dictionaries containing 'word', 'start', and 'end' keys.
    """
    if not os.path.exists(audio_filepath):
        raise FileNotFoundError(f"Audio file not found: {audio_filepath}")

    print(f"Running WhisperX for transcription and forced alignment on: {audio_filepath}")
    
    # We will invoke WhisperX via command line. This assumes whisperx is installed globally.
    # whisperx --model base.en --output_format json --language en --align_model WAV2VEC2_ASR_BASE_960H <audio_file>
    
    output_dir = os.path.dirname(audio_filepath)
    if output_filepath is None:
        basename = os.path.splitext(os.path.basename(audio_filepath))[0]
        output_filepath = os.path.join(output_dir, f"{basename}.json")

    cmd = [
        "whisperx",
        audio_filepath,
        "--model", "base.en",
        "--output_dir", output_dir,
        "--output_format", "json",
        "--language", "en",
        "--compute_type", "int8", # int8 for faster execution on macs (CPU/MPS)
    ]
    
    try:
        # Run WhisperX subprocess
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"WhisperX Error:\n{e.stderr.decode('utf-8')}")
        raise RuntimeError("Failed to run WhisperX.")
        
    # Read the output JSON
    basename = os.path.splitext(os.path.basename(audio_filepath))[0]
    generated_json = os.path.join(output_dir, f"{basename}.json")
    
    with open(generated_json, 'r') as f:
        data = json.load(f)
        
    # Extract word timestamps
    words = []
    for segment in data.get('segments', []):
        for word in segment.get('words', []):
            if 'start' in word and 'end' in word:
                words.append({
                    "word": word.get("word").strip(),
                    "start": word.get("start"),
                    "end": word.get("end")
                })
                
    if output_filepath != generated_json:
        with open(output_filepath, 'w') as f:
            json.dump(words, f, indent=4)
            
    print(f"Generated {len(words)} word timestamps.")
    return words

if __name__ == "__main__":
    # For testing, you must have whisperx installed.
    # pip install git+https://github.com/m-bain/whisperx.git
    pass
