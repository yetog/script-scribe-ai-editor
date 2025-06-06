
"""Main application entry point for ScriptVoice - Pure Gradio Application."""

import os
from interface_factory import create_interface
from config import IONOS_API_TOKEN, OPENAI_API_KEY

def ensure_directories():
    """Ensure required directories exist."""
    directories = ["audio_output", "temp", "chromadb_storage", "generated_images", "mood_boards"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def check_dependencies():
    """Check if critical dependencies are available."""
    print("\n📦 Dependency Status:")
    
    try:
        import pandas
        print("  ✅ pandas - Available")
    except ImportError:
        print("  ❌ pandas - Missing (install with: pip install pandas)")
    
    try:
        import elevenlabs
        print("  ✅ elevenlabs - Available")
    except ImportError:
        print("  ❌ elevenlabs - Missing (install with: pip install elevenlabs)")
    
    try:
        import pytesseract
        print("  ✅ pytesseract - Available")
    except ImportError:
        print("  ❌ pytesseract - Missing (install with: pip install pytesseract)")
    
    try:
        import chromadb
        print("  ✅ chromadb - Available")
    except ImportError:
        print("  ❌ chromadb - Missing (install with: pip install chromadb)")

def check_ai_providers():
    """Check and display available AI providers."""
    print("\n🤖 AI Provider Status:")
    
    if IONOS_API_TOKEN and IONOS_API_TOKEN != "your_token_here":
        print("  ✅ IONOS AI Model Hub - Available (Primary)")
    else:
        print("  ❌ IONOS AI Model Hub - Not configured (set IONOS_API_TOKEN)")
    
    if OPENAI_API_KEY:
        print("  ✅ OpenAI - Available (Fallback)")
    else:
        print("  ❌ OpenAI - Not configured (set OPENAI_API_KEY)")
    
    if not IONOS_API_TOKEN and not OPENAI_API_KEY:
        print("  ⚠️  No AI providers configured - AI features will be limited")
    
    print()

if __name__ == "__main__":
    print("🚀 Starting ScriptVoice - AI-Powered Story Intelligence Platform")
    print("📦 Make sure you have installed dependencies: pip install -r requirements.txt")
    print("🌐 The app will be available at: http://localhost:7860")
    print("💡 A simple React landing page is available at: http://localhost:8080")
    
    # Ensure required directories exist
    ensure_directories()
    
    # Check dependencies
    check_dependencies()
    
    # Check AI provider status
    check_ai_providers()
    
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
        print(f"❌ Error starting the application: {e}")
        print("Please check that all dependencies are installed correctly.")
        print("Run: pip install -r requirements.txt")
