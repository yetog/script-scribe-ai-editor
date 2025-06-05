
"""Data models and project management for ScriptVoice."""

import json
import os
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List
from config import PROJECTS_FILE


# Story Intelligence Data Models
class Character:
    def __init__(self, id: str, name: str, description: str = "", traits: List[str] = None, relationships: Dict[str, str] = None, notes: str = ""):
        self.id = id
        self.name = name
        self.description = description
        self.traits = traits or []
        self.relationships = relationships or {}
        self.notes = notes
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

class WorldElement:
    def __init__(self, id: str, name: str, type: str, description: str = "", tags: List[str] = None, notes: str = ""):
        self.id = id
        self.name = name
        self.type = type  # location, organization, concept, item
        self.description = description
        self.tags = tags or []
        self.notes = notes
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

class Scene:
    def __init__(self, id: str, title: str, content: str = "", characters: List[str] = None, order: int = 0):
        self.id = id
        self.title = title
        self.content = content
        self.characters = characters or []
        self.order = order

class Chapter:
    def __init__(self, id: str, title: str, content: str = "", scenes: List[Scene] = None, order: int = 0):
        self.id = id
        self.title = title
        self.content = content
        self.scenes = scenes or []
        self.order = order

class Story:
    def __init__(self, id: str, title: str, description: str = "", content: str = "", tags: List[str] = None, characters: List[str] = None, world_elements: List[str] = None, chapters: List[Chapter] = None):
        self.id = id
        self.title = title
        self.description = description
        self.content = content
        self.tags = tags or []
        self.characters = characters or []
        self.world_elements = world_elements or []
        self.chapters = chapters or []
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()


def load_projects() -> Dict[str, Any]:
    """Load projects from JSON file."""
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            data = json.load(f)
            # Ensure new story intelligence fields exist
            if "stories" not in data:
                data["stories"] = {}
            if "characters" not in data:
                data["characters"] = {}
            if "world_elements" not in data:
                data["world_elements"] = {}
            return data
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
        "stories": {},
        "characters": {},
        "world_elements": {},
        "settings": {
            "dyslexic_mode": False,
            "voice_speed": 1.0,
            "voice_volume": 1.0
        }
    }


def save_projects(data: Dict[str, Any]) -> None:
    """Save projects to JSON file."""
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# ... keep existing code (get_word_count, update_word_count, create_new_project, load_project, save_script_content functions)


# Story Management Functions
def create_story(title: str, description: str = "") -> Tuple[str, Any]:
    """Create a new story."""
    if not title.strip():
        return '<div class="status-error">❌ Please enter a story title</div>', None
    
    data = load_projects()
    new_id = str(len(data["stories"]) + 1)
    
    story_data = {
        "id": new_id,
        "title": title.strip(),
        "description": description,
        "content": "",
        "tags": [],
        "characters": [],
        "world_elements": [],
        "chapters": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    data["stories"][new_id] = story_data
    save_projects(data)
    
    import gradio as gr
    choices = [(story["title"], story_id) for story_id, story in data["stories"].items()]
    return f'<div class="status-success">✅ Story "{title}" created successfully!</div>', gr.update(choices=choices, value=new_id)


def create_character(name: str, description: str = "") -> Tuple[str, Any]:
    """Create a new character."""
    if not name.strip():
        return '<div class="status-error">❌ Please enter a character name</div>', None
    
    data = load_projects()
    new_id = str(len(data["characters"]) + 1)
    
    character_data = {
        "id": new_id,
        "name": name.strip(),
        "description": description,
        "traits": [],
        "relationships": {},
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    data["characters"][new_id] = character_data
    save_projects(data)
    
    import gradio as gr
    choices = [(char["name"], char_id) for char_id, char in data["characters"].items()]
    return f'<div class="status-success">✅ Character "{name}" created successfully!</div>', gr.update(choices=choices, value=new_id)


def create_world_element(name: str, element_type: str, description: str = "") -> Tuple[str, Any]:
    """Create a new world element."""
    if not name.strip():
        return '<div class="status-error">❌ Please enter an element name</div>', None
    
    data = load_projects()
    new_id = str(len(data["world_elements"]) + 1)
    
    element_data = {
        "id": new_id,
        "name": name.strip(),
        "type": element_type,
        "description": description,
        "tags": [],
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    data["world_elements"][new_id] = element_data
    save_projects(data)
    
    import gradio as gr
    choices = [(elem["name"], elem_id) for elem_id, elem in data["world_elements"].items()]
    return f'<div class="status-success">✅ World element "{name}" created successfully!</div>', gr.update(choices=choices, value=new_id)


def get_all_stories() -> List[Dict]:
    """Get all stories."""
    data = load_projects()
    return list(data["stories"].values())


def get_all_characters() -> List[Dict]:
    """Get all characters."""
    data = load_projects()
    return list(data["characters"].values())


def get_all_world_elements() -> List[Dict]:
    """Get all world elements."""
    data = load_projects()
    return list(data["world_elements"].values())


def search_content(query: str) -> Dict[str, List[Dict]]:
    """Search across stories, characters, and world elements."""
    data = load_projects()
    query_lower = query.lower()
    
    stories = [story for story in data["stories"].values() 
               if query_lower in story["title"].lower() or 
                  query_lower in story["description"].lower() or
                  query_lower in story["content"].lower()]
    
    characters = [char for char in data["characters"].values()
                  if query_lower in char["name"].lower() or
                     query_lower in char["description"].lower()]
    
    world_elements = [elem for elem in data["world_elements"].values()
                      if query_lower in elem["name"].lower() or
                         query_lower in elem["description"].lower()]
    
    return {
        "stories": stories,
        "characters": characters,
        "world_elements": world_elements
    }


def get_word_count(text: str) -> int:
    """Count words in text."""
    if not text:
        return 0
    return len(text.split())


def update_word_count(text: str) -> str:
    """Update word count display with gold highlighting."""
    count = get_word_count(text)
    return f'<div class="word-count-highlight">📊 Word Count: {count}</div>'


def create_new_project(name: str) -> Tuple[str, Optional[Any]]:
    """Create a new project."""
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
    import gradio as gr
    choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    return f'<div class="status-success">✅ Project "{name}" created successfully!</div>', gr.update(choices=choices, value=new_id)


def load_project(project_id: str) -> Tuple[str, str, str]:
    """Load a specific project."""
    if not project_id:
        return "", "", '<div class="word-count-highlight">📊 Word Count: 0</div>'
    
    data = load_projects()
    if project_id in data["projects"]:
        project = data["projects"][project_id]
        word_count = get_word_count(project["content"])
        return project["content"], project["notes"], f'<div class="word-count-highlight">📊 Word Count: {word_count}</div>'
    
    return "", "", '<div class="word-count-highlight">📊 Word Count: 0</div>'


def save_script_content(project_id: str, content: str, notes: str) -> str:
    """Save script content and notes."""
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
