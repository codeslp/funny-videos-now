import os
import argparse
import torch
from transformers import pipeline
from PIL import Image

def generate_depth_map(image_path: str, output_path: str = None) -> str:
    """
    Reads an image, uses a pre-trained Monocular Depth Estimation model,
    and saves the resulting depth map as an image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source image not found: {image_path}")

    print(f"Loading Depth Estimation Model...")
    # Using DPT (Dense Prediction Transformers) for high quality depth estimation
    device = 0 if torch.cuda.is_available() else (-1 if not torch.backends.mps.is_available() else "mps")
    
    # Check if we should use MPS (Apple Silicon) if available, else CPU
    if torch.backends.mps.is_available():
        device = "mps"
        print("Using Apple MPS backend for acceleration.")
    else:
        device = -1 # CPU
        print("Using CPU for inference.")
        
    depth_estimator = pipeline("depth-estimation", model="Intel/dpt-large", device=device)
    
    print(f"Processing image: {image_path}")
    image = Image.open(image_path)
    
    # Run the model
    predictions = depth_estimator(image)
    
    # The pipeline returns a dictionary with the 'predicted_depth' (tensor) and 'depth' (PIL Image)
    depth_image = predictions["depth"]
    
    # Determine output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_depth.png"
        
    # Save the depth map
    depth_image.save(output_path)
    print(f"Saved depth map to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a depth map from a 2D image.")
    parser.add_argument("image_path", help="Path to the input image file")
    parser.add_argument("--output", "-o", default=None, help="Path to save the output depth map (defaults to <original_name>_depth.png)")
    
    args = parser.parse_args()
    
    generate_depth_map(args.image_path, args.output)
