
import gradio as gr
import json
import os
from datetime import datetime
import tempfile
import io
from gtts import gTTS
import pytesseract
from PIL import Image
import zipfile

# Global state for projects
PROJECTS_FILE = "projects.json"
current_project_id = None

# Custom CSS for ScriptVoice branding
CUSTOM_CSS = """
/* ScriptVoice Custom Styling */
:root {
    --script-red: #E63946;
    --script-gold: #FFD700;
    --script-black: #000000;
    --script-dark-gray: #1a1a1a;
    --script-border: rgba(230, 57, 70, 0.2);
}

/* Global dark theme */
.gradio-container {
    background-color: var(--script-black) !important;
    color: white !important;
}

/* Main container styling */
.contain {
    background-color: var(--script-black) !important;
}

/* Header styling */
.header-container {
    background: var(--script-black) !important;
    border-bottom: 2px solid var(--script-border) !important;
    padding: 1.5rem !important;
}

/* Sidebar styling */
.sidebar-column {
    background-color: var(--script-dark-gray) !important;
    border-right: 1px solid var(--script-border) !important;
    padding: 1rem !important;
}

/* Button styling */
.primary-button {
    background: linear-gradient(135deg, var(--script-red), #c62d36) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.primary-button:hover {
    background: linear-gradient(135deg, #c62d36, var(--script-red)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(230, 57, 70, 0.3) !important;
}

.secondary-button {
    background: var(--script-dark-gray) !important;
    color: white !important;
    border: 1px solid var(--script-border) !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.secondary-button:hover {
    background: var(--script-red) !important;
    border-color: var(--script-red) !important;
}

/* Input and textarea styling */
textarea, input[type="text"], .gr-textbox {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
}

textarea:focus, input[type="text"]:focus, .gr-textbox:focus {
    border-color: var(--script-red) !important;
    box-shadow: 0 0 0 2px rgba(230, 57, 70, 0.2) !important;
    outline: none !important;
}

/* Dropdown styling */
.gr-dropdown {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    color: white !important;
}

/* Group styling */
.gr-group {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
}

/* Audio player styling */
.gr-audio {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    border-radius: 8px !important;
}

/* File upload styling */
.gr-file {
    background-color: var(--script-dark-gray) !important;
    border: 2px dashed var(--script-border) !important;
    border-radius: 8px !important;
    color: white !important;
}

/* Slider styling */
.gr-slider input[type="range"] {
    background: var(--script-dark-gray) !important;
}

.gr-slider input[type="range"]::-webkit-slider-thumb {
    background: var(--script-red) !important;
}

/* Checkbox styling */
.gr-checkbox {
    accent-color: var(--script-red) !important;
}

/* Word count highlight */
.word-count-highlight {
    color: var(--script-gold) !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent) !important;
    padding: 0.25rem 0.5rem !important;
    border-radius: 4px !important;
}

/* Status messages */
.status-success {
    color: #4ade80 !important;
    background: rgba(74, 222, 128, 0.1) !important;
    padding: 0.5rem !important;
    border-radius: 6px !important;
    border-left: 3px solid #4ade80 !important;
}

.status-error {
    color: #f87171 !important;
    background: rgba(248, 113, 113, 0.1) !important;
    padding: 0.5rem !important;
    border-radius: 6px !important;
    border-left: 3px solid #f87171 !important;
}

/* Animated gold highlight for active elements */
@keyframes goldShine {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

.gold-highlight {
    background: linear-gradient(90deg, transparent, var(--script-gold), transparent) !important;
    background-size: 200% 100% !important;
    animation: goldShine 2s ease-in-out infinite !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* Logo styling */
.script-logo {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    margin-bottom: 1rem !important;
}

.script-text {
    color: var(--script-red) !important;
}

.voice-text {
    color: var(--script-gold) !important;
}

/* Section headers */
.section-header {
    color: var(--script-gold) !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    margin: 1rem 0 0.5rem 0 !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid var(--script-border) !important;
}
"""

def load_projects():
    """Load projects from JSON file"""
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
    return {
        "projects": {
            "1": {
                "id": "1",
                "name": "Sample Script",
                "content": "Welcome to ScriptVoice! This is your first script. Start editing to create amazing voice content.",
                "notes": "This is a sample note for your script.",
                "created_at": datetime.now().isoformat(),
                "word_count": 0
            }
        },
        "settings": {
            "dyslexic_mode": False,
            "voice_speed": 1.0,
            "voice_volume": 1.0
        }
    }

def save_projects(data):
    """Save projects to JSON file"""
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_word_count(text):
    """Count words in text"""
    if not text:
        return 0
    return len(text.split())

def update_word_count(text):
    """Update word count display with gold highlighting"""
    count = get_word_count(text)
    return f'<div class="word-count-highlight">📊 Word Count: {count}</div>'

def create_new_project(name):
    """Create a new project"""
    if not name.strip():
        return '<div class="status-error">❌ Please enter a project name</div>', None
    
    data = load_projects()
    new_id = str(len(data["projects"]) + 1)
    
    data["projects"][new_id] = {
        "id": new_id,
        "name": name.strip(),
        "content": "",
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "word_count": 0
    }
    
    save_projects(data)
    
    # Return updated project choices and select the new project
    choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    return f'<div class="status-success">✅ Project "{name}" created successfully!</div>', gr.update(choices=choices, value=new_id)

