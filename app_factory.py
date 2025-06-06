
"""Main application factory for ScriptVoice."""

import gradio as gr
from models import (
    load_projects, create_new_project, load_project, 
    save_script_content, update_word_count,
    create_story, create_character, create_world_element
)
from ui_components import CUSTOM_CSS, get_header_html
from enhancement_services import enhance_script_placeholder
from export_services import export_project
from interface_components import create_scripts_interface, create_story_intelligence_interface
from event_handlers import (
    query_knowledge_assistant, analyze_consistency, suggest_elements,
    enhance_with_context, rebuild_knowledge_index, display_stories,
    display_characters, display_world_elements, perform_search,
    enhanced_generate_tts, enhanced_extract_text
)


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


def setup_story_intelligence_event_handlers(story_components):
    """Set up event handlers for the story intelligence interface."""
    
    # Knowledge assistant
    story_components['assistant_btn'].click(
        fn=query_knowledge_assistant,
        inputs=[story_components['assistant_query']],
        outputs=[story_components['assistant_response'], story_components['assistant_response']]
    )
    
    # AI analysis tools
    story_components['consistency_btn'].click(
        fn=analyze_consistency,
        inputs=[story_components['ai_analysis_text']],
        outputs=[story_components['ai_analysis_output'], story_components['ai_analysis_output']]
    )
    
    story_components['suggest_btn'].click(
        fn=suggest_elements,
        inputs=[story_components['ai_analysis_text']],
        outputs=[story_components['ai_analysis_output'], story_components['ai_analysis_output']]
    )
    
    story_components['context_enhance_btn'].click(
        fn=enhance_with_context,
        inputs=[story_components['ai_analysis_text'], story_components['context_enhancement_type']],
        outputs=[story_components['ai_analysis_output'], story_components['ai_analysis_output']]
    )
    
    # Knowledge base management
    story_components['rebuild_btn'].click(
        fn=rebuild_knowledge_index,
        outputs=[story_components['rebuild_status'], story_components['rebuild_status']]
    )
    
    # Story creation
    story_components['create_story_btn'].click(
        fn=create_story,
        inputs=[story_components['new_story_title'], story_components['new_story_desc']],
        outputs=[story_components['story_status'], story_components['story_dropdown']]
    ).then(
        lambda: ("", "", gr.update(visible=True)),
        outputs=[story_components['new_story_title'], story_components['new_story_desc'], story_components['story_status']]
    ).then(
        fn=display_stories,
        outputs=[story_components['stories_display']]
    )
    
    # Character creation
    story_components['create_char_btn'].click(
        fn=create_character,
        inputs=[story_components['new_char_name'], story_components['new_char_desc']],
        outputs=[story_components['char_status'], story_components['character_dropdown']]
    ).then(
        lambda: ("", "", gr.update(visible=True)),
        outputs=[story_components['new_char_name'], story_components['new_char_desc'], story_components['char_status']]
    ).then(
        fn=display_characters,
        outputs=[story_components['characters_display']]
    )
    
    # World element creation
    story_components['create_world_btn'].click(
        fn=create_world_element,
        inputs=[story_components['new_world_name'], story_components['world_type'], story_components['new_world_desc']],
        outputs=[story_components['world_status'], story_components['world_dropdown']]
    ).then(
        lambda: ("", "", gr.update(visible=True)),
        outputs=[story_components['new_world_name'], story_components['new_world_desc'], story_components['world_status']]
    ).then(
        fn=display_world_elements,
        outputs=[story_components['world_display']]
    )
    
    # Search functionality
    story_components['search_btn'].click(
        fn=perform_search,
        inputs=[story_components['search_input']],
        outputs=[story_components['search_results']]
    )


def create_interface():
    """Create the main Gradio interface with improved UI."""
    
    # Load initial projects
    data = load_projects()
    project_choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    with gr.Blocks(
        title="ScriptVoice - AI-Powered Story Intelligence Platform", 
        theme=gr.themes.Base(),
        css=CUSTOM_CSS
    ) as app:
        
        # Header
        gr.HTML(get_header_html())
        
        # Main interface with improved tabs
        with gr.Tabs() as main_tabs:
            # Scripts Tab (Redesigned)
            with gr.TabItem("📝 Scripts", elem_id="scripts-tab"):
                scripts_components = create_scripts_interface()
                
                # Set initial project choices
                scripts_components['project_dropdown'].choices = project_choices
                if project_choices:
                    scripts_components['project_dropdown'].value = project_choices[0][1]
                
                # Set up event handlers
                setup_scripts_event_handlers(scripts_components)
            
            # Story Intelligence Tab (Redesigned)
            with gr.TabItem("📚 Story Intelligence", elem_id="intelligence-tab"):
                story_components = create_story_intelligence_interface()
                
                # Set up event handlers
                setup_story_intelligence_event_handlers(story_components)
        
        # Load initial data
        app.load(
            fn=display_stories,
            outputs=[story_components['stories_display']]
        )
        app.load(
            fn=display_characters,
            outputs=[story_components['characters_display']]
        )
        app.load(
            fn=display_world_elements,
            outputs=[story_components['world_display']]
        )
    
    return app
