
"""UI component creation functions for ScriptVoice."""

import gradio as gr
from models import load_projects
from ui_components import get_section_header


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
