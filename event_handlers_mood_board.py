
"""Event handlers for the mood board interface."""

import gradio as gr
from mood_board_components import generate_mood_board, save_mood_board, populate_mood_board_dropdowns


def setup_mood_board_event_handlers(mood_board_components):
    """Set up event handlers for the mood board interface."""
    
    # Generate mood board
    mood_board_components['generate_btn'].click(
        fn=generate_mood_board,
        inputs=[
            mood_board_components['story_selector'],
            mood_board_components['character_selector'], 
            mood_board_components['world_selector'],
            mood_board_components['custom_prompt'],
            mood_board_components['style_selector']
        ],
        outputs=[
            mood_board_components['mood_board_gallery'],
            mood_board_components['generation_status']
        ]
    )
    
    # Save mood board
    mood_board_components['save_btn'].click(
        fn=save_mood_board,
        inputs=[
            mood_board_components['mood_board_gallery'],
            mood_board_components['mood_board_name']
        ],
        outputs=[mood_board_components['save_status']]
    ).then(
        lambda: ("", gr.update(visible=True)),
        outputs=[mood_board_components['mood_board_name'], mood_board_components['save_status']]
    )


def update_mood_board_dropdowns():
    """Update mood board dropdowns with current story elements."""
    story_choices, character_choices, world_choices = populate_mood_board_dropdowns()
    return (
        gr.update(choices=story_choices),
        gr.update(choices=character_choices),
        gr.update(choices=world_choices)
    )
