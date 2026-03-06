import os
import subprocess
import json
import math
from datetime import datetime
import hashlib
try:
    from config import CARTESIA_API_KEY, DEFAULT_VOICE_ID, READY_TO_PUBLISH_DIR
except ImportError:
    from .config import OUTPUT_DIR

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MUSIC_ASSETS_DIR = os.path.join(PROJECT_ROOT, 'output', 'future_history', 'music_assets')


def _get_duration(filepath: str) -> float:
    """Get duration of an audio/video file in seconds via ffprobe."""
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', filepath],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


def assemble_final_video(
    timeline_config: dict,
    audio_path: str,
    word_timestamps: list,
    output_filename: str = "final_render.mp4",
    output_dir: str = None,
    allow_duplicates: bool = False,
    music_path: str = None,
    intro_clip_path: str = None,
    outro_audio_path: str = None,
    theme_path: str = None,
) -> str:
    """
    Assembles the final video:
      - Prepends pre-built intro clip (if exists)
      - Main content: scenes + narration + underscore at -18dB
        Scene timing is dynamic: hero videos play at full length,
        still images fill remaining time to match voiceover duration.
      - Appends outro (last scene + theme + deep voice) if provided
    """
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    if output_dir is None:
        output_dir_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(READY_TO_PUBLISH_DIR, output_dir_name)
    else:
        output_dir_name = os.path.basename(output_dir)

    os.makedirs(output_dir, exist_ok=True)
    print(f"Beginning FFmpeg Assembly in {output_dir_name}...")

    # Determine target resolution
    resolution = timeline_config.get('resolution', '1080x1920')
    res_parts = resolution.split('x')
    target_w, target_h = int(res_parts[0]), int(res_parts[1])
    zoom_w, zoom_h = target_w * 4, target_h * 4

    # Voiceover duration is the master clock for the main segment
    vo_duration = _get_duration(audio_path)
    print(f"  Voiceover duration: {vo_duration:.1f}s")

    # ── Phase 1: Build main content segment ─────────────────────
    print("Building main content segment...")
    main_path = os.path.join(output_dir, "_main_segment.mp4")

    inputs = []
    filter_complex = ""
    video_streams = []
    seen_hashes = set()

    # Dynamic scene timing: probe hero videos, distribute remaining time to stills
    total_video_dur = 0.0
    image_count = 0
    pre_timed_image_count = 0
    pre_timed_image_dur = 0.0
    
    for scene in timeline_config['scenes']:
        ext = os.path.splitext(scene['filepath'])[1].lower()
        if ext in ['.mp4', '.mov', '.webm']:
            actual_dur = _get_duration(scene['filepath'])
            scene['_actual_duration'] = actual_dur
            total_video_dur += actual_dur
        else:
            if '_actual_duration' in scene:
                pre_timed_image_count += 1
                pre_timed_image_dur += scene['_actual_duration']
            else:
                image_count += 1

    remaining_time = max(0, vo_duration - total_video_dur - pre_timed_image_dur)
    still_duration = remaining_time / max(image_count, 1) if image_count > 0 else 0

    print(f"  Dynamic timing: {len(timeline_config['scenes']) - image_count - pre_timed_image_count} videos "
          f"({total_video_dur:.1f}s) + {pre_timed_image_count} pre-timed stills ({pre_timed_image_dur:.1f}s) + "
          f"{image_count} auto-stills ({still_duration:.1f}s each) = {vo_duration:.1f}s target")

    for i, scene in enumerate(timeline_config['scenes']):
        filepath = os.path.abspath(scene['filepath'])

        if not allow_duplicates and os.path.exists(filepath):
            if filepath in seen_hashes:
                print(f"  WARNING: Duplicate filepath at Scene {i+1} ({filepath}). Continuing anyway.")
            seen_hashes.add(filepath)

        ext = os.path.splitext(filepath)[1].lower()
        inputs.extend(["-i", filepath])

        if ext in ['.png', '.jpg', '.jpeg']:
            actual_dur = scene.get('_actual_duration', still_duration)
            frames = int(actual_dur * 30)
            print(f"  Zoompan: {os.path.basename(filepath)} ({actual_dur:.1f}s)")
            filter_complex += (
                f"[{i}:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                f"crop={target_w}:{target_h},setsar=1/1,"
                f"scale={zoom_w}:{zoom_h},"
                f"zoompan=z='min(zoom+0.0005,1.2)':d={frames}"
                f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                f":s={target_w}x{target_h}:fps=30[v{i}];"
            )
        else:
            actual_dur = scene.get('_actual_duration', float(scene['duration']))
            print(f"  Video: {os.path.basename(filepath)} ({actual_dur:.1f}s full)")
            filter_complex += (
                f"[{i}:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                f"crop={target_w}:{target_h},setsar=1/1[v{i}];"
            )
        video_streams.append(f"[v{i}]")

    # Concatenate video
    concat_inputs = "".join(video_streams)
    filter_complex += f"{concat_inputs}concat=n={len(timeline_config['scenes'])}:v=1:a=0[vbase];"
    filter_complex += "[vbase]format=yuv420p[vout]"

    # Audio: voiceover + underscore
    inputs.extend(["-i", os.path.abspath(audio_path)])
    voiceover_index = len(timeline_config['scenes'])

    if music_path and os.path.exists(music_path):
        inputs.extend(["-i", os.path.abspath(music_path)])
        music_index = voiceover_index + 1
        filter_complex += (
            f";[{music_index}:a]volume=0.125,atrim=0:{vo_duration},asetpts=PTS-STARTPTS[bgmusic];"
            f"[{voiceover_index}:a]atrim=0:{vo_duration},asetpts=PTS-STARTPTS[vo];"
            f"[vo][bgmusic]amix=inputs=2:duration=first[aout]"
        )
        audio_map = "[aout]"
        print(f"  Mixing underscore at -18dB (trimmed to {vo_duration:.1f}s)")
    else:
        audio_map = f"{voiceover_index}:a"

    filter_file = os.path.abspath(os.path.join(output_dir, "_main_filter.txt"))
    with open(filter_file, "w") as ff:
        ff.write(filter_complex)

    main_cmd = [
        ffmpeg_exe, "-y",
    ] + inputs + [
        "-filter_complex_script", filter_file,
        "-map", "[vout]", "-map", audio_map,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(vo_duration),
        os.path.abspath(main_path)
    ]

    print(f"  Executing main FFmpeg (capped at {vo_duration:.1f}s)...")
    try:
        subprocess.run(main_cmd, check=True, capture_output=True, text=True)
        os.remove(filter_file)
        main_dur = _get_duration(main_path)
        print(f"  Main segment: {main_path} ({main_dur:.1f}s)")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Main Failed (exit {e.returncode}):")
        print(f"STDERR: {e.stderr[-2000:] if e.stderr else 'empty'}")
        raise e

    # ── Phase 2: Build outro segment (optional) ─────────────────
    outro_path = None
    has_outro = (outro_audio_path and os.path.exists(outro_audio_path)
                 and theme_path and os.path.exists(theme_path))

    if has_outro:
        print("Building outro segment...")
        outro_path = os.path.join(output_dir, "_outro_segment.mp4")
        last_scene = timeline_config['scenes'][-1]
        last_filepath = os.path.abspath(last_scene['filepath'])
        outro_dur = _get_duration(outro_audio_path) + 1.0  # 1s padding

        outro_filter = (
            f"[0:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
            f"crop={target_w}:{target_h},setsar=1/1,"
            f"scale={zoom_w}:{zoom_h},"
            f"zoompan=z='min(zoom+0.003,1.5)':d={int(outro_dur * 30 + 30)}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":s={target_w}x{target_h}:fps=30,format=yuv420p[vout];"
            f"[2:a]afade=t=out:st={max(0, outro_dur-1)}:d=1,volume=0.5[beat];"
            f"[1:a][beat]amix=inputs=2:duration=first[aout]"
        )

        outro_filter_file = os.path.abspath(os.path.join(output_dir, "_outro_filter.txt"))
        with open(outro_filter_file, "w") as ff:
            ff.write(outro_filter)

        outro_cmd = [
            ffmpeg_exe, "-y",
            "-i", last_filepath,
            "-i", os.path.abspath(outro_audio_path),
            "-i", os.path.abspath(theme_path),
            "-filter_complex_script", outro_filter_file,
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(outro_dur),
            os.path.abspath(outro_path)
        ]
        try:
            subprocess.run(outro_cmd, check=True, capture_output=True, text=True)
            os.remove(outro_filter_file)
            print(f"  Outro segment: {outro_path}")
        except subprocess.CalledProcessError as e:
            print(f"  WARNING: Outro failed: {e.stderr[-500:] if e.stderr else ''}")
            outro_path = None

    # ── Phase 3: Concatenate all segments ───────────────────────
    output_path = os.path.join(output_dir, output_filename)
    segments = []
    if intro_clip_path and os.path.exists(intro_clip_path):
        segments.append(intro_clip_path)
        print(f"  Prepending intro: {intro_clip_path}")
    segments.append(main_path)
    if outro_path and os.path.exists(outro_path):
        segments.append(outro_path)

    if len(segments) == 1:
        os.rename(main_path, output_path)
    else:
        print(f"Concatenating {len(segments)} segments (re-encoding to match resolution)...")

        # Use filter_complex concat to handle resolution/codec differences
        concat_inputs = []
        concat_filter = ""
        for idx, seg in enumerate(segments):
            concat_inputs.extend(["-i", os.path.abspath(seg)])
            # Scale each segment to target resolution
            concat_filter += (
                f"[{idx}:v]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
                f"crop={target_w}:{target_h},setsar=1/1,format=yuv420p[sv{idx}];"
                f"[{idx}:a]aresample=44100[sa{idx}];"
            )

        # Build concat string — concat filter needs interleaved v/a pairs
        pairs = "".join(f"[sv{i}][sa{i}]" for i in range(len(segments)))
        concat_filter += f"{pairs}concat=n={len(segments)}:v=1:a=1[vfinal][afinal]"

        concat_filter_file = os.path.abspath(os.path.join(output_dir, "_concat_filter.txt"))
        with open(concat_filter_file, "w") as cf:
            cf.write(concat_filter)

        concat_cmd = [
            ffmpeg_exe, "-y",
        ] + concat_inputs + [
            "-filter_complex_script", concat_filter_file,
            "-map", "[vfinal]", "-map", "[afinal]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            os.path.abspath(output_path)
        ]

        try:
            subprocess.run(concat_cmd, check=True, capture_output=True, text=True)
            os.remove(concat_filter_file)
        except subprocess.CalledProcessError as e:
            print(f"Concat failed (exit {e.returncode}):")
            print(f"STDERR: {e.stderr[-2000:] if e.stderr else 'empty'}")
            raise e

        for seg in segments:
            if os.path.exists(seg) and seg != intro_clip_path:
                os.remove(seg)

    final_dur = _get_duration(output_path)
    print(f"Assembly Complete! Output: {output_path} ({final_dur:.1f}s / {final_dur/60:.1f}m)")
    return output_path

