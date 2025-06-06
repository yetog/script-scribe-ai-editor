
"""Main application entry point for ScriptVoice - Pure Gradio Application."""

import os
from app_factory import create_interface

def ensure_directories():
    """Ensure required directories exist."""
    directories = ["audio_output", "temp", "chromadb_storage"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

if __name__ == "__main__":
    print("🚀 Starting ScriptVoice - AI-Powered Story Intelligence Platform")
    print("📦 Make sure you have installed dependencies: pip install -r requirements.txt")
    print("🌐 The app will be available at: http://localhost:7860")
    print("💡 A simple React landing page is available at: http://localhost:8080")
    
    # Ensure required directories exist
    ensure_directories()
    
    # Create and launch the app
    try:
        app = create_interface()
        app.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            show_error=True,
            show_tips=False,
            quiet=False
        )
    except Exception as e:
        print(f"Error starting the application: {e}")
        print("Please check that all dependencies are installed correctly.")
