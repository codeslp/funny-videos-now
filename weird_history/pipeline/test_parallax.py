import os
import argparse
import numpy as np
from PIL import Image
import imageio.v3 as iio
import imageio_ffmpeg

def create_parallax_video(image_path: str, depth_path: str, output_path: str, frames: int = 150, max_shift_x: int = 30):
    """
    Creates a 2.5D parallax video from an image and its depth map.
    The foreground (white in depth map) will shift more than the background.
    """
    print("Loading images...")
    img = Image.open(image_path).convert('RGB')
    depth_img = Image.open(depth_path).convert('L')
    
    # Ensure they are the same size
    if img.size != depth_img.size:
        depth_img = depth_img.resize(img.size, Image.Resampling.LANCZOS)
        
    img_np = np.array(img)
    depth_np = np.array(depth_img) / 255.0  # Normalize depth to 0.0 - 1.0 (1.0 is foreground)
    
    height, width, channels = img_np.shape
    
    print(f"Rendering {frames} frames of 2.5D parallax...")
    
    writer = imageio_ffmpeg.write_frames(
        output_path, 
        size=(width, height), 
        fps=30, 
        codec="libx264", 
        pix_fmt_in="rgb24",
        macro_block_size=8 # Important for vertical videos
    )
    writer.send(None) # Initialize generator
    
    # Create x and y coordinate grids
    y_idx, x_idx = np.indices((height, width))
    
    for i in range(frames):
        # Calculate the progress of the animation (0.0 to 1.0)
        progress = i / max(1, (frames - 1))
        
        # Calculate the shift for this frame
        current_max_shift_x = int(max_shift_x * progress)
        
        # Create a new blank frame
        frame = np.zeros_like(img_np)
        
        # Calculate displacement for each pixel
        # Foreground (depth ~ 1.0) shifts by current_max_shift_x
        # Background (depth ~ 0.0) shifts by 0
        shift_map = (depth_np * current_max_shift_x).astype(np.int32)
        
        # New X coordinates
        new_x = np.clip(x_idx - shift_map, 0, width - 1)
        
        # Map pixels
        frame[y_idx, x_idx] = img_np[y_idx, new_x]
        
        # Write to video
        writer.send(frame)
        
        if i % 30 == 0:
            print(f"Rendered {i}/{frames} frames...")
            
    writer.close()
    print(f"Success! Parallax video saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path")
    parser.add_argument("depth_path")
    parser.add_argument("--output", "-o", default="parallax_test.mp4")
    parser.add_argument("--frames", type=int, default=150)
    parser.add_argument("--shift", type=int, default=40)
    args = parser.parse_args()
    
    create_parallax_video(args.image_path, args.depth_path, args.output, args.frames, args.shift)
