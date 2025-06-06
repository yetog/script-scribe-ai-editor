"""RAG (Retrieval Augmented Generation) services for ScriptVoice with IONOS integration."""

import os
import json
import pickle
from typing import List, Dict, Any, Tuple, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from config import PROJECTS_FILE
from ionos_collections import ionos_collections

# Try to import FAISS, fallback to ChromaDB if not available
try:
    import faiss
    USE_FAISS = True
    print("Using FAISS for local vector storage")
except ImportError:
    try:
        import chromadb
        USE_FAISS = False
        print("FAISS not available, using ChromaDB as local fallback")
    except ImportError:
        raise ImportError("Either faiss-cpu or chromadb must be installed for local vector storage")


class HybridRAGService:
    """Handles both local and IONOS vector database operations."""
    
    def __init__(self, use_ionos: bool = True):
        self.use_ionos = use_ionos and ionos_collections.is_available()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", "! ", "? ", " "]
        )
        
        if self.use_ionos:
            print("Using IONOS Document Collections for RAG")
            # Initialize IONOS collections on startup
            self._ensure_ionos_collections()
        else:
            print("Using local vector storage for RAG")
            if USE_FAISS:
                self._init_faiss()
            else:
                self._init_chromadb()
    
    def _ensure_ionos_collections(self):
        """Ensure required IONOS collections exist."""
        collections = ["stories", "characters", "world_elements", "scripts"]
        for collection_name in collections:
            ionos_collections.get_collection_id(collection_name)
    
    def _init_faiss(self):
        """Initialize FAISS-based storage."""
        self.index = None
        self.documents = []
        self.metadata = []
        self.index_file = "vector_index.faiss"
        self.metadata_file = "vector_metadata.pkl"
        self._load_or_create_faiss_index()
    
    def _init_chromadb(self):
        """Initialize ChromaDB-based storage."""
        self.client = chromadb.PersistentClient(path="./chromadb_storage")
        self.collection = self.client.get_or_create_collection(
            name="scriptvoice_documents",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"ChromaDB collection has {self.collection.count()} documents")
    
    def _load_or_create_faiss_index(self):
        """Load existing FAISS index or create new one."""
        if os.path.exists(self.index_file) and os.path.exists(self.metadata_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.metadata_file, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data['documents']
                    self.metadata = data['metadata']
                print(f"Loaded FAISS index with {len(self.documents)} documents")
            except Exception as e:
                print(f"Error loading FAISS index: {e}")
                self._create_empty_faiss_index()
        else:
            self._create_empty_faiss_index()
    
    def _create_empty_faiss_index(self):
        """Create empty FAISS index."""
        dimension = 384  # all-MiniLM-L6-v2 dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.documents = []
        self.metadata = []
    
    def chunk_content(self, content: str, content_type: str, content_id: str, title: str) -> List[Document]:
        """Split content into chunks for embedding."""
        chunks = self.text_splitter.split_text(content)
        documents = []
        
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    'content_type': content_type,
                    'content_id': content_id,
                    'title': title,
                    'chunk_id': i,
                    'chunk_count': len(chunks)
                }
            )
            documents.append(doc)
        
        return documents
    
    def add_content(self, content: str, content_type: str, content_id: str, title: str):
        """Add content to the vector database (IONOS or local)."""
        if not content.strip():
            return
        
        if self.use_ionos:
            self._add_content_ionos(content, content_type, content_id, title)
        else:
            self._add_content_local(content, content_type, content_id, title)
    
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
    
    def _add_content_local(self, content: str, content_type: str, content_id: str, title: str):
        """Add content to local vector storage."""
        # Remove existing content for this ID
        self.remove_content(content_id)
        
        # Chunk the content
        documents = self.chunk_content(content, content_type, content_id, title)
        
        if not documents:
            return
        
        if USE_FAISS:
            self._add_content_faiss(documents)
        else:
            self._add_content_chromadb(documents)
    
    def _add_content_faiss(self, documents: List[Document]):
        """Add content using FAISS."""
        # Generate embeddings
        texts = [doc.page_content for doc in documents]
        embeddings = self.model.encode(texts)
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        
        # Store documents and metadata
        self.documents.extend(documents)
        for doc in documents:
            self.metadata.append(doc.metadata)
        
        # Save index
        self._save_faiss_index()
    
    def _add_content_chromadb(self, documents: List[Document]):
        """Add content using ChromaDB."""
        texts = [doc.page_content for doc in documents]
        embeddings = self.model.encode(texts).tolist()
        
        ids = [f"{doc.metadata['content_id']}_{doc.metadata['chunk_id']}" for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def remove_content(self, content_id: str):
        """Remove content from vector database."""
        if USE_FAISS:
            self._remove_content_faiss(content_id)
        else:
            self._remove_content_chromadb(content_id)
    
    def _remove_content_faiss(self, content_id: str):
        """Remove content from FAISS."""
        indices_to_remove = []
        for i, metadata in enumerate(self.metadata):
            if metadata.get('content_id') == content_id:
                indices_to_remove.append(i)
        
        if indices_to_remove:
            # Rebuild index without removed items
            new_documents = []
            new_metadata = []
            new_embeddings = []
            
            for i, (doc, meta) in enumerate(zip(self.documents, self.metadata)):
                if i not in indices_to_remove:
                    new_documents.append(doc)
                    new_metadata.append(meta)
                    embedding = self.model.encode([doc.page_content])
                    embedding = embedding / np.linalg.norm(embedding, axis=1, keepdims=True)
                    new_embeddings.append(embedding[0])
            
            # Recreate index
            self._create_empty_faiss_index()
            if new_embeddings:
                embeddings_array = np.array(new_embeddings).astype('float32')
                self.index.add(embeddings_array)
                self.documents = new_documents
                self.metadata = new_metadata
            
            self._save_faiss_index()
    
    def _remove_content_chromadb(self, content_id: str):
        """Remove content from ChromaDB."""
        # Get all documents for this content_id
        results = self.collection.get(where={"content_id": content_id})
        if results['ids']:
            self.collection.delete(ids=results['ids'])
    
    def search(self, query: str, k: int = 5, content_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for similar content (IONOS or local)."""
        if self.use_ionos:
            return self._search_ionos(query, k, content_type)
        else:
            return self._search_local(query, k, content_type)
    
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
    
    def _search_local(self, query: str, k: int, content_type: Optional[str]) -> List[Dict[str, Any]]:
        """Search using local storage."""
        if USE_FAISS:
            return self._search_faiss(query, k, content_type)
        else:
            return self._search_chromadb(query, k, content_type)
    
    def _search_faiss(self, query: str, k: int, content_type: Optional[str]) -> List[Dict[str, Any]]:
        """Search using FAISS."""
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search
        scores, indices = self.index.search(query_embedding.astype('float32'), min(k * 2, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx < len(self.documents):
                metadata = self.metadata[idx]
                
                # Filter by content type if specified
                if content_type and metadata.get('content_type') != content_type:
                    continue
                
                result = {
                    'content': self.documents[idx].page_content,
                    'metadata': metadata,
                    'score': float(score)
                }
                results.append(result)
                
                if len(results) >= k:
                    break
        
        return results
    
    def _search_chromadb(self, query: str, k: int, content_type: Optional[str]) -> List[Dict[str, Any]]:
        """Search using ChromaDB."""
        query_embedding = self.model.encode([query]).tolist()
        
        where_clause = {"content_type": content_type} if content_type else None
        
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k,
            where=where_clause
        )
        
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                result = {
                    'content': doc,
                    'metadata': metadata,
                    'score': 1.0 - distance  # Convert distance to similarity score
                }
                search_results.append(result)
        
        return search_results
    
    def get_context_for_content(self, content_id: str, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Get relevant context from other content for a specific item."""
        results = self.search(query, k=k)
        # Filter out results from the same content
        filtered_results = [r for r in results if r['metadata'].get('content_id') != content_id]
        return filtered_results[:k]
    
    def _save_faiss_index(self):
        """Save FAISS index and metadata to disk."""
        try:
            faiss.write_index(self.index, self.index_file)
            with open(self.metadata_file, 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'metadata': self.metadata
                }, f)
        except Exception as e:
            print(f"Error saving FAISS index: {e}")
    
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
        if USE_FAISS:
            self._create_empty_faiss_index()
        else:
            # Clear ChromaDB collection
            try:
                self.client.delete_collection("scriptvoice_documents")
                self.collection = self.client.create_collection(
                    name="scriptvoice_documents",
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e:
                print(f"Error clearing ChromaDB collection: {e}")
        
        # Load all projects data
        data = load_projects()
        
        # Add stories
        for story_id, story in data.get("stories", {}).items():
            content = f"{story['title']}\n\n{story['description']}\n\n{story['content']}"
            self.add_content(content, "story", story_id, story['title'])
        
        # Add characters
        for char_id, char in data.get("characters", {}).items():
            content = f"{char['name']}\n\n{char['description']}\n\nTraits: {', '.join(char.get('traits', []))}\n\n{char.get('notes', '')}"
            self.add_content(content, "character", char_id, char['name'])
        
        # Add world elements
        for elem_id, elem in data.get("world_elements", {}).items():
            content = f"{elem['name']} ({elem['type']})\n\n{elem['description']}\n\nTags: {', '.join(elem.get('tags', []))}\n\n{elem.get('notes', '')}"
            self.add_content(content, "world_element", elem_id, elem['name'])
        
        # Add scripts
        for proj_id, proj in data.get("projects", {}).items():
            if proj.get('content'):
                content = f"{proj['name']}\n\n{proj['content']}\n\nNotes: {proj.get('notes', '')}"
                self.add_content(content, "script", proj_id, proj['name'])
        
        if USE_FAISS:
            self._save_faiss_index()


# Global RAG service instance with IONOS integration
rag_service = HybridRAGService()
