
"""AI-powered text enhancement services for ScriptVoice."""

from typing import Tuple
from langchain_tools import analyze_text_with_ai, enhance_text_with_context

def analyze_character_consistency(text: str) -> Tuple[str, str]:
    """Analyze character consistency in the provided text."""
    if not text.strip():
        return "No text provided for analysis.", "error"
    
    try:
        analysis = analyze_text_with_ai(text, "character_consistency")
        return analysis, "success"
    except Exception as e:
        return f"Error analyzing character consistency: {str(e)}", "error"

def suggest_story_elements(text: str) -> Tuple[str, str]:
    """Suggest story elements and improvements."""
    if not text.strip():
        return "No text provided for suggestions.", "error"
    
    try:
        suggestions = analyze_text_with_ai(text, "story_elements")
        return suggestions, "success"
    except Exception as e:
        return f"Error generating story suggestions: {str(e)}", "error"

def enhance_script_with_context(text: str, enhancement_type: str = "dialogue") -> Tuple[str, str]:
    """Enhance script text with context awareness."""
    if not text.strip():
        return "No text provided for enhancement.", "error"
    
    try:
        enhanced_text = enhance_text_with_context(text, enhancement_type)
        return enhanced_text, "success"
    except Exception as e:
        return f"Error enhancing text: {str(e)}", "error"

def enhance_script_placeholder(text: str, enhancement_type: str = "dialogue") -> Tuple[str, str]:
    """Placeholder enhancement function for the UI."""
    if not text.strip():
        return text, "Please provide text to enhance."
    
    try:
        enhanced_text = enhance_text_with_context(text, enhancement_type)
        
        if enhanced_text == text:
            status = "Enhancement completed (no changes needed or AI unavailable)."
        else:
            status = f"Text enhanced using {enhancement_type} enhancement."
        
        return enhanced_text, status
    except Exception as e:
        return text, f"Enhancement error: {str(e)}"
