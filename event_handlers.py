
"""Event handler functions for ScriptVoice application."""

import gradio as gr
from models import (
    get_all_stories, get_all_characters, get_all_world_elements,
    search_content
)
from enhancement_services import (
    analyze_character_consistency, suggest_story_elements,
    enhance_script_with_context
)
from audio_services import generate_tts
from image_services import extract_text_from_image
from knowledge_assistant import knowledge_assistant


def query_knowledge_assistant(query: str) -> tuple[str, any]:
    """Process knowledge assistant queries."""
    if not query.strip():
        return "Please enter a query.", gr.update(visible=False)
    
    try:
        response = knowledge_assistant.process_query(query)
        formatted_response = f'<div class="search-results"><pre>{response}</pre></div>'
        return formatted_response, gr.update(visible=True)
    except Exception as e:
        error_response = f'<div class="status-error">❌ Error processing query: {str(e)}</div>'
        return error_response, gr.update(visible=True)


def analyze_consistency(text: str) -> tuple[str, any]:
    """Analyze character consistency."""
    if not text.strip():
        return "Please provide text to analyze.", gr.update(visible=False)
    
    analysis, status = analyze_character_consistency(text)
    formatted_response = f'<div class="search-results"><h4>Character Consistency Analysis</h4><pre>{analysis}</pre></div>'
    return formatted_response, gr.update(visible=True)


def suggest_elements(text: str) -> tuple[str, any]:
    """Suggest story elements."""
    if not text.strip():
        return "Please provide text for suggestions.", gr.update(visible=False)
    
    suggestions, status = suggest_story_elements(text)
    formatted_response = f'<div class="search-results"><h4>Story Element Suggestions</h4><pre>{suggestions}</pre></div>'
    return formatted_response, gr.update(visible=True)


def enhance_with_context(text: str, enhancement_type: str) -> tuple[str, any]:
    """Enhance text with context awareness."""
    if not text.strip():
        return "Please provide text to enhance.", gr.update(visible=False)
    
    enhanced, status = enhance_script_with_context(text, enhancement_type)
    formatted_response = f'<div class="search-results"><h4>Context-Aware Enhancement ({enhancement_type})</h4><pre>{enhanced}</pre></div>'
    return formatted_response, gr.update(visible=True)


def rebuild_knowledge_index() -> tuple[str, any]:
    """Rebuild the knowledge base index."""
    try:
        from rag_services import rag_service
        rag_service.rebuild_index_from_projects()
        response = '<div class="status-success">✅ Knowledge base index rebuilt successfully!</div>'
        return response, gr.update(visible=True)
    except Exception as e:
        response = f'<div class="status-error">❌ Error rebuilding index: {str(e)}</div>'
        return response, gr.update(visible=True)


def display_stories():
    """Display all stories in a formatted way."""
    stories = get_all_stories()
    if not stories:
        return "<div class='empty-state'>📚 No stories created yet. Create your first story above!</div>"
    
    html = "<div class='content-grid'>"
    for story in stories:
        html += f"""
        <div class='content-card story-card'>
            <div class='card-header'>
                <h3>📖 {story['title']}</h3>
                <span class='card-date'>{story['created_at'][:10]}</span>
            </div>
            <p class='card-description'>{story['description'][:100]}{'...' if len(story['description']) > 100 else ''}</p>
        </div>
        """
    html += "</div>"
    return html


def display_characters():
    """Display all characters in a formatted way."""
    characters = get_all_characters()
    if not characters:
        return "<div class='empty-state'>👥 No characters created yet. Create your first character above!</div>"
    
    html = "<div class='content-grid'>"
    for char in characters:
        html += f"""
        <div class='content-card character-card'>
            <div class='card-header'>
                <h3>👤 {char['name']}</h3>
                <span class='card-date'>{char['created_at'][:10]}</span>
            </div>
            <p class='card-description'>{char['description'][:100]}{'...' if len(char['description']) > 100 else ''}</p>
        </div>
        """
    html += "</div>"
    return html


def display_world_elements():
    """Display all world elements in a formatted way."""
    elements = get_all_world_elements()
    if not elements:
        return "<div class='empty-state'>🌍 No world elements created yet. Create your first element above!</div>"
    
    html = "<div class='content-grid'>"
    for elem in elements:
        html += f"""
        <div class='content-card world-card'>
            <div class='card-header'>
                <h3>🌍 {elem['name']} <span class='type-badge'>{elem['type']}</span></h3>
                <span class='card-date'>{elem['created_at'][:10]}</span>
            </div>
            <p class='card-description'>{elem['description'][:100]}{'...' if len(elem['description']) > 100 else ''}</p>
        </div>
        """
    html += "</div>"
    return html


def perform_search(query):
    """Perform search across all content."""
    if not query.strip():
        return gr.update(visible=False)
    
    results = search_content(query)
    
    html = f"<div class='search-results'><h4>Search Results for: '{query}'</h4>"
    
    if results['stories']:
        html += "<h5>📚 Stories:</h5><ul>"
        for story in results['stories']:
            html += f"<li><strong>{story['title']}</strong> - {story['description'][:50]}...</li>"
        html += "</ul>"
    
    if results['characters']:
        html += "<h5>👥 Characters:</h5><ul>"
        for char in results['characters']:
            html += f"<li><strong>{char['name']}</strong> - {char['description'][:50]}...</li>"
        html += "</ul>"
    
    if results['world_elements']:
        html += "<h5>🌍 World Elements:</h5><ul>"
        for elem in results['world_elements']:
            html += f"<li><strong>{elem['name']}</strong> ({elem['type']}) - {elem['description'][:50]}...</li>"
        html += "</ul>"
    
    if not any(results.values()):
        html += "<p>No results found.</p>"
    
    html += "</div>"
    return gr.update(value=html, visible=True)


def enhanced_generate_tts(text: str, speed: float = 1.0) -> tuple[str, str]:
    """Enhanced TTS generation with proper file handling."""
    if not text.strip():
        return None, '<div class="status-error">❌ Please enter some text to convert to speech</div>'
    
    try:
        audio_file, status = generate_tts(text, speed)
        if audio_file:
            return audio_file, '<div class="status-success">✅ Audio generated successfully. Click play to listen!</div>'
        else:
            return None, status
    except Exception as e:
        return None, f'<div class="status-error">❌ Error generating audio: {str(e)}</div>'


def enhanced_extract_text(image_path) -> tuple[str, str]:
    """Enhanced OCR with better error handling."""
    if not image_path:
        return "", '<div class="status-error">❌ Please upload an image first</div>'
    
    try:
        extracted_text, status = extract_text_from_image(image_path)
        if extracted_text:
            return extracted_text, '<div class="status-success">✅ Text extracted successfully! Content added to editor.</div>'
        else:
            return "", status
    except Exception as e:
        return "", f'<div class="status-error">❌ Error extracting text: {str(e)}</div>'
