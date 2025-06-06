
"""Document chunking utilities for ScriptVoice RAG system."""

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


class DocumentChunker:
    """Handles text chunking for RAG processing."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? ", " "]
        )
    
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


# Global chunker instance
document_chunker = DocumentChunker()
