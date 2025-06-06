
"""Configuration settings for ScriptVoice."""

import os

# File paths
PROJECTS_FILE = "projects.json"
AUDIO_FOLDER = "audio_output"
TEMP_FOLDER = "temp"

# API Keys (with fallbacks)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Default settings
DEFAULT_TTS_SPEED = 1.0
DEFAULT_ENHANCEMENT_TYPE = "dialogue"

# Voice settings for TTS
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
