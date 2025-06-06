
"""Database interface components for chapter and scene management."""

import gradio as gr
import pandas as pd
from typing import List, Dict, Any, Tuple
from database_models import (
    get_all_chapters, get_chapters_for_story, create_chapter, 
    update_chapter, delete_chapter, search_chapters, 
    get_chapter_statistics, bulk_update_chapters
)
from models import load_projects


def create_database_interface():
    """Create the database management interface."""
    
    with gr.Column(elem_id="database-container"):
        # Header section
        gr.HTML("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1a1a1a 0%, #2d1810 100%); border-radius: 15px; margin-bottom: 20px;">
                <h2 style="color: #ff6b35; margin: 0; font-size: 2.2em; font-weight: bold;">📊 Project Database</h2>
                <p style="color: #cccccc; margin: 10px 0 0 0; font-size: 1.1em;">Organize and manage your chapters, scenes, and story structure</p>
            </div>
        """)
        
        # Statistics dashboard
        with gr.Row():
            with gr.Column(scale=1):
                stats_display = gr.HTML(value=_get_stats_html(), elem_id="stats-dashboard")
            with gr.Column(scale=2):
                with gr.Row():
                    search_input = gr.Textbox(
                        placeholder="Search chapters by title, outline, location, or content...",
                        label="🔍 Search Chapters",
                        elem_id="chapter-search"
                    )
                    search_btn = gr.Button("Search", variant="primary")
                    refresh_btn = gr.Button("🔄 Refresh", variant="secondary")
        
        # Filter and view controls
        with gr.Row():
            with gr.Column(scale=1):
                story_filter = gr.Dropdown(
                    choices=_get_story_choices(),
                    label="Filter by Story",
                    value=None,
                    allow_custom_value=False
                )
            with gr.Column(scale=1):
                status_filter = gr.Dropdown(
                    choices=["All", "Not Started", "Draft", "In Progress", "Done"],
                    label="Filter by Status",
                    value="All"
                )
            with gr.Column(scale=1):
                act_filter = gr.Dropdown(
                    choices=["All"] + [f"Act {i}" for i in range(1, 6)],
                    label="Filter by Act",
                    value="All"
                )
        
        # Main chapters table
        chapters_table = gr.DataFrame(
            value=_format_chapters_for_display(get_all_chapters()),
            headers=["ID", "Story", "Act", "Block", "Chapter", "Title", "Outline", "Characters", "Location", "Status", "Progress"],
            datatype=["str", "str", "number", "number", "number", "str", "str", "str", "str", "str", "str"],
            interactive=True,
            wrap=True,
            elem_id="chapters-table"
        )
        
        # Action buttons
        with gr.Row():
            add_chapter_btn = gr.Button("➕ Add Chapter", variant="primary")
            edit_chapter_btn = gr.Button("✏️ Edit Selected", variant="secondary")
            delete_chapter_btn = gr.Button("🗑️ Delete Selected", variant="stop")
            bulk_update_btn = gr.Button("📝 Bulk Update", variant="secondary")
        
        # Chapter creation/editing form (initially hidden)
        with gr.Group(visible=False) as chapter_form:
            gr.HTML("<h3 style='color: #ff6b35; margin-bottom: 15px;'>Chapter Details</h3>")
            
            with gr.Row():
                chapter_story = gr.Dropdown(
                    choices=_get_story_choices(),
                    label="Story",
                    allow_custom_value=False
                )
                chapter_act = gr.Number(value=1, label="Act Number", minimum=1, maximum=10)
                chapter_block = gr.Number(value=1, label="Block Number", minimum=1, maximum=20)
            
            with gr.Row():
                chapter_title = gr.Textbox(label="Chapter Title", placeholder="Enter chapter title...")
                chapter_status = gr.Dropdown(
                    choices=["Not Started", "Draft", "In Progress", "Done"],
                    label="Status",
                    value="Not Started"
                )
            
            chapter_outline = gr.Textbox(
                label="Chapter Outline",
                placeholder="Brief outline of what happens in this chapter...",
                lines=3
            )
            
            with gr.Row():
                chapter_characters = gr.Dropdown(
                    choices=_get_character_choices(),
                    label="Characters",
                    multiselect=True,
                    allow_custom_value=True
                )
                chapter_location = gr.Textbox(label="Location", placeholder="Where does this chapter take place?")
            
            chapter_notes = gr.Textbox(
                label="Notes",
                placeholder="Additional notes, reminders, or ideas for this chapter...",
                lines=2
            )
            
            with gr.Row():
                save_chapter_btn = gr.Button("💾 Save Chapter", variant="primary")
                cancel_chapter_btn = gr.Button("❌ Cancel", variant="secondary")
        
        # Bulk update form (initially hidden)
        with gr.Group(visible=False) as bulk_form:
            gr.HTML("<h3 style='color: #ff6b35; margin-bottom: 15px;'>Bulk Update Selected Chapters</h3>")
            
            with gr.Row():
                bulk_status = gr.Dropdown(
                    choices=["", "Not Started", "Draft", "In Progress", "Done"],
                    label="Update Status",
                    value=""
                )
                bulk_location = gr.Textbox(label="Update Location", placeholder="Leave empty to keep current")
            
            bulk_notes = gr.Textbox(
                label="Append to Notes",
                placeholder="Text to append to existing notes..."
            )
            
            with gr.Row():
                apply_bulk_btn = gr.Button("✅ Apply Updates", variant="primary")
                cancel_bulk_btn = gr.Button("❌ Cancel", variant="secondary")
        
        # Status messages
        database_status = gr.HTML(visible=False, elem_id="database-status")
        
        # Hidden components for state management
        selected_chapter_id = gr.State("")
        editing_mode = gr.State(False)
        selected_rows = gr.State([])
    
    # Return all components for event handler setup
    return {
        'stats_display': stats_display,
        'search_input': search_input,
        'search_btn': search_btn,
        'refresh_btn': refresh_btn,
        'story_filter': story_filter,
        'status_filter': status_filter,
        'act_filter': act_filter,
        'chapters_table': chapters_table,
        'add_chapter_btn': add_chapter_btn,
        'edit_chapter_btn': edit_chapter_btn,
        'delete_chapter_btn': delete_chapter_btn,
        'bulk_update_btn': bulk_update_btn,
        'chapter_form': chapter_form,
        'chapter_story': chapter_story,
        'chapter_act': chapter_act,
        'chapter_block': chapter_block,
        'chapter_title': chapter_title,
        'chapter_status': chapter_status,
        'chapter_outline': chapter_outline,
        'chapter_characters': chapter_characters,
        'chapter_location': chapter_location,
        'chapter_notes': chapter_notes,
        'save_chapter_btn': save_chapter_btn,
        'cancel_chapter_btn': cancel_chapter_btn,
        'bulk_form': bulk_form,
        'bulk_status': bulk_status,
        'bulk_location': bulk_location,
        'bulk_notes': bulk_notes,
        'apply_bulk_btn': apply_bulk_btn,
        'cancel_bulk_btn': cancel_bulk_btn,
        'database_status': database_status,
        'selected_chapter_id': selected_chapter_id,
        'editing_mode': editing_mode,
        'selected_rows': selected_rows
    }


def _get_stats_html() -> str:
    """Generate HTML for statistics dashboard."""
    stats = get_chapter_statistics()
    
    total = stats.get('total', 0)
    by_status = stats.get('by_status', {})
    
    # Calculate progress percentage
    completed = by_status.get('Done', 0)
    progress_pct = (completed / total * 100) if total > 0 else 0
    
    # Status color mapping
    status_colors = {
        'Not Started': '#6b7280',
        'Draft': '#f59e0b', 
        'In Progress': '#3b82f6',
        'Done': '#10b981'
    }
    
    status_html = ""
    for status, count in by_status.items():
        color = status_colors.get(status, '#6b7280')
        status_html += f"""
            <div style="display: flex; justify-content: space-between; margin: 5px 0; padding: 8px; background: {color}20; border-radius: 6px; border-left: 4px solid {color};">
                <span style="color: #ffffff;">{status}</span>
                <span style="color: {color}; font-weight: bold;">{count}</span>
            </div>
        """
    
    return f"""
        <div style="background: #2d1810; padding: 20px; border-radius: 10px; border: 1px solid #ff6b35;">
            <h3 style="color: #ff6b35; margin: 0 0 15px 0; text-align: center;">📈 Progress Overview</h3>
            <div style="text-align: center; margin-bottom: 15px;">
                <div style="color: #ffffff; font-size: 2em; font-weight: bold;">{total}</div>
                <div style="color: #cccccc; font-size: 0.9em;">Total Chapters</div>
            </div>
            <div style="margin-bottom: 15px;">
                <div style="background: #1a1a1a; border-radius: 10px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #ff6b35, #ffd700); height: 100%; width: {progress_pct}%; transition: width 0.3s ease;"></div>
                </div>
                <div style="color: #cccccc; font-size: 0.9em; text-align: center; margin-top: 5px;">{progress_pct:.1f}% Complete</div>
            </div>
            <div style="margin-top: 15px;">
                {status_html}
            </div>
        </div>
    """


def _get_story_choices() -> List[Tuple[str, str]]:
    """Get story choices for dropdown."""
    data = load_projects()
    stories = data.get("stories", {})
    return [(story["title"], story_id) for story_id, story in stories.items()]


def _get_character_choices() -> List[str]:
    """Get character choices for dropdown."""
    data = load_projects()
    characters = data.get("characters", {})
    return [char["name"] for char in characters.values()]


def _format_chapters_for_display(chapters: List[Dict[str, Any]]) -> pd.DataFrame:
    """Format chapters data for display in the table."""
    if not chapters:
        return pd.DataFrame(columns=["ID", "Story", "Act", "Block", "Chapter", "Title", "Outline", "Characters", "Location", "Status", "Progress"])
    
    data = load_projects()
    formatted_data = []
    
    for chapter in chapters:
        # Get story title
        story_title = "Unknown Story"
        if chapter.get("story_id") and chapter["story_id"] in data.get("stories", {}):
            story_title = data["stories"][chapter["story_id"]]["title"]
        
        # Format characters
        characters_str = ", ".join(chapter.get("characters", []))
        
        # Format outline (truncate if too long)
        outline = chapter.get("outline", "")
        if len(outline) > 100:
            outline = outline[:97] + "..."
        
        # Status badge
        status = chapter.get("status", "Not Started")
        status_emoji = {
            'Not Started': '⚪',
            'Draft': '🟡', 
            'In Progress': '🔵',
            'Done': '🟢'
        }
        
        progress_indicator = f"{status_emoji.get(status, '⚪')} {status}"
        
        formatted_data.append([
            chapter["id"],
            story_title,
            chapter.get("act_number", 1),
            chapter.get("block_number", 1),
            chapter.get("chapter_number", 1),
            chapter.get("title", ""),
            outline,
            characters_str,
            chapter.get("location", ""),
            status,
            progress_indicator
        ])
    
    return pd.DataFrame(
        formatted_data,
        columns=["ID", "Story", "Act", "Block", "Chapter", "Title", "Outline", "Characters", "Location", "Status", "Progress"]
    )


def refresh_database_display():
    """Refresh the database display with current data."""
    chapters = get_all_chapters()
    return (
        _format_chapters_for_display(chapters),
        _get_stats_html(),
        gr.update(choices=_get_story_choices()),
        gr.update(choices=_get_character_choices())
    )


def filter_chapters(story_filter: str, status_filter: str, act_filter: str):
    """Filter chapters based on selected criteria."""
    chapters = get_all_chapters()
    
    # Apply filters
    if story_filter and story_filter != "All":
        chapters = [c for c in chapters if c.get("story_id") == story_filter]
    
    if status_filter and status_filter != "All":
        chapters = [c for c in chapters if c.get("status") == status_filter]
    
    if act_filter and act_filter != "All":
        act_num = int(act_filter.replace("Act ", ""))
        chapters = [c for c in chapters if c.get("act_number") == act_num]
    
    return _format_chapters_for_display(chapters)


def search_chapters_handler(query: str):
    """Handle chapter search."""
    if not query.strip():
        return _format_chapters_for_display(get_all_chapters())
    
    results = search_chapters(query)
    return _format_chapters_for_display(results)
