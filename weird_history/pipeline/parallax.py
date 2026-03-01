import os
import numpy as np
from PIL import Image
import imageio.v3 as iio
import imageio_ffmpeg
from .generate_depth import generate_depth_map

def apply_parallax_to_image(image_path: str, duration_sec: float, output_dir: str, fps: int = 30) -> str:
    """
    Takes a static image, generates a depth map, and renders a 2.5D parallax video.
    Returns the path to the newly rendered temporary video.
    """
    base_name = os.path.basename(image_path)
    name_no_ext = os.path.splitext(base_name)[0]
    
    depth_path = os.path.join(output_dir, f"{name_no_ext}_depth.png")
    output_video_path = os.path.join(output_dir, f"{name_no_ext}_parallax.mp4")
    
    # Generate depth map if it doesn't exist
    if not os.path.exists(depth_path):
        print(f"Generating depth map for {base_name}...")
        generate_depth_map(image_path, depth_path)
        
    frames = int(duration_sec * fps)
    max_shift_x = 45 # Pixels to shift the foreground across the duration
    
    print(f"Rendering 2.5D parallax for {base_name} ({frames} frames)...")
    img = Image.open(image_path).convert('RGB')
    depth_img = Image.open(depth_path).convert('L')
    
    if img.size != depth_img.size:
        depth_img = depth_img.resize(img.size, Image.Resampling.LANCZOS)
        
    img_np = np.array(img)
    depth_np = np.array(depth_img) / 255.0 
    
    height, width, channels = img_np.shape
    
    writer = imageio_ffmpeg.write_frames(
        output_video_path, 
        size=(width, height), 
        fps=fps, 
        codec="libx264", 
        pix_fmt_in="rgb24",
        macro_block_size=8
    )
    writer.send(None) 
    
    y_idx, x_idx = np.indices((height, width))
    
    for i in range(frames):
        # We want the zoom/shift to feel like a slow push in.
        # Foreground pixels shift left, creating parallax.
        progress = i / max(1, (frames - 1))
        current_shift_x = int(max_shift_x * progress)
        
        frame = np.zeros_like(img_np)
        
        # Depth > 0 means foreground. Shift it.
        shift_map = (depth_np * current_shift_x).astype(np.int32)
        
        # Map pixels (sliding the background relative to the foreground)
        new_x = np.clip(x_idx - shift_map, 0, width - 1)
        frame[y_idx, x_idx] = img_np[y_idx, new_x]
        
        writer.send(frame)
            
    writer.close()
    return output_video_path
