
"""Main interface factory for ScriptVoice application."""

import gradio as gr
from models import load_projects
from ui_components import CUSTOM_CSS, get_header_html
from interface_components import create_scripts_interface, create_story_intelligence_interface
from mood_board_components import create_mood_board_interface
from event_handlers import display_stories, display_characters, display_world_elements
from event_handlers_scripts import setup_scripts_event_handlers
from event_handlers_story import setup_story_intelligence_event_handlers
from event_handlers_mood_board import setup_mood_board_event_handlers, update_mood_board_dropdowns


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
            
            # Mood Board Tab (New)
            with gr.TabItem("🎨 Mood Board", elem_id="mood-board-tab"):
                mood_board_components = create_mood_board_interface()
                
                # Set up event handlers
                setup_mood_board_event_handlers(mood_board_components)
        
        # Load initial data for all tabs
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
        
        # Load mood board dropdown data
        app.load(
            fn=update_mood_board_dropdowns,
            outputs=[
                mood_board_components['story_selector'],
                mood_board_components['character_selector'],
                mood_board_components['world_selector']
            ]
        )
        
        # Update mood board dropdowns when stories/characters are created
        story_components['create_story_btn'].click(
            fn=update_mood_board_dropdowns,
            outputs=[
                mood_board_components['story_selector'],
                mood_board_components['character_selector'],
                mood_board_components['world_selector']
            ]
        )
        
        story_components['create_char_btn'].click(
            fn=update_mood_board_dropdowns,
            outputs=[
                mood_board_components['story_selector'],
                mood_board_components['character_selector'],
                mood_board_components['world_selector']
            ]
        )
        
        story_components['create_world_btn'].click(
            fn=update_mood_board_dropdowns,
            outputs=[
                mood_board_components['story_selector'],
                mood_board_components['character_selector'],
                mood_board_components['world_selector']
            ]
        )
    
    return app
