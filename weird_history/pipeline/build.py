import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
from generate_images import generate_still
from generate_video import generate_video_clip

def build():
    tl = json.load(open(os.path.join(os.path.dirname(__file__), 'blanket_courtship_timeline.json')))
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'weird_history', 'blanket_courtship_hyperrealism'))
    os.makedirs(out_dir, exist_ok=True)
    
    for s in tl['scenes']:
        out_path = os.path.join(out_dir, s['filename'])
        if s['type'] == 'image':
            if not os.path.exists(out_path):
                generate_still(s['prompt'], out_path)
            else:
                print(f"Skipping {s['filename']}")
        elif s['type'] == 'video':
            if not os.path.exists(out_path):
                generate_video_clip(s['prompt'], out_path)
            else:
                print(f"Skipping {s['filename']}")

if __name__ == "__main__":
    build()
