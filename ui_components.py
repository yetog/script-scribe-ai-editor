
"""UI components and styling for ScriptVoice application - Enhanced for new layout."""

CUSTOM_CSS = """
/* ScriptVoice Enhanced CSS - Black/White/Red/Gold Theme with Better Organization */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.gradio-container {
    background: #000000 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #FFFFFF !important;
}

/* Enhanced Word Count and Status Indicators */
.word-count {
    background: linear-gradient(45deg, #E63946, #FFD700) !important;
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 0.9em;
    padding: 8px 12px;
    border-radius: 6px;
    display: inline-block;
    margin-right: 10px;
    box-shadow: 0 2px 4px rgba(230, 57, 70, 0.3);
}

.auto-save {
    background: #1a1a1a !important;
    color: #4CAF50 !important;
    font-weight: 500;
    font-size: 0.9em;
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid #4CAF50;
    display: inline-block;
}

/* Enhanced Button Styling */
.primary-button {
    background: #E63946 !important;
    border: none !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    border-radius: 6px !important;
    padding: 10px 16px !important;
    font-size: 0.9em !important;
}

.primary-button:hover {
    background: #d12a36 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(230, 57, 70, 0.4) !important;
}

.secondary-button {
    background: #1a1a1a !important;
    border: 2px solid #FFD700 !important;
    color: #FFD700 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    border-radius: 6px !important;
    padding: 8px 14px !important;
    font-size: 0.9em !important;
}

.secondary-button:hover {
    background: #FFD700 !important;
    color: #000000 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4) !important;
}

/* Enhanced Sidebar */
.sidebar-column {
    background: #1a1a1a !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-right: 20px !important;
    border: 1px solid #333333 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5) !important;
}

/* Tool Sections */
.tool-section {
    color: #FFD700 !important;
    font-weight: 600;
    font-size: 1em;
    margin: 16px 0 8px 0;
    padding: 8px 0;
    border-bottom: 1px solid #333333;
    font-family: 'Inter', sans-serif;
}

.create-header {
    color: #E63946 !important;
    font-weight: 600;
    font-size: 1.1em;
    margin: 0 0 12px 0;
    padding: 8px 0;
    font-family: 'Inter', sans-serif;
}

/* Enhanced Content Cards */
.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
    margin: 20px 0;
}

.content-card {
    background: #1a1a1a !important;
    border: 1px solid #333333 !important;
    border-radius: 8px;
    padding: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.content-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 57, 70, 0.2);
    border-color: #E63946;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
}

.card-header h3 {
    color: #E63946 !important;
    margin: 0;
    font-size: 1.1em;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    flex: 1;
}

.card-date {
    color: #888888 !important;
    font-size: 0.8em;
    font-weight: 400;
    margin-left: 12px;
}

.card-description {
    color: #CCCCCC !important;
    margin: 0;
    line-height: 1.5;
    font-weight: 400;
    font-size: 0.9em;
}

.type-badge {
    background: #FFD700 !important;
    color: #000000 !important;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.7em;
    font-weight: 600;
    margin-left: 8px;
    display: inline-block;
}

/* Empty States */
.empty-state {
    text-align: center;
    color: #888888 !important;
    font-style: italic;
    padding: 40px 20px;
    background: #1a1a1a !important;
    border: 2px dashed #333333 !important;
    border-radius: 8px;
    margin: 20px 0;
}

/* Enhanced Status Messages */
.status-success {
    color: #4CAF50 !important;
    background-color: rgba(76, 175, 80, 0.1) !important;
    border: 1px solid rgba(76, 175, 80, 0.3) !important;
    padding: 12px 16px;
    border-radius: 6px;
    margin: 10px 0;
    font-weight: 500;
}

.status-error {
    color: #E63946 !important;
    background-color: rgba(230, 57, 70, 0.1) !important;
    border: 1px solid rgba(230, 57, 70, 0.3) !important;
    padding: 12px 16px;
    border-radius: 6px;
    margin: 10px 0;
    font-weight: 500;
}

/* Enhanced Tab Styling */
.gradio-tabs .tab-nav {
    background: #1a1a1a !important;
    border-radius: 8px !important;
    margin-bottom: 20px !important;
    border: 1px solid #333333 !important;
    padding: 4px !important;
}

.gradio-tabs .tab-nav button {
    background: transparent !important;
    color: #CCCCCC !important;
    border: none !important;
    padding: 12px 20px !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    margin: 2px !important;
}

.gradio-tabs .tab-nav button.selected {
    background: #E63946 !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(230, 57, 70, 0.3) !important;
}

.gradio-tabs .tab-nav button:hover:not(.selected) {
    background: rgba(255, 215, 0, 0.1) !important;
    color: #FFD700 !important;
}

/* Enhanced Search Results */
.search-results {
    background: #1a1a1a !important;
    border: 1px solid #333333 !important;
    border-radius: 8px;
    padding: 20px;
    margin: 16px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.search-results h4 {
    color: #E63946 !important;
    margin: 0 0 16px 0;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
}

.search-results h5 {
    color: #FFD700 !important;
    margin: 16px 0 8px 0;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
}

.search-results ul {
    margin: 0 0 16px 20px;
    padding: 0;
}

.search-results li {
    color: #CCCCCC !important;
    margin: 6px 0;
    line-height: 1.4;
}

.search-results pre {
    background: #0a0a0a !important;
    border: 1px solid #333333 !important;
    border-radius: 4px;
    padding: 16px;
    color: #FFFFFF !important;
    font-family: 'Inter', monospace;
    overflow-x: auto;
    font-size: 0.9em;
    line-height: 1.4;
}

/* Section Headers */
.section-header {
    background: linear-gradient(45deg, #E63946, #FFD700) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 700;
    font-size: 1.2em;
    margin: 20px 0 12px 0;
    padding: 8px 0;
    border-bottom: 2px solid #E63946;
    font-family: 'Inter', sans-serif;
}

/* Enhanced Accordions */
.gradio-accordion {
    margin: 12px 0 !important;
}

.gradio-accordion .label-wrap {
    background: #0a0a0a !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}

.gradio-accordion .label-wrap:hover {
    border-color: #E63946 !important;
    background: rgba(230, 57, 70, 0.05) !important;
}

/* Enhanced Form Groups */
.gradio-group {
    background: #1a1a1a !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
    padding: 16px !important;
    margin: 12px 0 !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
}

/* Enhanced Input Styling */
.gradio-textbox input, .gradio-textbox textarea {
    background: #0a0a0a !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
    padding: 10px 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    transition: all 0.3s ease !important;
    font-size: 0.9em !important;
}

.gradio-textbox input:focus, .gradio-textbox textarea:focus {
    border-color: #E63946 !important;
    box-shadow: 0 0 0 2px rgba(230, 57, 70, 0.2) !important;
    outline: none !important;
}

.gradio-textbox input::placeholder, .gradio-textbox textarea::placeholder {
    color: #666666 !important;
}

/* Enhanced Dropdown Styling */
.gradio-dropdown .wrap {
    background: #0a0a0a !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
}

.gradio-dropdown .wrap:focus-within {
    border-color: #E63946 !important;
    box-shadow: 0 0 0 2px rgba(230, 57, 70, 0.2) !important;
}

/* Label Styling */
.gradio-group label, .gradio-textbox label, .gradio-dropdown label {
    color: #FFFFFF !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    margin-bottom: 6px !important;
    font-size: 0.9em !important;
}

/* Audio Player Styling */
.gradio-audio {
    background: #1a1a1a !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
}

/* File Upload Styling */
.gradio-file {
    background: #1a1a1a !important;
    border: 2px dashed #333333 !important;
    border-radius: 6px !important;
    color: #FFFFFF !important;
}

.gradio-file:hover {
    border-color: #E63946 !important;
    background: rgba(230, 57, 70, 0.05) !important;
}

/* Image Upload Styling */
.gradio-image {
    background: #1a1a1a !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
}

/* Slider Styling */
.gradio-slider input[type="range"] {
    background: #333333 !important;
}

.gradio-slider input[type="range"]::-webkit-slider-thumb {
    background: #E63946 !important;
    border: 2px solid #FFFFFF !important;
}

/* Checkbox Styling */
.gradio-checkbox input[type="checkbox"]:checked {
    background: #E63946 !important;
    border-color: #E63946 !important;
}

/* Enhanced Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: #E63946;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #d12a36;
}

/* Overall Container Styling */
body, .gradio-container, .gradio-container > div {
    background: #000000 !important;
    color: #FFFFFF !important;
}

/* Ensure Proper Text Contrast */
h1, h2, h3, h4, h5, h6, p, span, div {
    color: inherit !important;
}

/* Loading States */
.loading-spinner {
    border: 2px solid #333333;
    border-top: 2px solid #E63946;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 8px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .content-grid {
        grid-template-columns: 1fr;
        gap: 12px;
    }
    
    .sidebar-column {
        margin-right: 0;
        margin-bottom: 20px;
    }
    
    .card-header {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .card-date {
        margin-left: 0;
        margin-top: 4px;
    }
}
"""

def get_header_html():
    """Generate the application header HTML."""
    return """
    <div style="text-align: center; padding: 30px 0; background: #000000; border-radius: 12px; margin-bottom: 20px; border: 2px solid #E63946; box-shadow: 0 4px 16px rgba(230, 57, 70, 0.3);">
        <h1 style="margin: 0; font-size: 2.8em; background: linear-gradient(45deg, #E63946, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; font-family: 'Inter', sans-serif;">
            🎬 ScriptVoice
        </h1>
        <p style="margin: 12px 0 0 0; color: #FFFFFF; font-size: 1.2em; font-weight: 400; font-family: 'Inter', sans-serif;">
            AI-Powered Story Intelligence Platform
        </p>
        <p style="margin: 6px 0 0 0; color: #CCCCCC; font-size: 0.9em; font-weight: 300; font-family: 'Inter', sans-serif;">
            Transform your stories with intelligent script writing, voice synthesis, and creative knowledge management
        </p>
    </div>
    """

def get_section_header(title):
    """Generate a section header with consistent styling."""
    return f'<div class="section-header">{title}</div>'
