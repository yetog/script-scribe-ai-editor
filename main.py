
"""Main application entry point for ScriptVoice."""

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
from enhancement_services import enhance_script_placeholder
from export_services import export_project


# Global state for current project
current_project_id = None


def create_story_intelligence_interface():
    """Create the story intelligence interface components."""
    
    with gr.Column():
        # Search functionality
        gr.HTML(get_section_header('🔍 Search Knowledge Base'))
        with gr.Row():
            search_input = gr.Textbox(label="Search", placeholder="Search stories, characters, world...")
            search_btn = gr.Button("🔍 Search", elem_classes=["primary-button"])
        search_results = gr.HTML(visible=False)
        
        # Story Management
        gr.HTML(get_section_header('📚 Stories'))
        with gr.Group():
            new_story_title = gr.Textbox(label="Story Title", placeholder="Enter story title...")
            new_story_desc = gr.Textbox(label="Description", placeholder="Brief description...", lines=2)
            create_story_btn = gr.Button("📖 Create Story", elem_classes=["primary-button"])
            story_status = gr.HTML(visible=False)
        
        story_dropdown = gr.Dropdown(label="Select Story", choices=[])
        stories_display = gr.HTML()
        
        # Character Management
        gr.HTML(get_section_header('👥 Characters'))
        with gr.Group():
            new_char_name = gr.Textbox(label="Character Name", placeholder="Enter character name...")
            new_char_desc = gr.Textbox(label="Description", placeholder="Character description...", lines=2)
            create_char_btn = gr.Button("👤 Create Character", elem_classes=["primary-button"])
            char_status = gr.HTML(visible=False)
        
        character_dropdown = gr.Dropdown(label="Select Character", choices=[])
        characters_display = gr.HTML()
        
        # World Building
        gr.HTML(get_section_header('🌍 World Elements'))
        with gr.Group():
            new_world_name = gr.Textbox(label="Element Name", placeholder="Enter element name...")
            world_type = gr.Dropdown(
                choices=["location", "organization", "concept", "item"],
                label="Type",
                value="location"
            )
            new_world_desc = gr.Textbox(label="Description", placeholder="Element description...", lines=2)
            create_world_btn = gr.Button("🏛️ Create Element", elem_classes=["primary-button"])
            world_status = gr.HTML(visible=False)
        
        world_dropdown = gr.Dropdown(label="Select World Element", choices=[])
        world_display = gr.HTML()
    
    return {
        'search_input': search_input,
        'search_btn': search_btn,
        'search_results': search_results,
        'new_story_title': new_story_title,
        'new_story_desc': new_story_desc,
        'create_story_btn': create_story_btn,
        'story_status': story_status,
        'story_dropdown': story_dropdown,
        'stories_display': stories_display,
        'new_char_name': new_char_name,
        'new_char_desc': new_char_desc,
        'create_char_btn': create_char_btn,
        'char_status': char_status,
        'character_dropdown': character_dropdown,
        'characters_display': characters_display,
        'new_world_name': new_world_name,
        'world_type': world_type,
        'new_world_desc': new_world_desc,
        'create_world_btn': create_world_btn,
        'world_status': world_status,
        'world_dropdown': world_dropdown,
        'world_display': world_display
    }


def display_stories():
    """Display all stories in a formatted way."""
    stories = get_all_stories()
    if not stories:
        return "<p>No stories created yet.</p>"
    
    html = "<div class='stories-grid'>"
    for story in stories:
        html += f"""
        <div class='story-card'>
            <h3>{story['title']}</h3>
            <p>{story['description'][:100]}{'...' if len(story['description']) > 100 else ''}</p>
            <small>Created: {story['created_at'][:10]}</small>
        </div>
        """
    html += "</div>"
    return html


def display_characters():
    """Display all characters in a formatted way."""
    characters = get_all_characters()
    if not characters:
        return "<p>No characters created yet.</p>"
    
    html = "<div class='characters-grid'>"
    for char in characters:
        html += f"""
        <div class='character-card'>
            <h3>{char['name']}</h3>
            <p>{char['description'][:100]}{'...' if len(char['description']) > 100 else ''}</p>
            <small>Created: {char['created_at'][:10]}</small>
        </div>
        """
    html += "</div>"
    return html


