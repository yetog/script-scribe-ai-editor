
"""Audio and TTS services for ScriptVoice."""

import tempfile
import os
from gtts import gTTS
from typing import Tuple, Optional


def generate_tts(text: str, speed: float = 1.0) -> Tuple[Optional[str], str]:
    """Generate TTS audio from text with improved error handling."""
    if not text.strip():
        return None, '<div class="status-error">❌ Please enter some text to convert to speech</div>'
    
    # Limit text length for TTS to avoid very long processing times
    if len(text) > 5000:
        text = text[:5000] + "... (truncated for audio generation)"
    
    try:
        # Create TTS with slower speed if requested
        slow_speech = speed < 0.8
        tts = gTTS(text=text, lang='en', slow=slow_speech)
        
        # Create a temporary file for the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            
            # Verify the file was created and has content
            if os.path.exists(tmp_file.name) and os.path.getsize(tmp_file.name) > 0:
                return tmp_file.name, '<div class="status-success">✅ Audio generated successfully! Click play to listen.</div>'
            else:
                return None, '<div class="status-error">❌ Error: Audio file was not generated properly</div>'
                
    except Exception as e:
        return None, f'<div class="status-error">❌ Error generating audio: {str(e)}</div>'


def cleanup_temp_audio_files():
    """Clean up temporary audio files (utility function)."""
    import glob
    temp_dir = tempfile.gettempdir()
    audio_files = glob.glob(os.path.join(temp_dir, "*.mp3"))
    
    for file_path in audio_files:
        try:
            # Only remove files older than 1 hour
            if os.path.getctime(file_path) < (time.time() - 3600):
                os.remove(file_path)
        except:
            pass  # Ignore cleanup errors
