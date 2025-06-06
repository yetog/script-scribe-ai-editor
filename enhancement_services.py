
"""AI-powered text enhancement services for ScriptVoice with IONOS integration."""

from typing import Tuple
from langchain_tools import analyze_with_ionos_automated_rag, enhance_with_ionos_automated_rag, analyze_text_with_ai, enhance_text_with_context
from ionos_collections import ionos_collections

def analyze_character_consistency(text: str) -> Tuple[str, str]:
    """Analyze character consistency using IONOS automated RAG if available."""
    if not text.strip():
        return "No text provided for analysis.", "error"
    
    try:
        # Try IONOS automated RAG first
        if ionos_collections.is_available():
            analysis = analyze_with_ionos_automated_rag(text, "character_consistency", "characters")
            if analysis and "Error" not in analysis:
                return analysis, "success"
        
        # Fallback to regular AI analysis
        analysis = analyze_text_with_ai(text, "character_consistency")
        if "AI analysis not available" in analysis or "Error during AI analysis" in analysis:
            return analysis, "error"
        return analysis, "success"
        
    except Exception as e:
        return f"Error analyzing character consistency: {str(e)}", "error"

def suggest_story_elements(text: str) -> Tuple[str, str]:
    """Suggest story elements using IONOS automated RAG if available."""
    if not text.strip():
        return "No text provided for suggestions.", "error"
    
    try:
        # Try IONOS automated RAG first
        if ionos_collections.is_available():
            suggestions = analyze_with_ionos_automated_rag(text, "story_elements", "stories")
            if suggestions and "Error" not in suggestions:
                return suggestions, "success"
        
        # Fallback to regular AI analysis
        suggestions = analyze_text_with_ai(text, "story_elements")
        if "AI analysis not available" in suggestions or "Error during AI analysis" in suggestions:
            return suggestions, "error"
        return suggestions, "success"
        
    except Exception as e:
        return f"Error generating story suggestions: {str(e)}", "error"

def enhance_script_with_context(text: str, enhancement_type: str = "dialogue") -> Tuple[str, str]:
    """Enhance script text using IONOS automated RAG if available."""
    if not text.strip():
        return "No text provided for enhancement.", "error"
    
    try:
        # Try IONOS automated RAG first
        if ionos_collections.is_available():
            enhanced_text = enhance_with_ionos_automated_rag(text, enhancement_type)
            if enhanced_text and enhanced_text != text:
                return enhanced_text, f"Text enhanced using IONOS automated RAG with {enhancement_type} enhancement."
        
        # Fallback to regular enhancement
        enhanced_text = enhance_text_with_context(text, enhancement_type)
        
        if enhanced_text == text:
            # Check if AI was available
            from langchain_tools import get_ai_client
            if get_ai_client() is None:
                status = "Enhancement not available (no AI provider configured)."
            else:
                status = "Enhancement completed (no changes needed)."
        else:
            status = f"Text enhanced using {enhancement_type} enhancement."
        
        return enhanced_text, status
        
    except Exception as e:
        return text, f"Enhancement error: {str(e)}"

def enhance_script_placeholder(text: str, enhancement_type: str = "dialogue") -> Tuple[str, str]:
    """Placeholder enhancement function for the UI with IONOS integration."""
    return enhance_script_with_context(text, enhancement_type)

def get_enhancement_context(text: str, enhancement_type: str = "dialogue") -> str:
    """Get relevant context for enhancement from IONOS collections."""
    if not ionos_collections.is_available():
        return "IONOS collections not available for context enhancement."
    
    # Map enhancement types to appropriate collections
    collection_map = {
        "dialogue": "characters",
        "description": "world_elements", 
        "pacing": "stories",
        "general": "stories"
    }
    
    collection_name = collection_map.get(enhancement_type, "stories")
    results = ionos_collections.query_collection(collection_name, text, 3)
    
    if not results:
        return f"No relevant context found in {collection_name} collection."
    
    context_parts = []
    for result in results:
        title = result['metadata'].get('title', 'Untitled')
        content = result['content'][:150] + "..." if len(result['content']) > 150 else result['content']
        context_parts.append(f"**{title}**: {content}")
    
    return f"📚 Relevant context for {enhancement_type} enhancement:\n\n" + "\n\n".join(context_parts)
