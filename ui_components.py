
"""UI components and styling for ScriptVoice application - Modern Dark Theme."""

CUSTOM_CSS = """
/* ScriptVoice Modern Dark Theme CSS */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --primary: #ff6b35;
  --primary-dark: #e55a2b;
  --secondary: #ffd700;
  --accent: #00d4aa;
  --background: #0a0a0a;
  --surface: #111111;
  --surface-elevated: #1a1a1a;
  --surface-hover: #222222;
  --border: #2a2a2a;
  --border-accent: #333333;
  --text-primary: #ffffff;
  --text-secondary: #b3b3b3;
  --text-muted: #666666;
  --success: #00d4aa;
  --error: #ff4757;
  --warning: #ffa726;
  --glass-bg: rgba(17, 17, 17, 0.8);
  --glass-border: rgba(255, 255, 255, 0.1);
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
  --shadow-accent: 0 4px 20px rgba(255, 107, 53, 0.3);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.gradio-container {
    background: var(--background) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

/* Modern Glass Cards */
.content-card {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-md) !important;
    padding: 24px !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-sm) !important;
    position: relative;
    overflow: hidden;
}

.content-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
}

.content-card:hover {
    transform: translateY(-4px) !important;
    box-shadow: var(--shadow-md) !important;
    border-color: var(--primary) !important;
    background: rgba(26, 26, 26, 0.9) !important;
}

/* Modern Buttons */
.primary-button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    border: none !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: var(--transition) !important;
    border-radius: var(--radius-sm) !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    box-shadow: var(--shadow-sm) !important;
    position: relative;
    overflow: hidden;
}

.primary-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.primary-button:hover::before {
    left: 100%;
}

.primary-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-accent) !important;
    background: linear-gradient(135deg, #ff7849, var(--primary)) !important;
}

.secondary-button {
    background: var(--surface-elevated) !important;
    border: 2px solid var(--secondary) !important;
    color: var(--secondary) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: var(--transition) !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 22px !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px) !important;
}

.secondary-button:hover {
    background: var(--secondary) !important;
    color: var(--background) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4) !important;
}

/* Modern Status Indicators */
.word-count {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    box-shadow: var(--shadow-sm) !important;
    backdrop-filter: blur(10px) !important;
}

.word-count::before {
    content: '📝';
    font-size: 16px;
}

.auto-save {
    background: var(--glass-bg) !important;
    color: var(--success) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    border: 1px solid var(--success) !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    backdrop-filter: blur(10px) !important;
}

.auto-save::before {
    content: '✓';
    font-weight: bold;
}

/* Enhanced Sidebar */
.sidebar-column {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: var(--radius-lg) !important;
    padding: 24px !important;
    margin-right: 24px !important;
    border: 1px solid var(--glass-border) !important;
    box-shadow: var(--shadow-md) !important;
    position: relative;
}

.sidebar-column::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: var(--radius-lg);
    padding: 1px;
    background: linear-gradient(145deg, var(--primary), var(--secondary), var(--accent));
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: xor;
    opacity: 0.3;
}

/* Modern Section Headers */
.section-header {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    font-weight: 800 !important;
    font-size: 18px !important;
    margin: 24px 0 16px 0 !important;
    padding: 0 !important;
    font-family: 'Inter', sans-serif !important;
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 40px;
    height: 3px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 2px;
}

.tool-section {
    color: var(--secondary) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    margin: 20px 0 12px 0 !important;
    padding: 12px 0 !important;
    border-bottom: 1px solid var(--border) !important;
    font-family: 'Inter', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.create-header {
    color: var(--primary) !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    margin: 0 0 16px 0 !important;
    padding: 0 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Enhanced Content Grid */
.content-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)) !important;
    gap: 20px !important;
    margin: 24px 0 !important;
}

.card-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    margin-bottom: 16px !important;
}

.card-header h3 {
    color: var(--text-primary) !important;
    margin: 0 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    flex: 1 !important;
}

.card-date {
    color: var(--text-muted) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    margin-left: 16px !important;
    background: var(--surface) !important;
    padding: 4px 8px !important;
    border-radius: 6px !important;
}

.card-description {
    color: var(--text-secondary) !important;
    margin: 0 !important;
    line-height: 1.6 !important;
    font-weight: 400 !important;
    font-size: 14px !important;
}

.type-badge {
    background: linear-gradient(135deg, var(--accent), var(--secondary)) !important;
    color: var(--background) !important;
    padding: 4px 12px !important;
    border-radius: 12px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    margin-left: 12px !important;
    display: inline-block !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* Modern Empty States */
.empty-state {
    text-align: center !important;
    color: var(--text-muted) !important;
    font-style: normal !important;
    padding: 48px 24px !important;
    background: var(--glass-bg) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius-md) !important;
    margin: 24px 0 !important;
    backdrop-filter: blur(10px) !important;
    font-weight: 500 !important;
}

/* Enhanced Status Messages */
.status-success {
    color: var(--success) !important;
    background: rgba(0, 212, 170, 0.1) !important;
    border: 1px solid rgba(0, 212, 170, 0.3) !important;
    padding: 16px 20px !important;
    border-radius: var(--radius-sm) !important;
    margin: 12px 0 !important;
    font-weight: 600 !important;
    backdrop-filter: blur(10px) !important;
}

.status-error {
    color: var(--error) !important;
    background: rgba(255, 71, 87, 0.1) !important;
    border: 1px solid rgba(255, 71, 87, 0.3) !important;
    padding: 16px 20px !important;
    border-radius: var(--radius-sm) !important;
    margin: 12px 0 !important;
    font-weight: 600 !important;
    backdrop-filter: blur(10px) !important;
}

/* Modern Tab Styling */
.gradio-tabs .tab-nav {
    background: var(--surface-elevated) !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 24px !important;
    border: 1px solid var(--border) !important;
    padding: 6px !important;
    backdrop-filter: blur(20px) !important;
}

.gradio-tabs .tab-nav button {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: var(--transition) !important;
    margin: 2px !important;
    font-size: 14px !important;
}

.gradio-tabs .tab-nav button.selected {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: var(--text-primary) !important;
    box-shadow: var(--shadow-sm) !important;
}

.gradio-tabs .tab-nav button:hover:not(.selected) {
    background: var(--surface-hover) !important;
    color: var(--text-primary) !important;
}

/* Enhanced Search Results */
.search-results {
    background: var(--glass-bg) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: var(--radius-md) !important;
    padding: 24px !important;
    margin: 20px 0 !important;
    box-shadow: var(--shadow-md) !important;
    backdrop-filter: blur(20px) !important;
}

.search-results h4 {
    color: var(--primary) !important;
    margin: 0 0 20px 0 !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 18px !important;
}

.search-results h5 {
    color: var(--secondary) !important;
    margin: 20px 0 12px 0 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

.search-results ul {
    margin: 0 0 20px 24px !important;
    padding: 0 !important;
}

.search-results li {
    color: var(--text-secondary) !important;
    margin: 8px 0 !important;
    line-height: 1.5 !important;
}

.search-results pre {
    background: var(--background) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 20px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    overflow-x: auto !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
}

/* Enhanced Input Styling */
.gradio-textbox input, .gradio-textbox textarea {
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    padding: 14px 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    transition: var(--transition) !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px) !important;
}

.gradio-textbox input:focus, .gradio-textbox textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
    outline: none !important;
    background: var(--surface-elevated) !important;
}

.gradio-textbox input::placeholder, .gradio-textbox textarea::placeholder {
    color: var(--text-muted) !important;
}

/* Enhanced Dropdown Styling */
.gradio-dropdown .wrap {
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    backdrop-filter: blur(10px) !important;
}

.gradio-dropdown .wrap:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
}

/* Modern Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--surface);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, var(--primary-dark), var(--secondary));
}

/* Loading States */
.loading-spinner {
    border: 3px solid var(--border);
    border-top: 3px solid var(--primary);
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
    display: inline-block;
    margin-right: 12px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
    .content-grid {
        grid-template-columns: 1fr !important;
        gap: 16px !important;
    }
    
    .sidebar-column {
        margin-right: 0 !important;
        margin-bottom: 24px !important;
    }
    
    .card-header {
        flex-direction: column !important;
        align-items: flex-start !important;
    }
    
    .card-date {
        margin-left: 0 !important;
        margin-top: 8px !important;
    }
}

/* Overall Theme */
body, .gradio-container, .gradio-container > div {
    background: var(--background) !important;
    color: var(--text-primary) !important;
}

h1, h2, h3, h4, h5, h6, p, span, div {
    color: inherit !important;
}

/* Label Styling */
.gradio-group label, .gradio-textbox label, .gradio-dropdown label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    margin-bottom: 8px !important;
    font-size: 14px !important;
}

/* Enhanced Group Styling */
.gradio-group {
    background: var(--glass-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 20px !important;
    margin: 16px 0 !important;
    box-shadow: var(--shadow-sm) !important;
    backdrop-filter: blur(10px) !important;
}

/* File Upload Styling */
.gradio-file {
    background: var(--surface) !important;
    border: 2px dashed var(--border-accent) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    transition: var(--transition) !important;
}

.gradio-file:hover {
    border-color: var(--primary) !important;
    background: var(--surface-elevated) !important;
}
"""

