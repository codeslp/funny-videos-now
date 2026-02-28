import whisperx
import json
import torch
import omegaconf

torch.serialization.add_safe_globals([
    omegaconf.listconfig.ListConfig, 
    omegaconf.base.ContainerMetadata, 
    set, 
    tuple
])

audio_path = '/Users/bfaris96/Claude Code Markdown/funny_video_generator/output/weird_history/blanket_courtship_hyperrealism/voiceover.wav'

device = "cpu"
print("Loading audio...")
audio = whisperx.load_audio(audio_path)
print("Loading model...")
model = whisperx.load_model("base.en", device, compute_type="int8")
print("Transcribing...")
result = model.transcribe(audio, batch_size=4)
print(f"Transcribed {len(result['segments'])} segments")
