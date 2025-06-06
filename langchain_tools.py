
"""LangChain tools and utilities for ScriptVoice."""

import os
from typing import Optional, List, Dict, Any

def get_openai_client():
    """Get OpenAI client if API key is available."""
    try:
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo")
        else:
            print("Warning: OpenAI API key not found. AI features will be limited.")
            return None
    except ImportError:
        print("Warning: langchain-openai not installed. AI features will be limited.")
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
    llm = get_openai_client()
    
    if not llm:
        return f"AI analysis not available (missing OpenAI API key). Analysis type: {analysis_type}"
    
    try:
        if analysis_type == "character_consistency":
            prompt = "Analyze the following text for character consistency and development:\n\n{text}"
        elif analysis_type == "story_elements":
            prompt = "Suggest story elements and improvements for the following text:\n\n{text}"
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
    llm = get_openai_client()
    
    if not llm:
        return text  # Return original text if AI not available
    
    try:
        if enhancement_type == "dialogue":
            prompt = "Enhance the dialogue in the following text to make it more natural and engaging:\n\n{text}"
        elif enhancement_type == "description":
            prompt = "Enhance the descriptions in the following text to be more vivid and immersive:\n\n{text}"
        elif enhancement_type == "pacing":
            prompt = "Improve the pacing and flow of the following text:\n\n{text}"
        else:
            prompt = "Improve and enhance the following text:\n\n{text}"
        
        chain = create_simple_chain(llm, prompt)
        if chain:
            result = chain.run(text=text)
            return result
        else:
            return text
    except Exception as e:
        print(f"Error during text enhancement: {str(e)}")
        return text
