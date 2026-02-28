import os
import subprocess
import json
import math
from datetime import datetime
import json
from datetime import datetime
try:
    from config import OUTPUT_DIR
except ImportError:
    from .config import OUTPUT_DIR

def assemble_final_video(
    timeline_config: dict,
    audio_path: str,
    word_timestamps: list,
    output_filename: str = "final_render.mp4",
    output_dir: str = None
) -> str:
    """
    Takes a timeline config (list of scenes with image/video filepaths and durations)
    and assembles them using FFmpeg.
    """
    if output_dir is None:
        output_dir_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(OUTPUT_DIR, output_dir_name)
    else:
        output_dir_name = os.path.basename(output_dir)
        
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_filename)

    print(f"Beginning FFmpeg Hybrid Assembly in {output_dir_name}...")
    
    # Assembly strategy:
    # 1. We will use an FFmpeg complex filter to concatenate the visual clips.
    # 2. For static images, we will apply the zoompan filter to create movement.
    # 3. We will overlay the audio.
    # 4. We will render dynamic subtitles via drawtext.
    
    inputs = []
    filter_complex = ""
    video_streams = []

    # Map inputs
    for i, scene in enumerate(timeline_config['scenes']):
        filepath = scene['filepath']
        duration = float(scene['duration'])
        
        # Determine if it's an image or video
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext in ['.png', '.jpg', '.jpeg']:
            # Loop the static image for the given duration at 30 fps
            inputs.extend(["-loop", "1", "-framerate", "30", "-t", str(duration), "-i", filepath])
        else:
            inputs.extend(["-i", filepath])
        
        # Determine if it's an image or video
        ext = os.path.splitext(filepath)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg']:
            # No zoompan / jitter effect. Keep images perfectly static, scaled and cropped to 9:16.
            # loop=1 is required for input mapping, but since we are mapping duration we use scale and setsar.
            filter_complex += f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1/1[v{i}];"
        else:
            # It's a video, scale and format it uniformly
            filter_complex += f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1/1[v{i}];"

        video_streams.append(f"[v{i}]")

    # Concatenate all visual streams
    concat_inputs = "".join(video_streams)
    filter_complex += f"{concat_inputs}concat=n={len(timeline_config['scenes'])}:v=1:a=0[vbase];"

    # Add audio input
    inputs.extend(["-i", audio_path])
    audio_index = len(timeline_config['scenes'])

    # Generate Drawtext Captions
    if word_timestamps and len(word_timestamps) > 0:
        drawtext_filters = []
        for w in word_timestamps:
            word = w.get("word", "").strip()
            if not word:
                continue
            start_t = w.get("start", 0)
            end_t = w.get("end", start_t + 0.3)
            # Use curly quote to bypass strict FFmpeg escaping bugs
            safe_word = word.replace("'", "\u2019").replace(":", "\\:").replace("%", "\\%")
            df = f"drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':text='{safe_word}':x=(w-text_w)/2:y=(h-text_h)/2+300:fontsize=120:fontcolor=white:borderw=6:bordercolor=black:enable='between(t,{start_t},{end_t})'"
            drawtext_filters.append(df)
            
        filter_complex += f"[vbase]{','.join(drawtext_filters)}[vcaptions];[vcaptions]format=yuv420p[vout]"
    else:
        filter_complex += f"[vbase]format=yuv420p[vout]"

    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_exe, "-y",
    ] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", f"{audio_index}:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest", # End when the shortest stream ends (audio vs video)
        output_path
    ]

    print(f"Executing FFmpeg Command:\n{' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, cwd=output_dir)
        print(f"Assembly Complete! Output saved to: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print("FFmpeg Assembly Failed.")
        raise e