def load_project(project_id):
    """Load a specific project"""
    if not project_id:
        return "", "", '<div class="word-count-highlight">📊 Word Count: 0</div>'
    
    global current_project_id
    current_project_id = project_id
    
    data = load_projects()
    if project_id in data["projects"]:
        project = data["projects"][project_id]
        word_count = get_word_count(project["content"])
        return project["content"], project["notes"], f'<div class="word-count-highlight">📊 Word Count: {word_count}</div>'
    
    return "", "", '<div class="word-count-highlight">📊 Word Count: 0</div>'

def save_script_content(project_id, content, notes):
    """Save script content and notes"""
    if not project_id:
        return '<div class="status-error">❌ No project selected</div>'
    
    data = load_projects()
    if project_id in data["projects"]:
        data["projects"][project_id]["content"] = content
        data["projects"][project_id]["notes"] = notes
        data["projects"][project_id]["word_count"] = get_word_count(content)
        save_projects(data)
        return '<div class="status-success">✅ Saved successfully</div>'
    
    return '<div class="status-error">❌ Error saving</div>'

def generate_tts(text, speed=1.0):
    """Generate TTS audio from text"""
    if not text.strip():
        return None, '<div class="status-error">❌ Please enter some text to convert to speech</div>'
    
    try:
        # Create a temporary file for the audio
        tts = gTTS(text=text, lang='en', slow=(speed < 1.0))
        
        # Use a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name, '<div class="status-success">✅ Audio generated successfully</div>'
    
    except Exception as e:
        return None, f'<div class="status-error">❌ Error generating audio: {str(e)}</div>'

def extract_text_from_image(image):
    """Extract text from uploaded image using OCR"""
    if image is None:
        return "", '<div class="status-error">❌ Please upload an image</div>'
    
    try:
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(Image.open(image))
        if text.strip():
            return text.strip(), '<div class="status-success">✅ Text extracted successfully</div>'
        else:
            return "", '<div class="status-error">❌ No text found in the image</div>'
    
    except Exception as e:
        return "", f'<div class="status-error">❌ Error extracting text: {str(e)}</div>'

def enhance_script_placeholder(text, enhancement_type):
    """Placeholder for AI script enhancement"""
    enhancements = {
        "dramatic": f"[DRAMATIC VERSION]\n{text}\n\n(Note: AI enhancement feature coming soon!)",
        "romantic": f"[ROMANTIC VERSION]\n{text}\n\n(Note: AI enhancement feature coming soon!)",
        "professional": f"[PROFESSIONAL VERSION]\n{text}\n\n(Note: AI enhancement feature coming soon!)",
        "casual": f"[CASUAL VERSION]\n{text}\n\n(Note: AI enhancement feature coming soon!)"
    }
    
    return enhancements.get(enhancement_type, text), '<div class="status-success">✅ Enhancement applied (demo mode)</div>'

