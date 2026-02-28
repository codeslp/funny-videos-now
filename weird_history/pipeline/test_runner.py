import json
import os
import sys

# Ensure pipeline is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from assemble_video import assemble_final_video

with open("pipeline/test_timeline.json") as f:
    config = json.load(f)

# The asset paths in JSON are relative to pipeline dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))
assemble_final_video(config, "test_assets/audio.wav", [], "test_needle_render.mp4")
print("Test completed.")
