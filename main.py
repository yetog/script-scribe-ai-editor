
"""Main application entry point for ScriptVoice - Pure Gradio Application."""

from app_factory import create_interface


if __name__ == "__main__":
    print("🚀 Starting ScriptVoice - AI-Powered Story Intelligence Platform")
    print("🌐 The app will be available at: http://localhost:7860")
    
    # Create and launch the app
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
