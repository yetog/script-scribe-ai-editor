
"""Event handlers for the database interface."""

import gradio as gr
from database_components import (
    refresh_database_display, filter_chapters, search_chapters_handler,
    _get_stats_html, _get_story_choices, _get_character_choices
)
from database_models import (
    create_chapter, update_chapter, delete_chapter, bulk_update_chapters
)


def setup_database_event_handlers(db_components):
    """Set up event handlers for the database interface."""
    
    # Search functionality
    db_components['search_btn'].click(
        fn=search_chapters_handler,
        inputs=[db_components['search_input']],
        outputs=[db_components['chapters_table']]
    )
    
    # Enter key search
    db_components['search_input'].submit(
        fn=search_chapters_handler,
        inputs=[db_components['search_input']],
        outputs=[db_components['chapters_table']]
    )
    
    # Refresh functionality
    db_components['refresh_btn'].click(
        fn=refresh_database_display,
        outputs=[
            db_components['chapters_table'],
            db_components['stats_display'],
            db_components['story_filter'],
            db_components['chapter_story']
        ]
    )
    
    # Filter functionality
    filter_inputs = [
        db_components['story_filter'],
        db_components['status_filter'],
        db_components['act_filter']
    ]
    
    for filter_component in filter_inputs:
        filter_component.change(
            fn=filter_chapters,
            inputs=filter_inputs,
            outputs=[db_components['chapters_table']]
        )
    
    # Add chapter functionality
    db_components['add_chapter_btn'].click(
        fn=lambda: (gr.update(visible=True), gr.update(visible=False), False, ""),
        outputs=[
            db_components['chapter_form'],
            db_components['bulk_form'],
            db_components['editing_mode'],
            db_components['selected_chapter_id']
        ]
    )
    
    # Edit chapter functionality
    db_components['edit_chapter_btn'].click(
        fn=handle_edit_chapter,
        inputs=[db_components['chapters_table']],
        outputs=[
            db_components['chapter_form'],
            db_components['bulk_form'],
            db_components['editing_mode'],
            db_components['selected_chapter_id'],
            db_components['chapter_story'],
            db_components['chapter_act'],
            db_components['chapter_block'],
            db_components['chapter_title'],
            db_components['chapter_status'],
            db_components['chapter_outline'],
            db_components['chapter_characters'],
            db_components['chapter_location'],
            db_components['chapter_notes'],
            db_components['database_status']
        ]
    )
    
    # Delete chapter functionality
    db_components['delete_chapter_btn'].click(
        fn=handle_delete_chapter,
        inputs=[db_components['chapters_table']],
        outputs=[
            db_components['chapters_table'],
            db_components['stats_display'],
            db_components['database_status']
        ]
    )
    
    # Bulk update functionality
    db_components['bulk_update_btn'].click(
        fn=lambda: (gr.update(visible=False), gr.update(visible=True)),
        outputs=[db_components['chapter_form'], db_components['bulk_form']]
    )
    
    # Save chapter functionality
    db_components['save_chapter_btn'].click(
        fn=handle_save_chapter,
        inputs=[
            db_components['editing_mode'],
            db_components['selected_chapter_id'],
            db_components['chapter_story'],
            db_components['chapter_act'],
            db_components['chapter_block'],
            db_components['chapter_title'],
            db_components['chapter_status'],
            db_components['chapter_outline'],
            db_components['chapter_characters'],
            db_components['chapter_location'],
            db_components['chapter_notes']
        ],
        outputs=[
            db_components['chapters_table'],
            db_components['stats_display'],
            db_components['chapter_form'],
            db_components['database_status']
        ]
    ).then(
        fn=lambda: ("", 1, 1, "", "Not Started", "", [], "", ""),
        outputs=[
            db_components['chapter_title'],
            db_components['chapter_act'],
            db_components['chapter_block'],
            db_components['chapter_outline'],
            db_components['chapter_status'],
            db_components['chapter_notes'],
            db_components['chapter_characters'],
            db_components['chapter_location'],
            db_components['selected_chapter_id']
        ]
    )
    
    # Cancel chapter form
    db_components['cancel_chapter_btn'].click(
        fn=lambda: (gr.update(visible=False), "", 1, 1, "", "Not Started", "", [], "", ""),
        outputs=[
            db_components['chapter_form'],
            db_components['chapter_title'],
            db_components['chapter_act'],
            db_components['chapter_block'],
            db_components['chapter_outline'],
            db_components['chapter_status'],
            db_components['chapter_notes'],
            db_components['chapter_characters'],
            db_components['chapter_location'],
            db_components['selected_chapter_id']
        ]
    )
    
    # Apply bulk updates
    db_components['apply_bulk_btn'].click(
        fn=handle_bulk_update,
        inputs=[
            db_components['chapters_table'],
            db_components['bulk_status'],
            db_components['bulk_location'],
            db_components['bulk_notes']
        ],
        outputs=[
            db_components['chapters_table'],
            db_components['stats_display'],
            db_components['bulk_form'],
            db_components['database_status']
        ]
    ).then(
        fn=lambda: ("", "", ""),
        outputs=[
            db_components['bulk_status'],
            db_components['bulk_location'],
            db_components['bulk_notes']
        ]
    )
    
    # Cancel bulk form
    db_components['cancel_bulk_btn'].click(
        fn=lambda: (gr.update(visible=False), "", "", ""),
        outputs=[
            db_components['bulk_form'],
            db_components['bulk_status'],
            db_components['bulk_location'],
            db_components['bulk_notes']
        ]
    )


