
"""Main interface factory for ScriptVoice application."""

import gradio as gr
from models import load_projects
from ui_components import CUSTOM_CSS, get_header_html
from interface_components import create_scripts_interface, create_story_intelligence_interface
from mood_board_components import create_mood_board_interface
from database_components import create_database_interface
from event_handlers import display_stories, display_characters, display_world_elements
from event_handlers_scripts import setup_scripts_event_handlers
from event_handlers_story import setup_story_intelligence_event_handlers
from event_handlers_mood_board import setup_mood_board_event_handlers, update_mood_board_dropdowns
from event_handlers_database import setup_database_event_handlers


def create_interface():
    """Create the main Gradio interface with improved UI."""
    
    # Load initial projects
    data = load_projects()
    project_choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    with gr.Blocks(
        title="ScriptVoice - AI-Powered Story Intelligence Platform", 
        theme=gr.themes.Base(),
        css=CUSTOM_CSS + """
        /* Database-specific styles */
        #database-container {
            max-width: 100%;
            margin: 0 auto;
        }
        
        #stats-dashboard {
            min-height: 300px;
        }
        
        #chapters-table {
            font-size: 0.9em;
        }
        
        #chapters-table td {
            padding: 8px 4px;
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        #chapter-search {
            border: 2px solid #ff6b35;
        }
        
        #database-status {
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
        }
        
        .database-btn {
            margin: 5px;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }
        """
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
            
            # Database Tab (New)
            with gr.TabItem("📊 Database", elem_id="database-tab"):
                database_components = create_database_interface()
                
                # Set up event handlers
                setup_database_event_handlers(database_components)
            
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
