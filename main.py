
"""Main application entry point for ScriptVoice - Pure Gradio Application."""

import gradio as gr
from models import (
    load_projects, create_new_project, load_project, 
    save_script_content, update_word_count,
    create_story, create_character, create_world_element,
    get_all_stories, get_all_characters, get_all_world_elements,
    search_content
)
from ui_components import CUSTOM_CSS, get_header_html, get_section_header
from audio_services import generate_tts
from image_services import extract_text_from_image
from enhancement_services import (
    enhance_script_placeholder, enhance_script_with_context,
    analyze_character_consistency, suggest_story_elements
)
from export_services import export_project
from knowledge_assistant import knowledge_assistant


# Global state for current project
current_project_id = None


def create_scripts_interface():
    """Create the main scripts interface with better organization."""
    
    with gr.Row():
        # Left Sidebar - Organized with Accordions
        with gr.Column(scale=1, min_width=320, elem_classes=["sidebar-column"]):
            
            # Project Management - Always Visible
            gr.HTML(get_section_header('📁 Project Workspace'))
            with gr.Group():
                new_project_name = gr.Textbox(
                    label="New Project", 
                    placeholder="Enter project name...",
                    scale=2
                )
                with gr.Row():
                    create_btn = gr.Button("➕ Create", elem_classes=["primary-button"], scale=1)
                create_status = gr.HTML(visible=False)
            
            project_dropdown = gr.Dropdown(
                label="Select Project",
                container=False
            )
            
            # Quick Actions - Collapsible
            with gr.Accordion("⚡ Quick Actions", open=True):
                with gr.Row():
                    save_btn = gr.Button("💾 Save", elem_classes=["secondary-button"])
                    tts_btn = gr.Button("🔊 Play", elem_classes=["primary-button"])
                save_status = gr.HTML(visible=False)
                tts_status = gr.HTML(visible=False)
            
            # Project Notes - Collapsible
            with gr.Accordion("📝 Notes", open=False):
                notes_textbox = gr.Textbox(
                    label="Project Notes",
                    placeholder="Add your notes here...",
                    lines=4,
                    container=False
                )
            
            # Advanced Tools - Collapsible
            with gr.Accordion("🛠️ Advanced Tools", open=False):
                # OCR Section
                gr.HTML('<div class="tool-section">📷 Extract Text from Image</div>')
                image_input = gr.Image(type="filepath", label="Upload Image", height=150)
                ocr_btn = gr.Button("Extract Text", elem_classes=["secondary-button"])
                ocr_status = gr.HTML(visible=False)
                
                # AI Enhancement
                gr.HTML('<div class="tool-section">🤖 AI Enhancement</div>')
                enhancement_type = gr.Dropdown(
                    choices=["dramatic", "romantic", "professional", "casual"],
                    label="Style",
                    value="dramatic",
                    container=False
                )
                enhance_btn = gr.Button("✨ Enhance", elem_classes=["primary-button"])
                enhance_status = gr.HTML(visible=False)
                
                # Export
                gr.HTML('<div class="tool-section">📤 Export</div>')
                export_type = gr.Dropdown(
                    choices=["text", "audio"],
                    label="Type",
                    value="text",
                    container=False
                )
                export_btn = gr.Button("📥 Export", elem_classes=["secondary-button"])
                export_file = gr.File(label="Download", visible=False)
                export_status = gr.HTML(visible=False)
            
            # Settings - Collapsible
            with gr.Accordion("⚙️ Settings", open=False):
                dyslexic_mode = gr.Checkbox(label="Dyslexic-friendly font", value=False)
                voice_speed = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Voice Speed")
                voice_volume = gr.Slider(0.1, 1.0, value=1.0, step=0.1, label="Voice Volume")
        
        # Main Editor Panel
        with gr.Column(scale=2):
            # Status Bar
            with gr.Row():
                word_count_display = gr.HTML('<div class="word-count">📊 Words: 0</div>')
                auto_save_status = gr.HTML('<div class="auto-save">💾 Saved</div>')
            
            # Script Editor
            script_textbox = gr.Textbox(
                label="Script Editor",
                placeholder="Start writing your script here...\n\nTip: Your content will be automatically indexed for the Knowledge Assistant.",
                lines=20,
                max_lines=30,
                container=False
            )
            
            # Audio Output
            audio_output = gr.Audio(label="Generated Audio", visible=False)
    
    return {
        'new_project_name': new_project_name,
        'create_btn': create_btn,
        'create_status': create_status,
        'project_dropdown': project_dropdown,
        'save_btn': save_btn,
        'tts_btn': tts_btn,
        'save_status': save_status,
        'tts_status': tts_status,
        'notes_textbox': notes_textbox,
        'image_input': image_input,
        'ocr_btn': ocr_btn,
        'ocr_status': ocr_status,
        'enhancement_type': enhancement_type,
        'enhance_btn': enhance_btn,
        'enhance_status': enhance_status,
        'export_type': export_type,
        'export_btn': export_btn,
        'export_file': export_file,
        'export_status': export_status,
        'dyslexic_mode': dyslexic_mode,
        'voice_speed': voice_speed,
        'voice_volume': voice_volume,
        'word_count_display': word_count_display,
        'auto_save_status': auto_save_status,
        'script_textbox': script_textbox,
        'audio_output': audio_output
    }


