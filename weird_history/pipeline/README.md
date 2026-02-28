# Weird History: Automated Production Pipeline

This directory contains the core Python scripts responsible for executing the **Hybrid Video Assembly** strategy. It translates the creative guidelines defined in the visual style guide into actual programmatic rendering steps.

## The Architecture
The pipeline is broken down into modular generation scripts, which are eventually orchestrated by an assembly file.

### 1. Configuration (`config.py`)
Loads the necessary API keys from the root `.env` file and defines global constants like video resolution (1080x1920) and FPS (30).

### 2. Audio Generation (`generate_audio.py`)
Hits the **Cartesia API** using the ultra-fast `sonic-english` model to render high-quality, expressive voiceovers. Cartesia is used to control comedic timing and emotion perfectly.

### 3. Caption Alignment (`generate_transcription.py`)
Uses the open-source **WhisperX** library to perform forced alignment on the generated Cartesia audio. This generates the exact millisecond timestamps for every single word spoken, a requirement for bouncy TikTok/Reels captions.

### 4. Visual Asset Generation
*   **Stills (`generate_images.py`):** Uses the **Flow API** (via Fal.ai or direct) to generate the baseline static images. These images establish the scene and visual aesthetic.
*   **Video (`generate_video.py`):** Uses the **Flow TV API** to generate the "Hero" clips. These are the 1-2 expensive clips per video that are fully animated for the comedic punchline.

### 5. Final Stitching (`assemble_video.py`)
The orchestrator. It uses **FFmpeg** to:
1. Concatenate all generated visuals together.
2. Apply the "Ken Burns" programmatic zoom-and-pan effect dynamically to the static images (so they feel like video).
3. Overlay the generated audio.
4. Render the captions onto the final `output/` file based on the WhisperX timestamps.

## Prerequisites
*   Python 3.9+
*   FFmpeg installed globally on the system (`brew install ffmpeg`)
*   WhisperX installed globally (`pip install git+https://github.com/m-bain/whisperx.git`)
*   Python libraries: `requests`, `python-dotenv`
