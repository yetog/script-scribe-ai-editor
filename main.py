
"""Main application entry point for ScriptVoice."""

import gradio as gr
from models import (
    load_projects, create_new_project, load_project, 
    save_script_content, update_word_count
)
from ui_components import CUSTOM_CSS, get_header_html, get_section_header
from audio_services import generate_tts
from image_services import extract_text_from_image
from enhancement_services import enhance_script_placeholder
from export_services import export_project


# Global state for current project
current_project_id = None


def create_interface():
    """Create the main Gradio interface."""
    
    # Load initial projects
    data = load_projects()
    project_choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    with gr.Blocks(
        title="ScriptVoice - AI-Powered TTS Script Editor", 
        theme=gr.themes.Base(),
        css=CUSTOM_CSS
    ) as app:
        
        # Header with ScriptVoice branding
        gr.HTML(get_header_html())
        
        with gr.Row():
            # Left Sidebar
            with gr.Column(scale=1, min_width=300, elem_classes=["sidebar-column"]):
                gr.HTML(get_section_header('📁 Projects'))
                
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
                gr.HTML(get_section_header('📝 Notes'))
                notes_textbox = gr.Textbox(
                    label="Project Notes",
                    placeholder="Add your notes here...",
                    lines=5,
                    max_lines=10
                )
                
                # Settings Section
                gr.HTML(get_section_header('⚙️ Settings'))
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
                    gr.HTML(get_section_header('📷 Extract Text from Image'))
                    with gr.Row():
                        image_input = gr.Image(type="filepath", label="Upload Image")
                        ocr_btn = gr.Button("Extract Text", elem_classes=["secondary-button"])
                    ocr_status = gr.HTML(visible=False)
                
                # AI Enhancement Section
                with gr.Group():
                    gr.HTML(get_section_header('🤖 AI Script Enhancement'))
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
                    gr.HTML(get_section_header('📤 Export'))
                    with gr.Row():
                        export_type = gr.Dropdown(
                            choices=["text", "audio"],
                            label="Export Type",
                            value="text"
                        )
                        export_btn = gr.Button("📥 Export", elem_classes=["secondary-button"])
                    export_file = gr.File(label="Download")
                    export_status = gr.HTML(visible=False)
        
        # Event Handlers
        
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
