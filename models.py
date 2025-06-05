
"""Data models and project management for ScriptVoice."""

import json
import os
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from config import PROJECTS_FILE


def load_projects() -> Dict[str, Any]:
    """Load projects from JSON file."""
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            return json.load(f)
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