def create_knowledge_tab():
    """Knowledge Assistant and Search."""
    with gr.Column():
        gr.HTML(get_section_header('🤖 Knowledge Assistant'))
        
        assistant_query = gr.Textbox(
            label="Ask your Knowledge Assistant", 
            placeholder="Try: !search dragons, !characters, !stories, or ask any question...",
            lines=2
        )
        assistant_btn = gr.Button("🔍 Query Assistant", elem_classes=["primary-button"])
        assistant_response = gr.HTML(visible=False)
        
        # Advanced Search
        with gr.Accordion("🔍 Advanced Search", open=False):
            search_input = gr.Textbox(label="Search Query", placeholder="Search stories, characters, world...")
            search_btn = gr.Button("🔍 Search", elem_classes=["secondary-button"])
            search_results = gr.HTML(visible=False)
        
        # Knowledge Base Management
        with gr.Accordion("⚙️ Knowledge Base", open=False):
            rebuild_btn = gr.Button("🔄 Rebuild Index", elem_classes=["secondary-button"])
            rebuild_status = gr.HTML(visible=False)
    
    return {
        'assistant_query': assistant_query,
        'assistant_btn': assistant_btn,
        'assistant_response': assistant_response,
        'search_input': search_input,
        'search_btn': search_btn,
        'search_results': search_results,
        'rebuild_btn': rebuild_btn,
        'rebuild_status': rebuild_status
    }


def create_stories_tab():
    """Stories management and display."""
    with gr.Column():
        # Create New Story
        with gr.Group():
            gr.HTML('<div class="create-header">📖 Create New Story</div>')
            with gr.Row():
                new_story_title = gr.Textbox(label="Title", placeholder="Story title...", scale=2)
                create_story_btn = gr.Button("➕ Create", elem_classes=["primary-button"], scale=1)
            new_story_desc = gr.Textbox(label="Description", placeholder="Brief description...", lines=2)
            story_status = gr.HTML(visible=False)
        
        # Stories Display
        story_dropdown = gr.Dropdown(label="Select Story", choices=[])
        stories_display = gr.HTML()
    
    return {
        'new_story_title': new_story_title,
        'new_story_desc': new_story_desc,
        'create_story_btn': create_story_btn,
        'story_status': story_status,
        'story_dropdown': story_dropdown,
        'stories_display': stories_display
    }


def create_characters_tab():
    """Characters management and display."""
    with gr.Column():
        # Create New Character
        with gr.Group():
            gr.HTML('<div class="create-header">👤 Create New Character</div>')
            with gr.Row():
                new_char_name = gr.Textbox(label="Name", placeholder="Character name...", scale=2)
                create_char_btn = gr.Button("➕ Create", elem_classes=["primary-button"], scale=1)
            new_char_desc = gr.Textbox(label="Description", placeholder="Character description...", lines=2)
            char_status = gr.HTML(visible=False)
        
        # Characters Display
        character_dropdown = gr.Dropdown(label="Select Character", choices=[])
        characters_display = gr.HTML()
    
    return {
        'new_char_name': new_char_name,
        'new_char_desc': new_char_desc,
        'create_char_btn': create_char_btn,
        'char_status': char_status,
        'character_dropdown': character_dropdown,
        'characters_display': characters_display
    }


def create_world_tab():
    """World elements management and display."""
    with gr.Column():
        # Create New World Element
        with gr.Group():
            gr.HTML('<div class="create-header">🌍 Create World Element</div>')
            with gr.Row():
                new_world_name = gr.Textbox(label="Name", placeholder="Element name...", scale=2)
                create_world_btn = gr.Button("➕ Create", elem_classes=["primary-button"], scale=1)
            with gr.Row():
                world_type = gr.Dropdown(
                    choices=["location", "organization", "concept", "item"],
                    label="Type",
                    value="location",
                    scale=1
                )
            new_world_desc = gr.Textbox(label="Description", placeholder="Element description...", lines=2)
            world_status = gr.HTML(visible=False)
        
        # World Elements Display
        world_dropdown = gr.Dropdown(label="Select Element", choices=[])
        world_display = gr.HTML()
    
    return {
        'new_world_name': new_world_name,
        'world_type': world_type,
        'new_world_desc': new_world_desc,
        'create_world_btn': create_world_btn,
        'world_status': world_status,
        'world_dropdown': world_dropdown,
        'world_display': world_display
    }


