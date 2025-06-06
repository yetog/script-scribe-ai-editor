
"""Event handlers for the scripts interface."""

import gradio as gr
from models import (
    create_new_project, load_project, save_script_content, update_word_count
)
from enhancement_services import enhance_script_placeholder
from export_services import export_project
from event_handlers import enhanced_generate_tts, enhanced_extract_text


def setup_scripts_event_handlers(scripts_components):
    """Set up event handlers for the scripts interface."""
    
    # Project creation
    scripts_components['create_btn'].click(
        fn=create_new_project,
        inputs=[scripts_components['new_project_name']],
        outputs=[scripts_components['create_status'], scripts_components['project_dropdown']]
    ).then(
        lambda: ("", gr.update(visible=True)),
        outputs=[scripts_components['new_project_name'], scripts_components['create_status']]
    )
    
    # Project loading
    scripts_components['project_dropdown'].change(
        fn=load_project,
        inputs=[scripts_components['project_dropdown']],
        outputs=[scripts_components['script_textbox'], scripts_components['notes_textbox'], scripts_components['word_count_display']]
    )
    
    # Word count update
    scripts_components['script_textbox'].change(
        fn=update_word_count,
        inputs=[scripts_components['script_textbox']],
        outputs=[scripts_components['word_count_display']]
    )
    
    # Save functionality
    scripts_components['save_btn'].click(
        fn=save_script_content,
        inputs=[scripts_components['project_dropdown'], scripts_components['script_textbox'], scripts_components['notes_textbox']],
        outputs=[scripts_components['save_status']]
    ).then(
        lambda: gr.update(visible=True),
        outputs=[scripts_components['save_status']]
    )
    
    # TTS functionality
    scripts_components['tts_btn'].click(
        fn=enhanced_generate_tts,
        inputs=[scripts_components['script_textbox'], scripts_components['voice_speed']],
        outputs=[scripts_components['audio_output'], scripts_components['tts_status']]
    ).then(
        lambda: (gr.update(visible=True), gr.update(visible=True)),
        outputs=[scripts_components['audio_output'], scripts_components['tts_status']]
    )
    
    # OCR functionality
    scripts_components['ocr_btn'].click(
        fn=enhanced_extract_text,
        inputs=[scripts_components['image_input']],
        outputs=[scripts_components['script_textbox'], scripts_components['ocr_status']]
    ).then(
        lambda: gr.update(visible=True),
        outputs=[scripts_components['ocr_status']]
    )
    
    # Enhancement functionality
    scripts_components['enhance_btn'].click(
        fn=enhance_script_placeholder,
        inputs=[scripts_components['script_textbox'], scripts_components['enhancement_type']],
        outputs=[scripts_components['script_textbox'], scripts_components['enhance_status']]
    ).then(
        lambda: gr.update(visible=True),
        outputs=[scripts_components['enhance_status']]
    )
    
    # Export functionality
    scripts_components['export_btn'].click(
        fn=export_project,
        inputs=[scripts_components['project_dropdown'], scripts_components['export_type']],
        outputs=[scripts_components['export_file'], scripts_components['export_status']]
    ).then(
        lambda: (gr.update(visible=True), gr.update(visible=True)),
        outputs=[scripts_components['export_file'], scripts_components['export_status']]
    )
