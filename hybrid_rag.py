
"""Hybrid RAG service combining IONOS and local storage for ScriptVoice."""

from typing import List, Dict, Any, Optional
from ionos_collections import ionos_collections
from vector_storage import LocalVectorStorage


class HybridRAGService:
    """Handles both local and IONOS vector database operations."""
    
    def __init__(self, use_ionos: bool = True):
        self.use_ionos = use_ionos and ionos_collections.is_available()
        self.local_storage = LocalVectorStorage()
        
        if self.use_ionos:
            print("Using IONOS Document Collections for RAG")
            # Initialize IONOS collections on startup
            self._ensure_ionos_collections()
        else:
            print("Using local vector storage for RAG")
    
    def _ensure_ionos_collections(self):
        """Ensure required IONOS collections exist."""
        collections = ["stories", "characters", "world_elements", "scripts"]
        for collection_name in collections:
            ionos_collections.get_collection_id(collection_name)
    
    def add_content(self, content: str, content_type: str, content_id: str, title: str):
        """Add content to the vector database (IONOS or local)."""
        if not content.strip():
            return
        
        if self.use_ionos:
            self._add_content_ionos(content, content_type, content_id, title)
        else:
            self.local_storage.add_content(content, content_type, content_id, title)
    
    def _add_content_ionos(self, content: str, content_type: str, content_id: str, title: str):
        """Add content to IONOS collections."""
        # Remove existing content first
        self.remove_content(content_id)
        
        # Determine collection name
        collection_map = {
            "story": "stories",
            "character": "characters", 
            "world_element": "world_elements",
            "script": "scripts"
        }
        collection_name = collection_map.get(content_type, "stories")
        
        # Add metadata
        metadata = {
            "content_type": content_type,
            "content_id": content_id,
            "title": title
        }
        
        ionos_collections.add_document(collection_name, content, title, metadata)
    
    def remove_content(self, content_id: str):
        """Remove content from vector database."""
        # Always try to remove from local storage
        self.local_storage.remove_content(content_id)
        
        # IONOS removal would need to be implemented in ionos_collections
        # For now, we don't remove from IONOS as documents are replaced when re-added
    
    def search(self, query: str, k: int = 5, content_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for similar content (IONOS or local)."""
        if self.use_ionos:
            return self._search_ionos(query, k, content_type)
        else:
            return self.local_storage.search(query, k, content_type)
    
    def _search_ionos(self, query: str, k: int, content_type: Optional[str]) -> List[Dict[str, Any]]:
        """Search using IONOS collections."""
        if content_type:
            # Search specific collection
            collection_map = {
                "story": "stories",
                "character": "characters",
                "world_element": "world_elements", 
                "script": "scripts"
            }
            collection_name = collection_map.get(content_type, "stories")
            return ionos_collections.query_collection(collection_name, query, k)
        else:
            # Search all collections and combine results
            all_results = []
            collections = ["stories", "characters", "world_elements", "scripts"]
            
            for collection_name in collections:
                results = ionos_collections.query_collection(collection_name, query, k//len(collections) + 1)
                all_results.extend(results)
            
            # Sort by score and return top k
            all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
            return all_results[:k]
    
    def get_context_for_content(self, content_id: str, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Get relevant context from other content for a specific item."""
        results = self.search(query, k=k)
        # Filter out results from the same content
        filtered_results = [r for r in results if r['metadata'].get('content_id') != content_id]
        return filtered_results[:k]
    
    def get_enhanced_context(self, query: str, content_type: Optional[str] = None) -> str:
        """Get enhanced context using IONOS automated RAG if available."""
        if self.use_ionos and content_type:
            # Use IONOS automated RAG for better context
            results = self._search_ionos(query, 3, content_type)
            if results:
                context_parts = []
                for result in results:
                    title = result['metadata'].get('title', 'Untitled')
                    content = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                    context_parts.append(f"[{title}]: {content}")
                return "\n\n".join(context_parts)
        
        # Fallback to regular search
        results = self.search(query, 3, content_type)
        if results:
            context_parts = []
            for result in results:
                title = result['metadata'].get('title', 'Untitled')
                content = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                context_parts.append(f"[{title}]: {content}")
            return "\n\n".join(context_parts)
        
        return "No relevant context found."
    
    def sync_to_ionos(self):
        """Sync local data to IONOS collections."""
        if ionos_collections.is_available():
            ionos_collections.sync_projects_to_collections()
    
    def rebuild_index_from_projects(self):
        """Rebuild the entire vector index from current projects data."""
        if self.use_ionos:
            self.sync_to_ionos()
        else:
            self._rebuild_local_index()
    
    def _rebuild_local_index(self):
        """Rebuild local index from projects data."""
        from models import load_projects
        
        # Clear existing index
        self.local_storage.clear_and_rebuild()
        
        # Load all projects data
        data = load_projects()
        
        # Add stories
        for story_id, story in data.get("stories", {}).items():
            content = f"{story['title']}\n\n{story['description']}\n\n{story['content']}"
            self.local_storage.add_content(content, "story", story_id, story['title'])
        
        # Add characters
        for char_id, char in data.get("characters", {}).items():
            content = f"{char['name']}\n\n{char['description']}\n\nTraits: {', '.join(char.get('traits', []))}\n\n{char.get('notes', '')}"
            self.local_storage.add_content(content, "character", char_id, char['name'])
        
        # Add world elements
        for elem_id, elem in data.get("world_elements", {}).items():
            content = f"{elem['name']} ({elem['type']})\n\n{elem['description']}\n\nTags: {', '.join(elem.get('tags', []))}\n\n{elem.get('notes', '')}"
            self.local_storage.add_content(content, "world_element", elem_id, elem['name'])
        
        # Add scripts
        for proj_id, proj in data.get("projects", {}).items():
            if proj.get('content'):
                content = f"{proj['name']}\n\n{proj['content']}\n\nNotes: {proj.get('notes', '')}"
                self.local_storage.add_content(content, "script", proj_id, proj['name'])
