
"""Helper functions to get context from story elements."""

import json
from models import load_projects

def get_story_context(story_id):
    """Get story context for image generation."""
    if not story_id:
        return ""
    
    try:
        data = load_projects()
        stories = data.get("stories", {})
        story = stories.get(story_id, {})
        
        title = story.get("title", "")
        description = story.get("description", "")
        
        return f"{title}: {description}" if title and description else title or description
    except:
        return ""

def get_character_context(character_id):
    """Get character context for image generation."""
    if not character_id:
        return ""
    
    try:
        data = load_projects()
        characters = data.get("characters", {})
        character = characters.get(character_id, {})
        
        name = character.get("name", "")
        description = character.get("description", "")
        
        return f"{name}: {description}" if name and description else name or description
    except:
        return ""

def get_world_context(world_id):
    """Get world element context for image generation."""
    if not world_id:
        return ""
    
    try:
        data = load_projects()
        world_elements = data.get("world_elements", {})
        element = world_elements.get(world_id, {})
        
        name = element.get("name", "")
        description = element.get("description", "")
        element_type = element.get("type", "")
        
        context = f"{name}: {description}" if name and description else name or description
        if element_type:
            context = f"{element_type} - {context}"
        
        return context
    except:
        return ""
