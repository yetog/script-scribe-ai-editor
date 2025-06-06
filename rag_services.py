
"""RAG (Retrieval Augmented Generation) services for ScriptVoice."""

import os
import json
import pickle
from typing import List, Dict, Any, Tuple, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from config import PROJECTS_FILE

# Try to import FAISS, fallback to ChromaDB if not available
try:
    import faiss
    USE_FAISS = True
    print("Using FAISS for vector storage")
except ImportError:
    try:
        import chromadb
        USE_FAISS = False
        print("FAISS not available, using ChromaDB as fallback")
    except ImportError:
        raise ImportError("Either faiss-cpu or chromadb must be installed for vector storage")


class RAGService:
    """Handles vector database operations and content retrieval."""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", "! ", "? ", " "]
        )
        
        if USE_FAISS:
            self._init_faiss()
        else:
            self._init_chromadb()
    
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
        """Add content to the vector database."""
        if not content.strip():
            return
        
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
        """Search for similar content."""
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
    
    def rebuild_index_from_projects(self):
        """Rebuild the entire vector index from current projects data."""
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


# Global RAG service instance
rag_service = RAGService()
