
"""Mood board UI components for Gradio interface."""

import gradio as gr
from image_generation_service import image_generator
from context_helpers import get_story_context, get_character_context, get_world_context
from models import load_projects

def create_mood_board_interface():
    """Create the mood board interface for Gradio."""
    
    with gr.Column():
        gr.HTML('<div class="section-header">🎨 AI Mood Board Generator</div>')
        
        # Context Selection
        with gr.Group():
            gr.HTML('<div class="subsection-header">📚 Story Context</div>')
            
            with gr.Row():
                story_selector = gr.Dropdown(
                    label="Select Story",
                    choices=[],
                    allow_custom_value=True,
                    scale=2
                )
                character_selector = gr.Dropdown(
                    label="Select Character", 
                    choices=[],
                    allow_custom_value=True,
                    scale=2
                )
            
            world_selector = gr.Dropdown(
                label="Select World Element",
                choices=[],
                allow_custom_value=True
            )
        
        # Generation Controls
        with gr.Group():
            gr.HTML('<div class="subsection-header">🎭 Generation Settings</div>')
            
            custom_prompt = gr.Textbox(
                label="Custom Prompt",
                placeholder="Add custom description or let AI use story context...",
                lines=2
            )
            
            with gr.Row():
                style_selector = gr.Dropdown(
                    label="Art Style",
                    choices=["photorealistic", "artistic", "cinematic", "fantasy", "noir"],
                    value="cinematic",
                    scale=2
                )
                generate_btn = gr.Button("🎨 Generate Mood Board", elem_classes=["primary-button"], scale=1)
        
        # Status and Results
        generation_status = gr.HTML(visible=False)
        
        # Image Gallery
        mood_board_gallery = gr.Gallery(
            label="Generated Mood Board",
            show_label=True,
            elem_id="mood-board-gallery",
            columns=2,
            rows=2,
            height=400,
            visible=False
        )
        
        # Save Controls
        with gr.Group():
            gr.HTML('<div class="subsection-header">💾 Save Mood Board</div>')
            
            with gr.Row():
                mood_board_name = gr.Textbox(
                    label="Mood Board Name",
                    placeholder="Enter name to save mood board...",
                    scale=2
                )
                save_btn = gr.Button("💾 Save", elem_classes=["secondary-button"], scale=1)
            
            save_status = gr.HTML(visible=False)
        
        # Saved Mood Boards
        with gr.Accordion("📁 Saved Mood Boards", open=False):
            saved_boards_gallery = gr.Gallery(
                label="Saved Mood Boards",
                show_label=False,
                columns=3,
                rows=2,
                height=300
            )
    
    return {
        'story_selector': story_selector,
        'character_selector': character_selector,
        'world_selector': world_selector,
        'custom_prompt': custom_prompt,
        'style_selector': style_selector,
        'generate_btn': generate_btn,
        'generation_status': generation_status,
        'mood_board_gallery': mood_board_gallery,
        'mood_board_name': mood_board_name,
        'save_btn': save_btn,
        'save_status': save_status,
        'saved_boards_gallery': saved_boards_gallery
    }

def generate_mood_board(story_id, character_id, world_id, custom_prompt, style):
    """Generate mood board images based on selected context."""
    try:
        # Get context from story elements
        story_context = get_story_context(story_id) if story_id else ""
        character_context = get_character_context(character_id) if character_id else ""
        world_context = get_world_context(world_id) if world_id else ""
        
        # Combine contexts
        full_context = custom_prompt
        if not full_context:
            contexts = [ctx for ctx in [story_context, character_context, world_context] if ctx]
            full_context = " | ".join(contexts) if contexts else "Creative story scene"
        
        # Generate images
        if story_context or character_context or world_context:
            images = image_generator.generate_mood_board_images(
                story_context, character_context, world_context
            )
        else:
            # Generate single image with custom prompt
            image_url = image_generator.generate_image(full_context, style)
            images = [image_url] if image_url else []
        
        if images:
            return (
                gr.update(value=images, visible=True),
                gr.update(value="✅ Mood board generated successfully!", visible=True)
            )
        else:
            return (
                gr.update(visible=False),
                gr.update(value="❌ Failed to generate images. Please check your IONOS API configuration.", visible=True)
            )
    
    except Exception as e:
        return (
            gr.update(visible=False),
            gr.update(value=f"❌ Error: {str(e)}", visible=True)
        )

def save_mood_board(images, name):
    """Save mood board with given name."""
    if not images or not name:
        return gr.update(value="❌ Please generate images and provide a name", visible=True)
    
    try:
        import os
        import json
        from datetime import datetime
        
        # Create mood_boards directory if it doesn't exist
        os.makedirs("mood_boards", exist_ok=True)
        
        # Save mood board data
        mood_board_data = {
            "name": name,
            "images": images,
            "created_at": datetime.now().isoformat(),
            "id": str(hash(name + str(datetime.now())))
        }
        
        # Save to JSON file
        mood_board_file = f"mood_boards/{name.replace(' ', '_')}.json"
        with open(mood_board_file, 'w') as f:
            json.dump(mood_board_data, f, indent=2)
        
        return gr.update(value=f"✅ Mood board '{name}' saved successfully!", visible=True)
    except Exception as e:
        return gr.update(value=f"❌ Error saving: {str(e)}", visible=True)

def populate_mood_board_dropdowns():
    """Populate the mood board dropdowns with story elements."""
    try:
        data = load_projects()
        
        # Get stories
        stories = data.get("stories", {})
        story_choices = [(story.get("title", f"Story {story_id}"), story_id) 
                        for story_id, story in stories.items()]
        
        # Get characters
        characters = data.get("characters", {})
        character_choices = [(char.get("name", f"Character {char_id}"), char_id) 
                           for char_id, char in characters.items()]
        
        # Get world elements
        world_elements = data.get("world_elements", {})
        world_choices = [(elem.get("name", f"Element {elem_id}"), elem_id) 
                        for elem_id, elem in world_elements.items()]
        
        return story_choices, character_choices, world_choices
    except:
        return [], [], []
