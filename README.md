
# ScriptVoice - AI-Powered TTS Script Editor

A powerful Gradio-based application for creating, editing, and managing text-to-speech scripts with AI enhancement capabilities.

## 🎯 Features

- **📝 Script Management**: Create, edit, and organize multiple scripts
- **🔊 Text-to-Speech**: Generate high-quality audio from your scripts using gTTS
- **📝 Notes System**: Add and manage notes for each script
- **📷 OCR Integration**: Extract text from images using Tesseract OCR
- **🤖 AI Enhancement**: Enhance scripts with different tones and styles (framework ready)
- **📤 Export Options**: Export scripts as text files or audio files
- **⚙️ Customizable Settings**: Adjust voice speed, volume, and accessibility options
- **📊 Real-time Word Count**: Track script length as you type

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd scriptvoice-gradio
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR** (for image text extraction)
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

4. **Run the application**
```bash
python app.py
```

5. **Open your browser** and navigate to `http://localhost:7860`

### HuggingFace Spaces Deployment

This app is designed to run on HuggingFace Spaces. Simply:

1. Create a new Space on [HuggingFace](https://huggingface.co/spaces)
2. Upload `app.py`, `requirements.txt`, and this `README.md`
3. Set the Space SDK to "Gradio"
4. Your app will be automatically deployed!

## 🎮 How to Use

### Creating Your First Script

1. **Create a New Project**: Enter a name in the "New Project Name" field and click "➕ Create Project"
2. **Write Your Script**: Use the main editor to write your content
3. **Add Notes**: Use the notes section for reminders, directions, or script metadata
4. **Generate Audio**: Click "🔊 Play TTS" to hear your script read aloud
5. **Save Your Work**: Click "💾 Save" to persist your changes

### Advanced Features

- **OCR Text Extraction**: Upload an image containing text, and the app will extract it for you
- **Voice Customization**: Adjust speed and volume in the settings panel
- **Export Options**: Download your scripts as text files or audio files
- **AI Enhancement**: (Framework ready) Enhance your scripts with different tones

### Keyboard Shortcuts

- **Ctrl+S** (planned): Quick save
- **Ctrl+P** (planned): Play TTS
- **Ctrl+N** (planned): New project

## 🛠️ Technical Architecture

### Core Components

- **Gradio Blocks**: Modern, responsive UI framework
- **gTTS**: Google Text-to-Speech for audio generation
- **Tesseract OCR**: Image text extraction
- **JSON Storage**: Simple, portable project persistence
- **Python 3.10+**: Modern Python features and type hints

### File Structure

```
scriptvoice-gradio/
├── app.py              # Main Gradio application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── projects.json      # Auto-generated project storage
└── temp/              # Auto-generated temp files
```

### Data Persistence

Projects are stored in `projects.json` with the following structure:

```json
{
  "projects": {
    "1": {
      "id": "1",
      "name": "Project Name",
      "content": "Script content...",
      "notes": "Project notes...",
      "created_at": "2024-01-01T00:00:00",
      "word_count": 42
    }
  },
  "settings": {
    "dyslexic_mode": false,
    "voice_speed": 1.0,
    "voice_volume": 1.0
  }
}
```

## 🔮 Future Enhancements

### Planned Features

- **🤖 Full AI Integration**: Connect to OpenAI GPT-4 or HuggingFace models for script enhancement
- **🎭 Voice Cloning**: Integrate with voice cloning services
- **📊 Analytics**: Script performance metrics and reading time estimates
- **🌐 Multi-language Support**: Support for multiple TTS languages
- **☁️ Cloud Storage**: Integration with Google Drive, Dropbox, or AWS S3
- **👥 Collaboration**: Multi-user editing and sharing capabilities

### AI Enhancement Framework

The app includes a ready-to-extend framework for AI script enhancement:

```python
def enhance_script_with_ai(text, enhancement_type, api_key):
    """
    Future implementation for AI script enhancement
    - Connect to OpenAI API or HuggingFace Hub
    - Apply different enhancement styles
    - Return enhanced script content
    """
    pass
```

## 🏆 Hackathon Demo

This project was built for **Track 3: Agentic Demo** with the following goals:

- ✅ **Rapid Prototyping**: From TypeScript to Python/Gradio in record time
- ✅ **AI-Ready Architecture**: Framework for intelligent script enhancement
- ✅ **Production Deployment**: Ready for HuggingFace Spaces hosting
- ✅ **User-Friendly Interface**: Notion-like editing experience for storytellers

### Demo Script

"Welcome to ScriptVoice - where your words come to life! This AI-powered editor lets you craft compelling scripts, generate professional voiceovers, and enhance your content with intelligent suggestions. Whether you're a content creator, educator, or storyteller, ScriptVoice transforms your text into engaging audio experiences."

## 🤝 Contributing

We welcome contributions! Areas where help is needed:

- **AI Model Integration**: Connect OpenAI or HuggingFace models
- **Voice Options**: Add more TTS providers and voice choices
- **UI/UX Improvements**: Enhance the user interface and experience
- **Performance Optimization**: Improve app speed and responsiveness
- **Testing**: Add comprehensive test coverage

## 📄 License

MIT License - see LICENSE file for details.

## 🏷️ Tags

`#gradio` `#text-to-speech` `#ai` `#python` `#huggingface` `#agent-demo-track` `#tts` `#script-editor` `#voice-generation`

---

**Built with ❤️ using Gradio and deployed on HuggingFace Spaces**
