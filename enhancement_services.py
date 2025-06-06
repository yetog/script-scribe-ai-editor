
"""AI enhancement services for ScriptVoice with RAG integration."""

from typing import Tuple
from langchain_tools import context_enhancer
from rag_services import rag_service


def enhance_script_placeholder(text: str, enhancement_type: str) -> Tuple[str, str]:
    """Enhanced script enhancement with context awareness."""
    if not text.strip():
        return text, '<div class="status-error">❌ Please provide text to enhance</div>'
    
    try:
        # Use context-aware enhancement
        enhanced_text, status = context_enhancer.enhance_script_with_context(text, enhancement_type)
        return enhanced_text, '<div class="status-success">✅ Script enhanced successfully</div>'
    except Exception as e:
        # Simple fallback enhancement
        enhanced_text = simple_enhance_text(text, enhancement_type)
        return enhanced_text, '<div class="status-success">✅ Script enhanced (basic mode)</div>'


def simple_enhance_text(text: str, enhancement_type: str) -> str:
    """Simple text enhancement fallback when AI services are unavailable."""
    if enhancement_type == "dramatic":
        return text.replace(".", "!").replace(",", "...").upper()
    elif enhancement_type == "romantic":
        romantic_words = {"said": "whispered", "looked": "gazed", "walked": "strolled"}
        enhanced = text
        for old, new in romantic_words.items():
            enhanced = enhanced.replace(old, new)
        return enhanced
    elif enhancement_type == "professional":
        return text.replace("can't", "cannot").replace("won't", "will not")
    else:
        return text


def enhance_script_with_context(text: str, enhancement_type: str) -> Tuple[str, str]:
    """Context-aware script enhancement using RAG."""
    if not text.strip():
        return "", '<div class="status-error">❌ Please provide text to enhance</div>'
    
    try:
        enhanced_text, status = context_enhancer.enhance_script_with_context(text, enhancement_type)
        return enhanced_text, '<div class="status-success">✅ Context-aware enhancement complete</div>'
    except Exception as e:
        # Fallback to simple enhancement
        enhanced_text = simple_enhance_text(text, enhancement_type)
        return enhanced_text, f'<div class="status-success">✅ Enhancement complete (fallback mode)</div>'


def analyze_character_consistency(text: str) -> Tuple[str, str]:
    """Analyze character consistency in the provided text."""
    if not text.strip():
        return "", '<div class="status-error">❌ Please provide text to analyze</div>'
    
    try:
        analysis = context_enhancer.analyze_character_consistency(text)
        return analysis, '<div class="status-success">✅ Character consistency analysis complete</div>'
    except Exception as e:
        # Simple fallback analysis
        words = text.split()
        char_count = len([w for w in words if w.istitle() and len(w) > 2])
        analysis = f"""Character Consistency Analysis (Basic Mode):
        
- Text length: {len(text)} characters
- Word count: {len(words)} words  
- Potential character names found: {char_count}
- Analysis: {"Good character density" if char_count > len(words)/50 else "Consider adding more character development"}

Note: Advanced AI analysis unavailable. This is a basic structural analysis."""
        return analysis, '<div class="status-success">✅ Basic character analysis complete</div>'


def suggest_story_elements(text: str) -> Tuple[str, str]:
    """Suggest relevant story elements for the text."""
    if not text.strip():
        return "", '<div class="status-error">❌ Please provide text for suggestions</div>'
    
    try:
        suggestions = context_enhancer.suggest_story_elements(text)
        return suggestions, '<div class="status-success">✅ Story element suggestions generated</div>'
    except Exception as e:
        # Simple fallback suggestions
        suggestions = f"""Story Element Suggestions (Basic Mode):

Based on your text content, consider adding:

📍 Locations:
- Detailed setting descriptions
- Multiple scene locations
- Atmospheric details

👥 Characters:  
- Character motivations
- Dialogue tags and speech patterns
- Character relationships

🎭 Plot Elements:
- Conflict introduction
- Rising action sequences
- Resolution planning

🌟 Enhancement Ideas:
- Sensory details (sight, sound, smell)
- Emotional depth
- Show vs. tell improvements

Note: Advanced AI suggestions unavailable. These are general writing improvement areas."""
        return suggestions, '<div class="status-success">✅ Basic story suggestions generated</div>'


def update_knowledge_base(content_type: str, content_id: str, title: str, content: str) -> str:
    """Update the knowledge base with new or modified content."""
    try:
        rag_service.add_content(content, content_type, content_id, title)
        return '<div class="status-success">✅ Knowledge base updated successfully</div>'
    except Exception as e:
        return f'<div class="status-error">❌ Error updating knowledge base: {str(e)}</div>'


def remove_from_knowledge_base(content_id: str) -> str:
    """Remove content from the knowledge base."""
    try:
        rag_service.remove_content(content_id)
        return '<div class="status-success">✅ Content removed from knowledge base successfully</div>'
    except Exception as e:
        return f'<div class="status-error">❌ Error removing from knowledge base: {str(e)}</div>'
