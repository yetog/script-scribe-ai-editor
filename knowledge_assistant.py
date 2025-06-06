
"""Knowledge assistant for ScriptVoice using RAG services."""

from typing import Dict, List, Any
from rag_services import rag_service

class KnowledgeAssistant:
    """AI-powered knowledge assistant for story intelligence."""
    
    def __init__(self):
        self.rag_service = rag_service
    
    def process_query(self, query: str) -> str:
        """Process a knowledge query and return relevant information."""
        if not query.strip():
            return "Please provide a query."
        
        try:
            # Search for relevant content
            results = self.rag_service.search(query, k=5)
            
            if not results:
                return f"No relevant information found for: '{query}'"
            
            # Format the response
            response = f"Knowledge search results for: '{query}'\n\n"
            
            for i, result in enumerate(results, 1):
                content_type = result['metadata'].get('content_type', 'unknown')
                title = result['metadata'].get('title', 'Untitled')
                score = result.get('score', 0)
                
                response += f"{i}. [{content_type.title()}] {title} (Relevance: {score:.2f})\n"
                response += f"   {result['content'][:200]}...\n\n"
            
            return response
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def get_context_for_writing(self, current_text: str, context_type: str = "general") -> str:
        """Get relevant context for writing assistance."""
        try:
            results = self.rag_service.search(current_text, k=3, content_type=context_type)
            
            if not results:
                return "No relevant context found."
            
            context = "Relevant context from your knowledge base:\n\n"
            for result in results:
                title = result['metadata'].get('title', 'Untitled')
                context += f"- {title}: {result['content'][:100]}...\n"
            
            return context
            
        except Exception as e:
            return f"Error retrieving context: {str(e)}"

# Global knowledge assistant instance
knowledge_assistant = KnowledgeAssistant()
