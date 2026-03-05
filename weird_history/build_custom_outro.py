import os
import subprocess
import sys
import json
from pipeline.generate_audio import generate_tts

def get_duration(filepath: str) -> float:
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', filepath],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data['format']['duration'])

OUTPUT_DIR = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output"
OUTRO_DIR = f"{OUTPUT_DIR}/future_history/intro_outro"
os.makedirs(OUTRO_DIR, exist_ok=True)

VO_TEXT = "Could this be the future? Read our research in the description. Subscribe for more news from outside your timeline."
VO_VOICE_ID = "PIGsltMj3gFMR34aFDI3"
VO_PATH = f"{OUTRO_DIR}/episode_outro_voice.wav"

VIDEO_PATH = "/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/future_history/episodes/outro/outro_field_video.mp4"
MUSIC_PATH = f"{OUTPUT_DIR}/future_history/music_assets/serene_episode_music.mp3"
FINAL_OUTRO_PATH = f"{OUTRO_DIR}/custom_episode_outro.mp4"

def build_outro():
    print("Generating VO...")
    generate_tts(
        text=VO_TEXT,
        output_filepath=VO_PATH,
        voice_id=VO_VOICE_ID
    )

    vo_dur = get_duration(VO_PATH)
    print(f"VO Duration: {vo_dur:.2f}s")
    
    if not os.path.exists(VIDEO_PATH):
        print(f"ERROR: Missing video asset at {VIDEO_PATH}")
        sys.exit(1)
        
    print("Assembling Outro...")
    
    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,setsar=1/1,format=yuv420p[vout];"
        f"[2:a]afade=t=in:d=2,afade=t=out:st={max(0, vo_dur - 2):.1f}:d=2,volume=0.35[music];"
        f"[1:a][music]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[aout]"
    )
    
    fc_file = os.path.join(OUTRO_DIR, "_outro_filter.txt")
    with open(fc_file, "w") as f:
        f.write(filter_complex)
        
    cmd = [
        "ffmpeg", "-y",
        "-i", VIDEO_PATH,
        "-i", VO_PATH,
        "-i", MUSIC_PATH,
        "-filter_complex_script", fc_file,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(vo_dur + 0.5), # Add half a second padding
        FINAL_OUTRO_PATH
    ]
    
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:")
        print(r.stderr[-2000:])
        sys.exit(1)
        
    os.remove(fc_file)
    print(f"✅ Outro built at: {FINAL_OUTRO_PATH}")

if __name__ == "__main__":
    build_outro()