def create_ai_tools_tab():
    """AI analysis and enhancement tools."""
    with gr.Column():
        gr.HTML(get_section_header('🎯 Context-Aware AI Tools'))
        
        ai_analysis_text = gr.Textbox(
            label="Text to Analyze", 
            placeholder="Paste your script text here for AI analysis and enhancement...",
            lines=6
        )
        
        with gr.Row():
            consistency_btn = gr.Button("✅ Check Consistency", elem_classes=["secondary-button"])
            suggest_btn = gr.Button("💡 Suggest Elements", elem_classes=["secondary-button"])
        
        with gr.Row():
            context_enhancement_type = gr.Dropdown(
                choices=["character_consistent", "plot_coherent", "dramatic", "romantic"],
                label="Enhancement Type",
                value="character_consistent",
                scale=2
            )
            context_enhance_btn = gr.Button("🎭 Enhance with Context", elem_classes=["primary-button"], scale=1)
        
        ai_analysis_output = gr.HTML(visible=False)
    
    return {
        'ai_analysis_text': ai_analysis_text,
        'consistency_btn': consistency_btn,
        'suggest_btn': suggest_btn,
        'context_enhancement_type': context_enhancement_type,
        'context_enhance_btn': context_enhance_btn,
        'ai_analysis_output': ai_analysis_output
    }


def create_story_intelligence_interface():
    """Create the redesigned story intelligence interface."""
    
    with gr.Column():
        # Main Tabs for Story Intelligence
        with gr.Tabs():
            with gr.TabItem("🤖 Knowledge", elem_id="knowledge-tab"):
                knowledge_components = create_knowledge_tab()
            
            with gr.TabItem("📚 Stories", elem_id="stories-tab"):
                stories_components = create_stories_tab()
            
            with gr.TabItem("👥 Characters", elem_id="characters-tab"):
                characters_components = create_characters_tab()
            
            with gr.TabItem("🌍 World", elem_id="world-tab"):
                world_components = create_world_tab()
            
            with gr.TabItem("🎯 AI Tools", elem_id="ai-tools-tab"):
                ai_tools_components = create_ai_tools_tab()
    
    # Combine all components
    all_components = {}
    all_components.update(knowledge_components)
    all_components.update(stories_components)
    all_components.update(characters_components)
    all_components.update(world_components)
    all_components.update(ai_tools_components)
    
    return all_components


# Helper functions for event handlers
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


