
"""LangChain tools and utilities for ScriptVoice with IONOS AI Model Hub integration."""

import os
import requests
import json
from typing import Optional
from config import IONOS_API_TOKEN, IONOS_MODEL_NAME, IONOS_ENDPOINT, OPENAI_API_KEY, IONOS_CHAT_URL
from ionos_collections import ionos_collections

# ... keep existing code (get_ionos_client, get_openai_client, get_ai_client functions)

def create_ionos_automated_rag_prompt(query: str, collection_name: str, enhancement_type: str = "general") -> str:
    """Create automated RAG prompt for IONOS with context variables."""
    
    if enhancement_type == "character_consistency":
        return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert story analyst. Use the information from the context to analyze character consistency and development. Focus on character traits, dialogue patterns, and behavioral consistency. Be specific and provide actionable insights.
<|eot_id|>
<|start_header_id|>context<|end_header_id|>
{{{{.context}}}}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{{{{.collection_query}}}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

    elif enhancement_type == "story_elements":
        return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a professional story development consultant. Use the context information to suggest story elements and improvements. Focus on plot development, pacing, narrative structure, and creative enhancements. Provide specific, actionable recommendations.
<|eot_id|>
<|start_header_id|>context<|end_header_id|>
{{{{.context}}}}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{{{{.collection_query}}}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

    elif enhancement_type == "dialogue":
        return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a dialogue specialist. Use the context to enhance dialogue to make it more natural, engaging, and character-specific. Maintain the original meaning while improving flow and authenticity. Consider character backgrounds and relationships from the context.
<|eot_id|>
<|start_header_id|>context<|end_header_id|>
{{{{.context}}}}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{{{{.collection_query}}}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

    elif enhancement_type == "description":
        return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a descriptive writing expert. Use the context information to enhance descriptions to be more vivid, immersive, and detailed. Use sensory details and precise language while maintaining consistency with the established world and characters.
<|eot_id|>
<|start_header_id|>context<|end_header_id|>
{{{{.context}}}}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{{{{.collection_query}}}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

    else:  # general analysis
        return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an AI writing assistant. Use the information from the context to provide helpful analysis and suggestions. Be thorough, constructive, and specific in your feedback.
<|eot_id|>
<|start_header_id|>context<|end_header_id|>
{{{{.context}}}}<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{{{{.collection_query}}}}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

def analyze_with_ionos_automated_rag(text: str, analysis_type: str = "general", content_type: str = "stories") -> str:
    """Analyze text using IONOS Automated RAG if available."""
    if not IONOS_API_TOKEN or not ionos_collections.is_available():
        return analyze_text_with_ai(text, analysis_type)  # Fallback
    
    # Get appropriate collection
    collection_id = ionos_collections.get_collection_id(content_type)
    if not collection_id:
        return analyze_text_with_ai(text, analysis_type)  # Fallback
    
    # Create automated RAG prompt
    prompt = create_ionos_automated_rag_prompt(text, content_type, analysis_type)
    
    # Use IONOS Automated RAG endpoint
    endpoint = f"https://inference.de-txl.ionos.com/models/{IONOS_MODEL_NAME}/predictions"
    
    body = {
        "properties": {
            "input": prompt,
            "collectionId": collection_id,
            "collectionQuery": text,
            "options": {
                "max_length": "1000",
                "temperature": "0.1"
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {IONOS_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        if response.status_code == 200:
            result = response.json()
            output = result.get("properties", {}).get("output", "")
            if output:
                return output
    except Exception as e:
        print(f"Error with IONOS automated RAG: {e}")
    
    # Fallback to regular AI analysis
    return analyze_text_with_ai(text, analysis_type)

def enhance_with_ionos_automated_rag(text: str, enhancement_type: str = "general", content_type: str = "stories") -> str:
    """Enhance text using IONOS Automated RAG if available."""
    if not IONOS_API_TOKEN or not ionos_collections.is_available():
        return enhance_text_with_context(text, enhancement_type)  # Fallback
    
    # Get appropriate collection based on enhancement type
    collection_map = {
        "dialogue": "characters",
        "description": "world_elements", 
        "pacing": "stories"
    }
    collection_name = collection_map.get(enhancement_type, content_type)
    collection_id = ionos_collections.get_collection_id(collection_name)
    
    if not collection_id:
        return enhance_text_with_context(text, enhancement_type)  # Fallback
    
    # Create automated RAG prompt for enhancement
    prompt = create_ionos_automated_rag_prompt(text, collection_name, enhancement_type)
    
    endpoint = f"https://inference.de-txl.ionos.com/models/{IONOS_MODEL_NAME}/predictions"
    
    body = {
        "properties": {
            "input": prompt,
            "collectionId": collection_id,
            "collectionQuery": text,
            "options": {
                "max_length": "1500",
                "temperature": "0.2"
            }
        }
    }
    
    headers = {
        "Authorization": f"Bearer {IONOS_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(endpoint, json=body, headers=headers)
        if response.status_code == 200:
            result = response.json()
            output = result.get("properties", {}).get("output", "")
            if output:
                return output
    except Exception as e:
        print(f"Error with IONOS automated RAG enhancement: {e}")
    
    # Fallback to regular enhancement
    return enhance_text_with_context(text, enhancement_type)

# Update existing functions to use IONOS automated RAG
def analyze_text_with_ai(text: str, analysis_type: str = "general") -> str:
    """Analyze text using AI with IONOS automated RAG priority."""
    # Try IONOS automated RAG first
    if IONOS_API_TOKEN and ionos_collections.is_available():
        result = analyze_with_ionos_automated_rag(text, analysis_type)
        if result and "Error" not in result:
            return result
    
    # ... keep existing code (fallback to regular LangChain)

def enhance_text_with_context(text: str, enhancement_type: str = "general") -> str:
    """Enhance text with AI using IONOS automated RAG priority."""
    # Try IONOS automated RAG first
    if IONOS_API_TOKEN and ionos_collections.is_available():
        result = enhance_with_ionos_automated_rag(text, enhancement_type)
        if result and result != text:
            return result
    
    # ... keep existing code (fallback to regular LangChain)
