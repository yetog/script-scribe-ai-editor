
"""Configuration settings for ScriptVoice."""

import os

# File paths
PROJECTS_FILE = "projects.json"
AUDIO_FOLDER = "audio_output"
TEMP_FOLDER = "temp"

# IONOS AI Model Hub settings (primary)
IONOS_API_TOKEN = os.getenv("IONOS_API_TOKEN", "").strip()
IONOS_MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
IONOS_ENDPOINT = "https://openai.inference.de-txl.ionos.com/v1"
IONOS_CHAT_URL = "https://inference.de-txl.ionos.com/models/meta-llama/Meta-Llama-3.1-8B-Instruct/predictions"
IONOS_IMAGE_URL = "https://openai.inference.de-txl.ionos.com/v1/images/generations"

# API Keys (with fallbacks to OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# ElevenLabs is now optional
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "").strip()

# Default settings
DEFAULT_TTS_SPEED = 1.0
DEFAULT_ENHANCEMENT_TYPE = "dialogue"

# Voice settings for TTS (ElevenLabs - optional)
DEFAULT_VOICE_ID = "9BWtsMINqrJLrRacOk9x"  # Aria voice
DEFAULT_MODEL_ID = "eleven_multilingual_v2"

# File upload limits
MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']

# Vector database settings
VECTOR_DB_CHUNK_SIZE = 500
VECTOR_DB_CHUNK_OVERLAP = 50

# Model settings
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"

# AI Provider validation
def is_ionos_configured():
    """Check if IONOS is properly configured."""
    return bool(IONOS_API_TOKEN and IONOS_API_TOKEN != "your_token_here")

def is_openai_configured():
    """Check if OpenAI is properly configured."""
    return bool(OPENAI_API_KEY)

def is_elevenlabs_configured():
    """Check if ElevenLabs is properly configured."""
    return bool(ELEVENLABS_API_KEY)
