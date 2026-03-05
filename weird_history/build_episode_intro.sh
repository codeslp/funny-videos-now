#!/bin/bash

echo "Starting Episode 001 Intro Assembly Build (Part 1)"

# 1. Kill any hung file copy processes just in case
pkill -f "rsync" || true
pkill -f "shutil" || true

# 2. Gather the slideshow images instantly using symlinks
BASE="output/future_history/in_progress"
DEST="output/future_history/episodes/episode_001/slideshow_images"

echo "Creating symlinks for slideshow images to bypass file copy hang..."
mkdir -p "$DEST"

ln -sf "../../in_progress/en_organ_loyalty_2026-03-02/scene_0_still.jpg" "$DEST/01_organ_s0.jpg"
ln -sf "../../in_progress/en_organ_loyalty_2026-03-02/scene_3_still.jpg" "$DEST/02_organ_s3.jpg"
ln -sf "../../in_progress/en_organ_loyalty_2026-03-02/scene_6_still.jpg" "$DEST/03_organ_s6.jpg"
ln -sf "../../in_progress/en_organ_loyalty_2026-03-02/scene_10_still.jpg" "$DEST/04_organ_s10.jpg"

ln -sf "../../in_progress/en_ai_confession_booth_2026-03-03/scene_0_still.jpg" "$DEST/05_confession_s0.jpg"
ln -sf "../../in_progress/en_ai_confession_booth_2026-03-03/scene_3_still.jpg" "$DEST/06_confession_s3.jpg"
ln -sf "../../in_progress/en_ai_confession_booth_2026-03-03/scene_6_still.jpg" "$DEST/07_confession_s6.jpg"
ln -sf "../../in_progress/en_ai_confession_booth_2026-03-03/scene_10_still.jpg" "$DEST/08_confession_s10.jpg"

ln -sf "../../in_progress/en_pet_awakening_2026-03-03/scene_0_still.jpg" "$DEST/09_pet_s0.jpg"
ln -sf "../../in_progress/en_pet_awakening_2026-03-03/scene_3_still.jpg" "$DEST/10_pet_s3.jpg"
ln -sf "../../in_progress/en_pet_awakening_2026-03-03/scene_6_still.jpg" "$DEST/11_pet_s6.jpg"
ln -sf "../../in_progress/en_pet_awakening_2026-03-03/scene_10_still.jpg" "$DEST/12_pet_s10.jpg"

echo "Symlinks created successfully."

# 3. Generate the updated voiceover
echo "Generating updated voiceover..."

cat << 'EOF' > generate_vo.py
import sys
from pipeline.generate_audio import generate_tts

generate_tts(
    text="It's getting weird out there. Here's what to expect. Because a new world is coming. News from the future.",
    output_filepath="output/future_history/episodes/episode_001/episode_intro_voice.wav",
    voice_id="qNkzaJoHLLdpvgh5tISm"
)
EOF

export PYTHONPATH=$PYTHONPATH:$(pwd)/weird_history
python3 generate_vo.py

# Clean up the temporary python file
rm generate_vo.py

echo "Done! The slideshow images are symlinked and the VO audio has been generated."
