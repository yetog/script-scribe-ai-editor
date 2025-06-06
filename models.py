
"""Data models and storage functions for ScriptVoice."""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from config import PROJECTS_FILE
import os

def ensure_projects_file():
    """Ensure the projects file exists with proper structure."""
    if not os.path.exists(PROJECTS_FILE):
        default_data = {
            "projects": {},
            "stories": {},
            "characters": {},
            "world_elements": {}
        }
        save_projects(default_data)
        print(f"Created initial {PROJECTS_FILE}")

def load_projects() -> Dict[str, Any]:
    """Load projects data from JSON file."""
    ensure_projects_file()
    
    try:
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ensure all required keys exist
        required_keys = ["projects", "stories", "characters", "world_elements"]
        for key in required_keys:
            if key not in data:
                data[key] = {}
        
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading projects file: {e}")
        # Return default structure
        return {
            "projects": {},
            "stories": {},
            "characters": {},
            "world_elements": {}
        }

def save_projects(data: Dict[str, Any]) -> bool:
    """Save projects data to JSON file."""
    try:
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving projects: {e}")
        return False

def create_new_project(name: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Create a new project and return status and updated choices."""
    if not name.strip():
        return "❌ Project name cannot be empty.", []
    
    data = load_projects()
    project_id = str(uuid.uuid4())
    
    # Check if project name already exists
    for proj in data["projects"].values():
        if proj["name"].lower() == name.strip().lower():
            return "❌ Project name already exists.", [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    data["projects"][project_id] = {
        "name": name.strip(),
        "content": "",
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    if save_projects(data):
        # Update RAG index
        try:
            from rag_services import rag_service
            rag_service.add_content("", "script", project_id, name.strip())
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
        return f"✅ Project '{name}' created successfully!", choices
    else:
        return "❌ Error saving project.", []

def load_project(project_id: str) -> Tuple[str, str, str]:
    """Load a specific project's content."""
    if not project_id:
        return "", "", "No words"
    
    data = load_projects()
    project = data["projects"].get(project_id, {})
    
    content = project.get("content", "")
    notes = project.get("notes", "")
    word_count = len(content.split()) if content else 0
    
    return content, notes, f"{word_count} words"

def save_script_content(project_id: str, content: str, notes: str) -> str:
    """Save script content and notes."""
    if not project_id:
        return "❌ No project selected."
    
    data = load_projects()
    if project_id not in data["projects"]:
        return "❌ Project not found."
    
    data["projects"][project_id]["content"] = content
    data["projects"][project_id]["notes"] = notes
    data["projects"][project_id]["updated_at"] = datetime.now().isoformat()
    
    if save_projects(data):
        # Update RAG index
        try:
            from rag_services import rag_service
            project_name = data["projects"][project_id]["name"]
            full_content = f"{project_name}\n\n{content}\n\nNotes: {notes}"
            rag_service.add_content(full_content, "script", project_id, project_name)
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        return "✅ Project saved successfully!"
    else:
        return "❌ Error saving project."

def update_word_count(content: str) -> str:
    """Update word count display."""
    word_count = len(content.split()) if content else 0
    return f"{word_count} words"

# Story, Character, and World Element functions
def create_story(title: str, description: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Create a new story."""
    if not title.strip():
        return "❌ Story title cannot be empty.", []
    
    data = load_projects()
    story_id = str(uuid.uuid4())
    
    data["stories"][story_id] = {
        "title": title.strip(),
        "description": description.strip(),
        "content": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    if save_projects(data):
        # Update RAG index
        try:
            from rag_services import rag_service
            content = f"{title}\n\n{description}"
            rag_service.add_content(content, "story", story_id, title)
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        choices = [(story["title"], story_id) for story_id, story in data["stories"].items()]
        return f"✅ Story '{title}' created successfully!", choices
    else:
        return "❌ Error saving story.", []

def create_character(name: str, description: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Create a new character."""
    if not name.strip():
        return "❌ Character name cannot be empty.", []
    
    data = load_projects()
    char_id = str(uuid.uuid4())
    
    data["characters"][char_id] = {
        "name": name.strip(),
        "description": description.strip(),
        "traits": [],
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    if save_projects(data):
        # Update RAG index
        try:
            from rag_services import rag_service
            content = f"{name}\n\n{description}"
            rag_service.add_content(content, "character", char_id, name)
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        choices = [(char["name"], char_id) for char_id, char in data["characters"].items()]
        return f"✅ Character '{name}' created successfully!", choices
    else:
        return "❌ Error saving character.", []

def create_world_element(name: str, element_type: str, description: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Create a new world element."""
    if not name.strip():
        return "❌ Element name cannot be empty.", []
    
    data = load_projects()
    elem_id = str(uuid.uuid4())
    
    data["world_elements"][elem_id] = {
        "name": name.strip(),
        "type": element_type,
        "description": description.strip(),
        "tags": [],
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    if save_projects(data):
        # Update RAG index
        try:
            from rag_services import rag_service
            content = f"{name} ({element_type})\n\n{description}"
            rag_service.add_content(content, "world_element", elem_id, name)
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        choices = [(elem["name"], elem_id) for elem_id, elem in data["world_elements"].items()]
        return f"✅ World element '{name}' created successfully!", choices
    else:
        return "❌ Error saving world element.", []

def get_all_stories() -> List[Dict[str, Any]]:
    """Get all stories."""
    data = load_projects()
    return list(data["stories"].values())

def get_all_characters() -> List[Dict[str, Any]]:
    """Get all characters."""
    data = load_projects()
    return list(data["characters"].values())

def get_all_world_elements() -> List[Dict[str, Any]]:
    """Get all world elements."""
    data = load_projects()
    return list(data["world_elements"].values())

def search_content(query: str) -> Dict[str, List[Dict[str, Any]]]:
    """Search across all content types."""
    if not query.strip():
        return {"stories": [], "characters": [], "world_elements": []}
    
    data = load_projects()
    query_lower = query.lower()
    
    results = {
        "stories": [],
        "characters": [],
        "world_elements": []
    }
    
    # Search stories
    for story in data["stories"].values():
        if (query_lower in story["title"].lower() or 
            query_lower in story["description"].lower() or
            query_lower in story.get("content", "").lower()):
            results["stories"].append(story)
    
    # Search characters
    for char in data["characters"].values():
        if (query_lower in char["name"].lower() or 
            query_lower in char["description"].lower() or
            query_lower in char.get("notes", "").lower()):
            results["characters"].append(char)
    
    # Search world elements
    for elem in data["world_elements"].values():
        if (query_lower in elem["name"].lower() or 
            query_lower in elem["description"].lower() or
            query_lower in elem.get("notes", "").lower()):
            results["world_elements"].append(elem)
    
    return results
