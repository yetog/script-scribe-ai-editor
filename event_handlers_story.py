
"""Event handlers for the story intelligence interface."""

import gradio as gr
from models import create_story, create_character, create_world_element
from event_handlers import (
    query_knowledge_assistant, analyze_consistency, suggest_elements,
    enhance_with_context, rebuild_knowledge_index, display_stories,
    display_characters, display_world_elements, perform_search
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