def get_header_html():
    """Generate the modern application header HTML."""
    return """
    <div style="text-align: center; padding: 40px 0; background: linear-gradient(135deg, rgba(255, 107, 53, 0.1), rgba(255, 215, 0, 0.1)); border-radius: 16px; margin-bottom: 32px; border: 1px solid rgba(255, 107, 53, 0.2); backdrop-filter: blur(20px); position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255, 107, 53, 0.5), transparent);"></div>
        <h1 style="margin: 0; font-size: 3.5em; background: linear-gradient(135deg, #ff6b35, #ffd700, #00d4aa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-family: 'Inter', sans-serif; line-height: 1.1;">
            🎬 ScriptVoice
        </h1>
        <p style="margin: 16px 0 0 0; color: #ffffff; font-size: 1.3em; font-weight: 500; font-family: 'Inter', sans-serif;">
            AI-Powered Story Intelligence Platform
        </p>
        <p style="margin: 8px 0 0 0; color: #b3b3b3; font-size: 1em; font-weight: 400; font-family: 'Inter', sans-serif;">
            Transform your stories with intelligent script writing, voice synthesis, and creative knowledge management
        </p>
    </div>
    """

def get_section_header(title):
    """Generate a section header with modern styling."""
    return f'<div class="section-header">{title}</div>'