def display_world_elements():
    """Display all world elements in a formatted way."""
    elements = get_all_world_elements()
    if not elements:
        return "<p>No world elements created yet.</p>"
    
    html = "<div class='world-grid'>"
    for elem in elements:
        html += f"""
        <div class='world-card'>
            <h3>{elem['name']} <span class='type-badge'>{elem['type']}</span></h3>
            <p>{elem['description'][:100]}{'...' if len(elem['description']) > 100 else ''}</p>
            <small>Created: {elem['created_at'][:10]}</small>
        </div>
        """
    html += "</div>"
    return html


def perform_search(query):
    """Perform search across all content."""
    if not query.strip():
        return gr.update(visible=False)
    
    results = search_content(query)
    
    html = f"<h4>Search Results for: '{query}'</h4>"
    
    if results['stories']:
        html += "<h5>Stories:</h5><ul>"
        for story in results['stories']:
            html += f"<li><strong>{story['title']}</strong> - {story['description'][:50]}...</li>"
        html += "</ul>"
    
    if results['characters']:
        html += "<h5>Characters:</h5><ul>"
        for char in results['characters']:
            html += f"<li><strong>{char['name']}</strong> - {char['description'][:50]}...</li>"
        html += "</ul>"
    
    if results['world_elements']:
        html += "<h5>World Elements:</h5><ul>"
        for elem in results['world_elements']:
            html += f"<li><strong>{elem['name']}</strong> ({elem['type']}) - {elem['description'][:50]}...</li>"
        html += "</ul>"
    
    if not any(results.values()):
        html += "<p>No results found.</p>"
    
    return gr.update(value=html, visible=True)