def handle_edit_chapter(table_data):
    """Handle editing a selected chapter."""
    if not table_data or len(table_data) == 0:
        return (
            gr.update(visible=False), gr.update(visible=False), False, "",
            gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(value="❌ No chapter selected.", visible=True)
        )
    
    # For now, edit the first row (in a real implementation, you'd handle row selection)
    chapter_id = table_data.iloc[0]['ID'] if 'ID' in table_data.columns else ""
    
    if not chapter_id:
        return (
            gr.update(visible=False), gr.update(visible=False), False, "",
            gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(value="❌ Invalid chapter selection.", visible=True)
        )
    
    # Load chapter data
    from database_models import get_all_chapters
    chapters = {c["id"]: c for c in get_all_chapters()}
    
    if chapter_id not in chapters:
        return (
            gr.update(visible=False), gr.update(visible=False), False, "",
            gr.update(), gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(), gr.update(), gr.update(), gr.update(),
            gr.update(value="❌ Chapter not found.", visible=True)
        )
    
    chapter = chapters[chapter_id]
    
    return (
        gr.update(visible=True),  # chapter_form
        gr.update(visible=False),  # bulk_form
        True,  # editing_mode
        chapter_id,  # selected_chapter_id
        gr.update(value=chapter.get("story_id", "")),  # chapter_story
        gr.update(value=chapter.get("act_number", 1)),  # chapter_act
        gr.update(value=chapter.get("block_number", 1)),  # chapter_block
        gr.update(value=chapter.get("title", "")),  # chapter_title
        gr.update(value=chapter.get("status", "Not Started")),  # chapter_status
        gr.update(value=chapter.get("outline", "")),  # chapter_outline
        gr.update(value=chapter.get("characters", [])),  # chapter_characters
        gr.update(value=chapter.get("location", "")),  # chapter_location
        gr.update(value=chapter.get("notes", "")),  # chapter_notes
        gr.update(value="", visible=False)  # database_status
    )


