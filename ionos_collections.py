
"""IONOS Document Collections service for ScriptVoice."""

import os
import json
import base64
import requests
from typing import List, Dict, Any, Optional, Tuple
from config import IONOS_API_TOKEN

class IONOSCollectionsService:
    """Manages IONOS Document Collections for vector storage and RAG."""
    
    def __init__(self):
        self.api_token = IONOS_API_TOKEN
        self.base_url = "https://inference.de-txl.ionos.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.collections = {}  # Cache collection IDs by name
    
    def is_available(self) -> bool:
        """Check if IONOS collections service is available."""
        return bool(self.api_token)
    
    def create_collection(self, name: str, description: str, content_type: str = "stories") -> Optional[str]:
        """Create a new document collection."""
        if not self.is_available():
            print("IONOS API token not available")
            return None
        
        # Optimize chunking based on content type
        chunk_config = {
            "stories": {"chunk_size": 1000, "chunk_overlap": 100},
            "characters": {"chunk_size": 500, "chunk_overlap": 50}, 
            "world_elements": {"chunk_size": 600, "chunk_overlap": 60},
            "scripts": {"chunk_size": 800, "chunk_overlap": 80}
        }
        
        config = chunk_config.get(content_type, chunk_config["stories"])
        
        body = {
            "properties": {
                "name": name,
                "description": description,
                "chunking": {
                    "enabled": True,
                    "strategy": {
                        "config": {
                            "chunk_overlap": config["chunk_overlap"],
                            "chunk_size": config["chunk_size"]
                        }
                    }
                },
                "embedding": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"
                },
                "engine": {
                    "db_type": "chromadb"
                }
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/collections", json=body, headers=self.headers)
            if response.status_code == 201:
                collection_data = response.json()
                collection_id = collection_data.get("id")
                self.collections[name] = collection_id
                print(f"Created IONOS collection '{name}' with ID: {collection_id}")
                return collection_id
            else:
                print(f"Failed to create collection: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error creating collection: {e}")
            return None
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """List all existing collections."""
        if not self.is_available():
            return []
        
        try:
            response = requests.get(f"{self.base_url}/collections", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                collections = data.get("items", [])
                # Update cache
                for collection in collections:
                    name = collection.get("properties", {}).get("name")
                    if name:
                        self.collections[name] = collection.get("id")
                return collections
            else:
                print(f"Failed to list collections: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing collections: {e}")
            return []
    
    def get_collection_id(self, name: str) -> Optional[str]:
        """Get collection ID by name, creating if doesn't exist."""
        # Check cache first
        if name in self.collections:
            return self.collections[name]
        
        # Refresh collections list
        collections = self.list_collections()
        for collection in collections:
            collection_name = collection.get("properties", {}).get("name")
            if collection_name == name:
                collection_id = collection.get("id")
                self.collections[name] = collection_id
                return collection_id
        
        # Create if doesn't exist
        print(f"Collection '{name}' not found, creating...")
        return self.create_collection(name, f"ScriptVoice {name} collection", name)
    
    def add_document(self, collection_name: str, content: str, name: str, metadata: Dict[str, Any] = None) -> bool:
        """Add a document to a collection."""
        collection_id = self.get_collection_id(collection_name)
        if not collection_id:
            return False
        
        # Encode content to base64
        content_base64 = base64.b64encode(content.encode('utf-8')).decode("utf-8")
        
        # Add metadata to document name if provided
        doc_name = name
        if metadata:
            doc_name = f"{name} | {json.dumps(metadata, separators=(',', ':'))}"
        
        body = {
            "items": [{
                "properties": {
                    "name": doc_name,
                    "contentType": "text/plain",
                    "content": content_base64
                }
            }]
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/collections/{collection_id}/documents",
                json=body,
                headers=self.headers
            )
            if response.status_code == 200:
                print(f"Added document '{name}' to collection '{collection_name}'")
                return True
            else:
                print(f"Failed to add document: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Error adding document: {e}")
            return False
    
    def update_document(self, collection_name: str, document_id: str, content: str, name: str, metadata: Dict[str, Any] = None) -> bool:
        """Update an existing document."""
        collection_id = self.get_collection_id(collection_name)
        if not collection_id:
            return False
        
        content_base64 = base64.b64encode(content.encode('utf-8')).decode("utf-8")
        
        doc_name = name
        if metadata:
            doc_name = f"{name} | {json.dumps(metadata, separators=(',', ':'))}"
        
        body = {
            "properties": {
                "id": document_id,
                "name": doc_name,
                "contentType": "text/plain",
                "content": content_base64
            }
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/collections/{collection_id}/documents/{document_id}",
                json=body,
                headers=self.headers
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
    
    def query_collection(self, collection_name: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Query a collection for relevant documents."""
        collection_id = self.get_collection_id(collection_name)
        if not collection_id:
            return []
        
        body = {
            "query": query,
            "limit": limit
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/collections/{collection_id}/query",
                json=body,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("properties", {}).get("matches", [])
                
                results = []
                for match in matches:
                    doc = match.get("document", {})
                    properties = doc.get("properties", {})
                    
                    # Decode content
                    content_b64 = properties.get("content", "")
                    try:
                        content = base64.b64decode(content_b64).decode('utf-8')
                    except:
                        content = ""
                    
                    # Parse metadata from name if present
                    name = properties.get("name", "")
                    metadata = {}
                    if " | " in name:
                        name_parts = name.split(" | ", 1)
                        name = name_parts[0]
                        try:
                            metadata = json.loads(name_parts[1])
                        except:
                            pass
                    
                    result = {
                        "content": content,
                        "metadata": {
                            "title": name,
                            "collection": collection_name,
                            **metadata
                        },
                        "score": match.get("score", 0)
                    }
                    results.append(result)
                
                return results
            else:
                print(f"Failed to query collection: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error querying collection: {e}")
            return []
    
    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection."""
        collection_id = self.get_collection_id(collection_name)
        if not collection_id:
            return False
        
        try:
            response = requests.delete(f"{self.base_url}/collections/{collection_id}", headers=self.headers)
            if response.status_code == 204:
                if collection_name in self.collections:
                    del self.collections[collection_name]
                print(f"Deleted collection '{collection_name}'")
                return True
            else:
                print(f"Failed to delete collection: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False
    
    def sync_projects_to_collections(self):
        """Sync all projects data to IONOS collections."""
        from models import load_projects
        
        if not self.is_available():
            print("IONOS collections not available - skipping sync")
            return
        
        print("Syncing projects to IONOS Document Collections...")
        
        data = load_projects()
        
        # Sync stories
        for story_id, story in data.get("stories", {}).items():
            content = f"{story['title']}\n\n{story['description']}\n\n{story['content']}"
            metadata = {
                "content_type": "story",
                "content_id": story_id,
                "tags": story.get("tags", [])
            }
            self.add_document("stories", content, story['title'], metadata)
        
        # Sync characters
        for char_id, char in data.get("characters", {}).items():
            content = f"{char['name']}\n\n{char['description']}\n\nTraits: {', '.join(char.get('traits', []))}\n\n{char.get('notes', '')}"
            metadata = {
                "content_type": "character",
                "content_id": char_id,
                "traits": char.get("traits", [])
            }
            self.add_document("characters", content, char['name'], metadata)
        
        # Sync world elements
        for elem_id, elem in data.get("world_elements", {}).items():
            content = f"{elem['name']} ({elem['type']})\n\n{elem['description']}\n\nTags: {', '.join(elem.get('tags', []))}\n\n{elem.get('notes', '')}"
            metadata = {
                "content_type": "world_element",
                "content_id": elem_id,
                "element_type": elem['type'],
                "tags": elem.get("tags", [])
            }
            self.add_document("world_elements", content, elem['name'], metadata)
        
        # Sync scripts
        for proj_id, proj in data.get("projects", {}).items():
            if proj.get('content'):
                content = f"{proj['name']}\n\n{proj['content']}\n\nNotes: {proj.get('notes', '')}"
                metadata = {
                    "content_type": "script",
                    "content_id": proj_id,
                    "project_name": proj['name']
                }
                self.add_document("scripts", content, proj['name'], metadata)
        
        print("Sync to IONOS collections completed")


# Global IONOS collections service instance
ionos_collections = IONOSCollectionsService()