def create_interface():
    """Create the main Gradio interface."""
    
    # Load initial projects
    data = load_projects()
    project_choices = [(proj["name"], proj_id) for proj_id, proj in data["projects"].items()]
    
    with gr.Blocks(
        title="ScriptVoice - AI-Powered Story Intelligence Platform", 
        theme=gr.themes.Base(),
        css=CUSTOM_CSS
    ) as app:
        
        # Header with ScriptVoice branding
        gr.HTML(get_header_html())
        
        # Main tabbed interface
        with gr.Tabs():
            # Scripts Tab (Original functionality)
            with gr.TabItem("📝 Scripts"):
                with gr.Row():
                    # Left Sidebar
                    with gr.Column(scale=1, min_width=300, elem_classes=["sidebar-column"]):
                        gr.HTML(get_section_header('📁 Projects'))
                        
                        # New Project Section
                        with gr.Group():
                            new_project_name = gr.Textbox(label="New Project Name", placeholder="Enter project name...")
                            create_btn = gr.Button("➕ Create Project", elem_classes=["primary-button"])
                            create_status = gr.HTML(visible=False)
                        
                        # Project Selection
                        project_dropdown = gr.Dropdown(
                            choices=project_choices,
                            label="Select Project",
                            value=list(data["projects"].keys())[0] if data["projects"] else None
                        )
                        
                        # Notes Section
                        gr.HTML(get_section_header('📝 Notes'))
                        notes_textbox = gr.Textbox(
                            label="Project Notes",
                            placeholder="Add your notes here...",
                            lines=5,
                            max_lines=10
                        )
                        
                        # Settings Section
                        gr.HTML(get_section_header('⚙️ Settings'))
                        with gr.Group():
                            dyslexic_mode = gr.Checkbox(label="Dyslexic-friendly font", value=False)
                            voice_speed = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Voice Speed")
                            voice_volume = gr.Slider(0.1, 1.0, value=1.0, step=0.1, label="Voice Volume")
                    
                    # Main Editor Panel
                    with gr.Column(scale=2):
                        # Word Count Display
                        word_count_display = gr.HTML('<div class="word-count-highlight">📊 Word Count: 0</div>')
                        
                        # Script Editor
                        script_textbox = gr.Textbox(
                            label="Script Editor",
                            placeholder="Start writing your script here...",
                            lines=15,
                            max_lines=25
                        )
                        
                        # Control Buttons Row
                        with gr.Row():
                            save_btn = gr.Button("💾 Save", elem_classes=["secondary-button"])
                            tts_btn = gr.Button("🔊 Play TTS", elem_classes=["primary-button"])
                            save_status = gr.HTML(visible=False)
                        
                        # TTS Audio Output
                        audio_output = gr.Audio(label="Generated Audio")
                        tts_status = gr.HTML(visible=False)
                        
                        # OCR Section
                        with gr.Group():
                            gr.HTML(get_section_header('📷 Extract Text from Image'))
                            with gr.Row():
                                image_input = gr.Image(type="filepath", label="Upload Image")
                                ocr_btn = gr.Button("Extract Text", elem_classes=["secondary-button"])
                            ocr_status = gr.HTML(visible=False)
                        
                        # AI Enhancement Section
                        with gr.Group():
                            gr.HTML(get_section_header('🤖 AI Script Enhancement'))
                            with gr.Row():
                                enhancement_type = gr.Dropdown(
                                    choices=["dramatic", "romantic", "professional", "casual"],
                                    label="Enhancement Style",
                                    value="dramatic"
                                )
                                enhance_btn = gr.Button("✨ Enhance Script", elem_classes=["primary-button"])
                            enhance_status = gr.HTML(visible=False)
                        
                        # Export Section
                        with gr.Group():
                            gr.HTML(get_section_header('📤 Export'))
                            with gr.Row():
                                export_type = gr.Dropdown(
                                    choices=["text", "audio"],
                                    label="Export Type",
                                    value="text"
                                )
                                export_btn = gr.Button("📥 Export", elem_classes=["secondary-button"])
                            export_file = gr.File(label="Download")
                            export_status = gr.HTML(visible=False)
            
            # Story Intelligence Tab (New functionality)
            with gr.TabItem("📚 Story Intelligence"):
                story_components = create_story_intelligence_interface()
        
        # Event Handlers for Scripts Tab
        
        # Create new project
        create_btn.click(
            fn=create_new_project,
            inputs=[new_project_name],
            outputs=[create_status, project_dropdown]
        ).then(
            lambda: ("", gr.update(visible=True)),
            outputs=[new_project_name, create_status]
        )
        
        # ... keep existing code (load project, update word count, save script content, generate TTS, OCR, AI enhancement, export functionality)
        
        # Event Handlers for Story Intelligence Tab
        
        # Create story
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
        
        # Create character
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
        
        # Create world element
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
        
        # Search functionality
        story_components['search_btn'].click(
            fn=perform_search,
            inputs=[story_components['search_input']],
            outputs=[story_components['search_results']]
        )
        
        # Load project when selected
        project_dropdown.change(
            fn=load_project,
            inputs=[project_dropdown],
            outputs=[script_textbox, notes_textbox, word_count_display]
        )
        
        # Update word count as user types
        script_textbox.change(
            fn=update_word_count,
            inputs=[script_textbox],
            outputs=[word_count_display]
        )
        
        # Save script content
        save_btn.click(
            fn=save_script_content,
            inputs=[project_dropdown, script_textbox, notes_textbox],
            outputs=[save_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[save_status]
        )
        
        # Generate TTS
        tts_btn.click(
            fn=generate_tts,
            inputs=[script_textbox, voice_speed],
            outputs=[audio_output, tts_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[tts_status]
        )
        
        # OCR text extraction
        ocr_btn.click(
            fn=extract_text_from_image,
            inputs=[image_input],
            outputs=[script_textbox, ocr_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[ocr_status]
        )
        
        # AI Enhancement
        enhance_btn.click(
            fn=enhance_script_placeholder,
            inputs=[script_textbox, enhancement_type],
            outputs=[script_textbox, enhance_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[enhance_status]
        )
        
        # Export functionality
        export_btn.click(
            fn=export_project,
            inputs=[project_dropdown, export_type],
            outputs=[export_file, export_status]
        ).then(
            lambda: gr.update(visible=True),
            outputs=[export_status]
        )
        
        # Load initial story intelligence data
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
    # Create and launch the app
    app = create_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