def handle_delete_chapter(table_data):
    """Handle deleting a selected chapter."""
    if not table_data or len(table_data) == 0:
        return (
            gr.update(),
            gr.update(),
            gr.update(value="❌ No chapter selected.", visible=True)
        )
    
    chapter_id = table_data.iloc[0]['ID'] if 'ID' in table_data.columns else ""
    
    if not chapter_id:
        return (
            gr.update(),
            gr.update(),
            gr.update(value="❌ Invalid chapter selection.", visible=True)
        )
    
    # Delete the chapter
    message = delete_chapter(chapter_id)
    
    # Refresh display
    from database_components import refresh_database_display
    new_table, new_stats, _, _ = refresh_database_display()
    
    return (
        new_table,
        new_stats,
        gr.update(value=message, visible=True)
    )


def handle_save_chapter(editing_mode, selected_chapter_id, story_id, act_number, block_number, title, status, outline, characters, location, notes):
    """Handle saving a chapter (create or update)."""
    if not title.strip():
        return (
            gr.update(),
            gr.update(),
            gr.update(visible=True),
            gr.update(value="❌ Chapter title is required.", visible=True)
        )
    
    try:
        if editing_mode and selected_chapter_id:
            # Update existing chapter
            updates = {
                "story_id": story_id,
                "act_number": int(act_number) if act_number else 1,
                "block_number": int(block_number) if block_number else 1,
                "title": title,
                "status": status,
                "outline": outline,
                "characters": characters if isinstance(characters, list) else [characters] if characters else [],
                "location": location,
                "notes": notes
            }
            message, updated_chapter = update_chapter(selected_chapter_id, updates)
        else:
            # Create new chapter
            message, new_chapter = create_chapter(
                story_id=story_id,
                act_number=int(act_number) if act_number else 1,
                block_number=int(block_number) if block_number else 1,
                title=title,
                outline=outline,
                characters=characters if isinstance(characters, list) else [characters] if characters else [],
                location=location,
                status=status,
                notes=notes
            )
        
        # Refresh display
        from database_components import refresh_database_display
        new_table, new_stats, _, _ = refresh_database_display()
        
        return (
            new_table,
            new_stats,
            gr.update(visible=False),  # Hide form
            gr.update(value=message, visible=True)
        )
    
    except Exception as e:
        return (
            gr.update(),
            gr.update(),
            gr.update(visible=True),
            gr.update(value=f"❌ Error saving chapter: {str(e)}", visible=True)
        )


def handle_bulk_update(table_data, bulk_status, bulk_location, bulk_notes):
    """Handle bulk updating selected chapters."""
    if not table_data or len(table_data) == 0:
        return (
            gr.update(),
            gr.update(),
            gr.update(visible=True),
            gr.update(value="❌ No chapters selected.", visible=True)
        )
    
    # Get all chapter IDs from the table (in a real implementation, you'd handle selection)
    chapter_ids = table_data['ID'].tolist() if 'ID' in table_data.columns else []
    
    if not chapter_ids:
        return (
            gr.update(),
            gr.update(),
            gr.update(visible=True),
            gr.update(value="❌ No valid chapters found.", visible=True)
        )
    
    # Prepare updates
    updates = {}
    
    if bulk_status:
        updates["status"] = bulk_status
    
    if bulk_location.strip():
        updates["location"] = bulk_location.strip()
    
    if bulk_notes.strip():
        # For bulk notes, we append to existing notes
        # This would need to be handled specially in the bulk_update_chapters function
        updates["notes_append"] = bulk_notes.strip()
    
    if not updates:
        return (
            gr.update(),
            gr.update(),
            gr.update(visible=True),
            gr.update(value="❌ No updates specified.", visible=True)
        )
    
    # Apply bulk updates
    message = bulk_update_chapters(chapter_ids[:5], updates)  # Limit to first 5 for demo
    
    # Refresh display
    from database_components import refresh_database_display
    new_table, new_stats, _, _ = refresh_database_display()
    
    return (
        new_table,
        new_stats,
        gr.update(visible=False),  # Hide bulk form
        gr.update(value=message, visible=True)
    )
