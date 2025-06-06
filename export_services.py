
"""Export services for ScriptVoice."""

import tempfile
import json
import os
from gtts import gTTS
from models import load_projects
from typing import Tuple, Optional


def export_project(project_id: str, export_type: str) -> Tuple[Optional[str], str]:
    """Export project content with improved error handling."""
    if not project_id:
        return None, '<div class="status-error">❌ No project selected for export</div>'
    
    try:
        data = load_projects()
        if project_id not in data["projects"]:
            return None, '<div class="status-error">❌ Selected project not found</div>'
        
        project = data["projects"][project_id]
        
        if export_type == "text":
            return export_as_text(project)
        elif export_type == "audio":
            return export_as_audio(project)
        else:
            return None, '<div class="status-error">❌ Invalid export type selected</div>'
            
    except Exception as e:
        return None, f'<div class="status-error">❌ Error during export: {str(e)}</div>'


def export_as_text(project: dict) -> Tuple[Optional[str], str]:
    """Export project as text file."""
    try:
        # Create comprehensive text export
        content = f"""ScriptVoice Project Export
{'=' * 50}

Project: {project['name']}
Created: {project.get('created_at', 'Unknown')}
Last Modified: {project.get('updated_at', 'Unknown')}
Word Count: {project.get('word_count', 0)}

SCRIPT CONTENT:
{'-' * 30}
{project.get('content', 'No content available')}

PROJECT NOTES:
{'-' * 30}
{project.get('notes', 'No notes available')}

Export completed at: {str(time.time())}
"""
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            return tmp_file.name, '<div class="status-success">✅ Text file exported successfully! Click download below.</div>'
            
    except Exception as e:
        return None, f'<div class="status-error">❌ Error creating text export: {str(e)}</div>'


def export_as_audio(project: dict) -> Tuple[Optional[str], str]:
    """Export project as audio file."""
    try:
        script_content = project.get('content', '').strip()
        
        if not script_content:
            return None, '<div class="status-error">❌ No script content available to convert to audio</div>'
        
        # Limit content length for audio generation
        if len(script_content) > 5000:
            script_content = script_content[:5000] + "... Audio truncated due to length limits."
        
        # Generate TTS
        tts = gTTS(text=script_content, lang='en')
        
        # Create temporary file with project name
        project_name_safe = "".join(c for c in project['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            
            # Verify file was created
            if os.path.exists(tmp_file.name) and os.path.getsize(tmp_file.name) > 0:
                return tmp_file.name, '<div class="status-success">✅ Audio file exported successfully! Click download below.</div>'
            else:
                return None, '<div class="status-error">❌ Error: Audio file was not generated properly</div>'
                
    except Exception as e:
        return None, f'<div class="status-error">❌ Error creating audio export: {str(e)}</div>'


def export_project_data_json(project_id: str) -> Tuple[Optional[str], str]:
    """Export project data as JSON (utility function)."""
    try:
        data = load_projects()
        if project_id not in data["projects"]:
            return None, '<div class="status-error">❌ Project not found</div>'
        
        project_data = {
            "project": data["projects"][project_id],
            "export_timestamp": time.time(),
            "export_format": "ScriptVoice JSON v1.0"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as tmp_file:
            json.dump(project_data, tmp_file, indent=2, ensure_ascii=False)
            return tmp_file.name, '<div class="status-success">✅ Project data exported as JSON</div>'
            
    except Exception as e:
        return None, f'<div class="status-error">❌ Error exporting JSON: {str(e)}</div>'
