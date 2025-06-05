
"""UI components and custom CSS styling for ScriptVoice."""

# Custom CSS for ScriptVoice branding
CUSTOM_CSS = """
/* ScriptVoice Custom Styling */
:root {
    --script-red: #E63946;
    --script-gold: #FFD700;
    --script-black: #000000;
    --script-dark-gray: #1a1a1a;
    --script-border: rgba(230, 57, 70, 0.2);
}

/* Global dark theme */
.gradio-container {
    background-color: var(--script-black) !important;
    color: white !important;
}

/* Main container styling */
.contain {
    background-color: var(--script-black) !important;
}

/* Header styling */
.header-container {
    background: var(--script-black) !important;
    border-bottom: 2px solid var(--script-border) !important;
    padding: 1.5rem !important;
}

/* Sidebar styling */
.sidebar-column {
    background-color: var(--script-dark-gray) !important;
    border-right: 1px solid var(--script-border) !important;
    padding: 1rem !important;
}

/* Button styling */
.primary-button {
    background: linear-gradient(135deg, var(--script-red), #c62d36) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.primary-button:hover {
    background: linear-gradient(135deg, #c62d36, var(--script-red)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(230, 57, 70, 0.3) !important;
}

.secondary-button {
    background: var(--script-dark-gray) !important;
    color: white !important;
    border: 1px solid var(--script-border) !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.secondary-button:hover {
    background: var(--script-red) !important;
    border-color: var(--script-red) !important;
}

/* Input and textarea styling */
textarea, input[type="text"], .gr-textbox {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
}

textarea:focus, input[type="text"]:focus, .gr-textbox:focus {
    border-color: var(--script-red) !important;
    box-shadow: 0 0 0 2px rgba(230, 57, 70, 0.2) !important;
    outline: none !important;
}

/* Dropdown styling */
.gr-dropdown {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    color: white !important;
}

/* Group styling */
.gr-group {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
}

/* Audio player styling */
.gr-audio {
    background-color: var(--script-dark-gray) !important;
    border: 1px solid var(--script-border) !important;
    border-radius: 8px !important;
}

/* File upload styling */
.gr-file {
    background-color: var(--script-dark-gray) !important;
    border: 2px dashed var(--script-border) !important;
    border-radius: 8px !important;
    color: white !important;
}

/* Slider styling */
.gr-slider input[type="range"] {
    background: var(--script-dark-gray) !important;
}

.gr-slider input[type="range"]::-webkit-slider-thumb {
    background: var(--script-red) !important;
}

/* Checkbox styling */
.gr-checkbox {
    accent-color: var(--script-red) !important;
}

/* Word count highlight */
.word-count-highlight {
    color: var(--script-gold) !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent) !important;
    padding: 0.25rem 0.5rem !important;
    border-radius: 4px !important;
}

/* Status messages */
.status-success {
    color: #4ade80 !important;
    background: rgba(74, 222, 128, 0.1) !important;
    padding: 0.5rem !important;
    border-radius: 6px !important;
    border-left: 3px solid #4ade80 !important;
}

.status-error {
    color: #f87171 !important;
    background: rgba(248, 113, 113, 0.1) !important;
    padding: 0.5rem !important;
    border-radius: 6px !important;
    border-left: 3px solid #f87171 !important;
}

/* Animated gold highlight for active elements */
@keyframes goldShine {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

.gold-highlight {
    background: linear-gradient(90deg, transparent, var(--script-gold), transparent) !important;
    background-size: 200% 100% !important;
    animation: goldShine 2s ease-in-out infinite !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* Logo styling */
.script-logo {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    margin-bottom: 1rem !important;
}

.script-text {
    color: var(--script-red) !important;
}

.voice-text {
    color: var(--script-gold) !important;
}

/* Section headers */
.section-header {
    color: var(--script-gold) !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    margin: 1rem 0 0.5rem 0 !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid var(--script-border) !important;
}
"""


def get_header_html() -> str:
    """Get the header HTML with ScriptVoice branding."""
    return """
    <div class="header-container">
        <div class="script-logo">
            <span class="script-text">Script</span><span class="voice-text">Voice</span>
        </div>
        <div style="text-align: center; color: #888; font-size: 1.1rem; margin-top: 0.5rem;">
            AI-Powered TTS Script Editor
        </div>
    </div>
    """


def get_section_header(title: str) -> str:
    """Get a styled section header."""
    return f'<div class="section-header">{title}</div>'