def export_project(project_id, export_type):
    """Export project content"""
    if not project_id:
        return None, '<div class="status-error">❌ No project selected</div>'
    
    data = load_projects()
    if project_id not in data["projects"]:
        return None, '<div class="status-error">❌ Project not found</div>'
    
    project = data["projects"][project_id]
    
    if export_type == "text":
        # Create text file
        content = f"Project: {project['name']}\n"
        content += f"Created: {project['created_at']}\n"
        content += f"Word Count: {project['word_count']}\n\n"
        content += "SCRIPT:\n" + "="*50 + "\n"
        content += project['content'] + "\n\n"
        content += "NOTES:\n" + "="*50 + "\n"
        content += project['notes']
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            return tmp_file.name, '<div class="status-success">✅ Text file exported</div>'
    
    elif export_type == "audio":
        # Generate TTS audio
        if not project['content'].strip():
            return None, '<div class="status-error">❌ No content to convert to audio</div>'
        
        try:
            tts = gTTS(text=project['content'], lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                return tmp_file.name, '<div class="status-success">✅ Audio file exported</div>'
        except Exception as e:
            return None, f'<div class="status-error">❌ Error generating audio: {str(e)}</div>'
    
    return None, '<div class="status-error">❌ Invalid export type</div>'

# Initialize the Gradio interface
def create_interface():
    """Create the main Gradio interface"""
    
    # Load initial projects
    data = load_projects()
    project_choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    with gr.Blocks(
        title="ScriptVoice - AI-Powered TTS Script Editor", 
        theme=gr.themes.Base(),
        css=CUSTOM_CSS
    ) as app:
        
        # Header with ScriptVoice branding
        gr.HTML("""
        <div class="header-container">
            <div class="script-logo">
                <span class="script-text">Script</span><span class="voice-text">Voice</span>
            </div>
            <div style="text-align: center; color: #888; font-size: 1.1rem; margin-top: 0.5rem;">
                AI-Powered TTS Script Editor
            </div>
        </div>
        """)
        
        with gr.Row():
            # Left Sidebar
            with gr.Column(scale=1, min_width=300, elem_classes=["sidebar-column"]):
                gr.HTML('<div class="section-header">📁 Projects</div>')
                
                # New Project Section
                with gr.Group():
                    new_project_name = gr.Textbox(label="New Project Name", placeholder="Enter project name...")
                    create_btn = gr.Button("➕ Create Project", elem_classes=["primary-button"])
                    create_status = gr.HTML(visible=False)
                
                # Project Selection
                project_dropdown = gr.Dropdown(
                    choices=project_choices,
                    label="Select Project",
                    value=list(data["projects"].keys())[0] if data["projects"] else None
                )
                
                # Notes Section
                gr.HTML('<div class="section-header">📝 Notes</div>')
                notes_textbox = gr.Textbox(
                    label="Project Notes",
                    placeholder="Add your notes here...",
                    lines=5,
                    max_lines=10
                )
                
                # Settings Section
                gr.HTML('<div class="section-header">⚙️ Settings</div>')
                with gr.Group():
                    dyslexic_mode = gr.Checkbox(label="Dyslexic-friendly font", value=False)
                    voice_speed = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Voice Speed")
                    voice_volume = gr.Slider(0.1, 1.0, value=1.0, step=0.1, label="Voice Volume")
            
            # Main Editor Panel
            with gr.Column(scale=2):
                # Word Count Display
                word_count_display = gr.HTML('<div class="word-count-highlight">📊 Word Count: 0</div>')
                
                # Script Editor
                script_textbox = gr.Textbox(
                    label="Script Editor",
                    placeholder="Start writing your script here...",
                    lines=15,
                    max_lines=25
                )
                
                # Control Buttons Row
                with gr.Row():
                    save_btn = gr.Button("💾 Save", elem_classes=["secondary-button"])
                    tts_btn = gr.Button("🔊 Play TTS", elem_classes=["primary-button"])
                    save_status = gr.HTML(visible=False)
                
                # TTS Audio Output
                audio_output = gr.Audio(label="Generated Audio")
                tts_status = gr.HTML(visible=False)
                
                # OCR Section
                with gr.Group():
                    gr.HTML('<div class="section-header">📷 Extract Text from Image</div>')
                    with gr.Row():
                        image_input = gr.Image(type="filepath", label="Upload Image")
                        ocr_btn = gr.Button("Extract Text", elem_classes=["secondary-button"])
                    ocr_status = gr.HTML(visible=False)
                
                # AI Enhancement Section
                with gr.Group():
                    gr.HTML('<div class="section-header">🤖 AI Script Enhancement</div>')
                    with gr.Row():
                        enhancement_type = gr.Dropdown(
                            choices=["dramatic", "romantic", "professional", "casual"],
                            label="Enhancement Style",
                            value="dramatic"
                        )
                        enhance_btn = gr.Button("✨ Enhance Script", elem_classes=["primary-button"])
                    enhance_status = gr.HTML(visible=False)
                
                # Export Section
                with gr.Group():
                    gr.HTML('<div class="section-header">📤 Export</div>')
                    with gr.Row():
                        export_type = gr.Dropdown(
                            choices=["text", "audio"],
                            label="Export Type",
                            value="text"
                        )
                        export_btn = gr.Button("📥 Export", elem_classes=["secondary-button"])
                    export_file = gr.File(label="Download")
                    export_status = gr.HTML(visible=False)
        
        # Event Handlers (keeping all existing functionality)
        
        # Create new project
        create_btn.click(
            fn=create_new_project,
            inputs=[new_project_name],
            outputs=[create_status, project_dropdown]
        ).then(
            lambda: ("", gr.update(visible=True)),
            outputs=[new_project_name, create_status]
        )
        
        # Load project when selected
        project_dropdown.change(
            fn=load_project,
            inputs=[project_dropdown],
            outputs=[script_textbox, notes_textbox, word_count_display]
        )
        
        # Update word count as user types
        script_textbox.change(
            fn=update_word_count,
            inputs=[script_textbox],
            outputs=[word_count_display]
        )
        
        # Save script content
        save_btn.click(
            fn=save_script_content,
            inputs=[project_dropdown, script_textbox, notes_textbox],
            outputs=[save_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[save_status]
        )
        
        # Generate TTS
        tts_btn.click(
            fn=generate_tts,
            inputs=[script_textbox, voice_speed],
            outputs=[audio_output, tts_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[tts_status]
        )
        
        # OCR text extraction
        ocr_btn.click(
            fn=extract_text_from_image,
            inputs=[image_input],
            outputs=[script_textbox, ocr_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[ocr_status]
        )
        
        # AI Enhancement
        enhance_btn.click(
            fn=enhance_script_placeholder,
            inputs=[script_textbox, enhancement_type],
            outputs=[script_textbox, enhance_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[enhance_status]
        )
        
        # Export functionality
        export_btn.click(
            fn=export_project,
            inputs=[project_dropdown, export_type],
            outputs=[export_file, export_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[export_status]
        )
    
    return app

if __name__ == "__main__":
    # Create and launch the app
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
