
"""UI components and styling for ScriptVoice application."""

CUSTOM_CSS = """
/* ScriptVoice Custom CSS */
.gradio-container {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%);
    font-family: 'Inter', sans-serif;
}

.word-count-highlight {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
    font-size: 1.1em;
    padding: 8px;
    border-radius: 8px;
    background-color: rgba(255, 107, 53, 0.1);
    border: 1px solid rgba(255, 107, 53, 0.3);
}

.primary-button {
    background: linear-gradient(45deg, #ff6b35, #f7931e) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.primary-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
}

.secondary-button {
    background: linear-gradient(45deg, #667eea, #764ba2) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.secondary-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
}

.sidebar-column {
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin-right: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.status-success {
    color: #4ade80;
    background-color: rgba(74, 222, 128, 0.1);
    border: 1px solid rgba(74, 222, 128, 0.3);
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
}

.status-error {
    color: #f87171;
    background-color: rgba(248, 113, 113, 0.1);
    border: 1px solid rgba(248, 113, 113, 0.3);
    padding: 10px;
    border-radius: 8px;
    margin: 10px 0;
}

/* Story Intelligence Styling */
.stories-grid, .characters-grid, .world-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.story-card, .character-card, .world-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
    transition: all 0.3s ease;
}

.story-card:hover, .character-card:hover, .world-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.2);
    border-color: rgba(255, 107, 53, 0.3);
}

.story-card h3, .character-card h3, .world-card h3 {
    color: #ff6b35;
    margin: 0 0 10px 0;
    font-size: 1.2em;
    font-weight: 600;
}

.story-card p, .character-card p, .world-card p {
    color: rgba(255, 255, 255, 0.8);
    margin: 10px 0;
    line-height: 1.4;
}

.story-card small, .character-card small, .world-card small {
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.85em;
}

.type-badge {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: 500;
    margin-left: 10px;
}

/* Tab styling */
.gradio-tabs .tab-nav {
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 12px !important;
    margin-bottom: 20px !important;
}

.gradio-tabs .tab-nav button {
    background: transparent !important;
    color: rgba(255, 255, 255, 0.7) !important;
    border: none !important;
    padding: 12px 20px !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

.gradio-tabs .tab-nav button.selected {
    background: linear-gradient(45deg, #ff6b35, #f7931e) !important;
    color: white !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3) !important;
}

/* Search results styling */
.search-results {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
}

.search-results h4 {
    color: #ff6b35;
    margin: 0 0 15px 0;
}

.search-results h5 {
    color: #f7931e;
    margin: 15px 0 10px 0;
}

.search-results ul {
    margin: 0 0 15px 20px;
}

.search-results li {
    color: rgba(255, 255, 255, 0.8);
    margin: 5px 0;
    line-height: 1.4;
}

/* Section headers */
.section-header {
    background: linear-gradient(45deg, #ff6b35, #f7931e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
    font-size: 1.2em;
    margin: 20px 0 10px 0;
    padding: 10px 0;
    border-bottom: 2px solid rgba(255, 107, 53, 0.3);
}

/* Form groups */
.gradio-group {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 15px 0 !important;
}

/* Input styling */
.gradio-textbox input, .gradio-textbox textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 8px !important;
    color: white !important;
    padding: 10px !important;
}

.gradio-textbox input:focus, .gradio-textbox textarea:focus {
    border-color: #ff6b35 !important;
    box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2) !important;
}

.gradio-dropdown .wrap {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 8px !important;
}

.gradio-dropdown .wrap:focus-within {
    border-color: #ff6b35 !important;
    box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2) !important;
}
"""

def get_header_html():
    """Generate the application header HTML."""
    return """
    <div style="text-align: center; padding: 30px 0; background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 100%); border-radius: 15px; margin-bottom: 30px; border: 1px solid rgba(255, 255, 255, 0.1);">
        <h1 style="margin: 0; font-size: 3em; background: linear-gradient(45deg, #ff6b35, #f7931e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
            📖 ScriptVoice
        </h1>
        <p style="margin: 10px 0 0 0; color: rgba(255, 255, 255, 0.7); font-size: 1.2em; font-weight: 300;">
            AI-Powered Story Intelligence Platform
        </p>
        <p style="margin: 5px 0 0 0; color: rgba(255, 255, 255, 0.5); font-size: 1em;">
            Transform your stories with intelligent script writing, voice synthesis, and creative knowledge management
        </p>
    </div>
    """

def get_section_header(title):
    """Generate a section header with consistent styling."""
    return f'<div class="section-header">{title}</div>'
