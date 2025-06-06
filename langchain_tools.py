
"""LangChain tools and utilities for ScriptVoice with IONOS AI Model Hub integration."""

import os
from typing import Optional
from config import IONOS_API_TOKEN, IONOS_MODEL_NAME, IONOS_ENDPOINT, OPENAI_API_KEY

def get_ionos_client():
    """Get IONOS AI client if API token is available."""
    try:
        from langchain_openai import ChatOpenAI
        if IONOS_API_TOKEN:
            return ChatOpenAI(
                api_key=IONOS_API_TOKEN,
                model=IONOS_MODEL_NAME,
                base_url=IONOS_ENDPOINT
            )
        else:
            print("Warning: IONOS API token not found.")
            return None
    except ImportError:
        print("Warning: langchain-openai not installed. AI features will be limited.")
        return None

def get_openai_client():
    """Get OpenAI client as fallback if API key is available."""
    try:
        from langchain_openai import ChatOpenAI
        if OPENAI_API_KEY:
            return ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
        else:
            print("Warning: OpenAI API key not found.")
            return None
    except ImportError:
        print("Warning: langchain-openai not installed.")
        return None

def get_ai_client():
    """Get AI client with IONOS as primary, OpenAI as fallback."""
    # Try IONOS first
    ionos_client = get_ionos_client()
    if ionos_client:
        print("Using IONOS AI Model Hub")
        return ionos_client
    
    # Fallback to OpenAI
    openai_client = get_openai_client()
    if openai_client:
        print("Using OpenAI as fallback")
        return openai_client
    
    print("Warning: No AI providers available. AI features will be limited.")
    return None

def create_simple_chain(llm, prompt_template: str):
    """Create a simple LangChain chain."""
    if not llm:
        return None
    
    try:
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        
        prompt = PromptTemplate(
            input_variables=["text"],
            template=prompt_template
        )
        return LLMChain(llm=llm, prompt=prompt)
    except ImportError:
        print("Warning: LangChain components not available.")
        return None

def analyze_text_with_ai(text: str, analysis_type: str = "general") -> str:
    """Analyze text using AI if available, otherwise return placeholder."""
    llm = get_ai_client()
    
    if not llm:
        return f"AI analysis not available (missing API keys). Analysis type: {analysis_type}"
    
    try:
        if analysis_type == "character_consistency":
            prompt = "Analyze the following text for character consistency and development. Focus on character traits, dialogue patterns, and behavioral consistency:\n\n{text}"
        elif analysis_type == "story_elements":
            prompt = "Suggest story elements and improvements for the following text. Include recommendations for plot development, pacing, and narrative structure:\n\n{text}"
        else:
            prompt = "Provide a general analysis of the following text:\n\n{text}"
        
        chain = create_simple_chain(llm, prompt)
        if chain:
            result = chain.run(text=text)
            return result
        else:
            return f"Analysis chain could not be created. Type: {analysis_type}"
    except Exception as e:
        return f"Error during AI analysis: {str(e)}"

def enhance_text_with_context(text: str, enhancement_type: str = "general") -> str:
    """Enhance text with AI if available."""
    llm = get_ai_client()
    
    if not llm:
        return text  # Return original text if AI not available
    
    try:
        if enhancement_type == "dialogue":
            prompt = "Enhance the dialogue in the following text to make it more natural, engaging, and character-specific. Maintain the original meaning while improving flow and authenticity:\n\n{text}"
        elif enhancement_type == "description":
            prompt = "Enhance the descriptions in the following text to be more vivid, immersive, and detailed. Use sensory details and more precise language:\n\n{text}"
        elif enhancement_type == "pacing":
            prompt = "Improve the pacing and flow of the following text. Adjust sentence structure, paragraph breaks, and narrative rhythm for better readability:\n\n{text}"
        else:
            prompt = "Improve and enhance the following text while maintaining its original meaning and style:\n\n{text}"
        
        chain = create_simple_chain(llm, prompt)
        if chain:
            result = chain.run(text=text)
            return result
        else:
            return text
    except Exception as e:
        print(f"Error during text enhancement: {str(e)}")
        return text