def create_interface():
    """Create the main Gradio interface with improved UI."""
    
    # Load initial projects
    data = load_projects()
    project_choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    with gr.Blocks(
        title="ScriptVoice - AI-Powered Story Intelligence Platform", 
        theme=gr.themes.Base(),
        css=CUSTOM_CSS
    ) as app:
        
        # Header
        gr.HTML(get_header_html())
        
        # Main interface with improved tabs
        with gr.Tabs() as main_tabs:
            # Scripts Tab (Redesigned)
            with gr.TabItem("📝 Scripts", elem_id="scripts-tab"):
                scripts_components = create_scripts_interface()
                
                # Set initial project choices
                scripts_components['project_dropdown'].choices = project_choices
                if project_choices:
                    scripts_components['project_dropdown'].value = project_choices[0][1]
            
            # Story Intelligence Tab (Redesigned)
            with gr.TabItem("📚 Story Intelligence", elem_id="intelligence-tab"):
                story_components = create_story_intelligence_interface()
        
        # Event Handlers for Scripts Tab
        scripts_components['create_btn'].click(
            fn=create_new_project,
            inputs=[scripts_components['new_project_name']],
            outputs=[scripts_components['create_status'], scripts_components['project_dropdown']]
        ).then(
            lambda: ("", gr.update(visible=True)),
            outputs=[scripts_components['new_project_name'], scripts_components['create_status']]
        )
        
        scripts_components['project_dropdown'].change(
            fn=load_project,
            inputs=[scripts_components['project_dropdown']],
            outputs=[scripts_components['script_textbox'], scripts_components['notes_textbox'], scripts_components['word_count_display']]
        )
        
        scripts_components['script_textbox'].change(
            fn=update_word_count,
            inputs=[scripts_components['script_textbox']],
            outputs=[scripts_components['word_count_display']]
        )
        
        scripts_components['save_btn'].click(
            fn=save_script_content,
            inputs=[scripts_components['project_dropdown'], scripts_components['script_textbox'], scripts_components['notes_textbox']],
            outputs=[scripts_components['save_status']]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[scripts_components['save_status']]
        )
        
        scripts_components['tts_btn'].click(
            fn=generate_tts,
            inputs=[scripts_components['script_textbox'], scripts_components['voice_speed']],
            outputs=[scripts_components['audio_output'], scripts_components['tts_status']]
        ).then(
            lambda: (gr.update(visible=True), gr.update(visible=True)),
            outputs=[scripts_components['audio_output'], scripts_components['tts_status']]
        )
        
        scripts_components['ocr_btn'].click(
            fn=extract_text_from_image,
            inputs=[scripts_components['image_input']],
            outputs=[scripts_components['script_textbox'], scripts_components['ocr_status']]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[scripts_components['ocr_status']]
        )
        
        scripts_components['enhance_btn'].click(
            fn=enhance_script_placeholder,
            inputs=[scripts_components['script_textbox'], scripts_components['enhancement_type']],
            outputs=[scripts_components['script_textbox'], scripts_components['enhance_status']]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[scripts_components['enhance_status']]
        )
        
        scripts_components['export_btn'].click(
            fn=export_project,
            inputs=[scripts_components['project_dropdown'], scripts_components['export_type']],
            outputs=[scripts_components['export_file'], scripts_components['export_status']]
        ).then(
            lambda: (gr.update(visible=True), gr.update(visible=True)),
            outputs=[scripts_components['export_file'], scripts_components['export_status']]
        )
        
        # Event Handlers for Story Intelligence Tab
        story_components['assistant_btn'].click(
            fn=query_knowledge_assistant,
            inputs=[story_components['assistant_query']],
            outputs=[story_components['assistant_response'], story_components['assistant_response']]
        )
        
        story_components['consistency_btn'].click(
            fn=analyze_consistency,
            inputs=[story_components['ai_analysis_text']],
            outputs=[story_components['ai_analysis_output'], story_components['ai_analysis_output']]
        )
        
        story_components['suggest_btn'].click(
            fn=suggest_elements,
            inputs=[story_components['ai_analysis_text']],
            outputs=[story_components['ai_analysis_output'], story_components['ai_analysis_output']]
        )
        
        story_components['context_enhance_btn'].click(
            fn=enhance_with_context,
            inputs=[story_components['ai_analysis_text'], story_components['context_enhancement_type']],
            outputs=[story_components['ai_analysis_output'], story_components['ai_analysis_output']]
        )
        
        story_components['rebuild_btn'].click(
            fn=rebuild_knowledge_index,
            outputs=[story_components['rebuild_status'], story_components['rebuild_status']]
        )
        
        story_components['create_story_btn'].click(
            fn=create_story,
            inputs=[story_components['new_story_title'], story_components['new_story_desc']],
            outputs=[story_components['story_status'], story_components['story_dropdown']]
        ).then(
            lambda: ("", "", gr.update(visible=True)),
            outputs=[story_components['new_story_title'], story_components['new_story_desc'], story_components['story_status']]
        ).then(
            fn=display_stories,
            outputs=[story_components['stories_display']]
        )
        
        story_components['create_char_btn'].click(
            fn=create_character,
            inputs=[story_components['new_char_name'], story_components['new_char_desc']],
            outputs=[story_components['char_status'], story_components['character_dropdown']]
        ).then(
            lambda: ("", "", gr.update(visible=True)),
            outputs=[story_components['new_char_name'], story_components['new_char_desc'], story_components['char_status']]
        ).then(
            fn=display_characters,
            outputs=[story_components['characters_display']]
        )
        
        story_components['create_world_btn'].click(
            fn=create_world_element,
            inputs=[story_components['new_world_name'], story_components['world_type'], story_components['new_world_desc']],
            outputs=[story_components['world_status'], story_components['world_dropdown']]
        ).then(
            lambda: ("", "", gr.update(visible=True)),
            outputs=[story_components['new_world_name'], story_components['new_world_desc'], story_components['world_status']]
        ).then(
            fn=display_world_elements,
            outputs=[story_components['world_display']]
        )
        
        story_components['search_btn'].click(
            fn=perform_search,
            inputs=[story_components['search_input']],
            outputs=[story_components['search_results']]
        )
        
        # Load initial data
        app.load(
            fn=display_stories,
            outputs=[story_components['stories_display']]
        )
        app.load(
            fn=display_characters,
            outputs=[story_components['characters_display']]
        )
        app.load(
            fn=display_world_elements,
            outputs=[story_components['world_display']]
        )
    
    return app


if __name__ == "__main__":
    print("🚀 Starting ScriptVoice - AI-Powered Story Intelligence Platform")
    print("🌐 The app will be available at: http://localhost:7860")
    
    # Create and launch the app
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
