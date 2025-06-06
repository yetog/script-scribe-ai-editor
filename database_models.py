
"""Database models for chapter, act, and scene management."""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from models import load_projects, save_projects
from rag_services import rag_service


def create_chapter(story_id: str, act_number: int, block_number: int, title: str, outline: str = "", characters: List[str] = None, location: str = "", status: str = "Not Started", notes: str = "") -> Tuple[str, Dict[str, Any]]:
    """Create a new chapter within a story."""
    if not title.strip():
        return "❌ Chapter title cannot be empty.", {}
    
    data = load_projects()
    
    # Ensure chapters structure exists
    if "chapters" not in data:
        data["chapters"] = {}
    
    chapter_id = str(uuid.uuid4())
    characters_list = characters or []
    
    chapter = {
        "id": chapter_id,
        "story_id": story_id,
        "act_number": act_number,
        "block_number": block_number,
        "chapter_number": len([c for c in data["chapters"].values() if c.get("story_id") == story_id and c.get("act_number") == act_number]) + 1,
        "title": title.strip(),
        "outline": outline.strip(),
        "content": "",
        "characters": characters_list,
        "location": location.strip(),
        "status": status,
        "notes": notes.strip(),
        "scenes": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    data["chapters"][chapter_id] = chapter
    
    if save_projects(data):
        # Add to vector storage for semantic search
        try:
            story_title = ""
            if story_id and story_id in data.get("stories", {}):
                story_title = data["stories"][story_id]["title"]
            
            content_for_rag = f"Chapter {chapter['chapter_number']}: {title}\n\nStory: {story_title}\nAct {act_number}, Block {block_number}\n\nOutline: {outline}\n\nLocation: {location}\nCharacters: {', '.join(characters_list)}\n\nNotes: {notes}"
            rag_service.add_content(content_for_rag, "chapter", chapter_id, f"{story_title} - Chapter {chapter['chapter_number']}: {title}")
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        return f"✅ Chapter '{title}' created successfully!", chapter
    else:
        return "❌ Error saving chapter.", {}


def update_chapter(chapter_id: str, updates: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Update an existing chapter."""
    data = load_projects()
    
    if "chapters" not in data or chapter_id not in data["chapters"]:
        return "❌ Chapter not found.", {}
    
    chapter = data["chapters"][chapter_id]
    chapter.update(updates)
    chapter["updated_at"] = datetime.now().isoformat()
    
    if save_projects(data):
        # Update vector storage
        try:
            story_title = ""
            if chapter.get("story_id") and chapter["story_id"] in data.get("stories", {}):
                story_title = data["stories"][chapter["story_id"]]["title"]
            
            content_for_rag = f"Chapter {chapter['chapter_number']}: {chapter['title']}\n\nStory: {story_title}\nAct {chapter['act_number']}, Block {chapter['block_number']}\n\nOutline: {chapter['outline']}\n\nLocation: {chapter['location']}\nCharacters: {', '.join(chapter.get('characters', []))}\n\nNotes: {chapter['notes']}"
            rag_service.add_content(content_for_rag, "chapter", chapter_id, f"{story_title} - Chapter {chapter['chapter_number']}: {chapter['title']}")
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        return "✅ Chapter updated successfully!", chapter
    else:
        return "❌ Error updating chapter.", {}


def delete_chapter(chapter_id: str) -> str:
    """Delete a chapter."""
    data = load_projects()
    
    if "chapters" not in data or chapter_id not in data["chapters"]:
        return "❌ Chapter not found."
    
    chapter_title = data["chapters"][chapter_id]["title"]
    del data["chapters"][chapter_id]
    
    if save_projects(data):
        # Remove from vector storage
        try:
            rag_service.remove_content(chapter_id)
        except Exception as e:
            print(f"Warning: Could not remove from RAG index: {e}")
        
        return f"✅ Chapter '{chapter_title}' deleted successfully!"
    else:
        return "❌ Error deleting chapter."


def get_chapters_for_story(story_id: str) -> List[Dict[str, Any]]:
    """Get all chapters for a specific story, sorted by act, block, and chapter number."""
    data = load_projects()
    
    if "chapters" not in data:
        return []
    
    chapters = [c for c in data["chapters"].values() if c.get("story_id") == story_id]
    chapters.sort(key=lambda x: (x.get("act_number", 0), x.get("block_number", 0), x.get("chapter_number", 0)))
    
    return chapters


def get_all_chapters() -> List[Dict[str, Any]]:
    """Get all chapters across all stories."""
    data = load_projects()
    
    if "chapters" not in data:
        return []
    
    chapters = list(data["chapters"].values())
    chapters.sort(key=lambda x: (x.get("story_id", ""), x.get("act_number", 0), x.get("block_number", 0), x.get("chapter_number", 0)))
    
    return chapters


def search_chapters(query: str) -> List[Dict[str, Any]]:
    """Search chapters using both text and semantic search."""
    # Text-based search in local data
    data = load_projects()
    text_results = []
    
    if "chapters" in data:
        query_lower = query.lower()
        for chapter in data["chapters"].values():
            if (query_lower in chapter.get("title", "").lower() or 
                query_lower in chapter.get("outline", "").lower() or
                query_lower in chapter.get("notes", "").lower() or
                query_lower in chapter.get("location", "").lower()):
                text_results.append(chapter)
    
    # Semantic search using RAG
    try:
        semantic_results = rag_service.search(query, k=10, content_type="chapter")
        semantic_chapter_ids = [r["metadata"].get("content_id") for r in semantic_results if r["metadata"].get("content_id")]
        
        # Combine results, prioritizing semantic search
        combined_results = []
        added_ids = set()
        
        # Add semantic results first
        for chapter in data.get("chapters", {}).values():
            if chapter["id"] in semantic_chapter_ids and chapter["id"] not in added_ids:
                combined_results.append(chapter)
                added_ids.add(chapter["id"])
        
        # Add text results that weren't already included
        for chapter in text_results:
            if chapter["id"] not in added_ids:
                combined_results.append(chapter)
                added_ids.add(chapter["id"])
        
        return combined_results
    except Exception as e:
        print(f"Warning: Semantic search failed: {e}")
        return text_results


def get_chapter_statistics() -> Dict[str, Any]:
    """Get statistics about chapters and progress."""
    data = load_projects()
    
    if "chapters" not in data:
        return {"total": 0, "by_status": {}, "by_story": {}}
    
    chapters = list(data["chapters"].values())
    
    stats = {
        "total": len(chapters),
        "by_status": {},
        "by_story": {},
        "by_act": {}
    }
    
    # Count by status
    for chapter in chapters:
        status = chapter.get("status", "Not Started")
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
    
    # Count by story
    for chapter in chapters:
        story_id = chapter.get("story_id", "Unknown")
        story_title = "Unknown Story"
        if story_id in data.get("stories", {}):
            story_title = data["stories"][story_id]["title"]
        
        stats["by_story"][story_title] = stats["by_story"].get(story_title, 0) + 1
    
    # Count by act
    for chapter in chapters:
        act = f"Act {chapter.get('act_number', 'Unknown')}"
        stats["by_act"][act] = stats["by_act"].get(act, 0) + 1
    
    return stats


def bulk_update_chapters(chapter_ids: List[str], updates: Dict[str, Any]) -> str:
    """Bulk update multiple chapters."""
    data = load_projects()
    updated_count = 0
    
    if "chapters" not in data:
        return "❌ No chapters found."
    
    for chapter_id in chapter_ids:
        if chapter_id in data["chapters"]:
            data["chapters"][chapter_id].update(updates)
            data["chapters"][chapter_id]["updated_at"] = datetime.now().isoformat()
            updated_count += 1
    
    if save_projects(data):
        # Update vector storage for all modified chapters
        try:
            for chapter_id in chapter_ids:
                if chapter_id in data["chapters"]:
                    chapter = data["chapters"][chapter_id]
                    story_title = ""
                    if chapter.get("story_id") and chapter["story_id"] in data.get("stories", {}):
                        story_title = data["stories"][chapter["story_id"]]["title"]
                    
                    content_for_rag = f"Chapter {chapter['chapter_number']}: {chapter['title']}\n\nStory: {story_title}\nAct {chapter['act_number']}, Block {chapter['block_number']}\n\nOutline: {chapter['outline']}\n\nLocation: {chapter['location']}\nCharacters: {', '.join(chapter.get('characters', []))}\n\nNotes: {chapter['notes']}"
                    rag_service.add_content(content_for_rag, "chapter", chapter_id, f"{story_title} - Chapter {chapter['chapter_number']}: {chapter['title']}")
        except Exception as e:
            print(f"Warning: Could not update RAG index: {e}")
        
        return f"✅ Updated {updated_count} chapters successfully!"
    else:
        return "❌ Error updating chapters."
