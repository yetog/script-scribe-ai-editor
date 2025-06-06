
"""Knowledge assistant for ScriptVoice using IONOS-enhanced RAG services."""

from typing import Dict, List, Any
from rag_services import rag_service
from ionos_collections import ionos_collections
from langchain_tools import analyze_with_ionos_automated_rag

class EnhancedKnowledgeAssistant:
    """AI-powered knowledge assistant with IONOS integration."""
    
    def __init__(self):
        self.rag_service = rag_service
        self.ionos_collections = ionos_collections
    
    def process_query(self, query: str, content_type: str = None) -> str:
        """Process a knowledge query with IONOS-enhanced search."""
        if not query.strip():
            return "Please provide a query."
        
        try:
            # Use IONOS collections if available
            if self.ionos_collections.is_available():
                results = self._search_ionos_collections(query, content_type)
                if results:
                    return self._format_ionos_response(query, results)
            
            # Fallback to local search
            results = self.rag_service.search(query, k=5, content_type=content_type)
            
            if not results:
                return f"No relevant information found for: '{query}'"
            
            return self._format_local_response(query, results)
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def _search_ionos_collections(self, query: str, content_type: str = None) -> List[Dict[str, Any]]:
        """Search IONOS collections with smart collection selection."""
        if content_type:
            # Search specific collection
            collection_map = {
                "story": "stories",
                "character": "characters",
                "world_element": "world_elements",
                "script": "scripts"
            }
            collection_name = collection_map.get(content_type, "stories")
            return self.ionos_collections.query_collection(collection_name, query, 5)
        else:
            # Search all collections intelligently
            all_results = []
            collections = ["stories", "characters", "world_elements", "scripts"]
            
            for collection_name in collections:
                results = self.ionos_collections.query_collection(collection_name, query, 2)
                for result in results:
                    result['metadata']['collection'] = collection_name
                all_results.extend(results)
            
            # Sort by relevance score
            all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
            return all_results[:5]
    
    def _format_ionos_response(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format IONOS search results with enhanced context."""
        response = f"🔍 Knowledge search results for: '{query}'\n\n"
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            collection = metadata.get('collection', 'unknown')
            title = metadata.get('title', 'Untitled')
            score = result.get('score', 0)
            
            # Add collection-specific icons
            icons = {
                'stories': '📖',
                'characters': '👤', 
                'world_elements': '🌍',
                'scripts': '📝'
            }
            icon = icons.get(collection, '📄')
            
            response += f"{i}. {icon} [{collection.title()}] {title} (Relevance: {score:.2f})\n"
            
            # Show relevant excerpt
            content = result['content']
            if len(content) > 150:
                content = content[:150] + "..."
            response += f"   {content}\n\n"
        
        return response
    
    def _format_local_response(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format local search results."""
        # ... keep existing code (format local response)
        
        response = f"Knowledge search results for: '{query}'\n\n"
        
        for i, result in enumerate(results, 1):
            content_type = result['metadata'].get('content_type', 'unknown')
            title = result['metadata'].get('title', 'Untitled')
            score = result.get('score', 0)
            
            response += f"{i}. [{content_type.title()}] {title} (Relevance: {score:.2f})\n"
            response += f"   {result['content'][:200]}...\n\n"
        
        return response
    
    def get_context_for_writing(self, current_text: str, context_type: str = "general") -> str:
        """Get relevant context for writing assistance with IONOS integration."""
        try:
            if self.ionos_collections.is_available():
                # Use IONOS automated RAG for better context
                collection_map = {
                    "dialogue": "characters",
                    "description": "world_elements",
                    "plot": "stories",
                    "general": "stories"
                }
                collection_name = collection_map.get(context_type, "stories")
                
                results = self.ionos_collections.query_collection(collection_name, current_text, 3)
                
                if results:
                    context = "📚 Relevant context from your knowledge base:\n\n"
                    for result in results:
                        title = result['metadata'].get('title', 'Untitled')
                        content = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                        context += f"• **{title}**: {content}\n"
                    return context
            
            # Fallback to local search
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
    
    def analyze_with_context(self, text: str, analysis_type: str = "general") -> str:
        """Analyze text with contextual knowledge from collections."""
        if self.ionos_collections.is_available():
            # Use IONOS automated RAG for analysis
            return analyze_with_ionos_automated_rag(text, analysis_type)
        else:
            # Fallback to regular analysis
            from langchain_tools import analyze_text_with_ai
            return analyze_text_with_ai(text, analysis_type)
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about available collections."""
        stats = {
            "ionos_available": self.ionos_collections.is_available(),
            "collections": {}
        }
        
        if self.ionos_collections.is_available():
            collections = self.ionos_collections.list_collections()
            for collection in collections:
                name = collection.get("properties", {}).get("name", "")
                doc_count = collection.get("properties", {}).get("documentsCount", 0)
                if name:
                    stats["collections"][name] = {
                        "document_count": doc_count,
                        "id": collection.get("id", ""),
                        "description": collection.get("properties", {}).get("description", "")
                    }
        
        return stats
    
    def sync_data_to_ionos(self) -> str:
        """Sync all project data to IONOS collections."""
        if not self.ionos_collections.is_available():
            return "IONOS collections not available. Please check your API token."
        
        try:
            self.ionos_collections.sync_projects_to_collections()
            return "✅ Successfully synced all project data to IONOS collections."
        except Exception as e:
            return f"❌ Error syncing to IONOS: {str(e)}"


# Global enhanced knowledge assistant instance
knowledge_assistant = EnhancedKnowledgeAssistant()
